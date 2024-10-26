import pandas as pd
from collections import defaultdict

def match_drug_mentions(drugs_df : pd.DataFrame, publications_df : pd.DataFrame, title_column : str, source : str) -> list[dict]:
    """
    Associe les mentions de médicaments dans les titres des publications.

    Args:
        - drugs_df (pd.DataFrame): DataFrame contenant les médicaments
        - publications_df (pd.DataFrame): DataFrame contenant les publications avec au moins une colonne pour le titre, 
                                          le journal et la date.
        - title_column (str): Colonne contenant les titres.
        - source (str) : provenance des données (ie pubmed)

    Returns:
        list: Une liste de dictionnaires, chaque dictionnaire représentant une mention de médicament
              dans une publication, avec les clés 'drug', 'titre', 'journal', et 'date'.
    """
    mentions = []
    for drug in drugs_df['drug']:
        for _, publication in publications_df.iterrows():
            if drug.lower() in publication[title_column].lower():  # Vérifie la mention de chaque médicament, insensible à la casse
                mentions.append({
                    'drug': drug,
                    'titre': publication[title_column],
                    'journal': publication['journal'],
                    'date': publication['date'], 
                    'source': source

                })
    return mentions

def generate_relationship_graph(mentions : list[dict]) -> dict:
    """
    Génère un graphe des relations entre médicaments et publications.

    Args:
        - mentions (list): Une liste de dictionnaires représentant des mentions de médicaments
                           (cf fonction match_drug_mentions)

    Returns:
        dict: Un dictionnaire où chaque clé est un médicament et chaque valeur est une liste
              de dictionnaires contenant 'journal', 'titre', et 'date' pour chaque mention
              associée à ce médicament.
    """
    graph = defaultdict(list)  # Utilisation de defaultdict pour simplifier la création du graphe
    for mention in mentions:
        drug = mention['drug']
        graph[drug].append({
            'journal': mention['journal'],
            'titre': mention['titre'], 
            'date': mention['date'], 
            'source': mention['source']
        })
    return graph

def journal_with_most_different_drugs(mentions: list[dict]) -> tuple[str, int, list[str]]:
    """
    Trouve le nom du journal qui mentionne le plus de médicaments différents,
    le nombre de ces médicaments distincts et leurs noms.

    Args:
        - mentions (list): Une liste de dictionnaires représentant des mentions de médicaments.

    Returns:
        tuple: Un tuple contenant le nom du journal, le nombre de médicaments différents,
               et une liste des noms des médicaments.
    """
    journal_drug_count = defaultdict(set)  # Utilisation d'un set pour éviter les doublons

    # Compte le nombre de médicaments différents mentionnés par journal
    for mention in mentions:
        journal = mention['journal']
        drug = mention['drug']
        journal_drug_count[journal].add(drug)  # Ajoute le médicament au set

    # Trouve le journal avec le maximum de médicaments différents
    most_diverse_journal = max(journal_drug_count, key=lambda k: len(journal_drug_count[k]))
    
    # Nombre de médicaments différents pour le journal le plus diversifié
    distinct_drugs_count = len(journal_drug_count[most_diverse_journal])
    
    # Liste des noms des médicaments distincts
    distinct_drugs = list(journal_drug_count[most_diverse_journal])

    return most_diverse_journal, distinct_drugs_count, distinct_drugs


def find_related_drugs(mentions: list[dict], target_drug: str) -> pd.DataFrame:
    """
    Trouve l'ensemble des médicaments mentionnés par les mêmes journaux
    référencés par les publications scientifiques (PubMed), mais non dans les essais cliniques (Clinical Trials).

    Args:
        - mentions (list): Une liste de dictionnaires représentant des mentions de médicaments.
        - target_drug (str): Le médicament cible pour lequel nous cherchons les médicaments associés.

    Returns:
        pd.DataFrame: Un DataFrame contenant les noms des médicaments associés.
    """
    # Ensemble pour stocker les journaux associés au médicament cible dans PubMed
    pubmed_journals = set()
    
    # Récupérer les journaux qui mentionnent le médicament cible dans PubMed
    for mention in mentions:
        if mention['drug'] == target_drug and mention['source'] == 'PubMed':
            pubmed_journals.add(mention['journal'])

    # Ensemble pour stocker tous les médicaments mentionnés dans ces journaux
    related_drugs = set()

    # Trouver tous les médicaments mentionnés dans les mêmes journaux, mais sans Clinical Trials
    for mention in mentions:
        if mention['journal'] in pubmed_journals and mention['source'] == 'PubMed':
            related_drugs.add(mention['drug'])
        elif mention['journal'] in pubmed_journals and mention['source'] == 'Clinical Trials':
            continue

    # Convertir l'ensemble en DataFrame
    related_drugs_df = pd.DataFrame(list(related_drugs), columns=['Drugs'])

    return related_drugs_df


