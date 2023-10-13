# graph-net-project

🚀 This project examines graph-based data storage for managing and connecting nodes from 
components such as _Compounds_, _Diseases_, _Genes_, and _Anatomies_.

## 📖 Files
- The _"nodes_test.tsv"_ contains over 20,000 nodes pertaining to these four element types with
  each unique attribute such as _ID_, _Name_, and _Kind_.

| ID                     | Name            | Kind      |
| ---------------------- |:---------------:| ---------:|
|Anatomy::UBERON:0000042 | serous membrane | Anatomy   |
| Compound::DB00396      | Progesterone    | Compound  |

- The _"edges_test.tsv_" file contains over 1M edge relationships between a target and source node
  with individually labeled relationship types referred to by the "_metaedges.tsv_" file.

| Metaedge                  | abbreviation     | edges   | source_nodes               | target_nodes     | unbiased   |
| ------------------------- |:---------------:| ---------:| ---------------------- |:---------------:| ---------:|
|Anatomy  downregulates Gene|   AdG        |	   102240	  |  36                    |  	15097	       |      102240|
|Anatomy - expresses - Gene|  	AeG	  |  526407	|   241 |    18094	 | 453477  |
|Anatomy - upregulates - Gene|  	 AuG | 	  97848  | 	36  |  15929	|  97848|


# 💡 NOTE 
- Files Can be hosted on a local Python server using:
    python3 -m http.server
- The Neo4J Base Server Requires authentication and must remain active.
- When creating a database, the data should only be loaded once for both Nodes and Edges.
  
- To execute a query from the terminal:
  - run: python3 projectBD.py <"QUERY SELECTED">

 
 # Example Node Structure 
![possibleCures](https://github.com/halaway/graph-net-project/assets/31904474/5c04b449-6a48-4b7d-b2af-ed7ee827f602)
- When finding possible treatments for Diseases that have no direct connection to any Compound, the approach for such a query is to begin by navigating the genes that are _DownRegulated\UpRegulated_ by a Compound and Anatomy, in the opposite direction, in which the same Disease localizes. This would create the following graph.


## 📝 QUERIES
 The following Queries solve a specific portion of the project using Neo4J as a graph-based NoSQL Store.


# Return Disease Name
    MATCH (n WHERE n.name='Disease' AND 
    n.id ='Disease::DOID:8577') 
    RETURN n

# Return Compounds that Palliate or Treat Disease
    MATCH m=(n:Data)-[:CpD|CtD]->(b:Data where 
    b.id='Disease::DOID:7148') RETURN n
    
# Return Genes that Cause this Disease

    MATCH p=(a:Data WHERE a.id='Disease::DOID:7148')
    -[r:DaG]->(n:Data where n.name ='Gene') RETURN n

# Return Where Disease Occurs

    MATCH p=(a:Data WHERE a.id ='Disease::DOID:7148')
    -[r:DlA]->(n:Data) RETURN 

# Potential Cures to Diseases

    match p = (d:Data where d.name='Disease')-[:DlA]->
    (a:Data where a.name ='Anatomy')-[:AuG|AdG]->(g:Data where g.name ='Gene')with d,a,g
    match (n:Data where n.name='Compound')-[:CdG|CuG]->
    (f:Data where f.name ='Gene' and f.id = g.id)
    with d,a,g,n match (n) where not (n)-[:CtD|CpD]->(d) return n

# Loading Nodes: ALREADY LOADED

    LOAD CSV WITH HEADERS FROM "http://localhost:8000/nodes_test.tsv" 
    As row FIELDTERMINATOR "\t"
    Create (n:Data {name:row.kind, id:row.id, dataName:row.name})
    
# Loading Edges: ALREADY LOADED
    LOAD CSV WITH HEADERS FROM "http://localhost:8000/edges_test.tsv" AS row FIELDTERMINATOR "\t"
    WITH row
    WHERE row.ource IS NOT NULL AND row.target IS NOT NULL and row.metaedge is not NULL
    MERGE (s:Data {id: row.ource})
    MERGE (t:Data {id: row.target})
    WITH s, t, row
    CALL apoc.create.relationship(s, row.metaedge, {}, t) YIELD rel
    RETURN *
