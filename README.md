Bonjour, 

Ce document accompagne le code qui a été réalisé dans le cadre du test technique Servier. Vous y trouverez des informations concernant le code ainsi que des réponses aux questions mentionnées dans l'énoncé. 

# Documentation 

## Pour lancer ce code :
- cloner ce répertoire
- se positionner à la racine du dossier
- exécuter `docker build -f ./DockerFile -t test_servier .`
- exécuter `docker run test_servier`
- le graph sera exporté dans le fichier ./out/. Le résultat est dilibérement laisser dans le repo afin de pouvoir le consulter.

## Dans le cas où vous ne souhaitez pas utiliser Docker :
- cloner le répertoire
- se positionner à la racine
- installer python 3.13
- exécuter `pip install -r requirements`
- exécuter ` python3 ./src/main.py`

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

Les actions à considérer en cas de forte volumétrie sont les suivantes :

- Utiliser une base de données scalable telles que BigQuery, Redshift, Snowflake afin de réduire les coûts en optimisant le stockage et les calculs.
- Optimiser les traitements en utilisant des clés de partitionnement et de clustering : dans le cas où les traitements sont exportés sur un outil comme BigQuery, il sera important d'avoir des données classées. Cela augmentera la vitesse de traitement.
- Changer la technologie de manipulation de données. Nous pouvons penser à utiliser une technologie plus adaptée telle que Spark si un cluster est à notre disposition, ou bien à paralléliser les traitements par batch (Dask, multiprocessing).
- Modifier l'infrastructure en utilisant un orchestrateur tel qu'Airflow, Dagster sur un cluster Kubernetes ou Argo. Le déploiement sur un cluster Kubernetes permettra de paralléliser les traitements à l'aide du déploiement des pods, qui permettent une bonne scalabilité et une tolérance aux pannes.
- Mettre en place un système de login afin de pouvoir suivre l'intégration parallèle et massive des données et de reprendre au bon endroit après une erreur.
- Mettre en place un système de monitoring : les alertes et rapports automatiques permettent une réaction rapide face aux dégradations de performances.


# SQL

## Chiffre d’affaires journalier (du 1er janvier 2019 au 31 décembre 2019)

```sql
SELECT 
    date AS date, 
    SUM(prod_price * prod_qty) AS ventes 
FROM 
    TRANSACTION 
WHERE 
    date BETWEEN '2019-01-01' AND '2019-12-31' 
GROUP BY 
    date 
ORDER BY 
    date ;
```

## Ventes par client et par type de produit (MEUBLE et DECO) sur l’année 2019

```sql
SELECT 
    T.client_id AS client_id,
    SUM(CASE WHEN P.product_type = 'MEUBLE' THEN T.prod_price * T.prod_qty ELSE 0 END) AS ventes_meuble,
    SUM(CASE WHEN P.product_type = 'DECO' THEN T.prod_price * T.prod_qty ELSE 0 END) AS ventes_deco
FROM 
    TRANSACTION T
JOIN 
    PRODUCT_NOMENCLATURE P ON T.prop_id = P.product_id
WHERE 
    T.date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY 
    T.client_id;
```
