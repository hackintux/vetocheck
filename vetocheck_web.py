# vetocheck_web.py

import streamlit as st
import json
from datetime import datetime

# === CONFIG ===
st.set_page_config(
    page_title="VetoCheck",
    page_icon="🐾",
    layout="centered"
)

# === CHARGEMENT DES RECOMMANDATIONS ===
@st.cache_data
def load_recommendations():
    with open("reco.json", "r", encoding="utf-8") as f:
        return json.load(f)

RECO = load_recommendations()

# === Titre & Intro ===
st.title("🐾 VetoCheck — Pré-diagnostic santé animale")
st.write("Analysez rapidement les besoins de votre animal et recevez des recommandations adaptées. "
         "Cet outil ne remplace pas une consultation vétérinaire.")

# === Profil animal ===
st.header("📋 Profil de l'animal")
animal_name = st.text_input("Nom de l'animal").capitalize()
animal_type = st.radio("Type d'animal", ["Chien", "Chat"])
age = st.number_input("Âge", min_value=0, max_value=25, step=1)
age_unit = st.selectbox("Unité", ["ans", "mois"])
sex = st.selectbox("Sexe", ["Mâle", "Femelle"])
steril = st.selectbox("Stérilisé(e)", ["Oui", "Non"])

# === Questions ===
st.header("🩺 Questions santé")
if animal_type == "Chien":
    questions = [
        ("digestion", f"{animal_name} vomit-il/elle fréquemment ?"),
        ("digestion", f"{animal_name} refuse-t-il/elle de manger depuis plus de 24h ?"),
        ("pelage", f"{animal_name} a-t-il/elle un pelage terne ou perd-il/elle beaucoup de poils ?"),
        ("parasites", f"{animal_name} se gratte-t-il/elle souvent ? (puces/tiques)"),
        ("dents", f"{animal_name} a-t-il/elle mauvaise haleine ou des dents abîmées ?"),
        ("yeux", f"{animal_name} a-t-il/elle les yeux rouges ou qui coulent ?"),
        ("oreilles", f"{animal_name} secoue-t-il/elle souvent la tête ou se gratte les oreilles ?")
    ]
else:
    questions = [
        ("pelage", f"{animal_name} a-t-il/elle un pelage terne ou perd-il/elle beaucoup de poils ?"),
        ("parasites", f"{animal_name} se gratte-t-il/elle souvent ? (puces/tiques)"),
        ("yeux", f"{animal_name} a-t-il/elle les yeux rouges ou qui coulent ?"),
        ("oreilles", f"{animal_name} secoue-t-il/elle souvent la tête ou se gratte les oreilles ?"),
        ("comportement", f"{animal_name} semble-t-il/elle agité(e) ou stressé(e) ?")
    ]

tags_score = {}
total_score = 0

for tag, question in questions:
    answer = st.radio(question, ["Oui", "Non"], key=question)
    if answer == "Oui":
        score = 2  # pondération simple, ajustable
        tags_score[tag] = tags_score.get(tag, 0) + score
        total_score += score

# === Bouton pour lancer diagnostic ===
if st.button("✅ Voir le diagnostic"):
    st.header("🎯 Résultat du diagnostic")

    # === Niveau ===
    if total_score <= 4:
        level = "Vert"
    elif 5 <= total_score <= 9:
        level = "Orange"
    else:
        level = "Rouge"

    st.subheader(f"Niveau : {level}")

    # === Message stérilisation ===
    if (age_unit == "ans" and age >= 1) or (age_unit == "mois" and age > 6):
        if steril == "Non":
            st.warning(f"⚠️ Penser à stériliser {animal_name}")

    # === Message urgence 3115 ===
    if level == "Rouge":
        st.error("⚠️ En cas d'urgence, appelez le **3115** (numéro gratuit) pour contacter un vétérinaire de garde.")

    # === Recommandations ===
    st.subheader("📦 Recommandations")
    active_tags = list(tags_score.keys())
    recos = []
    for reco in RECO:
        if reco["animal"] != animal_type.lower():
            continue
        if reco["level"] != level:
            continue
        if not any(tag in active_tags for tag in reco["tags"]):
            continue
        recos.append(reco["produit"])

    if recos:
        for p in recos:
            st.markdown(f"- [{p['nom']}]({p['lien']})")
    else:
        st.info("RAS pour le moment — surveillez l'état de votre animal ou consultez votre vétérinaire.")

    # === Historique simple ===
    st.write("🗂️ Diagnostic sauvegardé :", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# === Footer ===
st.write("---")
st.caption("VetoCheck BETA | Prototype proposé par Monsieur David Salvador | © 2025")

