import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.neighbors import LocalOutlierFactor

def inheritance_richness(graph):
    """
    Inheritance richness - the average number of sub-concepts per concept [Tartir2005]
    """    
    return stats.describe([int(node["hierarchical_in"]) for label, node in graph.nodes(data=True) if node["hierarchical_in"]>0 ] )

def inverse_inheritance_richness(graph):
    """
    Inverse Inheritance richness - the average number of superclasses (super-concepts) per class (concept) [Tartir2005]
    """
    return stats.describe( [int(node["hierarchical_out"]) for label, node in graph.nodes(data=True) if node["hierarchical_out"]>0])

def cohesion(graph):
    """
    Cohesion - the number of separate connected components
    return number of: weakly connected components, 
                      strongly connected components, 
                      attracting components,
                      isolates
    """
    wc = nx.algorithms.components.number_weakly_connected_components(graph)
    sc = nx.algorithms.components.number_strongly_connected_components(graph)
    ac = nx.algorithms.components.number_attracting_components(graph)
#     q = nx.algorithms.clique.graph_number_of_cliques(graph)
    i = nx.algorithms.isolate.number_of_isolates(graph)
    return (wc,sc,ac,i)

def weiner_index(graph):
    """
    """
    return nx.algorithms.wiener.wiener_index(graph)

def connectedness(graph):
    """
    Connectedness - the number of related concepts
    """
    return stats.describe( [int(node["orthogonal_out"]) for label, node in graph.nodes(data=True) ] )
    
def lexicalisation(graph):
    """
    Lexicalisation - the number of labels, comments and notes of the concept
    """
    dd = [ int(node["label_out"]) for label, node in graph.nodes(data=True) 
                                                       if node["hierarchical_out"]>0 or node["hierarchical_out"]>0 ]
    return stats.describe(dd)# np.histogram( dd ),     

def graph_depth(graph):
    dd = [ int(node["depth"]) for label, node in graph.nodes(data=True)
                                                       if (node["hierarchical_out"]>0 or node["hierarchical_in"]>0) and node["depth"]>-1 ]
    return stats.describe(dd)

# def eccentricity(graph):
#     """
#         The eccentricity of a node v is the maximum distance from v to all other nodes in G.
#     """
#     return nx.algorithms.distance_measures.eccentricity(graph)

def diameter(graph):
    """
        The diameter is the maximum eccentricity.
    """
    try:
         return nx.algorithms.distance_measures.diameter(graph) 
    except:
        return -1
     

def radius(graph):
    """
        The radius is the minimum eccentricity.
    """
    try:
        return nx.algorithms.distance_measures.radius(graph)
    except:
        return -1

def top_nodes(graph):
    """
        the number of top nodes, where a top node is a node that has incoming hierarchical relations and no outgoing
    """
    
    root_nodes = [node for label, node in graph.nodes(data=True) if node["hierarchical_in"]>0 and node["hierarchical_out"]==0]   
    return len(root_nodes)
    
def leaf_nodes(graph):
    """
        the number of leaf nodes, where a leaf node is a node that has outgoing hierarchical relation and no incoming ones
    """
    leaf_nodes = [node for label, node in graph.nodes(data=True) if node["hierarchical_out"]>0 and node["hierarchical_in"]==0]
    return len(leaf_nodes)
    
def depth_of_leaf_nodes(graph):
    """
    """
    leaf_nodes_depth = [node["depth"] for label, node in graph.nodes(data=True) if node["hierarchical_out"]>0 and node["hierarchical_in"]==0]
    return stats.describe(leaf_nodes_depth)
    
def graph_page_rank(graph):
    """
    """
    try:
        df = pd.DataFrame.from_dict(nx.algorithms.link_analysis.pagerank_alg.pagerank(graph,max_iter=1000), 
                                           orient='index', columns = ["page rank"])
        return stats.describe(df["page rank"])
    except:
        return [-1,[-1,-1],-1,-1,-1,-1]

def graph_hubs(graph):
    """
    """
    try:
        h, a = nx.algorithms.link_analysis.hits_alg.hits(graph,max_iter=1000)
        hubs = pd.DataFrame.from_dict(h, orient='index', columns = ["hubs"])
        #     authorities= pd.DataFrame.from_dict(a, orient='index', columns = ["authorities"])
        return stats.describe(hubs["hubs"])
    except:
        return [-1,[-1,-1],-1,-1,-1,-1]

def graph_authorities(graph):
    """
    """
    try:
        h, a = nx.algorithms.link_analysis.hits_alg.hits(graph,max_iter=1000)
        #     hubs = pd.DataFrame.from_dict(h, orient='index', columns = ["hubs"])
        authorities= pd.DataFrame.from_dict(a, orient='index', columns = ["authorities"])
        return stats.describe(authorities["authorities"])
    except:
        return [-1,[-1,-1],-1,-1,-1,-1]

def graph_degree_centrality(graph):
    """
    """
    try:
        degree_centrality = pd.DataFrame.from_dict(nx.algorithms.centrality.degree_centrality(graph), 
                                           orient='index', columns = ["degree centrality"])
        return stats.describe(degree_centrality["degree centrality"])
    except:
        return [-1,[-1,-1],-1,-1,-1,-1]

def graph_eigenvector_centrality(graph):
    """
    """
    try:
        eigenvector_centrality = pd.DataFrame.from_dict(nx.algorithms.centrality.eigenvector_centrality(graph,max_iter=1000), 
                                           orient='index', columns = ["eigenvector centrality"])
        return stats.describe(eigenvector_centrality["eigenvector centrality"])
    except:
        return [-1,[-1,-1],-1,-1,-1,-1]

    
    
METRICS=["name",
         "inheritance richness",
         "inverse inheritance richness",
         "lexicalisation", 
         "connectedness", 
         "depth",
         "diameter",
         "radius", 
         "page rank",
         "hubs", 
         "authorities",
         "degree centrality",
         "eigenvector centrality", 
         "cohesion",
         "top nodes", 
         "leaf nodes", 
         "leaf depth", ]

DESCRIPTIVE_STATS = ["nobs","min,max","mean","variance","skewness","kurtosis"]

def concept_scheme_stats(cs_graphs):
    """
        provided a list of (name, graph) generate descriptive statistics 
    """
    stats = pd.DataFrame([ (name, 
                            inheritance_richness(g),
                     inverse_inheritance_richness(g),
                     lexicalisation(g),
                     connectedness (g),
                     graph_depth(g),
                     diameter(g),
                     radius(g),                     
                     graph_page_rank(g),
                     graph_hubs(g),
                     graph_authorities(g),
                     graph_degree_centrality(g),
                     graph_eigenvector_centrality(g),
                     cohesion(g),
                     top_nodes(g),
                     leaf_nodes(g),
                     depth_of_leaf_nodes(g),
                     ) for name, g in cs_graphs]    , columns = METRICS)
    stats["nodes"] = stats["depth"].apply( lambda x: x[0])
    stats["depth - max"] = stats["depth"].apply( lambda x: x[1][1])
    stats["depth - mean"] = stats["depth"].apply( lambda x: x[2])
    
    stats["inheritance richness - min"] = stats["inheritance richness"].apply( lambda x: x[1][0])
    stats["inheritance richness - max"] = stats["inheritance richness"].apply( lambda x: x[1][1])
    stats["inheritance richness - mean"] = stats["inheritance richness"].apply( lambda x: x[2])
    stats["inheritance richness - variance"] = stats["inheritance richness"].apply( lambda x: x[3])

    stats["inverse inheritance richness - mean"] = stats["inverse inheritance richness"].apply( lambda x: x[2])
    
    stats["lexicalisation - min"] = stats["lexicalisation"].apply( lambda x: x[1][0])
    stats["lexicalisation - max"] = stats["lexicalisation"].apply( lambda x: x[1][1])
    stats["lexicalisation - mean"] = stats["lexicalisation"].apply( lambda x: x[2])
    stats["lexicalisation - variance"] = stats["lexicalisation"].apply( lambda x: x[3])
    
    stats["connectedness - min"] = stats["connectedness"].apply( lambda x: x[1][0])
    stats["connectedness - max"] = stats["connectedness"].apply( lambda x: x[1][1])
    stats["connectedness - mean"] = stats["connectedness"].apply( lambda x: x[2])
    stats["connectedness - variance"] = stats["connectedness"].apply( lambda x: x[3])
    
    stats["page rank - min"] = stats["page rank"].apply( lambda x: x[1][0])
    stats["page rank - max"] = stats["page rank"].apply( lambda x: x[1][1])
    stats["page rank - mean"] = stats["page rank"].apply( lambda x: x[2])

    stats["hubs - min"] = stats["hubs"].apply( lambda x: x[1][0])
    stats["hubs - max"] = stats["hubs"].apply( lambda x: x[1][1])
    stats["hubs - mean"] = stats["hubs"].apply( lambda x: x[2])

    stats["authorities - min"] = stats["authorities"].apply( lambda x: x[1][0])
    stats["authorities - max"] = stats["authorities"].apply( lambda x: x[1][1])
    stats["authorities - mean"] = stats["authorities"].apply( lambda x: x[2])
    
    stats["eigenvector centrality - min"] = stats["eigenvector centrality"].apply( lambda x: x[1][0])
    stats["eigenvector centrality - max"] = stats["eigenvector centrality"].apply( lambda x: x[1][1])
    stats["eigenvector centrality - mean"] = stats["eigenvector centrality"].apply( lambda x: x[2])
    
    stats["degree centrality - min"] = stats["degree centrality"].apply( lambda x: x[1][0])
    stats["degree centrality - max"] = stats["degree centrality"].apply( lambda x: x[1][1])
    stats["degree centrality - mean"] = stats["degree centrality"].apply( lambda x: x[2])

    stats["cohesion - weakly connected components"] = stats["cohesion"].apply( lambda x: x[0])
    stats["cohesion - strongly connected components"] = stats["cohesion"].apply( lambda x: x[1])
    stats["cohesion - attracting components"] = stats["cohesion"].apply( lambda x: x[2])
    stats["cohesion - isolates components"] = stats["cohesion"].apply( lambda x: x[3])
    
    stats["leaf depth - min"] = stats["leaf depth"].apply( lambda x: x[1][0])
    stats["leaf depth - max"] = stats["leaf depth"].apply( lambda x: x[1][1])
    stats["leaf depth - mean"] = stats["leaf depth"].apply( lambda x: x[2])
    stats["leaf depth - variance"] = stats["leaf depth"].apply( lambda x: x[3])
    
    del stats["depth"]
    del stats["connectedness"]
    del stats["lexicalisation"]
    del stats["inheritance richness"]
    del stats["inverse inheritance richness"]
    del stats["page rank"]    
    del stats["hubs"]
    del stats["authorities"]
    del stats["degree centrality"]
    del stats["eigenvector centrality"]
    del stats["cohesion"]
    del stats["leaf depth"]
    
    return stats


CENTRALITY_COLUMNS = ["page rank", "hubs", "authorities", "degree centrality", "eigenvector centrality"]


def nodes_centrality_metrics(graph):
    """
        returns a dataframe with various node centrality metrics
        
    """
    result = pd.DataFrame()
    page_rank = pd.DataFrame.from_dict(nx.algorithms.link_analysis.pagerank_alg.pagerank(graph,max_iter=1000), 
                                       orient='index', columns = ["page rank"])
    result = page_rank.join(result)
    
    h, a = nx.algorithms.link_analysis.hits_alg.hits(graph,max_iter=1000)
    hubs = pd.DataFrame.from_dict(h, orient='index', columns = ["hubs"])
    authorities= pd.DataFrame.from_dict(a, orient='index', columns = ["authorities"])
    result = hubs.join(result)
    
    result = authorities.join(result)
    
    degree_centrality = pd.DataFrame.from_dict(nx.algorithms.centrality.degree_centrality(graph), 
                                       orient='index', columns = ["degree centrality"])
    result = degree_centrality.join(result)
    eigenvector_centrality = pd.DataFrame.from_dict(nx.algorithms.centrality.eigenvector_centrality(graph), 
                                       orient='index', columns = ["eigenvector centrality"])
    result = eigenvector_centrality.join(result)
    # getting the node properties 
    return result

def get_detect_outliers(df, feature_columns, ):
    """        
        df: data frame
        feature_columns: columns representing the features
    """
    outlier_detector = LocalOutlierFactor(n_neighbors=35, contamination=0.15)
    t0 = time.time()
    algorithm.fit(df[feature_columns])
    t1 = time.time()
    # TODO: continue

def graph_centrality_metrics(graph):
    """
        starting from the set of node centrality metrics generate descriptive centrality stats for the graph
        @return : 
        for each centrality measure x:
            min x_centrality - 
            average x_centrality -             
            max x_centrality -            
    """
    
