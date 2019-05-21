import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
import rdflib
from IPython.display import HTML, Markdown, display
import seaborn as sns
from itertools import combinations, chain
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer


plt.rcParams['figure.figsize'] = [7, 4]
plt.rcParams['figure.dpi'] = 150
pd.options.display.float_format = '{:,.2f}'.format
sns.set_style("whitegrid", {'axes.grid' : False})

tokenizer = RegexpTokenizer('[\s_]+',gaps=True)

COLUMNS = ["concept","node1","node2","node3"]
STOP_WORDS = stopwords.words("english")

def dsp(df):
    """ Dysplay a dataframe in IPython environment"""
    display(HTML(df.to_html()))

def to_excel(df, file_name):
    """
        write a data frame in excel format using propert float formating
    """
    df.to_excel(file_name, sheet_name = "data", float_format="%.4f")
    
def draw_graph(graph, show_node_labels=True, show_edge_labels=True):
    NODE_SIZE = 300
    EDGE_WIDTH = 1
    
    
    try:
        pos = nx.nx_agraph.graphviz_layout(graph)   
    except:
        pos = nx.spring_layout(graph, iterations=20)
        
    
    nx.draw_networkx_nodes(graph, pos, node_size=NODE_SIZE, node_color='b', alpha=0.4)
    nx.draw_networkx_edges(graph, pos, alpha=0.4, node_size=NODE_SIZE, width=EDGE_WIDTH, edge_color='orangered')
    nx.draw_networkx_labels(graph, pos, fontsize=10)
    
    # hides the axis completly
    plt.axis('off')
    plt.show()
    plt.close()
    

def subgraph_of_hierarchical_nodes(graph):
    """
        Creates a graph with hierarchical edges only  
    """
    return graph.edge_subgraph([ (u,v) for u,v,d in graph.edges(data=True) if "hierarchical" in d["rels"]])

def distance_to_first_root(graph, node):
    """
        Return the depth of the node in the hierarchy
    """
    hierarchy_graph = subgraph_of_hierarchical_nodes(graph)
    first_root = list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(graph,source=node))[0]
    first_path_to_root = list(nx.algorithms.simple_paths.shortest_simple_paths(graph, node, first_root ))[0]
    return len(first_path_to_root)-1
    

def enrich_nodes_with_depth_info(graph):
    """
        Add to every node of the graph the depth at which it is situated in the hierarchy tree
    """
    hierarchy_graph = subgraph_of_hierarchical_nodes(graph)
    for node in hierarchy_graph.nodes():
        first_root = list(nx.algorithms.traversal.depth_first_search.dfs_postorder_nodes(hierarchy_graph,source=node))[0]
        first_path_to_root = list(nx.algorithms.simple_paths.shortest_simple_paths(hierarchy_graph, node, first_root ))[0]
        graph.nodes[node]["depth"]= len(first_path_to_root)-1 
    
    for n,d in graph.nodes(data=True):
        if "depth" not in d:
            # initialise the propoerty anyway
            graph.nodes[n]["depth"] = -1
            # get the depth of the parent , probably because this is the alt label node
            for u,v,d in graph.in_edges(n,data=True):
                graph.nodes[n]["depth"] = graph.nodes[u]["depth"] if "depth" in graph.nodes[u] else -1
    
def filter_stop_words(data_frame, columns = COLUMNS, stop_wrods = STOP_WORDS):
    """
        removes stop words from the columns
    """
    df = data_frame.copy()    
    for c in columns:
        df[c] = df[c].apply(lambda x: " ".join([i for i in tokenizer.tokenize(x.lower()) if i not in stop_wrods]))
    return df

def create_grah_from_jrc_dataset(df, directional=True):
    """
        Create networkx graph from JRC data
    """
    g = nx.DiGraph() if directional else nx.Graph()
    for row in df.itertuples():
        count, data  = row[1], row[2:]
        for a,b in combinations(range(len(COLUMNS)),2):
            if not g.has_edge(data[a], data[b],):
                g.add_edge( data[a], data[b], weight=1, rels="orthogonal")                
            else:
                g[data[a]][data[b]]['weight'] += 1
            if "weight" not in g.nodes[data[a]]: g.nodes[data[a]]["weight"] = count
            else: g.nodes[data[a]]["weight"] += count
            if "weight" not in g.nodes[data[b]]: g.nodes[data[b]]["weight"] = count
            else: g.nodes[data[b]]["weight"] += count                
    return g    

def create_grah_from_eurovoc_label_query(query_result):
    """
        Create networkx graph from EuroVoc query resul having the following signature: 
        __?uri ?scheme ?prefLabel ?altLabel ?rel__
        __  0      1          2       3       4__
        # count the number of hierarchical_edges in
        # count the number of hierarchical_edges out
        # count the number of related_edges 
        # count the number of label edges out
        # for a related_edge create the inverse
    """
    g = nx.DiGraph() #if directional else nx.Graph()
    for row in query_result.itertuples():
        idx, uri, scheme, pl, al, rel = str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])
        
        if not g.has_edge(pl,al):
            g.add_edge(pl,al, weight=1, rels=set([rel]) )
        else:
            g[pl][al]['weight'] += 1
            g[pl][al]['rels'].add(rel)
            
        if "weight" not in g.nodes[pl]: 
            g.nodes[pl]["weight"] = 1
            g.nodes[pl]["uris"] = set([uri])
        else: 
            g.nodes[pl]["weight"] += 1
            g.nodes[pl]["uris"].add(uri)
            
        if "weight" not in g.nodes[al]: 
            g.nodes[al]["weight"] = 1
            g.nodes[al]["uris"] = set([])
        else: 
            g.nodes[al]["weight"] += 1
            # g.nodes[al]["uris"].add(uri)
    
    # reducing node set attributes to lists
    for node in g.nodes:
        if "uris" in g.nodes[node]:
            g.nodes[node]["uris"] = ",".join(list(g.nodes[node]["uris"]))
    
    # reducing edge set attributes to lists
    for edge in g.edges():
        if "rels" in g[edge[0]][edge[1]]:
            g[edge[0]][edge[1]]["rels"] = ",".join(list(g[edge[0]][edge[1]]["rels"]))
    
    # for a related_edge create the inverse
    for edge in g.edges():            
        if "orthogonal" in g[edge[0]][edge[1]]["rels"]:
            g.add_edge(edge[1],edge[0],**g[edge[0]][edge[1]])

    # a few extra attr on nodes
    for node in g.nodes:
        in_edges = g.in_edges(nbunch=node,data=True)
        out_edges = g.out_edges(nbunch=node,data=True)
        # count the number of hierarchical_edges in
        hierarchical_in = [ edge for edge in in_edges if "hierarchical" in edge[2]["rels"]]
        # count the number of hierarchical_edges out
        hierarchical_out = [ edge for edge in out_edges if "hierarchical" in edge[2]["rels"]]
        # count the number of related_edges 
        orthogonal_out = [ edge for edge in out_edges if "orthogonal" in edge[2]["rels"]]
        # count the number of label edges out    
        label_out = [ edge for edge in out_edges if "label" in edge[2]["rels"]]
        g.nodes[node]["hierarchical_in"]=len(hierarchical_in)
        g.nodes[node]["hierarchical_out"]=len(hierarchical_out)
        g.nodes[node]["orthogonal_out"]=len(orthogonal_out)
        g.nodes[node]["label_out"]=len(label_out)
    
    enrich_nodes_with_depth_info(g)    
    return g
    

def create_grah_per_scheme_from_eurovoc_label_query(query_result, directional=False):
    """
        Creates a set of (scheme name, networkx graph) tuples from EuroVoc query resul having the following signature: 
        __?uri ?scheme ?prefLabel ?altLabel ?rel__
        __  0      1          2       3       4__
    """
    results = []
    for name, group in query_result.groupby("scheme"):
        results.append ( (name, create_grah_from_eurovoc_label_query(group) ) )
    return results



def eurovoc_nodes_as_pd(graph):    
    return  pd.DataFrame.from_dict({ n:[d["weight"],d["hierarchical_in"],
                                        d["hierarchical_out"],d["orthogonal_out"],
                                        d["label_out"],
                                        d["depth"],
                                       ] for n,d in graph.nodes(data=True)}, 
                                  orient='index', columns = ["weight", "hierarchical_in", 
                                                             "hierarchical_out",  "orthogonal_out", 
                                                             "label_out","depth"])

def cm_nodes_as_pd(graph):
    return  pd.DataFrame.from_dict({ n:[d["weight"]] for n,d in graph.nodes(data=True)}, 
                                  orient='index', columns = ["weight"])