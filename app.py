import streamlit as st
import numpy as np
import matplotlib.image as mpimg

st.set_page_config(page_title="Traitement d'Image", layout="wide")
st.title("Application de Traitement du Signal")

# On n'accepte que le JPG pour des histoires de simplicité
fichier_image = st.file_uploader("Chargez une image JPG", type=['jpg', 'jpeg'])

if fichier_image is not None:
    filtre = st.selectbox("Choisissez un filtre :", ["Aucun", "Noir et Blanc", "Ajout de bruit"])

    intensite = 50
    if filtre == "Ajout de bruit":
        intensite = st.slider("Intensité du bruit", min_value=0, max_value=150, value=50)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Image Originale")
        st.image(fichier_image, use_container_width=True)

    with col2:
        st.subheader("Image Filtrée")

        image_courante = mpimg.imread(fichier_image).astype(float)

        if filtre == "Noir et Blanc":
            gris = image_courante.mean(axis=2)
            image_courante = np.stack([gris, gris, gris], axis=-1)

        elif filtre == "Ajout de bruit":
            # Bruit gaussien
            bruit = np.random.normal(loc=0, scale=intensite, size=image_courante.shape)
            image_courante = image_courante + bruit

        # On plafonne entre 0 et 255 puis on convertit en entiers
        image_finale = np.clip(image_courante, 0, 255).astype(np.uint8)
        st.image(image_finale, use_container_width=True)
else:
    st.info("Veuillez charger une image pour commencer le traitement.")