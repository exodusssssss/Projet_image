import streamlit as st
import numpy as np
import matplotlib.image as mpimg
from scipy.ndimage import gaussian_filter
from scipy.io import wavfile


def convoluer_1d(signal, noyau):
    # On décale le signal et on le multiplie par chaque coefficient du noyau. On perd les valeurs aux extrémités.
    n = len(signal)
    k = len(noyau)
    sortie = np.zeros(n - k + 1)
    for i in range(k):
        sortie += signal[i : n - k + 1 + i] * noyau[i]
    return sortie


st.set_page_config(page_title="Traitement du Signal", layout="wide")
st.title("Application de Traitement du Signal")

# Deux onglets : un pour les images, un pour l'audio
onglet_image, onglet_audio = st.tabs(["Image", "Audio"])

with onglet_image:
    # On n'accepte que le JPG : les valeurs sont alors toujours des entiers entre 0 et 255
    fichier_image = st.file_uploader("Chargez une image JPG", type=['jpg', 'jpeg'])

    if fichier_image is not None:
        liste_filtres = ["Noir et Blanc", "Ajout de bruit", "Flou gaussien"]
        # Sélection multiple : les filtres sont appliqués dans l'ordre où on les coche
        filtres_choisis = st.multiselect("Choisissez les filtres à appliquer (l'ordre compte !) :", liste_filtres)

        intensite = 50
        if "Ajout de bruit" in filtres_choisis:
            intensite = st.slider("Intensité du bruit", min_value=0, max_value=150, value=50)

        sigma = 2
        if "Flou gaussien" in filtres_choisis:
            sigma = st.slider("Intensité du flou", min_value=1, max_value=20, value=2)

        st.write("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Image Originale")
            st.image(fichier_image, use_container_width=True)

        with col2:
            st.subheader("Image Filtrée")

            # Lecture en matricielle de l'image
            image_courante = mpimg.imread(fichier_image).astype(float)

            # Chaque filtre travaille sur le résultat du précédent
            for filtre in filtres_choisis:
                if filtre == "Noir et Blanc":
                    gris = image_courante.mean(axis=2)
                    image_courante = np.stack([gris, gris, gris], axis=-1)

                elif filtre == "Ajout de bruit":
                    bruit = np.random.normal(loc=0, scale=intensite, size=image_courante.shape)
                    image_courante = image_courante + bruit

                elif filtre == "Flou gaussien":
                    image_courante = gaussian_filter(image_courante, sigma=(sigma, sigma, 0))

            # On plafonne entre 0 et 255 puis on convertit en entiers
            image_finale = np.clip(image_courante, 0, 255).astype(np.uint8)
            st.image(image_finale, use_container_width=True)

            # Téléchargement de l'image filtrée
            mpimg.imsave("image_filtree.png", image_finale)
            with open("image_filtree.png", "rb") as fichier:
                st.download_button(
                    label="📥 Télécharger l'image filtrée",
                    data=fichier,
                    file_name="image_filtree.png",
                    mime="image/png",
                )
    else:
        st.info("Veuillez charger une image pour commencer le traitement.")

with onglet_audio:
    fichier_audio = st.file_uploader("Chargez un fichier audio court (.wav)", type=['wav'])

    if fichier_audio is not None:
        liste_filtres_audio = ["Aucun", "Ajout de bruit",
                               "Filtre son grave", "Filtre son aigu"]
        filtre_audio = st.selectbox("Choisissez un filtre audio :", liste_filtres_audio)

        intensite_audio = 2000
        if filtre_audio == "Ajout de bruit":
            intensite_audio = st.slider("Intensité du souffle (bruit)", min_value=0, max_value=10000, value=2000)

        st.write("---")

        frequence, signal = wavfile.read(fichier_audio)

        # Si le fichier est stéréo (2 colonnes), on garde une seule piste
        if signal.ndim > 1:
            signal = signal[:, 0]

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Audio Original")
            st.audio(fichier_audio, format="audio/wav")
            st.write(f"Fréquence : {frequence} Hz | Nombre d'échantillons : {len(signal)}")

        with col4:
            st.subheader("Audio Filtré")

            signal_courant = signal.astype(float)

            if filtre_audio == "Ajout de bruit":
                bruit_audio = np.random.normal(loc=0, scale=intensite_audio, size=signal_courant.shape)
                signal_courant = signal_courant + bruit_audio

            elif filtre_audio == "Filtre son grave":
                # Moyenne glissante sur 21 échantillons. Les variations aigus sont lissées, il reste les graves.
                noyau = [1/21] * 21
                signal_courant = convoluer_1d(signal_courant, noyau)

            elif filtre_audio == "Filtre son aigu":
                # Noyau [-1, 2, -1] : la somme des poids vaut 0, donc les parties graves s'annulent et seules les variations aigus restent.
                noyau = np.array([-1, 2, -1])
                signal_courant = convoluer_1d(signal_courant, noyau)

            # On plafonne aux limites du 16 bits puis on reconvertit en entiers
            signal_final = np.clip(signal_courant, -32768, 32767).astype(np.int16)

            # Pour l'écoute, on enregistre un fichier .wav temporaire
            wavfile.write("audio_filtre.wav", frequence, signal_final)
            st.audio("audio_filtre.wav", format="audio/wav")
    else:
        st.info("Veuillez charger un fichier .wav pour commencer.") 