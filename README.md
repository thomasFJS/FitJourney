# FitJourney
Cette application fait en Python, est une application utilitaire pour aider la pratique du métier de coach sportif. Elle permet a un coach de gérer sa salle de sport ainsi que le suivi des clients. FitJourney utilise l'API Polar Accesslink pour accéder aux données d'entrainement enregistré avec les montres connectés.

## Guide d'installation 
FitJourney utilise la 3ème version de Python (donc `python3`)

### Windows
Premièrement, cela serait intéressant de travailler sur un envirronement WSL avec VSCode. Pour mettre en place WSL, j'ai suivi le guide disponible directement dans la documentation de VSCode : [https://code.visualstudio.com/docs/remote/wsl](https://code.visualstudio.com/docs/remote/wsl)

### MySQL
Une fois l'envirronement de développement installé correctement, il faut installer MySQL (si cela n'est pas déjà fait) à l'aide de la commande :

```sudo apt install mysql-server```

Puis lancer le service MySQL:

```sudo service mysql start```

et 

```sudo mysql_secure_installation```

Pour se connecter à la base de données, utiliser un DBMS comme *DBeaver* ou *MySQLWorkbench*.

### `pip3`
Il faut s'assurer que pip3 a bien été installé afin de télécharger tous les paquets/librairies pour faire fonctionner l'application comme il faut.

```sudo apt install python3-pip```

Si une erreur survient, utiliser la commande :

```sudo apt update && sudo apt upgrade```

Sinon, vous pouvez vérifier que pip3 a bien été installé en utilisant : 

```pip3 --version```

### Pyscard 
Pour pouvoir installer la librairie `pyscard` sur Windows, il faut au préalable installer [SWIG](#swig) depuis le lien suivant : [https://www.swig.org/download.html](https://www.swig.org/download.html)

Il faut ensuite l'ajouter directement au PATH en modifiant les variables d'envirronement dans les propriétés système.

![variables env](./docs/img/param_system.PNG)

On peut ensuite ajouter simplement le chemin vers le dossier `swig` que l'on a téléchargé :

![add swig](./docs/img/swig_path.PNG)

Une fois ajouté, il faut ensuite installer Visual C++ version 14.0 ou plus récente (directement installable depuis le Visual Studio Installer) ([https://visualstudio.microsoft.com/fr/downloads/](https://visualstudio.microsoft.com/fr/downloads/))

### Requirements
Une fois que `swig` a été ajouté au PATH et que `pip3` a été installé, il faut installer tous les paquets nécessaires pour l'application. Un fichier `requirements.txt` contenant toutes les librairies nécessaire est disponible dans le dossier *src/*

```pip3 install -r requirements.txt```

/!\ Ne pas toucher ce fichier.

### API 
L'API utilisée est l'API Accesslink v3.144.0 de Polar [https://www.polar.com/accesslink-api/#polar-accesslink-api](https://www.polar.com/accesslink-api/#polar-accesslink-api).

Pour pouvoir utiliser l'API, il faut disposer au préalable d'un compte Polar Flow [https://flow.polar.com/](https://flow.polar.com/).

#### Création d'un nouveau client pour l'API
Aller sur [https://admin.polaraccesslink.com/](https://admin.polaraccesslink.com/). Il faut se connecter avec votre compte Polar Flow et ajouter un nouveau client. Il faut utiliser `http://localhost:5000/oauth2_callback` pour la callback d'authorisation.

#### Configuration des identifiants
Ajouter l'`id` et le `secret` client dans le fichier `src/cardsChecker/config.yml` comme ceci : 

```
client_id: 57a715f8-b7e8-11e7-abc4-cec278b6b50a
client_secret: 62c54f4a-b7e8-11e7-abc4-cec278b6b50a
```
 
#### Authentification
Le compte utilisateur doit être relié au client créé avant de pouvoir accéder aux données. Pour le relier il faut lancer le script `src/cardsChecker/authorization.py`

```
python3 authorization.py
```

puis aller sur la page '[https://flow.polar.com/oauth2/authorization?response_type=code&client_id=CLIENT_ID](https://flow.polar.com/oauth2/authorization?response_type=code&client_id=CLIENT_ID)' pour relier votre compte utilisateur. ('*CLIENT_ID*' doit être remplacé par votre id client)

Une fois ces étapes effectuées, votre compte aura accès aux données Polar.

### Base de données
Pour la base de données, il suffit de créer un base nommée `fitjourney`, (respcter le nom sinon l'application ne fonctionnera pas). Vous pouvez ensuite exécuter le script sql disponible à `src/apps/db.sql`.

