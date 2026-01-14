# Budgo – Project Context

## Objectif
Créer un site web + une API pour la gestion financière personnelle,
avec une future application mobile connectée à la même API.

## Stack technique
- Web : PHP (pages), HTML, CSS, JavaScript
- API : FastAPI (Python)
- Base de données : MySQL
- Environnement local : Windows + Git Bash
- DB locale : Docker (MySQL 8)
- Versioning : Git
- Dépôt distant : GitHub (à créer)

## Structure actuelle
- services/api : API FastAPI
- site/pages : pages PHP
- site/public : assets (css, js, img)
- docs : documentation projet

## Règles importantes
- L’API est indépendante du web
- Toutes les routes API seront versionnées (/v1)
- Le site PHP consomme l’API via HTTP (fetch / curl)
- Pas de secrets en dur dans le repo

## Environnements
- Local : localhost
- API locale : http://127.0.0.1:8000
- Web local : http://127.0.0.1:8080

## État actuel
- API FastAPI minimale créée
- MySQL Docker en cours
- Site PHP en local

