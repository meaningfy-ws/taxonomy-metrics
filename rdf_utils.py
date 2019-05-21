import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pathlib
import rdflib
from IPython.display import HTML, Markdown, display
import seaborn as sns
from itertools import combinations
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer

# create a network of related labels
from rdflib.namespace import FOAF, SKOS
from rdflib.plugins.sparql import prepareQuery

# EuroVoc can be expressed (for each language) as:
# * a undirected graph of connected labels (pref label is central to alt labels)
# * a digraph of preflabels following the broader relation (hopefully the result is a set of trees - no it is not)


NAMESPACES = { "foaf": FOAF, "skos":SKOS }
QUERY_LABELS = """
select ?uri ?scheme ?prefLabel ?altLabel ?rel
from <http://eurovoc.europa.eu/100141>
where {
    ?uri a skos:Concept.
    ?uri skos:inScheme ?schemeUri .
        optional {
            ?schemeUri skos:prefLabel ?scheme .
        }

    bind( "en" as ?language )
    {
        select ?uri ?prefLabel ?altLabel ?rel 
        where{
            ?uri skos:prefLabel ?prefLabel .
            ?uri skos:altLabel ?altLabel .
            bind ("label" as ?rel)
        }
    } 
    UNION
    {
        select ?uri ?prefLabel ?altLabel ?rel ?schemeUri 
        where{
            ?uri skos:prefLabel ?prefLabel .
            ?uri skos:broader ?altUri . # |^skos:narrower
            ?altUri skos:prefLabel ?altLabel .

            ?uri skos:inScheme ?schemeUri . 
            ?altUri skos:inScheme ?schemeUri .
            
            bind("hierarchical" as ?rel)            
        }
    }
    UNION
    {
        select ?uri ?prefLabel ?altLabel ?rel
        where{
            ?uri skos:prefLabel ?prefLabel .
            ?uri skos:related ?altUri .
            ?altUri skos:prefLabel ?altLabel .
            bind("orthogonal" as ?rel)
        }
    }
    FILTER (lang(?prefLabel)=?language && lang(?altLabel)=?language && lang(?scheme)=?language)
} 
"""
# 
# this takes forever, run the query in a SPARQL endpoint and use the CSV resultset
# TODO: transform into sparql endpoint query in cellar rather than loading EuroVoc from a file
# query = prepareQuery(QUERY_LABELS, initNs=NAMESPACES)
# query_result_labels =  EUROVOC_RDF_DATASET.query(query, ) # initBindings={'person': tim}