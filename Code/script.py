from pypdf import PdfReader
import os
import re
from collections import defaultdict
import json

def load_pdf_files(directory):
    """
    Charge tous les fichiers PDF dans le répertoire donné.
    
    :param directory: Chemin du répertoire contenant les fichiers PDF
    :return: Liste des chemins complets des fichiers PDF
    """
    # Récupération de tous les fichiers PDF dans le dossier spécifié
    pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]
    return pdf_files


def extract_text_from_pdf(pdf_file):
    """
    Extrait le texte d'un fichier PDF.
    
    :param pdf_file: Chemin du fichier PDF
    :return: Texte extrait du fichier PDF
    """
    # Création du lecteur PDF
    reader = PdfReader(pdf_file)
    text = ""
    
    # Boucle à travers toutes les pages et extraction du texte
    for page in reader.pages:
        text += page.extract_text()
    
    return text


def preprocess_text(text):
    """
    Pré-traite le texte extrait en le mettant en minuscules et en supprimant la ponctuation.
    
    :param text: Texte brut extrait du fichier PDF
    :return: Texte nettoyé (minuscule, sans ponctuation)
    """
    # Conversion du texte en minuscules
    text = text.lower()
    # Suppression de la ponctuation et des caractères spéciaux
    text = re.sub(r'\W+', ' ', text)
    
    return text


def create_index(text, pdf_filename):
    """
    Crée un index des mots et de leurs positions dans le texte extrait d'un fichier PDF.
    
    :param text: Texte pré-traité
    :param pdf_filename: Nom du fichier PDF associé
    :return: Index des mots avec leurs positions dans le texte
    """
    # Dictionnaire pour stocker les mots et leurs positions
    index = defaultdict(list)
    words = text.split()
    
    # Boucle pour indexer chaque mot avec sa position
    for position, word in enumerate(words):
        index[word].append((pdf_filename, position))
    
    return index


def build_global_index(pdf_files):
    """
    Crée un index global pour tous les fichiers PDF d'un répertoire.
    
    :param pdf_files: Liste des fichiers PDF
    :return: Index global des mots avec leurs occurrences dans chaque fichier PDF
    """
    # Dictionnaire pour stocker l'index global
    global_index = defaultdict(list)
    
    # Boucle sur chaque fichier PDF
    for pdf_file in pdf_files:
        # Extraction du texte
        text = extract_text_from_pdf(pdf_file)
        # Prétraitement du texte
        preprocessed_text = preprocess_text(text)
        # Création d'un index pour chaque fichier
        file_index = create_index(preprocessed_text, pdf_file)
        
        # Ajout des index locaux à l'index global
        for word, locations in file_index.items():
            global_index[word].extend(locations)
    
    return global_index


def search_index(global_index, search_word):
    """
    Recherche un mot dans l'index global.
    
    :param global_index: Index global des mots
    :param search_word: Mot à rechercher
    :return: Liste des emplacements du mot dans les fichiers PDF
    """
    # Mettre le mot de recherche en minuscules pour correspondre au format de l'index
    search_word = search_word.lower()
    
    # Retourne les emplacements du mot recherché ou une liste vide si non trouvé
    return global_index.get(search_word, [])


def save_index(global_index, output_file):
    """
    Sauvegarde l'index global dans un fichier JSON.
    
    :param global_index: Index global des mots
    :param output_file: Chemin du fichier de sortie pour l'index JSON
    """
    # Sauvegarde de l'index dans un fichier JSON
    with open(output_file, 'w') as f:
        json.dump(global_index, f)


def index_pdf_directory(directory, output_index_file):
    """
    Fonction principale pour indexer tous les fichiers PDF d'un répertoire et sauvegarder l'index dans un fichier JSON.
    
    :param directory: Chemin du répertoire contenant les fichiers PDF
    :param output_index_file: Chemin du fichier de sortie pour l'index
    """
    # Charger tous les fichiers PDF
    pdf_files = load_pdf_files(directory)
    # Construire l'index global
    global_index = build_global_index(pdf_files)
    # Sauvegarder l'index global dans un fichier JSON
    save_index(global_index, output_index_file)
