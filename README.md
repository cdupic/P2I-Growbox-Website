# Code Website du projet GrowBox

## Description

Ce code est responsable du site internet [mygrowbox.fr](https://mygrowbox.fr/).
Il est développé avec le framework Flask en Python, en utilisant le langage de templating Jinja2.

## Fonctionnalités
- **Inscription/Connexion** : Les utilisateurs peuvent s'inscrire et se connecter à leur compte. Les mots de passe sont hashés et stockés en base de données.
- **Enregistrement d'une serre** : Un utilisateur peut associer une serre à son compte en saisissant son numéro de série et en lui attribuant un nom.
- **Rôles** : Le premier utilisateur d'une serre est propriétaire, les autres sont des invités. Le propriétaire peut gérer les rôles et définir des collaborateurs, ayant le droit de gérer les paramètres de la serre.
- **Paramètres de la serre** : Les utilisateurs peuvent configurer manuellement les valeurs cibles des capteurs de leur serre. Cela peut aussi être fait automatiquement via la définition d'un ensemble de plantes à partir de notre base de donnée de spécificité d'une grande variété de plantes.
- **Notifications** : Un système de notifications est intégré au site internet, et permet aux utilisateurs de recevoir des notifications et alertes lorsque les valeurs réelles sont trop éloignées des valeurs cibles.
- **Visualisations** : L'utilisateur peut choisir de visualiser les données des capteurs sur une plage de temps personnalisable. Certaines indications sont ajoutées sur certains graphiques comme pour l'O2, où des indicateurs montrent les valeurs minimales, maximales, et moyennes le jour et la nuit. Il est aussi possible de choisir de visualiser les données traitées ou non traitées (voir le code DataProc du projet, c'est-à-dire celui de la phase P5).

## Structure du code
- ``static/`` : fichiers servis statiquement par flask, contient le code css et javascript, mais aussi les ressources classiques (images, etc.).
- **Dossier templates** : fichiers j2 utilisés pour le rendu des pages web (code HTML utilisant le moteur de templating Jinja2).
- ``src/`` : code source Python du backend :
  - ``src/main.py`` :  code d'initialisation du site web, c'est lui qui enregistre les url prises en charge par le site internet, et correspondant à des fichiers python dans ``src/pages/`` et ``src/managers``. 
  - ``src/database/`` : contient des fonctions utilitaires permettant de travailler avec la base de donnée sur des tâches spécifiques. Le fichier ``database.py`` établis un pool de connexions SQL pour pouvoir traiter les requêtes de manière asynchrone sans avoir à re-établir de connexion à chaque requête.
  - ```src/managers``` : les managers sont des url qui servent à effectuer des actions, mais qui ne délivrent aucun contenu html. Ce sont des fichiers appelés suite à des soumissions de formulaires, et qui redirigent vers des pages traditionnelles (Voir le design pattern Post/Redirect/Get : [https://en.wikipedia.org/wiki/Post/Redirect/Get](https://en.wikipedia.org/wiki/Post/Redirect/Get)).
  - ``src/pages/`` : chaque fichier correspond à une ou plusieurs pages du site. Ces pages chargent les templates j2, et implémentent uniquement la méthode ``get``.
  - ``/src/utils/`` : fichiers utilitaires pour la gestion d'utilisateurs notamment.

## Points d'améliorations

- **Sécurité** : Si notre site internet est conçu pour résister aux failles XSS et aux injections SQL, nous n'avons pas implémenté de sécurité CSRF (Cross Site Request Forgery).
- **Droit à la rectification et RGPD** : Notre site internet reste un produit minimum viable, et ne permet pas encore à l'utilisateur de modifier ses données personnelles, ni de les supprimer. Il n'est pas non plus conforme au RGPD. Beaucoup d'actions importantes ne sont aussi pas implémentées par manque de temps, notamment les actions de suppression de serre ou de retrait d'invités.

## Auteurs

P2I2 Groupe 221-A Equipe GrowBox Clément Grennerat, Clément Dupic, Nathan Daval, Victoria Nomezine, Hicham Boudjeroua, Sophie Anthoine

## À contacter en cas de questions

Clément Grennerat (clement.grennerat@insa-lyon.fr)
Clément Dupic (clement.dupic@insa-lyon.fr)
