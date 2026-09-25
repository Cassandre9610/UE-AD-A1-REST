# UE-AD-A1-REST

Pour la première partie ne vous souciez pas des fichiers Docker, cela sera abordé par la suite en séance 4.

https://helene-coullon.fr/pages/ue-ad-fil-25-26/tp-rest/

# 1. Description

Nous allons concevoir une petite application permettant de gérer une salle de cinéma, et les réservations des utilisateurs :

Il s’agit d’une application jouet et peu réaliste. Cette application est composée de 4 micro-services :

**Movie** est le micro-service responsable de la gestion des films du cinéma. Il contient et gère une petite base de données json contenant la liste des films disponibles avec quelques informations sur les films.

**Schedule** est le micro-service responsable des jours de passage des films dans le cinéma. Il contient et gère une petite base de données json contenant la liste des dates avec l’ensemble des films disponibles à cette date.

**Booking** est le micro-service responsable de la réservation des films par les utilisateurs. Il contient et gère une petite base de données json contenant une entrée par utilisateur avec la liste des dates et films réservés. Booking fait appel à Schedule pour connaître et vérifier que les créneaux réservés existent bien puisqu’il ne connait pas lui-même les créneaux des films.

**User** est le micro-service est le micro-service qui servirait typiquement à authentifier les utilisateurs. Il contient et gère une petite base de données json avec la liste des utilisateurs.

# 2. Travail à réaliser

Coder chacun des services pour permettre tout simplement d’accéder, d’ajouter ou de supprimer des éléments de leur petite base de données json (CRUD). Pas d’update nécessaire sur Booking et Schedule.

Certains points d’entrée ont besoin d’intéragir avec d’autres services, par exemple à l’ajout d’une réservation le service Booking doit vérifier auprès de Schedule que la date réservée pour le film est correcte (d’où la flèche de Booking vers Schedule).

Soyez logique ! par exemple, il ne parait pas adapté de pouvoir accéder à toutes les réservations de tous les utilisateurs si on n’est pas admin.

Coder deux ou trois points d’entrée supplémentaires plus intéressants permettant de recouper des informations.

Par exemple un point d’entrée dans Booking permettant de récupérer les réservations et le détail du film réservé (d’où les flèches de booking vers Movie).

Si vous avez besoin, vous pouvez ajouter des flèches entre les services.

Écrire les documentations OpenAPI associées à vos services avec des exemples et avec la description des données en entrée et en sortie.

## Important

Pour coder Booking vous aurez besoin d’appeler d’autres services par le biais de leur API REST. Pour cela, vous utiliserez le paquet requests (déjà présent dans requirements.txt) et utilisez la fonction get (ou post). Voir ici

# Aide

## Windows

```bash
python3 -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
cd .\movie\
pymon movie.py
```

## Linux

```cmd
python3 -m venv venv
source venv/Scripts/activate (ou source venv/bin/activate)
pip install -r requirements.txt
cd .\movie\
pymon movie.py
```
