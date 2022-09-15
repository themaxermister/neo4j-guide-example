from neo4j import GraphDatabase

class NBA_Example:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_player(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)
    
    def read_all_players(self):
        with self.driver.session() as session:
            greeting = session.execute_read(self._return_all_players)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Player) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]
    
    @staticmethod
    def _return_all_players(tx):
        result = tx.run("MATCH (n:PLAYER) return n")
        return result


if __name__ == "__main__":
    greeter = NBA_Example("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    greeter.read_all_players()
    greeter.close()