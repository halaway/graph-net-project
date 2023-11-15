
import re
from typing import Dict
import pandas as pd

from neo4j import GraphDatabase
import matplotlib.pyplot as plt

from neo4j import GraphDatabase
import sys

# Using Neo4j For Graph Storage
from pyvis.network import Network
from pyvis import network as net
import numpy as np

from pyspark.sql import SparkSession
from pyspark import SparkContext 
from pyspark.sql.functions import col,desc
from pyspark.sql.functions import count





# Authentication 9
URI = "bolt://localhost:7689"
AUTH = ("neo4j", "spiky1234567")

# http://localhost:7474/browser/


# Creating Spark Session For using with NEO4J
class SparkSess:

    # Creating Spark
    def __init__(self, URI, username, password):
        self.spark = SparkSession.builder \
            .config("spark.neo4j.bolt.url", URI) \
            .config("spark.jars", "/Users/donnie/Downloads/neo4j-connector-apache-spark-5.2.0/neo4j-connector-apache-spark_2.12-5.2.0_for_spark_3.jar")\
            .config("spark.neo4j.bolt.password", password) \
            .config("spark.neo4j.bolt.user", username) \
            .getOrCreate()

    # Creating MapReduce Query For Question One
    def runQuestionOne(self):
        """
            For each drug, compute the number of genes and the number of diseases
            associated with the drug.
        """

        # Creating Map Portion 
        df = self.spark.read.format("org.neo4j.spark.DataSource")\
        .option("url", "bolt://localhost:7689")\
        .option("authentication.type", "basic")\
        .option("authentication.basic.username", "neo4j")\
        .option("authentication.basic.password", "spiky1234567")\
        .option("query", """MATCH (a:Data)-[:CbG|CuG|CtD|CpD]->(relatedNode) WITH a, COUNT(CASE WHEN relatedNode.name = 'Gene' THEN relatedNode END) AS geneCount, Count(Case when relatedNode.name = 'Disease' THEN relatedNode END) as DiseaseCount RETURN a.dataName AS Compound, geneCount, DiseaseCount""" )\
        .load()

        # Creating Reduce Portion Using Spark for Aggregration
        df_updated = (df.groupBy("Compound")
                .agg({"geneCount": "sum", "diseaseCount": "sum"})
                .withColumnRenamed("sum(geneCount)", "Gene Count")
                .withColumnRenamed("sum(diseaseCount)", "Disease Count")
                .orderBy(col("Gene Count").desc(), col("Disease Count").desc(), "Compound"))
    
        # Showing updated dataframe
        df_updated.show()


    # Creating MapReduce Query For Question Two
    def runQuestionTwo(self):
        """
            Compute the number of diseases associated with 1, 2, 3, …, n drugs. Output
            results with the top 5 number of diseases in a descending order
        """

        # Question Two Performing Spark Query 
        df = self.spark.read.format("org.neo4j.spark.DataSource")\
            .option("url", "bolt://localhost:7689")\
            .option("authentication.type", "basic")\
            .option("authentication.basic.username", "neo4j")\
            .option("authentication.basic.password", "spiky1234567")\
            .option("query", """MATCH (a:Data)-[:CpD|CtD]->(b:Data) RETURN a.name AS drugName, COUNT(DISTINCT b) AS numberOfDiseases""")\
            .load()

        # Reducing Dataframe using Aggregration
        df_updated = (df.groupBy("numberOfDiseases")
                .agg(count("drugName").alias("numberOfDrugs"))
                .orderBy("numberOfDiseases"))
    
        # Showing updated dataframe
        df_updated.show()

    # Creating MapReduce Query for Question Three
    def runQuestionThree(self):
        """
            Get the name of drugs that have the top 5 number of genes. 
            Output the results.
        """

        df = self.spark.read.format("org.neo4j.spark.DataSource")\
        .option("url", "bolt://localhost:7689")\
        .option("authentication.type", "basic")\
        .option("authentication.basic.username", "neo4j")\
        .option("authentication.basic.password", "spiky1234567")\
        .option("query", """MATCH (a:Data)-[:CbG|CuG]->(letter) with a, COUNT( case when letter.name='Gene' THEN letter END) AS geneCount  RETURN a.dataName AS Compound, geneCount order by geneCount desc""")\
        .load()

        df.show()


def main():


    questionOne = SparkSess(URI, 'neo4j','spiky1234567')

    questionOne.runQuestionOne()

    # questionOne.runQuestionTwo()
    # questionOne.runQuestionThree()



    return 0;


if __name__ == "__main__":

    main()


