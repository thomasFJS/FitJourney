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
Il existe très peu d'outil qui permet à un coach sportif de gérer sa salle de sport avec le suivi de tous ses clients. 


## Cahier des charges

## Analyse de l'existant

## Analyse fonctionnelle

## Analyse Organique

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
La page d'accueil est très basique et propose les boutons permettant de s'enregistrer ou de se connecter.
##### Page de connexion 
![Login Page](./mockups/Interface_mockups/sign_in.jpg)
La page de connexion permet aux utilisateurs de se connecter. Un lien est disponible si le mot de passe a été oublié.

##### Page d'enregistrement
![Register Page](./mockups/Interface_mockups/sign_up.jpg)
La page d'enregistrement permet aux utilisateurs de s'enregistrer 

#### En tant que client 
Si on se connecte à l'application en tant que client, 4 pages supplémentaires sont disponibles.

##### Page profile
![Profile Page](./mockups/Interface_mockups/profile.jpg)

La page profile permet au client de modifier ses informations personnelles. Il a également accès à des statistiques sur les données des entrainements qu'il a effectué cette semaine.

##### Page liste de nos entrainements

##### Page détails entrainement

##### Page prochaine session

#### En tant que coach
Si on se connecte à l'application en tant que coach, on a alors accès à 3 pages supplémentaire.

##### Page profile client

##### Page tableau de bord

##### Page Calendrier
