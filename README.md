Daniel Perez A.

# graph-net-project

This file contains all the necessary queries needed for running this program.

- Each Query Solves a specific portion of the project using Neo4J as a graph based NoSQL Store.

To execute a query from the terminal:
    - run: python3 projectBD.py <"QUERY SELETED">

# NOTE
- Files Can be hosted on a local Python server using:
    python3 -m http.server
- When creating a database, the data should only be loaded once for both Nodes and Edges.


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

# 3. Return Genes that Cause this Disease
"""
    MATCH p=(a:Data WHERE a.id='Disease::DOID:7148')
    -[r:DaG]->(n:Data where n.name ='Gene') RETURN n
"""

# 4. Return Where Disease Occurs
"""
    MATCH p=(a:Data WHERE a.id ='Disease::DOID:7148')
    -[r:DlA]->(n:Data) RETURN n
"""


# Potential Cures to Diseases
"""
    match p = (d:Data where d.name='Disease')-[:DlA]->
    (a:Data where a.name ='Anatomy')-[:AuG|AdG]->(g:Data where g.name ='Gene')with d,a,g
    match (n:Data where n.name='Compound')-[:CdG|CuG]->
    (f:Data where f.name ='Gene' and f.id = g.id)
    with d,a,g,n match (n) where not (n)-[:CtD|CpD]->(d) return n
"""


# Loading Nodes: ALREADY LOADED
"""
    #LOAD CSV WITH HEADERS FROM "http://localhost:8000/nodes_test.tsv" 
    As row FIELDTERMINATOR "\t"
    Create (n:Data {name:row.kind, id:row.id, dataName:row.name})
"""

# Loading Edges: ALREADY LOADED
"""
    #LOAD CSV WITH HEADERS FROM "http://localhost:8000/edges_test.tsv" AS row FIELDTERMINATOR "\t"
    WITH row
    WHERE row.ource IS NOT NULL AND row.target IS NOT NULL and row.metaedge is not NULL
    MERGE (s:Data {id: row.ource})
    MERGE (t:Data {id: row.target})
    WITH s, t, row
    CALL apoc.create.relationship(s, row.metaedge, {}, t) YIELD rel
    RETURN *
"""
