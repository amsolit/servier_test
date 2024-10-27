Bonjour, 

Ce document accompagne le code qui a été réalisé dans le cadre du test technique Servier. Vous y trouverez des informations concernant le code ainsi que des réponses aux questions mentionnés dans l'énoncé. 

# Documentation 

Pour lancer ce code :
- se positionner à la racine du dossier
- exécuter `docker build -f ./DockerFile -t test_servier .`
- exécuter `docker run test_servier`

# Réponses

**Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses
volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?**

Les éléments à prendre en compte sont:
- l'architecture : Assurer la scalabilité avec des infrastructures adaptées (clusters, bases de données distribuées).
- la performance : Optimiser les traitements et utiliser des technologies comme Spark ou Dask pour le calcul distribué.
- la technologie de traitement de données : Choisir des outils scalables pour la manipulation (BigQuery, Redshift).
- le coût : Contrôler l’utilisation des ressources et opter pour des solutions cloud pay-as-you-go pour une gestion efficace des dépenses.

**Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de
telles volumétries ?**

Les actions à considérer en cas de forte volumétrie sont les suivantes:
- utiliser une base de données scalable tels que Big Query, Redshift, Snowflake afin de réduire les coûts en optimisant le stockage et les calculs
- optimiser les traitement en utilisant des clés de partitionnement et de clustering : dans le cas où les traitements sont exportés sur un outil comme Big Query, il sera important d'avoir des données classées. Celà augmentera la vitesse de traitement.
- changer la technologie de manipulation de données. Nous pouvons penser à utiliser une technologie plus adaptée tel que spark si un cluster est à notre disposition ou bien à paralélliser les traitements par batch (Dask, multiprocessing)
- modifier l'infrastructure en utilisant un orchestrateur tels que Airflow, Dagster sur un cluster Kubernetes ou Argo. Le déploiement sur cluster Kubernetes permettra de paralléliser les traitements à l'aide du déploiement des pods qui permettent une bonne scalabilité et une tolérance aux pannes.
- mettre en place un système de login afin de pouvoir suivre l'intégration parallèle et massive des données et de réprendre au bon endroit après une erreur.
- mettre en place un système de monitoring: les alertes et rapports automatiques permettent une réaction rapide face aux dégradations de performances.
