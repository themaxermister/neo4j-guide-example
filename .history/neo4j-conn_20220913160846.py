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
                print(f"{player['name']} is in {list(player.labels)}")
            
    def read_all_coaches(self):
        with self.driver.session() as session:
            result = session.execute_read(self._return_all_coaches)
            for coach in result:
                print(f"{coach['name']} is in {list(coach.labels)}")
    
    def create_new_team(self, name):
        with self.driver.session() as session:
            team = session.execute_write(self._create_and_return_team, name)
            print(team['name'])
    
    def create_new_player(self, name, number, weight, height, age, team=None):
        with self.driver.session() as session:
            player = session.execute_write(self._create_and_return_player, name, number, weight, height, age, team)
            print(player['name'])
        
            if team != None:

            

        

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
    
    @staticmethod
    def _create_and_return_team(tx, name):
        result = tx.run("CREATE (team:TEAM) "
                        "SET team.name = $name "
                        "RETURN team", name=name)
        return result.single()[0]

    @staticmethod
    def _create_and_return_player(tx, name, number, weight, height, age):
        pass
    
    def _add_player_to_team(tx, player, team):
        result = tx.run("MATCH (player:PLAYER) WHERE ID(player) = $player_id "
                        "MATCH (team:TEAM) WHERE ID(team) = $team "
                        "CREATE (player)-[:PLAYS_FOR]->(team) "
                        "RETURN player, team", player=player, team=team)
        return result.single()[0]
        return result.single()[0]
    

if __name__ == "__main__":
    nba = NBA_Example("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    #nba.read_all_players()
    #print("\n")
    #nba.read_all_coaches()
    nba.create_new_team("Golden State Warriors")
    nba.close()