## Journal de bord - Thomas Fujise 

### Lundi, 04 Avril 2022
Premier jour du travail de diplôme, il faudrait réussir à mettre en place l'environnement de travail aujourd'hui. Suite à la présentation du déroulement du TD, je change de salle pour m'installer dans la salle à côté. Je vais prendre contact avec M. Jossi, qui est responsable du suivi de mon projet, pour connaitre ses exigences en ce début de projet. Je commence à lister les backlogs identifiables à ce stade sur un Trello. Je réalise en parralèle le planning prévisionnel sur Excel. La journée se termine un peu plus tôt (vers 15h) car nous avons une visite à l'HEPIA.

### Mardi, 05 Avril 2022
Deuxième jour du travail de diplôme, aujourd'hui il faut que j'avance un maximum sur le planning prévisionnel et l'identification des backlogs. J'ai rajouté les difficultés, la priorité et les dépendances sur les tâches dans le Trello. Cela me permet de mieux m'organiser dans l'exécution de tous les backlogs. M. Garcia est venu vers moi pour définir le nom de mon projet (je l'avais appelé "CoachingTools" par défaut), j'ai finalement décidé de nommer mon projet "FitJourney". Je vais terminer de définir les backlogs avant la fin de la journée.

### Mercredi, 06 Avril 2022 
Aujourd'hui, je vais modifier encore quelques détails sur mon planning prévisionnel avant qu'il soit terminé. Le planning prévisionnel est donc terminé ainsi que l'identification des backlogs (du moins ceux identifiables à ce stade). Je vais commencer le maquettage des interfaces avec Figma. Pour les maquettes je vais essayer de faire quelque chose d'assez simple, pour éviter de prendre trop de temps sur cette tâche. Je n'avais pas beaucoup utilisé Figma auparavant mais j'ai réussi à bien prendre l'outil en main durant la matinée. J'ai pu terminer déjà quelques maquettes (Profil, Login, Register) et bientôt celle du tableau de bord pour coach. J'ai pu avancer sur les maquettes, il ne me manque plus que la maquette de la page pour créer  une séance avec un coach. J'ai pris étonnamment beaucoup moins de temps que prévu pour réaliser les maquettes. Je vais donc pouvoir très bientôt commencer à coder. **RAPPEL**: Il faut que je commence la documentation demain pour déjà documenter les maquettes que j'ai réalisées. 

### Jeudi, 07 Avril 2022
Aujourd'hui, je vais terminer les maquettes et commencer la documentation technique. Je vais documenter déjà toutes les maquettes que j'ai réalisé pour ne pas avoir à le faire plus tard. J'ai pu terminer les maquettes avant la fin de la matinée. Il faut maintenant que je créer la structure de la documentation technique, je pourrai ensuite commencer à documenter les maquettes que j'ai réalisé. 

Suite à une discussion avec un ami coach, j'ai découvert l'existence d'une solution similaire à mon projet [Inithy](www.inithy.com). Inithy propose globalement les mêmes fonctionnalités que FitJourney à l'exception que leurs application est orienté coaching à distance là ou moi je m'oriente plus sur le coaching en salle (d'ou les cartes de membres RFID). Inithy est toujours au stade de démo, il faut les contacter pour avoir un accès à leurs application qui n'est pas encore ouvert à tous.

Je vais leurs envoyer une demande pour essayer d'avoir accès à leurs application et pouvoir analyser leurs application un peu plus en détail.

J'ai pu commnecer la documentation des maquettes que j'ai réalisé.
J'ai eu une réflexion sur l'enregistrement d'un nouveau coach, j'envisage deux cas possible :

* Soit l'application est délivré avec un compte coach(admin) et le formulaire d'enregistrement n'est disponible que lorsqu'on est authentifié en tant que coach(admin) (C'est le coach qui rempli le formulaire pour les nouveaux clients)
* Soit rajouter un champ lors de l'inscription avec un code pour créer un novueau compte coach.

### Vendredi, 08 Avril 2022
Fin de la première semaine sur ce travail de diplôme, j'ai pu commencer la documentation et documenter les maquettes que j'ai réalisé. Suite à ma réflexion sur l'enregistrement d'un nouveau coach, j'ai décidé de simplement rajouter une option sur le formulaire d'enregistrement pour créer un compte coach. 
Si une personne venait à créer un compte coach sans l'être ce ne serait pas très dérangeant car un coach n'a accès qu'aux comptes des clients qu'il suit et pour suivre un client il faut que le client confirme de son côté.

Pour un client 2 manières d'avoir un compte :

* Par le formulaire d'enregistrement au préalable, le coach n'aura qu'a séléctionner le profile client lors de la prise en charge.
* Par le coach (un coach peut créer un compte lors de l'ajout d'une prise en charge d'un client, le compte sera créer avec les infos basiques qui seront demandées (Nom, prénom, date de naissance, adresse) et un mot de passe est généré pour permettre au client de se connecter plus tard)

J'ai ajouté la structure de l'application et initialisé les blueprints.
(Les blueprints permettent de séparer l'application en plusieurs modules qui sont ensuite importé au même endroit)

J'ai créer un fichier de config qui permet d'avoir 2 mode : 

* Debug
* Production 

Qui permet d'avoir des paramètres différents. J'ai également ajouté un fichier run qui permet de lancer l'application. Il charge la configuration correspondant au mode actuel (Debug/Production) et run l'application Flask.


### Lundi, 11 Avril 2022

Début de la deuxième semaine du travail de diplôme, aujourd'hui je vais commencer mes pages HTML. Je pense que cela risque de prendre un peu de temps mais en tout cas les maquettes que j'ai réalisé vont me faire gagner pas mal de temps. J'ai réussi à créer une structure de base pour les fichiers html. J'ai décidé d'utiliser *Sneat* qui est un thème css open-source publié par [ThemeSelection](https://themeselection.com/) sous licence MIT. J'ai ajouté un fichier HTML pour les liens CSS qui sera inclus dans toutes mes pages. 

M. Maréchal est venu voir l'avancer du projet car il va superviser mon travail de diplôme de "loin". M. Jossi reste mon suiveur principal. M. Maréchal m'a conseillé de faire un diagramme explicatif du fonctionnement de l'application.

J'ai ajouté la route par défaut pour pouvoir tester une page index avec le css (pour vérifier que tout marche bien). Pour l'instant, je n'ai pas de problème tout à l'air de fonctionner comme il faut. J'ai fait une class "prototype" Users avec SQLAlchemy pour empêcher des erreurs bloquantes avec Flask-Login.

Flask-Login est une librairie qui permet de gérer les sessions utilisateurs pour Flask. (Flask-Login gère les connexions, déconnexions et garde la session utilisateur pour savoir l'utilisateur connecté ou qui vient de se déconnecter)

J'ai maintenant une page index qui peut afficher des composants à l'aide du thème CSS Sneat. Demain je poursuivrai la création de mes pages HTML et il faut également que je commence à rajouter des éléments dans la documentation 

**Ne pas oublier d'avancer la documentation**

### Mardi, 12 Avril 2022
Aujourd'hui je vais essayer de terminer la partie authentification de l'application (Login/Register). J'utilise FlaskForm pour créer mes formulaires et je pense utiliser Mashmallow pour valider les champs en relation avec la BD (Je regarde quelques exemples d'utilisation avec SQLAlchemy : [Exemple](https://marshmallow.readthedocs.io/en/stable/examples.html)).

Il faut également que je fasse le diagramme qui m'a été conseillé par M.Maréchal pour la description du fonctionnement de l'application. 

Pour la sécurité des mots de passe j'ai déjà rajouté 2 méthodes pour permettre de hasher et de vérifier les mots de passe. J'utilise la librairie Python hashlib qui me permet d'hasher les mots de passe avec un salt. Pour éviter d'enregistrer le salt en base, le salt est hashé en *sha256* et est placé avant le mot de passe dans la chaine. Comme un *sha256* a toujours 64 caractères, pour vérifier le mot de passe je saute les 64 premiers caractères de la chaine pour pouvoir comparer avec la saisie de l'utilisateur.

J'ai pu faire un diagramme explicatif des différents processus lors de l'utilisation de mon application en fonction de notre rôle (Client, coach)

[Image](./diagram/diagram.png)

J'ai également terminé le login (le register ne devrait pas prendre beaucoup de temps). J'ai eu quelques soucis pour inclure les formulaires avec FlaskForm (avec les imports python). J'ai ajouté une navbar pour mes pages qui servira pour la navigation dans l'application. J'ai juste encore quelques soucis avec le css mais ce n'est pas du tout prioritaire pour le moment. 

J'ai regardé pour utiliser un outil de génération de documentations, je pense utiliser Pdoc qui à l'air assez complet et qui permet de générer la documentation sur les librairies inclues dans le projet.

### Mercredi, 13 Avril 2022
Dernier jour avant les vacances de pâques, j'essaye d'intégrer pdoc à mon projet mais lorsque je lance la commande pour générer le doc j'obtiens une erreur. Il n'arrive pas à trouver *apps* qui est le dossier principal. 

J'ai pris un peu de retard par rapport à ma planification initiale mais j'ai avancé sur des points que j'étais censé effectuer plus tard dans le projet donc au final je n'ai pas beaucoup de retard. Je vais juste terminer encore ma page register qui va de pair avec la page Login. Il faudra ensuite que je commence à documenter tous le back-end que j'ai déjà effectué. Je pourrai ensuite commencer à travailler sur la base de données car pour le moment j'utilisais une base de données temporaire pour tester mon login. 

En faisant des tests sur le login je me rends compte que j'ai une erreur qui s'affiche lors de la connexion. Lorsque j'effectue la requête pour voir si le mail que l'utlisateur a saisit existe je ne rencontre aucune erreur si le mail inséré n'est pas dans la base mais lorsque le mail rentré se trouve dans la base de données alors une erreur s'affiche : 

```
string argument without an encoding 
```

Après quelques heures d'incompréhension sur cette erreur, je viens d'en trouver la raison. J'avais seulement mit le mauvais type dans l'initialisation du champ mot de passe avec SQLAlchemy.

J'ai enfin finis le register et le login, tout fonctionne comme il faut. Je n'ai plus qu'a rajouter les champs que je veux dans le register (tout le back-end est fonctionnelle). Je vais commencer à documenter les points que j'ai avancé jusque là je pourrai ensuite commencer à travailler sur la base de données.

