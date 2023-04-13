import time
from operator import itemgetter
from operator import attrgetter
import pandas as pd
from controllers import main_control
from controllers import create_menus
from models import tournament_model
from models import player_model
from views import view_main


class CreateTournamentController:
    """Create a tournament with entering all the details, then save it in the database"""

    def __init__(self):
        self.create_menu = create_menus.CreateMenus()
        self.tournament_values = []
        self.players_in_tournament = []
        self.players_ids = []
        self.players_serialized = []
        self.player = player_model.Player()
        self.home_menu_controller = main_control.HomeMenuController()
        self.tournament = tournament_model.Tournament()

    def __call__(self):
        self.tournament_values.append(self.add_tournament_name())
        self.tournament_values.append(self.add_location())
        self.tournament_values.append(self.add_tournament_date())
        self.tournament_values.append(self.add_number_of_rounds())
        self.tournament_values.append(self.add_time_control())
        self.tournament_values.append(self.add_description())
        self.add_players_to_tournament()
        self.tournament_values.append(self.players_in_tournament)
        self.tournament.add_to_database(self.tournament_values)
        self.home_menu_controller()

    def add_tournament_name(self):
        """Asks user for the name of the tournament."""
        valid_tournament_name = False
        # This loop will repeat until valid
        while not valid_tournament_name:
            # Get tournament name
            tournament_name = input("Entrez le nom du tournoi: ")
            # Check if tournament name is not empty
            if tournament_name != "":
                # If the tournament name is not empty, we can exit the loop
                valid_tournament_name = True
            else:
                print("Vous devez entrer un nom")
        return tournament_name

    def add_location(self):
        # Initialize a while loop to ask the user to enter the location
        while True:
            # Ask the user to enter the location
            location = input("Entrez l'endroit où se déroule le tournoi: ")
            # If the location is not empty, return the location
            if location != "":
                return location
            # If the location is empty, print an error message
            else:
                print("L'emplacement du tournoi ne peut pas être vide")

    def add_tournament_date(self):
        while True:
            day = input("Entrez le jour du tournoi: ")
            month = input("Entrez le mois du tournoi: ")
            year = input("Entrez l'année du tournoi: ")
            if day.isdigit() and month.isdigit() and year.isdigit():
                if int(day) in range(1, 32) and int(month) in range(1, 13) and int(year) in range(2000, 2100):
                    return f"{day}/{month}/{year}"
                else:
                    print("La date n'est pas valide")
            else:
                print("Vous devez entrer un nombre entier")

    def add_number_of_rounds(self):
        default_number_of_rounds = 4
        print(
            "Le nombre de rounds est de 4 par défaut.\n"
            "Souhaitez-vous changer ce nombre ?"
            )
        while True:
            choice = input(
                "Entrez 'Y' pour changer, ou 'N' pour continuer: "
            ).lower()
            if choice == "y":
                while True:
                    number_of_rounds = input("Entrez le nombre de rounds: ")
                    if number_of_rounds.isdigit():
                        if int(number_of_rounds) in range(1, 9):
                            return int(number_of_rounds)
                        else:
                            print("Le nombre de rounds doit être compris entre 1 et 8")
                    else:
                        print("Vous devez entrer un nombre entier")
            elif choice == "n":
                return default_number_of_rounds
            else:
                print("Veuillez entrer 'Y' ou 'N'")

    def add_time_control(self):
        print("Choisissez le contrôle du temps:")
        time_control = None
        entry = self.create_menu(self.create_menu.time_control_menu)
        if entry == "1":
            time_control = "Bullet"
        if entry == "2":
            time_control = "Blitz"
        if entry == "3":
            time_control = "Coup rapide"
        return time_control

    def add_description(self):
        description = input("Entrer une description au tournoi :\n"
                            "-->")
        return description

    def add_players_to_tournament(self):
        """Add the ids of the selected players in a list, and return the list"""

        view_main.ClearScreen()

        while True:
            add_player_choice = input(
                "\nVoulez-vous ajouter un joueur ?\n\n"
                "Appuyer sur 'Y' pour confirmer, ou 'N' pour poursuivre: "
            ).upper()

            if add_player_choice == "N":
                return
            elif add_player_choice == "Y":
                break
            else:
                print("Appuyez sur 'Y' ou 'N'")

        display_players_database = pd.read_json("models/players.json")
        print(display_players_database)
        print("\nVous devez choisir un nombre de joueurs pair\n")
        print("Joueurs dans le tournoi : " + str(self.players_ids) + "\n")
        while True:
            id_choices = input("Entrez les numéros des joueurs séparés par des virgules (ex. 1,2,3): ")
            try:
                id_choices = [int(id) for id in id_choices.split(",")]
                invalid_ids = [id for id in id_choices if id <= 0 or id > len(player_model.player_database)]
                if invalid_ids:
                    print(f"\nLes numéros suivants ne sont pas valides : {invalid_ids}\n")
                elif any(id in self.players_ids for id in id_choices):
                    print("\nVous avez déjà choisi un ou plusieurs de ces joueurs dans ce tournoi\n")
                    print("Joueurs dans le tournoi : " + str(self.players_ids) + "\n")
                elif len(id_choices) % 2 == 1:
                    print("\nVous devez choisir un nombre de joueurs pair\n")
                else:
                    break
            except ValueError:
                print("\nVous devez entrer des numéros entiers séparés par des virgules (ex. 1,2,3)\n")
        self.players_ids.extend(id_choices)
        print("Joueurs dans le tournoi : " + str(self.players_ids) + "\n")
        self.add_players_to_tournament()

        # Iterate through the ids list, create instances of players, then sort them by ranking
        self.players_serialized = [player_model.player_database.get(doc_id=id) for id in self.players_ids]
        self.players_serialized.sort(key=itemgetter("Classement"), reverse=True)
        self.players_ids = [player.doc_id for player in self.players_serialized]
        self.tournament_values.append(self.players_ids.copy())


class StartTournament:
    """Controller who start the tournament, stop when the tournament is ended"""
    MATCHS_PLAYED = []
    TOURS_PLAYED = []

    def __call__(self):
        self.sorted_players = []
        self.tournament_menu_controller = main_control.TournamentMenuController()
        self.tour = tournament_model.Tour()
        self.view_final_scores = view_main.EndTournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()

        # Ask to choose a tournament and return an instance of tournament
        self.tournament_object = self.select_a_tournament()

        # copy in the list "sorted_players" the players by ranking
        self.sorted_players = self.sort_player_first_tour(self.tournament_object)
        # 1st tour, copy the instance in tournament
        self.tournament_object.list_of_tours.append(self.tour.run(self.sorted_players, self.tournament_object))
        self.save_tournament_statement(self.tournament_object)

        # all the others tours
        for tour in range(int(self.tournament_object.number_of_tours) - 1):
            self.sorted_players.clear()
            self.sorted_players = self.sort_players_by_score(self.tournament_object.list_of_tours[tour])
            self.tournament_object.list_of_tours.append(self.tour.run(self.sorted_players, self.tournament_object))
            self.save_tournament_statement(self.tournament_object)

        self.view_final_scores(self.tournament_object)
        self.home_menu_controller()

    def save_tournament_statement(self, tournament_object):

        self.home_menu_controller = main_control.HomeMenuController()
        db_tournament = tournament_model.tournament_database
        tours_table = db_tournament.table("tours")

        tour_object = tournament_object.list_of_tours[-1]
        tour_serialized = tour_object.serialized()
        tour_serialized['Matchs'] = tour_object.list_of_finished_matchs

        tour_id = tours_table.insert(tour_serialized)
        StartTournament.TOURS_PLAYED.append(tour_id)
        db_tournament.update({"Tours": StartTournament.TOURS_PLAYED}, doc_ids=[tournament_object.tournament_id])

        print("Voulez vous sauvegarder et quitter le tournoi en cours ? Y / N")
        valid_choice = False
        while not valid_choice:
            choice = input("-->")
            if choice == 'Y':
                valid_choice = True
                self.home_menu_controller()
            elif choice == 'N':
                valid_choice = True
                break
            else:
                print("Vous devez entrer 'Y' ou 'N'")
                continue

    def load_tournament_statement(self):
        # choisir un tournoi et calculer le nombre de tours restant
        sorted_players = []
        self.tournament = tournament_model.Tournament()
        self_display_tournament = view_main.LoadTournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()
        self.tour = tournament_model.Tour()
        self.view_final_scores = view_main.EndTournamentDisplay()
        db_tournament = tournament_model.tournament_database
        tours_table = db_tournament.table("tours")
        tours_instances = []

        if self_display_tournament():  # True if there is tournaments already started
            valid_entry = False
            while not valid_entry:
                print("Entrez le chiffre correspondant au tournoi")
                choice = input("--> ")
                try:
                    int(choice)
                    valid_entry = True
                except Exception:
                    print("Vous devez entrer le chiffre correspondant au tournoi")
            else:
                choosen_tournament = tournament_model.tournament_database.get(doc_id=int(choice))
                for tour in choosen_tournament["Tours"]:
                    tour_serialized = tours_table.get(doc_id=tour)
                    tour_object = self.tour.unserialized(tour_serialized)
                    tours_instances.append(tour_object)
                choosen_tournament["Tours"] = tours_instances
                tournament_object = self.tournament.unserialized(choosen_tournament)

        else:
            print("Pas de tournoi en cours, retour au menu principal")
            time.sleep(1)
            self.home_menu_controller()

        for tour in range(int(tournament_object.number_of_tours) - len(tournament_object.list_of_tours)):
            sorted_players.clear()
            sorted_players = self.sort_players_by_score(tournament_object.list_of_tours[tour])
            tournament_object.list_of_tours.append(self.tour.run(sorted_players, tournament_object))
            self.save_tournament_statement(tournament_object)

        self.view_final_scores(tournament_object)
        self.home_menu_controller()

    def select_a_tournament(self):
        self.tournament = tournament_model.Tournament()
        self.display_tournaments = view_main.TournamentDisplay()
        self.home_menu_controller = main_control.HomeMenuController()

        if self.display_tournaments():

            valid_entry = False
            while not valid_entry:
                print("Entrez le chiffre correspondant au tournoi")
                choice = input("--> ")
                try:
                    choice.isdigit() is False
                    int(choice) < len(tournament_model.tournament_database)
                    int(choice) <= 0
                except Exception:
                    print("Vous devez entrer le chiffre correspondant au tournoi")
                else:
                    choosen_tournament = tournament_model.tournament_database.get(doc_id=int(choice))
                    tournament_object = self.tournament.unserialized(choosen_tournament)
                    return tournament_object
        else:
            print("Pas de tournois créé, veuillez créer un tournoi")
            time.sleep(1)
            self.home_menu_controller()

    def sort_player_first_tour(self, tournament):
        """Retourne une liste de joueurs triée pour le premier tour"""
        self.player = player_model.Player()
        sorted_players = []
        players_instances = []

        # Création d'une liste d'instances de joueurs triée par rang pour le premier tour
        for id in tournament.players_ids:
            player = player_model.player_database.get(doc_id=id)
            player = self.player.unserialized(player)
            players_instances.append(player)

        # Division du nombre de joueurs par 2 et ajout du résultat à l'index
        # Exemple : pour 8 joueurs, j'ajoute 4 au premier index
        # joueur[0] contre joueur[4], joueur[1] contre joueur[5], etc.
        for player in players_instances:
            player_1 = player
            index_player_1 = players_instances.index(player)

            if index_player_1 + len(tournament.players_ids) / 2 < len(tournament.players_ids):
                index_player_2 = index_player_1 + int(len(tournament.players_ids) / 2)
                player_2 = players_instances[index_player_2]
                sorted_players.append(player_1)
                sorted_players.append(player_2)
                self.MATCHS_PLAYED.append({player_1.player_id, player_2.player_id})
            else:
                pass
        return sorted_players

    def sort_players_by_score(self, tour_instance):
        """Retourne une liste de joueurs triée par score"""
        # Création des variables nécessaires
        self.player = player_model.Player()
        players_sorted_by_score = []
        players_sorted_flat = []
        players_instance = []

        # Ajout de tous les joueurs qui ont participé au tournoi à une liste
        for match in tour_instance.list_of_finished_matchs:
            for player in match:
                players_sorted_by_score.append(player)

        # Création d'une liste contenant seulement les IDs des joueurs
        players_sorted_flat = [player[0] for player in players_sorted_by_score]

        # Nettoyage de la liste des joueurs triés par score pour y ajouter les instances des joueurs triés
        players_sorted_by_score.clear()

        # Création d'une liste d'instances de joueurs triés par score
        for player_id in players_sorted_flat:
            player = self.players_database.get(doc_id=player_id)
            players_instance.append(self.player.unserialized(player))

        # Tri des joueurs par score, en cas d'égalité, tri par rang
        players_instance.sort(key=attrgetter("tournament_score", "ranking"), reverse=True)

        # Création d'une liste de joueurs triée par score
        for i in range(0, len(players_instance)-1, 2):
            player_1 = players_instance[i]
            player_2 = players_instance[i+1]

            # Vérification si le match a déjà été joué
            if {player_1.player_id, player_2.player_id} in self.MATCHS_PLAYED:
                print(f"Le match {player_1} CONTRE {player_2} a déjà eu lieu")
                time.sleep(1)
                continue

            # Ajout du match à la liste des matches déjà joués
            self.MATCHS_PLAYED.append({player_1.player_id, player_2.player_id})

            # Ajout des joueurs à la liste triée par score
            players_sorted_by_score.append(player_1)
            players_sorted_by_score.append(player_2)

            print(f"Ajout du match {player_1} (blanc) CONTRE {player_2} (noir)")
            time.sleep(1)

        return players_sorted_by_score


class TournamentReport:
    """Display the tournament reports"""

    def __init__(self):
        self.clear = view_main.ClearScreen()
        self.create_menu = create_menus.CreateMenus()
        self.display_tournament = view_main.DisplayTournamentsReport()
        self.display_player = view_main.DisplayPlayersReport()
        self.home_menu_controller = main_control.HomeMenuController()
        self.players_database = player_model.player_database
        self.player = player_model.Player()
        self.tournament_database = tournament_model.tournament_database
        self.tournament = tournament_model.Tournament()

    def display_all_tournaments(self):
        tournament_serialized = [self.tournament.unserialized(tournament) for tournament in self.tournament_database]
        player_serialized = []
        for tournament in tournament_serialized:
            for id in tournament.players_ids:
                player = self.players_database.get(doc_id=id)
                player_serialized.append(self.player.unserialized(player))
        player_serialized.sort(key=lambda player: player.last_name)
        self.display_tournament.display_tournaments(tournament_serialized, player_serialized)

    def display_players_alphabetical(self, tournament_object):
        player_serialized = [
            self.player.unserialized(self.players_database.get(doc_id=int(id)))
            for id in tournament_object.players_ids
        ]
        player_serialized.sort(key=lambda player: player.last_name)
        self.display_player.display_alphabetical(player_serialized)

    def display_players_ranking(self, tournament_object):
        player_serialized = [
            self.player.unserialized(self.players_database.get(doc_id=int(id)))
            for id in tournament_object.players_ids
        ]
        player_serialized.sort(key=lambda player: player.ranking)
        self.display_player.display_ranking(player_serialized)

    def display_tours(self, tournament_object):
        tour_table = self.tournament_database.table("tours")
        for tour_id in tournament_object.list_of_tours:
            tour = tour_table.get(doc_id=tour_id)
            tour_name = tour["Nom"]
            tour_start = tour["Debut"]
            tour_end = tour["Fin"]
            print(f"{tour_name} - Début: {tour_start} - Fin: {tour_end}\n")

    def display_matchs(self, tournament_object):
        tour_table = self.tournament_database.table("tours")
        for tour in tournament_object.list_of_tours:
            tour_object = tour_table.get(doc_id=tour)
            tour_name = tour_object["Nom"]
            print(f"{tour_name} :")
            for match in tour_object["Matchs"]:
                player_1_id = match[0][0]
                player_1 = self.players_database.get(doc_id=player_1_id)
                player_2_id = match[1][0]
                player_2 = self.players_database.get(doc_id=player_2_id)
                score_player_1 = match[0][1]
                score_player_2 = match[1][1]
                print(
                    f"{player_1['Nom']} {player_1['Prenom']} CONTRE {player_2['Nom']} {player_2['Prenom']}\n"
                    f"Score : {score_player_1} -- {score_player_2}\n"
                    )

    def __call__(self):
        self.clear()
        self.display_tournament()
        entry = self.create_menu(self.create_menu.tournaments_report_menu)

        if entry == "1":
            self.display_all_tournaments()
            self.home_menu_controller()

        elif entry == "2":
            # Affichage des tournois avec leur id
            # Création d'une liste de tournois
            # Demande de l'id du tournoi
            for tournament in self.tournament_database:
                tournament_object = self.tournament.unserialized(tournament)
                print(f"{tournament.doc_id}")
                # Affichage de l'id du tournoi
            tournament_chosen = False
            while not tournament_chosen:
                choice_id = input("Entrez le numéro correspondant au tournoi : ")
                for tournament in self.tournament_database:
                    if int(choice_id) == tournament.doc_id:
                        tournament_object = self.tournament.unserialized(tournament)
                        if tournament_object.list_of_tours == []:
                            print("\nLe tournoi n'a pas encore eu lieu, vous ne pouvez pas afficher les résultats.\n")
                            time.sleep(1)
                        else:
                            entry = self.create_menu(self.create_menu.tournaments_report_menu_2)

                            if entry == "1":
                                entry = self.create_menu(self.create_menu.players_report_menu)

                                if entry == "1":
                                    self.display_players_alphabetical(tournament_object)
                                    TournamentReport.__call__(self)

                                elif entry == "2":
                                    self.display_players_ranking(tournament_object)
                                    input("Appuyez sur une touche pour revenir au menu rapport de tournoi")
                                    TournamentReport.__call__(self)

                            elif entry == "2":
                                self.display_tours(tournament_object)
                                input("Appuyez sur une touche pour revenir au menu rapport de tournoi")
                                TournamentReport.__call__(self)

                            elif entry == "3":
                                self.display_matchs(tournament_object)
                                input("Appuyez sur une touche pour revenir au menu rapport de tournoi")
                                TournamentReport.__call__(self)

                            elif entry == "4":
                                tournament_chosen = True
                                self.home_menu_controller()

                if not tournament_chosen:
                    print("Vous devez entrer le numéro correspondant au tournoi")

        elif entry == "3":
            self.home_menu_controller()

        else:
            print("Vous devez entrer le numéro correspondant au tournoi")
