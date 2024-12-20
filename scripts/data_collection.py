import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

def retrieve_data_from_kaggle(kaggle_dataset_name, download_path="data/raw", output_filename="raw_tweets.csv"):
    try:
      
        output_filepath = os.path.join(download_path, output_filename)
        
       
        if os.path.exists(output_filepath):
            print(f"Le fichier {output_filename} est déjà présent dans {download_path}")
            return
        
        api = KaggleApi()
        api.authenticate()
        
      
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
       
        api.dataset_download_files(kaggle_dataset_name, path=download_path, unzip=True)
        
      
        downloaded_files = [f for f in os.listdir(download_path) if f.endswith('.csv') and os.path.isfile(os.path.join(download_path, f))]
        if not downloaded_files:
            print("Aucun fichier CSV trouvé après le téléchargement.")
            return
        
        downloaded_file = downloaded_files[0]
        shutil.move(os.path.join(download_path, downloaded_file), output_filepath)
        
        print(f"Dataset {kaggle_dataset_name} téléchargé et renommé en {output_filepath}")
        
    except Exception as e:
        print(f"Une erreur est survenue lors du téléchargement du dataset {kaggle_dataset_name}: {e}")

if __name__ == "__main__":
    retrieve_data_from_kaggle("kazanova/sentiment140")
