Ce fichier readme décrit une application permettant de gérer un tournoi d'échecs, développée dans le cadre d'un projet d'Openclassroom. L'application permet de créer la structure d'un tournoi, d'ajouter des joueurs dans une base de données et utilise un algorithme de tournoi pour calculer la rotation des joueurs. Le design pattern MVC a été utilisé et la librairie TinyDB a été utilisée pour sauvegarder les joueurs et les tournois.

Le document fournit également des instructions pour les prérequis, le démarrage et la génération du rapport flake8. Les prérequis comprennent l'installation de Python, de plusieurs librairies externes et de l'environnement virtuel venv. Les instructions pour démarrer le programme incluent la copie des fichiers et des répertoires du référentiel et l'exécution du programme depuis un terminal.

Le rapport flake8 est un outil de qualité du code qui vérifie la conformité avec les règles de codage et fournit des informations sur les erreurs et les avertissements. Le rapport flake8 pour ce projet ne contient aucune erreur.


Pour pouvoir utiliser l'application, il est nécessaire d'installer Python, la dernière version étant disponible sur le site https://www.python.org/downloads/.

Les scripts Python sont exécutés à partir d'un terminal. Pour ouvrir un terminal sur Windows, appuyez sur la touche Windows + R, puis entrez "cmd". Sur Mac, appuyez sur la touche Command + Espace, puis entrez "Terminal". Sur Linux, vous pouvez ouvrir un terminal en appuyant sur les touches Ctrl + Alt + T.

L'application utilise plusieurs librairies externes et des modules Python qui sont répertoriés dans le fichier "requirements.txt". Vous pouvez installer un environnement virtuel en utilisant la commande "pip install myenv" dans le terminal. Ensuite, pour installer toutes les librairies, entrez la commande "pip install -r requirements.txt". Cela permettra de s'assurer que toutes les dépendances nécessaires sont installées et que l'application peut fonctionner correctement.

Pour lancer l'application, il est nécessaire de copier tous les fichiers et répertoires du référentiel. Ensuite, depuis un terminal, entrez la commande suivante : python main.py
Cela permettra de lancer l'application.

Le référentiel contient également un rapport flake8, qui ne présente aucune erreur. Si vous souhaitez générer un nouveau rapport, vous pouvez installer le module flake8 et entrer la commande suivante dans le terminal : flake8
Le fichier "setup.cfg" situé à la racine du référentiel contient les paramètres de génération du rapport. Le rapport sera généré dans le répertoire "flake-report".

Cette application a été développée en utilisant Python, TinyDB et le pattern MVC pour gérer les rotations des joueurs dans un tournoi d'échecs.

