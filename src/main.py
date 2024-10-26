# from data_processing.graph import 
import pandas as pd
from typing import Tuple

from data_processing.io_agent import load_csv, load_json, export_json
from data_processing.cleaner import lower_df_columns, convert_dates, strip_to_nan_df_columns, drop_na_in_columns
from data_processing.graph import match_drug_mentions, generate_relationship_graph, journal_with_most_different_drugs, find_related_drugs

from config.vars import OUTPUT_PATH, DRUGS_FILE, PUBMED_CSV_FILE, PUBMED_JSON_FILE,CLINICAL_TRIALS_FILE

def extract(clinical_file = CLINICAL_TRIALS_FILE, pubmed_csv = PUBMED_CSV_FILE, 
            pubmed_json = PUBMED_JSON_FILE, drug_file = DRUGS_FILE) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Extrait les données des fichiers spécifiés pour les essais cliniques, les publications PubMed et les médicaments.

    Args:
        - clinical_file (str): Chemin vers le fichier CSV des essais cliniques.
        - pubmed_csv (str): Chemin vers le fichier CSV des publications PubMed.
        - pubmed_json (str): Chemin vers le fichier JSON des publications PubMed
        - drug_file (str): Chemin vers le fichier CSV des médicaments.

    Returns:
        tuple:
               - df_clinical_trials : Données des essais cliniques.
               - df_pubmed : DataFrame combiné contenant les données des publications PubMed (CSV et JSON).
               - df_drugs : Données des médicaments.
    """
    
    df_clinical_trials = load_csv(clinical_file)

    df_pubmed_csv = load_csv(pubmed_csv)
    df_pubmed_json = load_json(pubmed_json)
    df_pubmed = pd.concat([df_pubmed_csv, df_pubmed_json], axis = 0, ignore_index= True) 

    df_drugs = load_csv(drug_file)

    return df_clinical_trials, df_pubmed, df_drugs

def clean(df_clinical_trials : pd.DataFrame, df_pubmed : pd.DataFrame, df_drugs : pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame] :
    """
    Nettoie et transforme les colonnes des DataFrames provenants des fichiers sources

    Args:
        - df_clinical_trials (DataFrame): Essais cliniques.
        - df_pubmed (DataFrame): Publications PubMed
        - df_drugs (DataFrame): Médicaments.

    Returns:
        tuple: DataFrames nettoyés et formatés .
               - df_clinical_trials : Essais cliniques avec les colonnes mises en minuscules et les valeurs NaN traitées.
               - df_pubmed : Publications PubMed nettoyé.
               - df_drugs : Médicaments nettoyé.
    """

    df_clinical_trials = lower_df_columns(df_clinical_trials, ['scientific_title', 'journal' ])
    df_clinical_trials = strip_to_nan_df_columns(df_clinical_trials, ['id', 'scientific_title', 'journal' ])
    df_clinical_trials = drop_na_in_columns(df_clinical_trials, ['id', 'scientific_title', 'journal'])
    df_clinical_trials.loc[:, 'date'] = convert_dates(df_clinical_trials['date'])

    df_pubmed = lower_df_columns(df_pubmed, ['title', 'journal' ])
    df_pubmed = drop_na_in_columns(df_pubmed, ['id'])
    df_pubmed.loc[:, 'date'] = convert_dates(df_pubmed['date'])

    df_drugs = lower_df_columns(df_drugs, ['drug' ])

    return df_clinical_trials, df_pubmed, df_drugs

def transform(df_clinical_trials : pd.DataFrame, df_pubmed : pd.DataFrame, df_drugs : pd.DataFrame) -> Tuple[list, dict] :

    """
    Transforme les données pour générer des relations entre les publications et les médicaments mentionnés.

    Args:
        - df_clinical_trials (DataFrame): DataFrame des essais cliniques nettoyé.
        - df_pubmed (DataFrame): DataFrame des publications PubMed nettoyé.
        - df_drugs (DataFrame): DataFrame des médicaments nettoyé.

    Returns:
        tuple: Liste des mentions de médicaments et graphe des relations entre les médicaments et les publications.
               - drugs_mentions : Liste des mentions de médicaments extraites des essais cliniques et des publications PubMed.
               - graph : Graphe des relations entre les médicaments et les publications.
    """

    pubmed_mentions = match_drug_mentions(df_drugs, df_pubmed, 'title', 'PubMed')

    clinical_trials_mentions = match_drug_mentions(df_drugs, df_clinical_trials, 'scientific_title', 'Clinical Trials')

    drugs_mentions = pubmed_mentions + clinical_trials_mentions
    graph = generate_relationship_graph(drugs_mentions)

    return drugs_mentions, graph


if __name__ == "__main__":
     # Extract
    df_clinical_trials, df_pubmed, df_drugs = extract()

    # Clean
    df_clinical_trials, df_pubmed, df_drugs = clean(df_clinical_trials, df_pubmed, df_drugs)

    # Transform
    drugs_mentions, graph = transform(df_clinical_trials, df_pubmed, df_drugs)

    # Export
    export_json(graph, OUTPUT_PATH+'graph.json')

    ### Bonus ###
    # Extraire le nom du journal qui mentionne le plus de médicaments différents.
    most_diverse_journal, distinct_drugs_count, distinct_drugs = journal_with_most_different_drugs(drugs_mentions)
    print("\n")
    print(f" -> Le journal qui mentionne le plus de médicaments différents est : {most_diverse_journal} \n")
    print(f" -> Nombre de médicaments différents mentionnés : {distinct_drugs_count} \n")
    print(f" -> Noms des médicaments mentionnés : {', '.join(distinct_drugs)} \n")

    # Pour un médicament donné, trouver l’ensemble des médicaments mentionnés par les mêmes journaux référencés 
    # par les publications scientifiques (PubMed) mais non les tests cliniques (ClinicalTrials)
    target_drug = 'tetracycline'
    related_drugs_df = find_related_drugs(drugs_mentions, target_drug)
    print(f" -> Médicaments mentionnés par les mêmes journaux référencés par les publications scientifiques PubMed : {related_drugs_df["Drugs"].str.cat(sep=', ')}")
