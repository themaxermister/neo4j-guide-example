from neo4j import GraphDatabase

class NBA_Example:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def read_all_players(self):
        with self.driver.session() as session:
            result = session.execute_read(self._return_all_players)
            for player in result:
                print(f"{player['name']} is labelled as a {player['label']}")
            
    def read_all_coaches(self):
        with self.driver.session() as session:
            result = session.execute_read(self._return_all_coaches)
            for coach in result:
                print(coach)
                
    @staticmethod
    def _return_all_players(tx):
        player_ls = []
        result = tx.run("MATCH (player:PLAYER) return player")
        for player in result:
            player_ls.append(player['player'])
        
        return player_ls
            
    
    @staticmethod
    def _return_all_coaches(tx):
        coach_ls = []
        result = tx.run("MATCH (coach:COACH) return coach")
        for coach in result:
            coach_ls.append(coach['coach'])

        return coach_ls
           

if __name__ == "__main__":
    nba = NBA_Example("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    nba.read_all_players()
    nba.close()