import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import webbrowser  # Pour ouvrir les fichiers dans le navigateur par défaut

# Fonction pour centrer une fenêtre
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Fonction pour charger l'index JSON
def load_index():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    index_file = os.path.join(base_directory, 'index.json')
    with open(index_file, 'r') as file:
        return json.load(file)

# Fonction de recherche
def search():
    search_word = entry_search.get().strip().lower()
    if not search_word:
        messagebox.showwarning("Avertissement", "Veuillez entrer un mot clé.")
        return
    
    index = load_index()
    results = {}
    
    for word, occurrences in index.items():
        if search_word in word:
            for file_path, _ in occurrences:
                file_name = os.path.basename(file_path)
                if file_name not in results:
                    results[file_name] = 0
                results[file_name] += 1
    
    # Fermer la fenêtre de recherche
    search_window.destroy()
    
    # Afficher les résultats
    show_results(results)

# Fonction pour ouvrir le fichier sélectionné
def open_file(event):
    item = tree.selection()[0]
    file_name = tree.item(item, 'values')[1]
    # Définir le répertoire contenant les fichiers
    base_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Documents')
    file_path = os.path.join(base_directory, file_name)
    
    # Debug: afficher le chemin du fichier
    print(f"Chemin du fichier: {file_path}")
    
    if os.path.isfile(file_path):
        webbrowser.open(file_path)  # Ouvre le fichier avec l'application par défaut
    else:
        messagebox.showerror("Erreur", f"Le fichier {file_name} n'existe pas ou le chemin est incorrect.")

# Fonction pour afficher les résultats dans une nouvelle fenêtre
def show_results(results):
    global tree
    results_window = tk.Tk()
    results_window.title("Résultats de la recherche")
    center_window(results_window, 1000, 700)
    
    # Titre
    title_label = tk.Label(results_window, text="Documents classés par pertinence (nombre d'occurrences)", font=('Arial', 14, 'bold'))
    title_label.pack(pady=10)
    
    # Création du tableau
    table_frame = ttk.Frame(results_window)
    table_frame.pack(fill=tk.BOTH, expand=True)
    
    tree = ttk.Treeview(table_frame, columns=('No', 'Fichier', 'Nombre d\'occurrences'), show='headings')
    tree.heading('No', text='No')
    tree.heading('Fichier', text='Fichier')
    tree.heading('Nombre d\'occurrences', text='Nombre d\'occurrences')
    tree.column('No', width=50, anchor=tk.CENTER)
    tree.column('Fichier', width=600, anchor=tk.W)
    tree.column('Nombre d\'occurrences', width=200, anchor=tk.CENTER)
    
    for i, (file_name, count) in enumerate(sorted(results.items(), key=lambda item: item[1], reverse=True), 1):
        tree.insert('', tk.END, values=(i, file_name, count))
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Lier le clic sur une ligne du tableau à la fonction d'ouverture de fichier
    tree.bind('<Double-1>', open_file)
    
    # Bouton de fermeture
    close_button = tk.Button(results_window, text="Fermer", command=results_window.destroy, font=('Arial', 10, 'bold'))
    close_button.pack(pady=10)
    
    results_window.mainloop()

# Fonction pour ouvrir la fenêtre de recherche
def open_search_window():
    global search_window
    search_window = tk.Tk()
    search_window.title("Recherche")
    center_window(search_window, 400, 200)
    
    # Titre
    title_label = tk.Label(search_window, text="Recherche", font=('Arial', 14, 'bold'))
    title_label.pack(pady=10)
    
    # Champ de recherche
    tk.Label(search_window, text="Entrez un mot clé:", font=('Arial', 12)).pack(pady=5)
    global entry_search
    entry_search = tk.Entry(search_window, width=50, font=('Arial', 12))
    entry_search.pack(pady=5)
    
    # Bouton de recherche
    search_button = tk.Button(search_window, text="Rechercher", command=search, font=('Arial', 12, 'bold'))
    search_button.pack(pady=10)
    
    search_window.bind('<Return>', lambda event: search())
    
    # Bouton de fermeture
    close_button = tk.Button(search_window, text="Fermer", command=search_window.destroy, font=('Arial', 10, 'bold'))
    close_button.pack(pady=10)
    
    search_window.mainloop()

# Démarrer directement avec la fenêtre de recherche
open_search_window()
