from neo4j import GraphDatabase

class NBA_Neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_all_NBA(self, message):
        with self.driver.session() as session:
            query = "MATCH (n) RETURN n"
            all_nodes = session.execute_write(query)
            print(all_nodes)


if __name__ == "__main__":
    greeter = NBA_Neo4j("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    greeter.print_all_NBA("hello, world")
    greeter.close()