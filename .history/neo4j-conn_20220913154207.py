from neo4j import GraphDatabase

class NBA_Example:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def read_all_players(self):
        with self.driver.session() as session:
            session.execute_read(self._return_all_players)
                
    @staticmethod
    def _return_all_players(tx):
        result = tx.run("MATCH (player:PLAYER) return player")
        for player in result:
            print(player["player"])
            #print(player["n"].get("name"))


if __name__ == "__main__":
    nba = NBA_Example("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    nba.read_all_players()
    nba.close()