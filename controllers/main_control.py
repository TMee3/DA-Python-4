import sys

from views.view_main import MainDisplay, ClearScreen
from controllers.create_menus import CreateMenus
from controllers.player_controller import CreatePlayerController, PlayerReport
from controllers.tournament_controller import (
    TournamentReport,
    CreateTournamentController,
    StartTournament
)
from models.player_model import Player


class HomeMenuController:
    """Affiche le titre et dirige vers le menu principal"""

    def __init__(self):
        # appelle les classes qui vont afficher le titre et le menu principal
        self.view = MainDisplay()
        self.clear = ClearScreen()
        self.create_menu = CreateMenus()
        self.choosen_controller = None

    def __call__(self):
        self.clear()
        self.view.display_title()
        entry = self.create_menu(self.create_menu.main_menu)

        if entry == "1":
            self.choosen_controller = PlayerMenuController()
            self.go_to_player_menu_controller()
        if entry == "2":
            self.choosen_controller = TournamentMenuController()
            self.go_to_tournament_menu_controller()
        if entry == "3":
            self.choosen_controller = QuitAppController()
            self.go_to_quit_app_controller()

    def go_to_player_menu_controller(self):
        self.choosen_controller.__call__()

    def go_to_tournament_menu_controller(self):
        self.choosen_controller.__call__()

    def go_to_quit_app_controller(self):
        self.choosen_controller.__call__()


    def go_to_player_menu_controller(self):
        return self.choosen_controller()

    def go_to_tournament_menu_controller(self):
        return self.choosen_controller()

    def go_to_quit_app_controller(self):
        return self.choosen_controller()


class PlayerMenuController(HomeMenuController):

    def __init__(self):
        super().__init__()
        self.create_player = CreatePlayerController()
        self.players_report = PlayerReport()
        self.home_menu_controller = HomeMenuController()
        self.player_model = Player()

    def __call__(self):
        entry = self.create_menu(self.create_menu.player_menu)
        if entry == "1":
            self.choosen_controller = self.create_player
            self.go_to_create_player_controller()
        elif entry == "2":
            self.choosen_controller = self.player_model.update_ranking
            self.choosen_controller()
        elif entry == "3":
            self.choosen_controller = self.players_report
            self.go_to_players_report_controller()
        elif entry == "4":
            self.choosen_controller = self.home_menu_controller
            self.go_to_home_menu_controller()

    def go_to_create_player_controller(self):
        self.create_player.__call__()

    def go_to_players_report_controller(self):
        self.players_report.__call__()

    def go_to_home_menu_controller(self):
        self.home_menu_controller.__call__()



class TournamentMenuController(HomeMenuController):
    """this class is used to manage the tournament menu"""

    def __init__(self):
        super().__init__()
        self.tournament_report_controller = TournamentReport()
        self.create_tournament_controller = CreateTournamentController()
        self.start_tournament_controller = StartTournament()
        self.home_menu_controller = HomeMenuController()

    def __call__(self):
        """this method is used to call the tournament menu and to start the tournament"""
        entry = self.create_menu(self.create_menu.tournament_menu)
        if entry == "1":
            self.choosen_controller = self.create_tournament_controller
            self.go_to_create_tournament_controller()
        elif entry == "2":
            self.choosen_controller = self.start_tournament_controller
            self.choosen_controller()
        elif entry == "3":
            self.choosen_controller = self.start_tournament_controller.load_tournament_statement
            self.choosen_controller()
        elif entry == "4":
            self.choosen_controller = self.tournament_report_controller
            self.go_to_tournament_report_controller()
        elif entry == "5":
            self.choosen_controller = self.home_menu_controller
            self.go_to_home_menu_controller()

    def go_to_create_tournament_controller(self):
        """this method is used to call the create tournament controller"""
        self.create_tournament_controller.__call__()

    def go_to_tournament_report_controller(self):
        """this method is used to call the tournament report controller"""
        self.tournament_report_controller.__call__()

    def go_to_home_menu_controller(self):
        """this method is used to call the home menu controller"""
        self.home_menu_controller.__call__()



class QuitAppController:

    def __call__(self):
        sys.exit()
