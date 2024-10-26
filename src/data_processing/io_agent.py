import pandas as pd
import ast
import json

def load_csv(file_path : str) -> pd.DataFrame:
    """
    Doc : Charge un fichier CSV et retourne un DataFrame.

    Args:
        - file_path (str): Le chemin vers le fichier CSV à charger.

    Returns:
        pd.DataFrame: Un DataFrame contenant les données du fichier CSV.
    """
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Erreur : le fichier {file_path} n'a pas été trouvé.")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur
    return data

def load_json(file_path: str) -> pd.DataFrame:
    """
    Charge un fichier JSON et retourne un DataFrame.

    Args:
        file_path (str): Le chemin vers le fichier JSON à charger.

    Returns:
        pd.DataFrame: Un DataFrame contenant les données du fichier JSON.
    """
    try:
        data = pd.read_json(file_path)
        return data
    except FileNotFoundError:
        print(f"Erreur : le fichier {file_path} n'a pas été trouvé.")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur
    except ValueError:
        # Gestion des cas où il y a une virgule surnuméraire
        with open(file_path, 'r') as f:
            data = f.read().rstrip(", \n")  # Enlève la virgule surnuméraire
            # Si le contenu n'est pas une liste, on le met dans une liste
            json_data = ast.literal_eval(data)
            if isinstance(json_data, dict):  # Si c'est un dictionnaire
                json_data = [json_data]  # Convertir en liste de dictionnaires
            return pd.DataFrame(json_data)  # Retourne le DataFrame
    return pd.DataFrame()  # Assurez-vous de retourner un DataFrame même si toutes les exceptions échouent

  

    return data

def export_json(dict_res : dict, output_file : str) -> None:
    """
    Exporte un dictionnaire dans un fichier JSON

    Args:
        - dict_res (dict): Dictionnaire contenant les données à exporter.
        - output_file (str): Chemin et nom du fichier de sortie pour le fichier JSON.

    Returns:
        None
    """
    with open(output_file, mode='w') as file:
        json.dump(dict_res, file, indent=4)
        print(f"Le fichier {output_file} a été chargé ! ")

