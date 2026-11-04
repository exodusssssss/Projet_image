import streamlit as st

st.set_page_config(page_title="Traitement d'Image", layout="wide")
st.title("Application de Traitement du Signal")

fichier_image = st.file_uploader("Chargez une image", type=['png', 'jpg', 'jpeg'])

if fichier_image is not None:
    st.image(fichier_image, use_container_width=True)
else:
    st.info("Veuillez charger une image pour commencer le traitement.")