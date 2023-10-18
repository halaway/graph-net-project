# Daniel Perez A.
# CSCI Big Data: Project One

import re
from typing import Dict
import pandas as pd
import hetnetpy.hetnet

from neo4j import GraphDatabase
from pprint import pprint
import json
import networkx as nx
import matplotlib.pyplot as plt

from neo4j import GraphDatabase
import sys

from nltk.tokenize import word_tokenize

# Using Neo4j For Graph Storage
from pyvis.network import Network
from pyvis import network as net
import numpy as np


# Authentication
URI = "bolt://localhost:7689"
AUTH = ("neo4j", "spiky1234567")


# Neo4j Database Class
class Neo4j:
    # Initialzing Neo4j driver
    def __init__(self, URI, user, password):
        self.driver = GraphDatabase.driver(URI, auth=(user,password))

    # Closing Server 
    def close(self):
        self.driver.close()

    def run_query(self, query, **params):
        with self.driver.session() as session:
            result = session.run(query,**params)

        return result

    def r_query(self, query, **params):
        with self.driver.session() as session:
            record = {}

            # Tokenizing Query for Keyword Word
            word_query = word_tokenize(query.lower())
            
            # Running Query
            try:
                result = session.run(query, **params)
            except:
                print ("Query Not Possible")
                return 1
            
            else:
                if 'load' in word_query:
                    print('Neo4j Loaded Data Succesfully')
                    return 1

                for x in result:
                    record = dict(x)
                    print(record['n']['name'], "Name: ", record['n']['dataName'].title())
                    
                
                if not record :
                    print("No Matches Found")
        return 1  #


# Main Program for Querying and Visualizing Data
def main(argv):

    # Creating Database Instance
    database_db = Neo4j('bolt://localhost:7689', 'neo4j', 'spiky1234567')
    

    try:
        # Argument From Command Line
        command_line_query = argv[1]
    except:

        print("Query is not Defined. Here's a Visual")
        
        # Visualizing Query
        # %%
        import networkx as nx
        import matplotlib.pyplot as plt

        data_graph = nx.Graph()

        with database_db.driver.session() as session:
            result = session.run("""MATCH n=(a:Data)-[:CpD]->\
                (b:Data where b.id='Disease::DOID:7148') RETURN a,b""")
            for record in result: 
                
                # Extracting the nodes from both nodes
                node_a = record["a"]
                node_b = record["b"]
                
                # Adding nodes to the network graph
                data_graph.add_node(node_a["id"])  
                data_graph.add_node(node_b["id"])

                # Adding edge to graph
                data_graph.add_edge(node_a["id"], node_b["id"])


        pos = nx.spring_layout(data_graph)  
        edge_labels = {edge: 'CpD' for edge in data_graph.edges()}
        nx.draw_networkx_edge_labels(data_graph, pos, edge_labels=edge_labels)

        nx.draw_networkx(data_graph, pos,with_labels=True, node_size=100)
        
        plt.show()

    else:
        # Running Query From Termnial
        database_db.r_query(command_line_query)

    # Closing Data Base
    database_db.close()



    return 0


if __name__ == "__main__":
    main(sys.argv)

# %%
