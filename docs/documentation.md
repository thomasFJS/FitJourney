# Documentation technique 

## Résumé 
FitJourney est une application permettant, d'une part, à un coach sportif de gérer le suivi de tous ses clients avec des données d'entrainements récupérées à l'aide de montres connectés Polar. D'autre part, elle permet aux clients d'accéder à leurs programmes d'entrainements et de nutrition. L'application permet également aux clients de visionner le détail de chacune de leurs séances.

FitJourney est une application WEB réalisée avec le framework Flask du langage Python, elle repose principalement sur l'API Polar Accesslink qui permet l'utilisation des données des montres connectées

Ce document reprend toutes les étapes du projet qui a été réalisé dans le cadre du travail de diplôme de la formation Technicien ES en informatique de Thomas Fujise.

## Abstract
FitJourney is an application that allows personal trainers to follow up all his clients training data that is retrieved using Polar connected watches. It also allows clients to access their training and diet plan. The application allows clients to look at the details of each of their workouts.

FitJourney is a WEB application made with Flask Python framework. It relies mainly on the Polar Accesslink API which allows the use of data from connected watches.

This document contains all the steps of the project, which was carried out within the diploma project of the IT Technician formation of Thomas Fujise

## Introduction
Il existe très peu d'outil qui permet à un coach sportif de gérer sa salle de sport avec le suivi de tous ses clients. C'est pourquoi, j'ai décidé de créer une application qui permettrait de gérer une salle de sports ainsi que le suivi des membres. Ayant passé un diplôme de coach sportif l'année passée, j'étais à l'aise avec les besoins qu'un professionnel aurait en cas d'utilisation de l'application.

Cette application permet de gérer la salle de sport avec les cartes de membres qui permettent l'accès à la salle ou encore les montres connectés pour enregistrés les données d'entrainements des clients. Elle permet également le suivi des clients.

## Analyse de l'existant

## Cahier des charges



## Analyse fonctionnelle

### Maquettage
Pour préparer les interfaces, j'ai réalisé des maquettes avec l'outil Figma. Les maquettes m'ont permis de mettre à plat les éléments nécessaires pour les interfaces et ont évité de perdre trop de temps lors de la création des interfaces.

L'application FitJourney propose 3 niveaux d'accès :

* Visiteur
* Client
* Coach

#### En tant que visiteur 
Lorsqu'on arrive sur l'application sans être authentifié, seuls 3 pages sont accessibles. 
##### Page d'accueil
![Home Page](./mockups/Interface_mockups/home.jpg)
La page d'accueil est très basique et propose 2 boutons :

* 1 bouton de connexion
* 1 bouton pour s'enregistrer

##### Page d'enregistrement
![Register Page](./mockups/Interface_mockups/sign_up.jpg)
La page d'enregistrement permet aux utilisateurs de s'enregistrer, une option est disponible pour permettre la création d'un nouveau compte coach. 

##### Page de connexion 
![Login Page](./mockups/Interface_mockups/sign_in.jpg)
La page de connexion permet aux utilisateurs de se connecter. Un lien est disponible si le mot de passe a été oublié.



#### En tant que client 
Si on se connecte à l'application en tant que client, 4 pages supplémentaires sont disponibles.

##### Page profile
![Profile Page](./mockups/Interface_mockups/profile.jpg)

La page profil permet au client de modifier ses informations personnelles. Plusieurs boutons sont disponibles : 

* 1 bouton "Update" pour appliquer les modifications effectuées sur les informations du compte
* 1 bouton pour modifier le mot de passe 
* 1 bouton pour importer une photo de profil.

 Il a également accès à des statistiques sur les données des entrainements qu'il a effectué cette semaine (En dessous des informations de son compte).

##### Page liste de nos entrainements
![List Workouts](./mockups/Interface_mockups/workouts_list.jpg)

Cette page affiche la liste de toutes les entrainements effectués par le client. L'utilisateur peut cliquer sur chaque élément de la liste pour avoir les détails de l'entrainement

##### Page détails entrainement
![Detail workout](./mockups/Interface_mockups/workout_details.jpg)

Cette page affiche les détails d'un entrainement avec les données récupéré à l'aide de la smartwatch. On peut retrouver des informations comme : 

* Le nombre de calories brûlées
* Les pulsations cardiaques par minute avec un graphique montrant l'évolution durant l'entrainement
* La durée de l'entrainement 
* Le type d'entrainement

##### Page prochaine session
![Next session](./mockups/Interface_mockups/client_next_session.jpg)

Cette page affiche les prochaines sessions d'entrainements avec un coach du client 


#### En tant que coach
Si on se connecte à l'application en tant que coach, on a alors accès à 5 pages supplémentaire.

##### Page tableau de bord
![Coach dashboard](./mockups/Interface_mockups/coach_dashboard.jpg)

La page tableau de bord permet au coach de voir la liste des clients dont il effectue le suivi. Le coach peut cliquer sur le nom d'un de ses clients pour afficher le profil du client concerné. Il a également accès à un bouton pour ajouter un nouveau client.
Les informations de la prochaine session avec un client sont disponible en dessous de la liste des clients. 

##### Page Ajout de client 
![Coach Add Client](./mockups/Interface_mockups/add_client.jpg)

La page ajout de client permet au coach d'effectuer la prise en charge d'un nouveau client. Le coach peut séléctionner un compte déjà existant (si le client en a déjà créé un) ou créer un nouveau compte client. Si le coach séléctionne un compte déjà existant les champs se remplisse automatiquement.

##### Page profil client
![Client profil](./mockups/Interface_mockups/profile_with_coach_option.jpg)

La page profil client permet au coach de visionner le profil de ses clients. Plusieurs boutons supplémentaires sont disponibles :

* 1 bouton pour le changement de la carte de membre
* 1 bouton pour le renouvellement de l'abonnement
* 1 bouton pour l'annulation de l'abonnement 
* Importation des programmes

##### Page Paiement
![Coach payment](./mockups/Interface_mockups/payment.jpg)

La page paiement permet de valider le paiement d'un client (Aucune transaction n'est effectué par l'application). Le coach peut séléctionner le type d'abonnement que le client souhaite prendre, la date d'échéance du nouvel abonnement séléctionné ainsi que son coût seront affichés.

##### Page Calendrier
![Coach calendar](./mockups/Interface_mockups/coach_calendar.jpg)

La page calendrier permet au coach d'avoir accès à un calendrier et de visionner les rendez-vous enregistré à la date séléctionné. Un bouton pour ajouter une nouvelle session avec un client est disponible. Le coach doit seulement renseigner :

* Le nom du client (Liste déroulante parmis ses clients)
* L'heure de la session
* La durée
* Le type de session 



### Sitemap

## Analyse Organique

### Mise en place / Envirronement

#### Visual Studio Code


#### GitHub
![Logo Github](./img/github.svg){width=200 align="right"}

Pour pouvoir garder un suivi constant de mon projet, j'ai choisis d'utiliser GitHub comme outil de contrôle de version.

Voici comment est structuré le github :

![Arborescence Github](./img/github_arborescence.PNG)

* Le dossier docs/ contient les fichiers de documentation et de journal de bord
* Le dossier src/ contient tout le code source de l'application
 
#### Trello
![Logo Trello](./img/trello.png){width=200 align="right"}

Trello est un outil de gestion de projet en ligne, inspiré par la méthode Kanban. Il repose sur une organisation des projets en planches listant des cartes, chacune représentant des tâches. 

Afin de créer une roadmap pour mon projet, j'ai utilisé Trello pour lister les différentes étapes de mon projet. J'ai ensuite pu définir les échéances pour chaque tâches/étapes avec mon planning prévisionnel.

J'ai créé 5 colonnes :

* Backlog (Liste de toutes les tâches)
* To-Do (Les tâches qui ont été validées et qui sont à faire)
* Doing (Les tâches en cours)
* Testing (Les tâches en cours de test)
* Done (Les tâches terminées)

#### Python Flask
Flask est un micro-framework Python qui permet la création d'applications web évolutives. Flask dépend de la boite à outils WSGI de [Werkzeug](https://werkzeug.palletsprojects.com/en/2.0.x/) et du moteur de templates [Jinja](https://jinja.palletsprojects.com/en/3.0.x/). Flask était le framework qui répondait le plus à mes besoins, avec l'utilisation de l'API Polar qui est également en Python.

##### Installation Flask
En premier lieu, il faut disposer d'une version à jour de PIP afin d'installer Python Flask avec la commande :

```
pip install Flask
```

##### Utilisation Flask
Pour lancer une application Flask, il faut utiliser la méthode de l'objet Flask : 
```
.run()
```
ou lancer directement l'application à l'aide de la commande : 
```
Flask run
```

##### Micro framework
Un micro framework est un framework qui tente de fournir uniquement les composants absoluments nécessaires à un développeur pour la création d'une application. Par exemple dans le cas d'une application Web, un micro framework peut être spécifiquement conçu pour la construction d'API pour un autre service/application.

Le terme *micro* dans le micro framework signifie que Flask vise à garder le code de base simple mais extensible. Flask ne prendra pas beaucoup de décisions, par exemple quelle base de données utiliser. Les décisions qu'il prend, telles que le moteur de templates à utiliser, sont faciles à modifier. Tout le reste est libre, de sorte que Flask puisse répondre à tous nos besoins et à tous ce que vous ne voulez pas en même temps.

En définissant uniquement le moteur de templates et un système de routes, Flask laisse le choix de personnaliser (en ajoutant des packages) pour la gestion des formulaires par exemple.


### Use case
![Use case](./img/use_case.png)
### Diagramme d'utilisation
![Use diagram](./img/diagram.png)
Diagramme de l'utilisation de l'application pour les 2 types d'utilisateurs.
### Base de données
#### MCD
#### MLD
#### Accès
#### Données de tests
#### Tables
#### SQLAlchemy
