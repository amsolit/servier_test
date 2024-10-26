import pandas as pd
import numpy as np

def lower_df_columns(df : pd.DataFrame, column_names : list[str]) -> pd.DataFrame :
    """
    Raisonnement : comparer des chaines de caractères en minusucule réduit le risque d'erreur
    Doc : Convertir les colonnes spécifiés en minuscules.

    Args
        - df (pandas.DataFrame) : Le DataFrame à traiter
        - column_names (list) : Liste des ncolonnes à convertir en minuscules.

    Returns :
        pd.DataFrame : Un DataFrame avec les colonnes spécifiées en minuscules.
    """
    for col in column_names:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' n'existe pas dans le DataFrame.")

    for col in column_names:
        df[col] = df[col].astype(str).str.lower()
    
    return df

def convert_dates(date_series : pd.Series) -> pd.Series :
    """
    Raisonnement : les dates n'ont pas le même format dans les différents fichiers
    Doc : Standardisation des dates qui ne sont pas au format YYYY-MM-DD.

    Parameters : 
        - date_series (pd.Series) : Colonne du dataframe à à standardiser.

    Returns
        pd.Series : La série de dates au format YYYY-MM-DD.
    """
    try:
        return pd.to_datetime(date_series, errors='coerce').dt.strftime('%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Erreur de conversion des dates: {e}")

def strip_to_nan_df_columns(df : pd.DataFrame , column_names : list[str]) -> pd.DataFrame :
    """
    Raisonnement : certains champs sont seulement composés d'espace. 
    Doc : Remplacement des espaces surnuméraires par "" et par np.nan si la chaine de caractères est vide.

    Parameters
        - df (pd.DataFrame) : Le DataFrame à traiter.
        - column_names (list) : Liste des noms de colonnes à traiter.

    Returns
        pd.DataFrame : Le DataFrame avec les colonnes spécifiées mises à jour.
    """
    for col in column_names:
        if col not in df.columns:
            raise ValueError(f"Colonne '{col}' n'existe pas dans le DataFrame.")

    for col in column_names:
        df[col] = df[col].astype(str).str.strip().replace('', np.nan)
    
    return df

def drop_na_in_columns(df : pd.DataFrame , column_names : list[str]) -> pd.DataFrame:
    """
    Raisonnement : on considère que les lignes contenant une valeur nulles doivent être supprimées
    Doc : Supprimer les lignes avec des valeurs nulles dans les colonnes spécifiées.

    Parameters
        - df (pd.DataFrame) : Le DataFrame à traiter.
        - column_names (list) : Liste des colonnes

    Returns
        pd.DataFrame : Le DataFrame sans les lignes contenant des valeurs nulles dans les colonnes spécifiées.
    """
    df.replace(["", " ", "nan", "NaN"], np.nan, inplace=True)
    return df.dropna(subset=column_names)
