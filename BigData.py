

from queue import Empty
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



graph_nodes = 'nodes_test.tsv'
graph_edges = 'edges_test.tsv'


# Using Neo4j For Graph Storage


# Authentication
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "spiky1234567")

#with GraphDatabase.driver(URI, auth=AUTH) as driver:
#    driver.verify_connectivity()


# Neo4j Database Class
class Neo4j:
    # Initialzing Neo4j driver
    def __init__(self, URI, user, password):
        self.driver = GraphDatabase.driver(URI, auth=(user,password))

    # Closing Server 
    def close(self):
        self.driver.close()

    # Performing Query on Database
    def run_query(self, query, **params):
        #lst = []
        with self.driver.session() as session:
            result = session.run(query, **params)
            for record in result:
                print(type(record))
                #print('ID:', record['properties']['id'])
            #lst = [dict(record) for record in result]
            return 1

    def r_query(self, query, **params):
        with self.driver.session() as session:
            record = {}

            result = session.run(query, **params)
            for x in result:
                # Access the 'id' property within each record
                #id_value = record['name']
                #print(record['n.id'])

                record = dict(x)
                # FOR DISEASE NAME ON ID
                #print("Disease Name: ",record['n.dataName'].title())
                print(record['n']['name'], "Name: ", record['n']['dataName'].title())

            if not record :
                print("No Matches Found")
        return 1  #




# Notes
"""
    - cd into test folder
    - run "python -m http.server
        which hosts the data on a http server 
        "http://localhost:8000/nodes_test.tsv"
    - query : loading the data from the server 

"""


# QUERIES

# 1. Return Disease Name
"""
    MATCH (n WHERE n.name='Disease' AND 
    n.id ='Disease::DOID:8577') 
    RETURN n
"""

# 2. Return Compounds that Palliate or Treats
"""
    MATCH m=(n:Data)-[:CpD|CtD]->(b:Data where 
    b.id='Disease::DOID:7148') RETURN n
"""

# 3 Return Genes that Cause this Disease
"""
    MATCH p=(a:Data WHERE a.id='Disease::DOID:7148')
    -[r:DaG]->(n:Data where n.name ='Gene') RETURN n
"""

# 4. Return Where Disease Occurs
"""
    MATCH p=(a:Data WHERE a.id ='Disease::DOID:7148')
    -[r:DlA]->(n:Data) RETURN n
"""



def main(argv):



    # Query String
    query = """LOAD CSV with HEADERS FROM 
        "http://localhost:8000/nodes_test.tsv" AS row 
        CREATE (n:Anatomy {id: row.id}) WHERE row.kind = 'anatomy'
        CREATE (n:Compound {id: row.id}) WHERE row.kind = 'compound' 
        Create (n:Gene {id: row.id}) WHERE row.kind = 'gene'
        Create (n:Disease {id: row:id}) WHERE row.kind = 'disease'
        """
    quer = """LOAD CSV WITH HEADERS FROM "http://localhost:8000/nodes_test.tsv" 
                As row FIELDTERMINATOR "\t"
                Create (n:Data {name:row.kind, id:row.id, dataName:row.name})
            """

    # Creating Database Instance
    #database_db = Neo4j('neo4j://localhost:7687','neo4j','spiky1234567')
    database_db = Neo4j('bolt://localhost:7689', 'neo4j', 'spiky1234567')
    qu = """Match ( n where n.name='Gene') return n limit 100"""
    q = """Match(n:Data)-[r:GiG]->(a:Data) return n limit 10"""
    r = """Match (n:Data)-[:CrC]->(a:Data) return n"""
    p = """MATCH ()-->() RETURN count(*)"""
    
    # Command Line 
    #print(argv[1])

    resul = argv[1]
    resul = database_db.r_query(resul)
    
    
    database_db.close()

    

   



    #info =[]
    #with driver.session() as session:
        #info = session.run(query)
        #print(info)
        #for item in info:
            #print(item)
    


    #data = [dict(record) for record in info]
    #json_file = 'file_query.json'

    #with open(json_file, "w") as json_f:json.dump(data, json_f, indent=4)


    
    #driver.close()
    # Creating Database
    #database_db = Neo4j(URI, 'neo4j', 'spiky1234567')

    # Creating a Query 
    #query = """LOAD CSV WITH HEADERS FROM "file:///nodes_test.tsv" AS row CREATE (n:Label {property1: row.property1, property2: row.property2})"""
    #qy = "MATCH (n1)-[r]->(n2) RETURN r, n1, n2 LIMIT 25"
    #result = database_db.run_query(qy)

    #for record in result:print(record)


    #database_db.close()






    return 0


if __name__ == "__main__":
    # Command Line Query
    main(sys.argv)



#LOAD CSV WITH HEADERS FROM "http://localhost:8000/nodes_test.tsv" 
#As row with row where row.id is not null 
#Merge (n:Thing {id:row.id}) SET n.name = row.Label




# NODES DATA THIS 
#LOAD CSV WITH HEADERS FROM "http://localhost:8000/nodes_test.tsv" 
#As row FIELDTERMINATOR "\t"
#Create (n:Data {name:row.kind, id:row.id, dataName:row.name})


# EDGES DATA THIS
#LOAD CSV WITH HEADERS FROM "http://localhost:8000/edges_test.tsv" as row FIELDTERMINATOR "\t"
#MERGE (s:Gene{id:row.source})
#MERGE (t:Gene{id:row.target})
#CALL apoc.create.relationship(s, row.metaedge, {}, t) YIELD rel

#Creating Relationship EXAMPLE
#MATCH (a:Data), (m:Data)
#WHERE a.dataName = 'tendon' AND m.dataName = 'ganglion'
#CREATE (a)-[:rel_type]->(m)
#RETURN a, m

# USE THIS
#LOAD CSV WITH HEADERS FROM "http://localhost:8000/edge.tsv" AS row FIELDTERMINATOR "\t"
#WITH row
#MATCH (r:Data {id: row.ource})
#MATCH (s:Data {id: row.target})
#CREATE (r)-[:rel_type]->(s)
#return r,s


#MATCH (n:Data where n.name = 'Gene' ) RETURN n LIMIT 5