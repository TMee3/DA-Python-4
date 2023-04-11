class CreateMenus:
    """Crée le menu principal, et dirige ensuite
    vers les branches de menus en fonction du numéro choisi"""

    main_menu = [("1", "Menu Joueur"),
                 ("2", "Menu Tournoi"),
                 ("3", "Quitter")]

    player_menu = [("1", "Créer un joueur"),
                   ("2", "Mettre à jour le classement d'un joueur"),
                   ("3", "Afficher un rapport"),
                   ("4", "Retour au menu principal")]

    tournament_menu = [("1", "Créer un nouveau tournoi"),
                       ("2", "Lancer un tournoi existant"),
                       ("3", "Reprendre un tournoi en cours"),
                       ("4", "Afficher un rapport"),
                       ("5", "Retour au menu principal")]

    time_control_menu = [("1", "Bullet"),
                         ("2", "Blitz"),
                         ('3', "Coup rapide")]

    players_report_menu = [("1", "Par ordre alphabétique"),
                           ("2", "Par ordre de classement"),
                           ("3", "Retour au menu principal")]

    tournaments_report_menu = [("1", "Afficher tous les tournois"),
                               ("2", "Choisir un tournoi"),
                               ("3", "Retour au menu principal")]

    tournaments_report_menu_2 = [("1", "Afficher les joueurs"),
                                 ("2", "Afficher les tours"),
                                 ("3", "Afficher les matchs"),
                                 ("4", "Retour au menu principal")]

    def __call__(self, menu_to_display):
        """Affiche un menu et demande à l'utilisateur de choisir"""
        for numero, description in menu_to_display:
            print(f"{numero} : {description}")
        while True:
            entry = input("-->")
            for numero, _ in menu_to_display:
                if entry == numero:
                    return str(numero)
            print("Vous devez entrer le numéro correspondant")
