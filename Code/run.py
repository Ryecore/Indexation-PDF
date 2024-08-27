import os
from script import load_pdf_files, build_global_index, save_index

# Définir le répertoire de base
base_directory = os.path.dirname(os.path.abspath(__file__))

# Chemin vers le répertoire contenant les fichiers PDF
pdf_directory = os.path.join(base_directory, '..', 'Documents')  # Répertoire des fichiers PDF

# Chemin vers le fichier de sortie index.json
output_index_file = os.path.join(base_directory, 'index.json')

def main():
    """
    Fonction principale pour indexer tous les fichiers PDF dans un répertoire
    et sauvegarder l'index dans un fichier JSON.
    """
    # Charger tous les fichiers PDF du répertoire
    pdf_files = load_pdf_files(pdf_directory)
    
    # Vérifier si des fichiers PDF sont présents
    if not pdf_files:
        print(f"Aucun fichier PDF trouvé dans le répertoire : {pdf_directory}")
        return

    # Construire l'index global à partir des fichiers PDF
    global_index = build_global_index(pdf_files)
    
    # Sauvegarder l'index global dans un fichier JSON
    save_index(global_index, output_index_file)
    
    print(f"Indexation terminée. Le fichier d'index a été sauvegardé sous '{output_index_file}'.")

if __name__ == "__main__":
    main()
