import re
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
                print(f"{player.element_id}: {player['name']} is in {list(player.labels)}")
            
    def read_all_coaches(self):
        with self.driver.session() as session:
            result = session.execute_read(self._return_all_coaches)
            for coach in result:
                print(f"{coach['name']} is in {list(coach.labels)}")
    
    def create_new_team(self, name):
        with self.driver.session() as session:
            team = session.execute_write(self._create_and_return_team, name)
            print(f"{team.element_id}: {team['name']}")
            return team
    
    def get_all_players_in_team(self, team):
        with self.driver.session() as session:
            players = session.execute_write(self._create_and_return_team_members, team)
            for player in players:
                print(f"{player.element_id}: {player['name']} is in {list(player.labels)}")
    
    def create_new_player(self, name, number, weight, height, age, team=None):
        with self.driver.session() as session:
            player = session.execute_write(self._create_and_return_player, name, number, weight, height, age)
            print(f"{player.element_id}: {player['name']} is in {list(player.labels)}")
            return player

    def add_player_to_team(self, player, team):
         with self.driver.session() as session:
            results = session.execute_write(self._add_player_to_team, player, team)
            for node in results:
                print(f"{node['player'].get('name')} added to {node['team'].get('name')}")

    def get_player(self, name):
        with self.driver.session() as session:
            player = session.execute_write(self._return_player, name)
            if player:
                print(f"{player.element_id}: {player['name']} is in {list(player.labels)}")
                return player
            
            print("PLAYER NOT FOUND")
            return None
    

    def check_player_exist(self, name):
        with self.driver.session() as session:
            results = session.execute_write(self._return_player_exist, name)
            print(results)

    @staticmethod
    def _create_and_return_team_members(tx, team):
        players_ls = []
        result = tx.run("MATCH (player:Player)-[:PLAYS_FOR]->(team:Team {name: $team_name}) RETURN player", team_name=team)
        for player in result:
            print(player)
            players_ls.append(player["player"])
        exit(0)

    @staticmethod
    def _return_player_exist(tx, name):
        result = tx.run("MATCH (p:PLAYER {name:$name}) WITH COUNT(p) > 0 as node_count RETURN node_count", name=name)
        return result.single()[0]

    @staticmethod
    def _return_player(tx, name):
        result = tx.run("MATCH (player:PLAYER) WHERE player.name = $name return player", name=name)
        if result.single() == None: #NTF TO CHECK EXIST
            return None
        return result.single()[0]

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
        result = tx.run("""MERGE (team:TEAM {name: $name})
                        SET team.name = $name
                        RETURN team""", name=name)
        
        return result.single()[0]

    @staticmethod
    def _create_and_return_player(tx, name, number, weight, height, age):
        result = tx.run("MERGE (player:PLAYER {name: $name}) "
                        "SET player.name = $name, player.number = $number, player.weight = $weight, player.height = $height, player.age = $age "
                        "RETURN player", name=name, number=number, weight=weight, height=height, age=age)


        return result.single()[0]
    
    @staticmethod
    def _add_player_to_team(tx, player, team):
        relation_nodes = []
        results = tx.run("MATCH (player:PLAYER {name: $player_id}) "
                        "MATCH (team:TEAM {name: $team_id}) "
                        "MERGE (player)-[:PLAYS_FOR]->(team) "
                        "RETURN player, team", player_id=player.get('name'), team_id=team.get('name'))
        for record in results:
            relation_nodes.append(record)
        
        return relation_nodes
    

if __name__ == "__main__":
    nba = NBA_Example("bolt://localhost:7687", "neo4j", "P@ssw0rd123")
    #nba.read_all_players()
    #print("\n")
    #nba.read_all_coaches()
    #team = nba.create_new_team("Milwaukee Bucks")
    #player = nba.create_new_player("Stephen Curry", 30, 84, 1.88, 34, "Golden State Warriors")
    #nba.add_player_to_team(player, team)
    #nba.get_player("Stephen Curry")
    nba.get_all_players_in_team("Golden State Warriors")

    nba.close()