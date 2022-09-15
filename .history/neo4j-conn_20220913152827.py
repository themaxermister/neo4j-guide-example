from neo4j import GraphDatabase

class NBA_Neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_all_NBA(self):
        query = "MATCH (n) RETURN n"
        with self.driver.session() as session:
            print(session.execute(tx.run(query)))


if __name__ == "__main__":
    greeter = NBA_Neo4j("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    greeter.print_all_NBA("hello, world")
    greeter.close()