import streamlit as st
import numpy as np
import matplotlib.image as mpimg

st.set_page_config(page_title="Traitement d'Image", layout="wide")
st.title("Application de Traitement du Signal")

fichier_image = st.file_uploader("Chargez une image", type=['png', 'jpg', 'jpeg'])

if fichier_image is not None:
    filtre = st.selectbox("Choisissez un filtre :", ["Aucun", "Noir et Blanc"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Image Originale")
        st.image(fichier_image, use_container_width=True)

    with col2:
        st.subheader("Image Filtrée")
        image_matrice = mpimg.imread(fichier_image)
        image_courante = image_matrice[:, :, :3]
        if image_courante.max() <= 1.0:
            image_courante = image_courante * 255

        if filtre == "Noir et Blanc":
            R, G, B = image_courante[:, :, 0], image_courante[:, :, 1], image_courante[:, :, 2]
            gris = 0.299 * R + 0.587 * G + 0.114 * B
            image_courante = np.stack([gris, gris, gris], axis=-1)

        image_finale = np.clip(image_courante, 0, 255).astype(np.uint8)
        st.image(image_finale, use_container_width=True)
else:
    st.info("Veuillez charger une image pour commencer le traitement.")