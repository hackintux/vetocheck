# vetocheck_web.py

import streamlit as st
import json
from datetime import datetime

# === CONFIGURATION ===
st.set_page_config(
    page_title="VetoCheck",
    page_icon="🐾",
    layout="centered"
)

# === COULEURS ===
COLOR_BG = "#ffffff"
COLOR_PRIMARY = "#2ca6a4"
COLOR_TEXT = "#1b4f4e"

# === CHARGEMENT DES RECOMMANDATIONS ===
@st.cache_data
def load_reco():
    with open("reco.json", "r", encoding="utf-8") as f:
        return json.load(f)

RECO = load_reco()

# === TITRE & LOGO ===
st.markdown(
    f"<h1 style='text-align: center; color: {COLOR_PRIMARY};'>🐾 VetoCheck</h1>",
    unsafe_allow_html=True
)
st.image("vetocheck_logo.png",text-align: center, width=180)
st.markdown(
    f"<p style='text-align: center; color: {COLOR_TEXT};'>Diagnostic Préventif Animal — Licensing Maxi Zoo</p>",
    unsafe_allow_html=True
)
st.divider()

# === FORMULAIRE PROFIL ===
st.header("📋 Profil de l'animal")
col1, col2 = st.columns(2)
with col1:
    animal_name = st.text_input("Nom de l'animal").capitalize()
    age = st.number_input("Âge", min_value=0, max_value=25, step=1)
    age_unit = st.selectbox("Unité", ["ans", "mois"])
with col2:
    sex = st.selectbox("Sexe", ["Mâle", "Femelle"])
    steril = st.selectbox("Stérilisé(e)", ["Oui", "Non"])

st.markdown("---")

# === SÉLECTION ANIMAL ===
st.subheader("🐶 / 🐱 Choisissez l'animal")
animal_type = st.radio("Type", ["Chien", "Chat"], horizontal=True)

# === QUESTIONS ===
st.header("🩺 Questionnaire")
tags_score = {}
total_score = 0

if animal_type == "Chien":
    questions = [
        ("digestion", f"{animal_name} vomit-il/elle fréquemment ?"),
        ("digestion", f"{animal_name} refuse-t-il/elle de manger depuis plus de 24h ?"),
        ("pelage", f"{animal_name} a-t-il/elle un pelage terne ou perd-il/elle beaucoup de poils ?"),
        ("articulations", f"{animal_name} a-t-il/elle des difficultés à marcher ou se lever ?"),
        ("comportement", f"{animal_name} montre-t-il/elle une agressivité inhabituelle ?"),
        ("parasites", f"{animal_name} se gratte-t-il/elle souvent ? (puces/tiques)"),
        ("yeux", f"{animal_name} a-t-il/elle les yeux rouges ou qui coulent ?"),
        ("dents", f"{animal_name} a-t-il/elle mauvaise haleine ou des dents abîmées ?"),
        ("oreilles", f"{animal_name} secoue-t-il/elle la tête ou se gratte les oreilles ?")
    ]
else:
    questions = [
        ("digestion", f"{animal_name} vomit-il/elle fréquemment ?"),
        ("digestion", f"{animal_name} refuse-t-il/elle de manger depuis plus de 24h ?"),
        ("pelage", f"{animal_name} a-t-il/elle un pelage terne ou perd-il/elle beaucoup de poils ?"),
        ("comportement", f"{animal_name} semble-t-il/elle agité(e) ou stressé(e) ?"),
        ("parasites", f"{animal_name} se gratte-t-il/elle souvent ? (puces/tiques)"),
        ("yeux", f"{animal_name} a-t-il/elle les yeux rouges ou qui coulent ?"),
        ("oreilles", f"{animal_name} secoue-t-il/elle la tête ou se gratte les oreilles ?")
    ]

for tag, question in questions:
    answer = st.radio(question, ["Oui", "Non"], key=question)
    if answer == "Oui":
        tags_score[tag] = tags_score.get(tag, 0) + 2
        total_score += 2

# === DIAGNOSTIC ===
if st.button("✅ Voir le diagnostic"):
    st.header("🎯 Résultat")

    if total_score <= 4:
        level = "Vert"
        st.success("🟢 Aucun signe inquiétant — surveillance normale.")
    elif 5 <= total_score <= 9:
        level = "Orange"
        st.warning("🟠 Signes à surveiller — soyez attentif.")
    else:
        level = "Rouge"
        st.error("🔴 Risque élevé — consultez un vétérinaire dès que possible !")

    # Message stérilisation
    if (age_unit == "ans" and age >= 1) or (age_unit == "mois" and age > 6):
        if steril == "Non":
            st.warning(f"⚠️ Penser à stériliser {animal_name}")

    # Alerte 3115
    if level == "Rouge":
        st.error("⚠️ Contactez le **3115** (numéro gratuit) pour urgence vétérinaire.")

    # Recommandations
    st.subheader("📦 Recommandations Maxi Zoo")
    active_tags = list(tags_score.keys())
    recos = []
    for cat, prod in RECO.get(animal_type.lower(), {}).items():
        if cat in active_tags and level in prod:
            recos.extend(prod[level])

    if recos:
        for p in recos:
            st.markdown(f"- [{p['nom']}]({p['lien']})")
    else:
        st.info("RAS ou consultez votre vétérinaire.")

    # Historique
    st.caption(f"🗂️ Diagnostic sauvegardé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# === FOOTER ===
st.divider()
st.caption(f"VetoCheck | © 2025 David Salvador | Licensing Demo Maxi Zoo")
