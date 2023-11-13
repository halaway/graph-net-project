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

from pyspark.sql import SparkSession



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

# http://localhost:7474/browser/



spark = SparkSession\
    .builder\
    .config("spark.neo4j.bolt.url", URI)\
        .config("spark.neo4j.bolt.password", 'spiky1234567')\
            .config("spark.neo4j.bolt.user", 'neo4j')


def main():


    return 0;


if __name__ == "__main__":

    main()


