Projet Image/son Titouan DEFORGE

# Traitement du signal : application Streamlit

Application web qui permet de charger une image JPG ou un fichier audio WAV, de lui appliquer des filtres et de comparer le résultat à l'original.

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

L'application contient deux onglets : **Image** et **Audio**.

### Onglet Image

1. Charger une image JPG.
2. Choisir un ou plusieurs filtres. Ils sont appliqués dans l'ordre de sélection.
3. Régler l'intensité du bruit ou du flou avec les curseurs.
4. Comparer l'image originale (à gauche) et l'image filtrée (à droite).
5. Télécharger l'image filtrée avec le bouton sous l'image.

Filtres disponibles :

- **Noir et blanc** : moyenne des trois canaux (rouge, vert, bleu).
- **Ajout de bruit** : bruit aléatoire gaussien, le curseur règle son intensité.
- **Flou gaussien** : moyenne pondérée des pixels voisins (convolution), le curseur règle la largeur du flou.

### Onglet Audio

1. Charger un fichier audio court au format WAV 16 bits. Un fichier stéréo est converti en mono (première piste conservée).
2. Choisir un ou plusieurs filtres. Ils sont appliqués dans l'ordre de sélection.
3. Régler l'intensité du bruit avec le curseur.
4. Écouter l'audio original (à gauche) et l'audio filtré (à droite).
5. Télécharger l'audio filtré avec le bouton sous le lecteur.

Filtres disponibles :

- **Ajout de bruit** : bruit aléatoire gaussien (souffle), le curseur règle son intensité.
- **Filtre son grave** : moyenne glissante sur 21 échantillons (convolution 1D). Les variations rapides sont lissées, il reste les graves.
- **Filtre son aigu** : convolution 1D avec le noyau [-1, 2, -1]. Les variations lentes s'annulent, il reste les aigus.
- **Filtre passe-bande** : on applique le filtre son grave puis le filtre son aigu. Seules les fréquences intermédiaires sont conservées.