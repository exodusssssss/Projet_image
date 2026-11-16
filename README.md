Projet Image/son Titouan DEFORGE

# Traitement du signal : application Streamlit

Application web qui permet de charger une image JPG, de lui appliquer des filtres et de comparer le résultat à l'original.

## Paquets nécessaires

Python 3.10, streamlit, numpy, matplotlib, scipy.

Tout est défini dans le fichier `environment.yaml`.

## Installation

conda env create -f environment.yaml
conda activate streamlit

## Lancement

Depuis le dossier du projet :
streamlit run app.py

## Fonctionnement

1. Charger une image JPG.
2. Choisir un ou plusieurs filtres. Ils sont appliqués dans l'ordre de sélection.
3. Régler l'intensité du bruit ou du flou avec les curseurs.
4. Comparer l'image originale (à gauche) et l'image filtrée (à droite).
5. Télécharger l'image filtrée avec le bouton sous l'image.

Filtres disponibles :

- **Noir et blanc** : moyenne des trois canaux (rouge, vert, bleu).
- **Ajout de bruit** : bruit aléatoire gaussien, le curseur règle son intensité.
- **Flou gaussien** : moyenne pondérée des pixels voisins (convolution), le curseur règle la largeur du flou.