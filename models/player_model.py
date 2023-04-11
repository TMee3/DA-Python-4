import time
from tinydb import TinyDB
from controllers import main_control
from views import view_main

player_database = TinyDB('models/players.json')

class Player:
    def __init__(self, last_name=None, first_name=None, birthdate=None, chess_id=None, gender=None, ranking=None, tournament_score=0, player_id=0):
        self.last_name = last_name
        self.first_name = first_name
        self.birthdate = birthdate
        self.chess_id = chess_id
        self.gender = gender
        self.ranking = ranking
        self.tournament_score = tournament_score
        self.player_id = player_id

    def serialized(self):
        return {
            'Nom': self.last_name,
            'Prenom': self.first_name,
            'Date de naissance': self.birthdate,
            'FFE': self.chess_id,
            'Sexe': self.gender,
            'Classement': self.ranking,
            'Score': self.tournament_score,
            'Id du joueur': self.player_id
        }

    @classmethod
    def unserialized(cls, serialized_player):
        return cls(
            serialized_player['Nom'],
            serialized_player['Prenom'],
            serialized_player['Date de naissance'],
            serialized_player['FFE'],
            serialized_player['Sexe'],
            serialized_player['Classement'],
            serialized_player['Score'],
            serialized_player['Id du joueur']
        )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def __repr__(self):
        return f"{self.last_name} {self.first_name}, classement : {self.ranking}"

    @classmethod
    def get_player(cls, player_id):
        player_to_modify = player_database.get(doc_id=int(player_id))
        return cls.unserialized(player_to_modify)

    def update_ranking(self):
        self.home_menu_controller = main_control.HomeMenuController()
        self.view_players = view_main.PlayersDiplay()
        self.players_database = player_database

        self.view_players()

        while True:
            player_id = input("Entrer le numéro du joueur : ")
            if player_id.isdigit() and int(player_id) >= 0 and int(player_id) <= len(self.players_database):
                break
            else:
                print("Vous devez entrer le numéro correspondant au joueur")

        while True:
            new_ranking = input("Entrez le nouveau classement : ")
            if new_ranking.isdigit() and int(new_ranking) >= 0:
                break
            else:
                print("Vous devez entrer un nombre entier positif")

        player = self.get_player(player_id)
        player.ranking = int(new_ranking)

        player_database.update({"Classement": int(new_ranking)}, doc_ids=[int(player_id)])
        print(f"{player.last_name} {player.first_name} \nNouveau classement : {new_ranking}")
        time.sleep(2.5)
        self.home_menu_controller()

    @classmethod
    def add_to_database(cls, player_values):
        player = cls(*player_values)
        player_id = player_database.insert(player.serialized())
        player_database.update({'Id du joueur': player_id}, doc_ids=[player_id])
        time.sleep(2)
