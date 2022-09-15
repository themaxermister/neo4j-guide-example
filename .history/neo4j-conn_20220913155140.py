from neo4j import GraphDatabase

class NBA_Example:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def read_all_players(self):
        with self.driver.session() as session:
            result = session.execute_read(self._return_all_players)
            print(result)
            
    def read_all_coaches(self):
        with self.driver.session() as session:
            result = session.execute_read(self._return_all_coaches)
            print(result)
                
    @staticmethod
    def _return_all_players(tx):
        result = tx.run("MATCH (player:PLAYER) return player")
        return result
        for player in result:
            print(list((player["player"].labels)))  # Get all labels
            print(player["player"].get("name")) # Access properties
    
    @staticmethod
    def _return_all_coaches(tx):
        result = tx.run("MATCH (coach:COACH) return coach")
        return result
        for coach in result:
            print(list((coach["coach"].labels)))  # Get all labels
            print(coach["coach"].get("name")) # Access properties
        

if __name__ == "__main__":
    nba = NBA_Example("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    nba.read_all_players()
    nba.close()