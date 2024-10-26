import unittest
import pandas as pd
import json
import os
from io import StringIO
from unittest import mock
from src.data_processing.io_agent import load_json, load_csv, export_json

class TestFunctions(unittest.TestCase):

    def test_load_csv(self):
        # Crée un faux fichier CSV en mémoire pour le test
        csv_data = StringIO("col1,col2\n1,2\n3,4")
        expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
        
        # Simule la lecture du CSV
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=csv_data.getvalue())):
            result = load_csv("fake_path.csv")
        
        pd.testing.assert_frame_equal(result, expected_df)

    def test_load_json(self):
        # Crée un fichier JSON pour le test
        json_data = {
            "key1": "value1",
            "key2": "value2"
        }
        file_path = "./tests/data/test_io_agent.json"  # Chemin vers le fichier JSON

        with open(file_path, 'w') as f:
            json.dump(json_data, f, indent=4)

        # Charge le JSON à partir du fichier créé
        expected_df = pd.DataFrame([{"key1": "value1", "key2": "value2"}])
        result = load_json(file_path)

        # Vérifie que le DataFrame retourné est égal à ce que nous attendions
        pd.testing.assert_frame_equal(result, expected_df)


    def test_export_json(self):
        # Définit les données de test et le fichier de sortie
        data = {"key1": "value1", "key2": "value2"}
        output_file = "test_output.json"

        # Exécute la fonction d'exportation
        export_json(data, output_file)
        
        # Vérifie que le fichier est correctement créé
        self.assertTrue(os.path.exists(output_file))

        # Charge le contenu du fichier pour vérifier les données
        with open(output_file, 'r') as file:
            result_data = json.load(file)
        
        self.assertEqual(data, result_data)

        # Nettoie le fichier de test
        os.remove(output_file)

if __name__ == "__main__":
    unittest.main()
