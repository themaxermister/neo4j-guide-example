from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687",
                              auth=("neo4j", "password"))
    
    

driver.close()