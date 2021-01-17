Projet de Python réalisé par Thomas Brunet en 2020/2021 dans le cadre de l'unité Python d'E3 à l'ESIEE

les données utilisés ne m'appartiennent pas : 
 - données sur les professions de la médecine : https://drees.shinyapps.io/demographie-ps/
 - donneés sur la population Française par départements : https://www.insee.fr/en/accueil
 
j'ai également utilisé ces ressources extérieurs :
 - geojson pour la carte de France : "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"

# User Guide
prérequis, installation des packages (commandes à faire en console): 
  panda : pip install panda
  plotly : pip install plotly
  plotly express : pip install plotly_express
  requests : pip install requests
  dash : pip install dash

Installation du projet :
  1) Télécharger le projet et le placer dans un répertoire.
  2) Aller dans la console  de commande et placer vous dans ce répertoire
  3) Faire la commande "python main.py"
  4) Taper l'adresse "http://127.0.0.1:8050/" dans la barre de recher de votre navigateur
  5) Ne pas fermez la console de commande pendant la visualisation du site
  
Le processus de création des données et du site peut prendre une trentainne de seconde...
Si la page ne s'affiche pas directement, attendre pendant quelques secondes et raffraichir la page 

/!\ Attention, ne pas changer le nom des dossiers et documents dans le projet 

Vous pouvez naviguer sur le site en utilisant les boutons en bas de page
Vous pouvez choisir une année avec le slider en bas de page (diagramme+diagramme circulaire)
et choisir une profession avec la liste déroulable (diagramme circulaire)

# Developper Guide

Structure du projet :

le projet contient un seul fichier py segmenté grâce à des commentaires et organisé en famille de fonctions :

1) Les imports et créations des variables contenant les chemins des fichiers
2) Ouverture des fichiers csv et créations de constantes pour les données telle que les années disponibles
3) Fonction de création des dictionnaires de données
4) Fonction de création des datasets pour toutes les années disponibles
5) Création des layout pour l'app dash et démarrage de l'app

Pour rajouter des données il faut donc rajouter un jeu de donnée sous format csv dans le dossier donnéesDocteur, 
une fonction pour faire un dictionnaire, un dataset, puis rajouter un layout pour ajouter une page au site, ou modifier
un layout existant.

# Rapport d'analyse

J'ai décidé de faire ce projet sur les professions de la médecine car je suis actuellement en alternance dans la 
société Julie Solutions qui développe un logiciel de gestion de cabinet pour les dentistes. Le milieu de la médecine 
m'as tourjours intéressé, je souhaitait donc en vavoir un peu plus ce secteur.
Ce projet étudie 3 points sur la profession : l'age moyen, la parité et la répartition sur le territoire français des
professionnels de la santé.

 - Le diagramme : 
 Le diagramme présente la répartition de l'age des médecins, infirmiers et dentistes de France.
 En 2012 on remarque déja que la proportion de médecins et de dentistes ayant plus de 50 ans est très grande :
 55% pour les médecins et 53% pour les dentistes, tandis que c'est équilibré pour les infirmiers.
 En avancant vers 2020 on observe une augmentation de jeunes arrivant dans les 3 professions, mais également
 une augmentation général des personnes travaillant après 65 ans :
 
 
 - Le diagramme circulaire :
 
 
 
 - La carte :
