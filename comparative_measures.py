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


def common_concept_acjacency(g1, g2, g1_name="G1", g2_name="G2"):
    """
     provided two graphs g1 and g2 returns the adjaceny nodes for the common concepts 
    """
    results = []
    exact_matches = set(g1.nodes()).intersection(set(g2.nodes()) )
    for em in exact_matches:
        g1_succ = list(g1.successors(em))
        g1_pred = list(g1.predecessors(em))
        g2_succ = list(g2.successors(em))
        g2_pred = list(g2.predecessors(em))
        
        common_words_succ = set(" ".join(g1_succ).split()).intersection( " ".join(g2_succ).split() )
        common_words_pred = set(" ".join(g1_pred).split()).intersection( " ".join(g2_pred).split() )        
        
        results.append( (em,", ".join(g1_succ),", ".join(g2_succ), ", ".join(common_words_succ) ,", ".join(g1_pred),", ".join(g2_pred), ", ".join(common_words_pred) ) )
    return pd.DataFrame(results,
                        columns=["concept", 
                                 g1_name+" successors", g2_name+" successors", "common successor words", 
                                 g1_name+" predecessors", g2_name+" predecessors", "common predecessor words"])

def paths_between_common_concepts(g1, g2, g1_name="G1", g2_name="G2"):
    """
     provided two graphs g1 and g2 returns the paths available from one to another concept both in G1 and G2. 
     This provides a way to compare the paths of any common ones exist. 
     
     @return: path sequence (if any in G1), length in G1, path sequence (if any in G2), length in G2, common parts
    """
    results = []
    exact_matches = set(g1.nodes()).intersection(set(g2.nodes()))
    comb = list (combinations(exact_matches,2) ) 
    
    for n1,n2 in comb:
        if nx.algorithms.shortest_paths.generic.has_path(g1,n1,n2) and nx.algorithms.shortest_paths.generic.has_path(g2,n1,n2):
#             all_paths_g1 = nx.algorithms.shortest_paths.generic.all_shortest_paths(g1,n1,n2) 
            shortest_path_g1 = nx.algorithms.shortest_paths.generic.shortest_path(g1,n1,n2) 
#             all_paths_g2 = nx.algorithms.shortest_paths.generic.all_shortest_paths(g2,n1,n2)
            shortest_path_g2 = nx.algorithms.shortest_paths.generic.shortest_path(g2,n1,n2)     
            nodes_in_g1_path = set(shortest_path_g1) #set( chain(*all_paths_g1) )
            nodes_in_g2_path = set(shortest_path_g2) #set( chain(*all_paths_g2) )
            len_g1 = len(nodes_in_g1_path)  #np.average( [len(i) for i in all_paths_g1] )
            len_g2 = len(nodes_in_g2_path) #np.average( [len(i) for i in all_paths_g2] )
            common_nodes =  nodes_in_g1_path.intersection(nodes_in_g2_path)
            
            edges_on_shortest_path_g1 = list( zip(shortest_path_g1[:-1],shortest_path_g1[1:]))                        
            hierarchical_edges_on_path_g1 = len( [ (u,v) for u,v in edges_on_shortest_path_g1 if "hierarchical" in g1[u][v]["rels"] ] )
            orthogonal_edges_on_path_g1 = len( [ (u,v) for u,v in edges_on_shortest_path_g1 if "orthogonal" in g1[u][v]["rels"] ] )
            label_edges_on_path_g1 = len( [ (u,v) for u,v in edges_on_shortest_path_g1 if "label" in g1[u][v]["rels"] ] )
            
            
            edges_on_shortest_path_g2 = zip(shortest_path_g2[:-1],shortest_path_g2[1:])
            hierarchical_edges_on_path_g2 = len( [ (u,v) for u,v in edges_on_shortest_path_g2 if "hierarchical" in g2[u][v]["rels"] ] )
            orthogonal_edges_on_path_g2 = len( [ (u,v) for u,v in edges_on_shortest_path_g2 if "orthogonal" in g2[u][v]["rels"] ] )
            label_edges_on_path_g2 = len( [ (u,v) for u,v in edges_on_shortest_path_g2 if "label" in g2[u][v]["rels"] ] )
            
            results.append((n1, n2, 
                           " - ".join(shortest_path_g1), len_g1, 
                            hierarchical_edges_on_path_g1, orthogonal_edges_on_path_g1 , label_edges_on_path_g1, 
                           " - ".join(shortest_path_g2), len_g2,
                            hierarchical_edges_on_path_g2, orthogonal_edges_on_path_g2 , label_edges_on_path_g2, 
                           " - ".join(common_nodes) )
                          )
    return  pd.DataFrame(results, columns =["source concept","target concept",
                                            "paths in "+g1_name, "length in " + g1_name, 
                                            "hierarchical edges on " +g1_name + " path", "orthogonal edges on " +g1_name + " path", 
                                            "label edges on " +g1_name + " path",
                                            
                                            "paths in "+g2_name, "length in " + g2_name,
                                            "hierarchical edges on " +g2_name + " path", "orthogonal edges on " +g2_name + " path", 
                                            "label edges on " +g2_name + " path",
                                            
                                            "common nodes"
                                           ])