# Daniel Perez A.
# CSCI Big Data: Project One

from curses import window
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

import tkinter as tk
from tkinter import *
from tkinter import ttk
import math

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

    def r_query_gui(self, query, **params):
           
            with self.driver.session() as session:
                record = {} 
                s = ""

                # Tokenizing Query for Keyword Word
                word_query = word_tokenize(query.lower())
                
                # Running Query
                try:
                    result = session.run(query, **params)
                except:
                    print ("Query Not Possible")
                    #return 1
                
                else:
                    if 'load' in word_query:
                        print('Neo4j Loaded Data Succesfully')
                        #return 1

                    for x in result:
                        record = dict(x)
                        #s = ''
                        s+= record['n']['name'] +  "Name: " + record['n']['dataName'].title()
                        #return s;
                        #print(record['n']['name'], "Name: ", record['n']['dataName'].title())
                        
                    
                    if not record :
                        print("No Matches Found")
            return s  #




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
        window = tk.Tk()
       #Set the geometry of tkinter frame
        window.geometry("512x270")

        #Create an entry widget to accept user input
        entry= Entry(window, width=20)
        entry.pack(ipadx= 20,pady=20)

        def find_compound():
            no = str(compound.get())
            query_text = f"""MATCH (n WHERE n.name='Compound' AND n.id ='{no}') RETURN n"""
            query = database_db.r_query_gui(query_text)
            Label(window, text=query).pack()


            #Disease::DOID:8577'
        def find_disease():
            no = str(entry.get())
            query_text = f"""MATCH (n WHERE n.name='Disease' AND n.id ='{no}') RETURN n"""
            query = database_db.r_query_gui(query_text)
            Label(window, text=query).pack()

        #Create a button to calculate the number
        ttk.Button(window, text= "Find Disease", command= find_disease).pack()

        #Find Compound
        compound = Entry(window, width=20)
        compound.pack(ipadx= 20,pady=20)

        #Create a button to calculate the number
        ttk.Button(window, text= "Find Compound", command= find_compound).pack()

        #Set the Title of Tkinter window
        window.title("Interative Query")
        window.mainloop()


    else:
        # Running Query From Termnial
        database_db.r_query_gui(command_line_query)

    # Closing Data Base
    database_db.close()



    return 0


if __name__ == "__main__":
    main(sys.argv)

# %%
