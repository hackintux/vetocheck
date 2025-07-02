# vetocheck_web.py

import streamlit as st
import json
from datetime import datetime

# === THEME ===
COLOR_BG = "#ffffff"
COLOR_PRIMARY = "#2ca6a4"
COLOR_TEXT = "#1b4f4e"

# === CONFIGURATION ===
st.set_page_config(
    page_title="VetoCheck",
    page_icon="🐾",
    layout="centered"
)

# === CHARGER LES RECOMMANDATIONS INTEL ===
@st.cache_data
def load_reco():
    with open("reco.json", "r", encoding="utf-8") as f:
        return json.load(f)

RECO = load_reco()

# === TITRE & LOGO ===
st.markdown(
    f"<h1 style='text-align: center; color:{COLOR_PRIMARY}'>🐾 VetoCheck</h1>",
    unsafe_allow_html=True
)

# Logo centré avec balise HTML
st.markdown(
    """
    <div style="text-align: center;">
        <img src='vetocheck_logo.png' width='150'>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align: center; color:{COLOR_TEXT}'>Diagnostic Préventif Animal — Licensing Maxi Zoo</p>",
    unsafe_allow_html=True
)

# === INFO TOOLTIP "?" ===
with st.expander("ℹ️ Qu'est-ce que VetoCheck ?", expanded=False):
    st.write(
        "🐾 **VetoCheck** est un outil de pré-diagnostic santé animale.\n"
        "- Questionnaire intelligent pour évaluer les signes.\n"
        "- Recommandations Maxi Zoo adaptées.\n"
        "- ⚠️ Ne remplace jamais une visite vétérinaire."
    )

st.divider()

# === PROFIL ANIMAL ===
st.header("📋 Profil de l'animal")

col1, col2 = st.columns(2)
with col1:
    animal_name = st.text_input("Nom de l'animal").capitalize()
    age = st.number_input("Âge", min_value=0, max_value=30, step=1)
    age_unit = st.selectbox("Unité", ["ans", "mois"])
with col2:
    sex = st.selectbox("Sexe", ["Mâle", "Femelle"])
    steril = st.selectbox("Stérilisé(e)", ["Oui", "Non"])

st.markdown("---")

# === CHOIX CHIEN / CHAT ===
st.subheader("🐶 / 🐱 Quel animal souhaitez-vous diagnostiquer ?")
animal_type = st.radio("Type d'animal :", ["Chien", "Chat"], horizontal=True)

# === QUESTIONS ===
if animal_type:
    st.header("🩺 Questionnaire santé")

    if animal_type == "Chien":
        questions = [
            {"text": "{} vomit-{} fréquemment ?", "score_if_yes": 3, "tags": ["digestion"]},
            {"text": "{} refuse-t-{} de manger depuis plus de 24h ?", "score_if_yes": 2, "tags": ["digestion"]},
            {"text": "{} a-t-{} un pelage terne ?", "score_if_yes": 2, "tags": ["pelage"]},
            {"text": "{} perd-{} beaucoup de poils ?", "score_if_yes": 2, "tags": ["pelage"]},
            {"text": "{} a-t-{} des difficultés à marcher ou se lever ?", "score_if_yes": 2, "tags": ["articulations"]},
            {"text": "{} montre-t-{} une agressivité inhabituelle ?", "score_if_yes": 2, "tags": ["comportement"]},
            {"text": "{} se gratte-t-{} souvent ? (puces/tiques)", "score_if_yes": 3, "tags": ["parasites"]},
            {"text": "{} a-t-{} les yeux rouges ou qui coulent ?", "score_if_yes": 2, "tags": ["yeux"]},
            {"text": "{} a-t-{} mauvaise haleine ou des dents abîmées ?", "score_if_yes": 2, "tags": ["dent"]},
            {"text": "{} secoue-t-{} souvent la tête ou se gratte les oreilles ?", "score_if_yes": 2, "tags": ["oreilles"]},
            {"text": "{} boit-{} normalement ?", "score_if_yes": 0, "score_if_no": 2, "tags": ["hydratation"]},
        ]
    else:
        questions = [
            {"text": "{} vomit-{} fréquemment ?", "score_if_yes": 3, "tags": ["digestion"]},
            {"text": "{} refuse-t-{} de manger depuis plus de 24h ?", "score_if_yes": 2, "tags": ["digestion"]},
            {"text": "{} fait-{} des bruits anormaux en respirant ?", "score_if_yes": 3, "tags": ["respiration"]},
            {"text": "{} montre-t-{} une agressivité inhabituelle ?", "score_if_yes": 2, "tags": ["comportement"]},
            {"text": "{} boit-{} normalement ?", "score_if_yes": 0, "score_if_no": 2, "tags": ["hydratation"]},
            {"text": "{} se gratte-t-{} souvent ? (puces/tiques)", "score_if_yes": 3, "tags": ["parasites"]},
            {"text": "{} a-t-{} les yeux rouges ou qui coulent ?", "score_if_yes": 2, "tags": ["yeux"]},
            {"text": "{} secoue-t-{} la tête ou se gratte les oreilles ?", "score_if_yes": 2, "tags": ["oreilles"]},
            {"text": "{} semble-t-{} agité(e) ou stressé(e) récemment ?", "score_if_yes": 3, "tags": ["comportement"]},
        ]

    total_score = 0
    symptom_tags = {}

    pronoun = "il" if sex == "Mâle" else "elle"

    for idx, q in enumerate(questions):
        question_text = q["text"].format(animal_name, pronoun)
        answer = st.radio(question_text, ["Oui", "Non", "Je ne sais pas"], key=f"q{idx}")

        if answer == "Oui":
            total_score += q.get("score_if_yes", 0)
            for tag in q.get("tags", []):
                symptom_tags[tag] = symptom_tags.get(tag, 0) + q.get("score_if_yes", 0)
        elif answer == "Non":
            total_score += q.get("score_if_no", 0)
        elif answer == "Je ne sais pas":
            total_score += q.get("score_if_unknown", 0)

    if st.button("✅ Voir le diagnostic complet"):
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
                st.warning(f"⚠️ Penser à stériliser {animal_name}.")

        # Message urgence 3115
        if level == "Rouge":
            st.error("⚠️ En cas d'urgence, appelez le **3115** (numéro gratuit) pour contacter un vétérinaire.")

        # Recommandations
        st.subheader("📦 Recommandations Maxi Zoo")
        dominant_need = max(symptom_tags, key=symptom_tags.get) if symptom_tags else "général"
        propositions = RECO.get(animal_type.lower(), {}).get(dominant_need, {}).get(level, [])

        if propositions:
            for p in propositions:
                st.markdown(f"- [{p['nom']}]({p['lien']})")
        else:
            st.info("RAS — surveillez ou consultez un vétérinaire.")

        st.caption(f"🗂️ Diagnostic sauvegardé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# === FOOTER ===
st.divider()
st.caption("VetoCheck | © 2025 David Salvador | Licensing Demo Maxi Zoo")
