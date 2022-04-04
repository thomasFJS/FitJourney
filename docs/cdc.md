# Cahier des charges
## Sujet
Créer une application WEB regroupant des clients et des coachs de sport pouvant récupérer des données d'entrainements directement depuis un appareil connecté Polar

## But du projet
Le but du projet est de créer une plateforme WEB regroupant pratiquants et coachs afin de gérer une salle de sport et le suivi des pratiquants.
Les données d'entrainements suivantes sont récupérées depuis une smartwatch Polar:

* Pulsation cardiaque (Repos/Actif/Après effort)
* Le type d'exercice effectué
* Date et durée de l'entrainement
* Nombre de total de calories brulées 
* Nombre de calories active
(Optionnel)
* Les données relatives au sommeil 
    * Pulsation cardiaque
    * Cycles de sommeil
    * Interruption
    * Hypnogramme

Il y a également un système de badging pour savoir quand le pratiquant commence et mets fin à son entrainement. 

## Utilisation
La plateforme Web permet de s'enregistrer soit en tant que pratiquant, soit en tant que coach.

**En tant que clients** :
L'ID utilisateur Polar doit être renseigné lors de l'inscription. Une fois le compte créé, on dispose d'une page profil avec plusieurs données d'entrainement, quelques graphiques pour les illustrer permettant d'observer la progression au fur et à mesure du temps. Lorsqu'un compte client est créé, une carte RFID lui est attribuée afin de badger le début et la fin d'un entrainement. Une fois la fin de l'entrainement badgé, l'API Accesslink Polar permettra de récupérer les données de la séance achevée. Le profil du client sera mis à jour automatiquement. 2 onglets sont également disponibles "Entrainements" et "Diète" qui comporteront les programmes d'entrainements et de nutritions du client.

**En tant que coach**: 
Une fois connecté, on dispose d'une page avec la liste de tous les pratiquants dont on a la charge. On peut ajouter un pratiquant en le recherchant par son nom, en cliquant sur le bouton "ajouter" un mail de confirmation sera envoyé au client concerné pour valider la prise en charge. Le coach peut uploader un fichier (.csv/.xls) pour les programmes et la diète sur le profil de ses pratiquants pour leur transmettre directement depuis l'application, lors de la mise à jour du programme d'un pratiquant, celui-ci reçoit un mail pour le prévenir. Un fichier "Template" pour conserver un format commun entre coachs sera disponible sur la page d'accueil, si le format mit à disposition n'est pas respecté le fichier ne sera pas pris en compte.


## Spécifications
* Les données d'entrainements sont récupérées avec l'API Accesslink de Polar en Python sous forme d'objet, elles sont vérifiées et stockées directement dans la base de données
* Le système de badge fonctionne à l'aide de cartes RFID et un lecteur NFC (ACS ACR 122u) 
* Les graphiques liés aux stats sont effectués avec la librairie javascript Chart.js
* Les programmes d'entrainements et de nutritions doivent respecter le format proposé (Lors de l'upload une vérification est effectuée)
* Un système de notification est mis en place pour avertir les utilisateurs des différents événements

## Restrictions
- Pour l'instant, il est uniquement possible d'utiliser des appareils Polar pour les données d'entrainement.
- Le système de badge est utilisé au début et à la fin et non pendant l'entrainement.
- L'API accepte au maximum 500 requête pour 20 utilisateurs différents en 15 min et 5000 pour 100 utilisateurs en 24h
- Les montres utilisées lors des entrainements sont celles du coach (montres déjà enregistrer sur le client qui accède à l'API)

## Environnement
Technologies utilisées :

* HTML5
* CSS3 
* Javascript
* SQL 
* Python
* Flask (Micro Framework Python)
* Lecteur NFC (ACS ACR122U)
* [API AccessLink Polar](https://www.polar.com/accesslink-api/#polar-accesslink-api)
* [Chart.js](https://www.chartjs.org/)


Système d'exploitation :

* Développement sur Windows

Versionning / Documentation :

* GitHub
* MarkDown (Mkdocs)

## Livrable
* Fichier zip contenant le projet + bdd
* Documentation technique et journal de bord au format PDF