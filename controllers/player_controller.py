from operator import attrgetter
from controllers import main_control
from models import player_model
from views import view_main
from controllers import create_menus
import re


class CreatePlayerController:
    """Entrer tous les détails du joueur, puis ajouter le joueur dans la base de données"""

    def __init__(self):
        self.player_keys = ["Nom", "Prénom", "FFE", "Date de naissance", "Sexe", "Classement"]
        self.home_menu_controller = main_control.HomeMenuController()

    def __call__(self):
        self.player_model = player_model.Player()
        player_values = [
            self.get_valid_input("Entrez le nom de famille: "),
            self.get_valid_input("Entrez le prénom: "),
            self.get_chess_id(), 
            self.get_birth_details(),
            self.get_valid_gender(),
            self.get_valid_ranking()
        ]
        if self.validate_player(player_values):
            self.player_model.add_to_database(player_values)
        self.home_menu_controller()
    
   

    def get_chess_id(self, entered_ids=[]):
        while True:
            chess_id = input("Entrez l'identifiant FFE: ")
            if not re.match(r'^[A-Za-z]{2}\d{5}$', chess_id):
                print("Vous devez entrer un identifiant FFE valide. Exemple: AA12345")
            elif chess_id in entered_ids:
                print("Cet identifiant a déjà été saisi.")
            else:
                entered_ids.append(chess_id)
                return chess_id




    @staticmethod
    def get_valid_input(message):
        while True:
            user_input = input(message)
            if user_input != "":
                return user_input
            else:
                print("Vous devez entrer une valeur.")

    @staticmethod
    def get_birth_details():
        while True:
            day = CreatePlayerController.get_valid_input("Entrez le jour de naissance: ")
            month = CreatePlayerController.get_valid_input("Entrez le mois de naissance: ")
            year = CreatePlayerController.get_valid_input("Entrez l'année de naissance: ")
            if day.isdigit() and month.isdigit() and year.isdigit():
                # TODO: check if the date is valid
                if int(day) < 32 and int(month) < 13 and int(year) < 2023:
                    return f"{day}/{month}/{year}"
            print("Veuillez entrer des valeurs valides pour la date de naissance.")

    @staticmethod
    def get_valid_gender():
        while True:
            gender = input("Choisissez le genre du joueur \n"
                           "'H' pour un homme \n'F' pour une femme: ")
            if gender.upper() == "H":
                return "Homme"
            elif gender.upper() == "F":
                return "Femme"
            else:
                print("Vous devez entrer un genre (H ou F)")

    @staticmethod
    def get_valid_ranking():
        while True:
            ranking = input("Entrez le classement du joueur: ")
            # TODO: check if the ranking is valid
            # ex: 1.5 is not valid, but 1500 is
            if ranking.isdigit() and int(ranking) >= 0:
                return int(ranking)
            else:
                print("Vous devez entrer un nombre entier positif.")

    def validate_player(self, player_values):
        # TODO: check if the player already exists in the database
        view_main.FrameDisplay.display_datas_in_a_frame(player_values, self.player_keys)
        while True:
            choice = input("Valider ce joueur ? \n'Y' pour valider, 'N' pour recommencer\n--> ")
            if choice.upper() == "Y":
                return True
            elif choice.upper() == "N":
                self.home_menu_controller()
            else:
                print("Vous devez entrer 'Y' ou 'N'.")


class PlayerReport:
    """Affiche les rapports des joueurs"""

    def __init__(self):
        self.create_menu = create_menus.CreateMenus()
        self.home_menu_controller = main_control.HomeMenuController()
        self.display_player = view_main.DisplayPlayersReport()
        self.players_database = player_model.player_database
        self.player = player_model.Player()

    def _get_player_serialized(self):
        return [self.player.unserialized(player) for player in self.players_database]

    def _sort_and_display_players(self, key, display_function):
        player_serialized = self._get_player_serialized()
        player_serialized.sort(key=attrgetter(key))
        display_function(player_serialized)
        self.__call__()

    def __call__(self):
        
        entry = self.create_menu(self.create_menu.players_report_menu)

        if entry == "1":
            # Sort the list of players by last name
            self._sort_and_display_players("last_name", self.display_player.display_alphabetical)

        elif entry == "2":
            # Sort the list of players by ranking
            self._sort_and_display_players("ranking", self.display_player.display_ranking)

        elif entry == "3":
            # go back to the home menu
            self.home_menu_controller()
        else:
            print("Invalid entry, please try again.")
            self.__call__()


