# ==============================================
# 🐾 VetoCheck - Diagnostic Préventif Animal 🐾
# © 2025 David Salvador
# Démo Licensing Maxi Zoo
# ==============================================

import tkinter as tk  # Librairie GUI standard Python
from tkinter import ttk, messagebox  # ttk = widgets modernes, messagebox = alertes
from PIL import Image, ImageTk  # Pour gérer images et logo
from datetime import datetime  # Pour l’historique ou date du diagnostic
import os, sys  # Pour gérer chemins de fichiers (logo) même après compilation
import webbrowser  # Pour ouvrir des liens vers produits Maxi Zoo

# Fonction utilitaire pour gérer les chemins relatifs en mode exécutable (.exe)
def resource_path(relative_path):
    """
    Retourne le chemin absolu du fichier.
    Si le programme est packagé avec PyInstaller,
    _MEIPASS pointe vers le dossier temporaire où tout est extrait.
    """
    try:
        base_path = sys._MEIPASS  # Dossier temp PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Sinon, on reste en local
    return os.path.join(base_path, relative_path)

# Thème de couleurs pour uniformiser l'interface
COLOR_BG = "#ffffff"      # Fond blanc
COLOR_PRIMARY = "#2ca6a4" # Couleur primaire (boutons, accents)
COLOR_TEXT = "#1b4f4e"    # Texte standard

# Base de données de recommandations intelligentes
# Organisé par type animal > besoin > niveau d'alerte
RECOMMANDATIONS_INTEL = {
    "chien": {
         # Exemple pour digestion : vert / orange / rouge
        "digestion": {
            "Vert": [
                {"nom": "Friandises digestes hypoallergéniques", "lien": "https://www.maxizoo.fr/chien-friandise-digestion"},
                {"nom": "Croquettes digestion facile", "lien": "https://www.maxizoo.fr/chien-croquette-digestion"}
            ],
            "Orange": [
                {"nom": "Compléments probiotiques pour chien", "lien": "https://www.maxizoo.fr/chien-probiotiques"}
            ],
            "Rouge": [
                {"nom": "Prendre RDV vétérinaire digestion", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
         # Même logique pour articulations, comportement, hydratation
        "articulations": {
            "Vert": [
                {"nom": "Tapis orthopédique confort", "lien": "https://www.maxizoo.fr/chien-tapis-orthopedique"}
            ],
            "Orange": [
                {"nom": "Complément articulation senior", "lien": "https://www.maxizoo.fr/chien-complement-articulation"}
            ],
            "Rouge": [
                {"nom": "Visite vétérinaire mobilité", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "oreilles": {
            "Vert": [
                {"nom": "Jouet d’occupation anti-stress", "lien": "https://www.maxizoo.fr/chien-jouet-antistress"}
            ],
            "Orange": [
                {"nom": "Diffuseur apaisant comportement", "lien": "https://www.maxizoo.fr/chien-diffuseur-apaisant"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "yeux": {
            "Vert": [
                {"nom": "Jouet d’occupation anti-stress", "lien": "https://www.maxizoo.fr/chien-jouet-antistress"}
            ],
            "Orange": [
                {"nom": "Diffuseur apaisant comportement", "lien": "https://www.maxizoo.fr/chien-diffuseur-apaisant"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "parasites": {
            "Vert": [
                {"nom": "Jouet d’occupation anti-stress", "lien": "https://www.maxizoo.fr/chien-jouet-antistress"}
            ],
            "Orange": [
                {"nom": "Diffuseur apaisant comportement", "lien": "https://www.maxizoo.fr/chien-diffuseur-apaisant"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "pelage": {
            "Vert": [
                {"nom": "Jouet d’occupation anti-stress", "lien": "https://www.maxizoo.fr/chien-jouet-antistress"}
            ],
            "Orange": [
                {"nom": "Diffuseur apaisant comportement", "lien": "https://www.maxizoo.fr/chien-diffuseur-apaisant"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "dent": {
            "Vert": [
                {"nom": "Jouet d’occupation anti-stress", "lien": "https://www.maxizoo.fr/chien-jouet-antistress"}
            ],
            "Orange": [
                {"nom": "Diffuseur apaisant comportement", "lien": "https://www.maxizoo.fr/chien-diffuseur-apaisant"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "comportement": {
            "Vert": [
                {"nom": "Jouet d’occupation anti-stress", "lien": "https://www.maxizoo.fr/chien-jouet-antistress"}
            ],
            "Orange": [
                {"nom": "Diffuseur apaisant comportement", "lien": "https://www.maxizoo.fr/chien-diffuseur-apaisant"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "hydratation": {
            "Vert": [
                {"nom": "Fontaine à boire", "lien": "https://www.maxizoo.fr/p/catit-fontaine--boire-avec-fleurs-led-1314661/?isSearchPage=fontaines%20eau"}
            ],
            "Orange": [
                {"nom": "Fontaine à boire", "lien": "https://www.maxizoo.fr/p/catit-fontaine--boire-avec-fleurs-led-1314661/?isSearchPage=fontaines%20eau"}
            ],
            "Rouge": [
                {"nom": "Fontaine à boire", "lien": "https://www.maxizoo.fr/p/catit-fontaine--boire-avec-fleurs-led-1314661/?isSearchPage=fontaines%20eau"}
            ]
        }
    },
    "chat": {
        "digestion": {
            "Vert": [
                {"nom": "Friandises digestes pour chat", "lien": "https://www.maxizoo.fr/chat-friandise-digestion"}
            ],
            "Orange": [
                {"nom": "Compléments probiotiques chat", "lien": "https://www.maxizoo.fr/chat-probiotiques"}
            ],
            "Rouge": [
                {"nom": "Prendre RDV vétérinaire digestion", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "oreilles": {
            "Vert": [
                {"nom": "Jouet stimulation mentale", "lien": "https://www.maxizoo.fr/chat-jouet-mental"}
            ],
            "Orange": [
                {"nom": "Diffuseur phéromone apaisante", "lien": "https://www.maxizoo.fr/chat-pheromone"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "yeux": {
            "Vert": [
                {"nom": "Jouet stimulation mentale", "lien": "https://www.maxizoo.fr/chat-jouet-mental"}
            ],
            "Orange": [
                {"nom": "Diffuseur phéromone apaisante", "lien": "https://www.maxizoo.fr/chat-pheromone"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "parasites": {
            "Vert": [
                {"nom": "Jouet stimulation mentale", "lien": "https://www.maxizoo.fr/chat-jouet-mental"}
            ],
            "Orange": [
                {"nom": "Diffuseur phéromone apaisante", "lien": "https://www.maxizoo.fr/chat-pheromone"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "pelage": {
            "Vert": [
                {"nom": "Jouet stimulation mentale", "lien": "https://www.maxizoo.fr/chat-jouet-mental"}
            ],
            "Orange": [
                {"nom": "Diffuseur phéromone apaisante", "lien": "https://www.maxizoo.fr/chat-pheromone"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "comportement": {
            "Vert": [
                {"nom": "Jouet stimulation mentale", "lien": "https://www.maxizoo.fr/chat-jouet-mental"}
            ],
            "Orange": [
                {"nom": "Diffuseur phéromone apaisante", "lien": "https://www.maxizoo.fr/chat-pheromone"}
            ],
            "Rouge": [
                {"nom": "Consultation comportementale", "lien": "https://www.maxizoo.fr/services-veterinaire"}
            ]
        },
        "hydratation": {
            "Vert": [
                {"nom": "Fontaine à boire", "lien": "https://www.maxizoo.fr/p/catit-fontaine--boire-avec-fleurs-led-1314661/?isSearchPage=fontaines%20eau"}
            ],
            "Orange": [
                {"nom": "Fontaine à boire", "lien": "https://www.maxizoo.fr/p/catit-fontaine--boire-avec-fleurs-led-1314661/?isSearchPage=fontaines%20eau"}
            ],
            "Rouge": [
                {"nom": "Fontaine à boire", "lien": "https://www.maxizoo.fr/p/catit-fontaine--boire-avec-fleurs-led-1314661/?isSearchPage=fontaines%20eau"}
            ]
        }
    }
}

# Chaque question a :
# - le texte formaté avec {} pour nom/pronom
# - le score attribué si OUI
# - éventuellement un score si NON ou 'unknown'
# - un ou plusieurs tags (pour cibler la recommandation finale)
questions_chien = [
    {"text": "{} vomit-{} fréquemment ?", "score_if_yes": 3, "tags": ["digestion"]},
    {"text": "{} refuse-t-{} de manger depuis plus de 24h ?", "score_if_yes": 2, "tags": ["digestion"]},
    {"text": "{} a-t-{} un pelage terne ?", "score_if_yes": 2, "tags": ["pelage"]},
    {"text": "{} perd-{} beaucoup de poils ?", "score_if_yes": 2, "tags": ["pelage"]},
    {"text": "{} a-t-{} des difficultés à marcher ou se lever ?", "score_if_yes": 2, "tags": ["articulations"]},
    {"text": "{} montre-t-{} une agressivité inhabituelle ?", "score_if_yes": 2, "tags": ["comportement"]},
    {"text": "{} se gratte-t-{} souvent ? (puces/tiques)", "score_if_yes": 3, "tags": ["parasites"]},
    {"text": "{} a-t-{} les yeux rouges ou qui coulent ?", "score_if_yes": 2, "tags": ["yeux"]},
    {"text": "{} a-t-{} mauvaise haleine ou des dents abîmées ?", "score_if_yes": 2, "tags": ["dents"]},
    {"text": "{} secoue-t-{} souvent la tête ou se gratte les oreilles ?", "score_if_yes": 2, "tags": ["oreilles"]},
    {"text": "{} boit-{} normalement ?", "score_if_yes": 0, "score_if_no": 2, "tags": ["hydratation"]},
    {"text": "{} présente-t-{} de la diarrhée ou du sang dans les selles ?", "score_if_yes": 4, "tags": ["digestion"]},
    {"text": "{} semble-t-{} triste ou amorphe ?", "score_if_yes": 2, "tags": ["comportement"]},
    {"text": "{} respire-t-{} rapidement ou bruyamment ?", "score_if_yes": 3, "tags": ["respiration"]},
    {"text": "{} tousse-t-{} fréquemment ?", "score_if_yes": 2, "tags": ["respiration"]},
    {"text": "{} présente-t-{} une perte de poids visible ?", "score_if_yes": 3, "tags": ["comportement"]},
    {"text": "Le comportement de {} a-t-{} changé brutalement ?", "score_if_yes": 2, "tags": ["comportement"]}
]
 # Même principe, adapté au chat
questions_chat = [
    {"text": "{} vomit-{} fréquemment ?", "score_if_yes": 3, "tags": ["digestion"]},
    {"text": "{} refuse-t-{} de manger depuis plus de 24h ?", "score_if_yes": 2, "tags": ["digestion"]},
    {"text": "{} fait-{} des bruits anormaux en respirant ?", "score_if_yes": 3, "tags": ["respiration"]},
    {"text": "{} montre-t-{} une agressivité inhabituelle ?", "score_if_yes": 2, "tags": ["comportement"]},
    {"text": "{} boit-{} normalement ?", "score_if_yes": 0, "score_if_no": 2, "tags": ["hydratation"]},
    {"text": "{} a-t-{} des selles anormales ou sanglantes ?", "score_if_yes": 4, "tags": ["digestion"]},
    {"text": "{} semble-t-{} caché, amorphe ou replié ?", "score_if_yes": 2, "tags": ["comportement"]},
    {"text": "{} présente-t-{} des boiteries ou mouvements douloureux ?", "score_if_yes": 2, "tags": ["comportement"]},
    {"text": "{} a-t-{} maigri visiblement ces derniers jours ?", "score_if_yes": 3, "tags": ["comportement"]},
    {"text": "{} utilise-t-{} normalement sa litière ?", "score_if_no": 2, "tags": ["digestion"]},
    {"text": "{} a-t-{} un pelage terne?", "score_if_yes": 2, "tags": ["pelage"]},
    {"text": "{} perd-{} beaucoup de poils ?", "score_if_yes": 2, "tags": ["pelage"]},
    {"text": "{} se gratte-t-{} souvent ? (puces/tiques)", "score_if_yes": 3, "tags": ["parasites"]},
    {"text": "{} a-t-{} les yeux rouges ou qui coulent ?", "score_if_yes": 2, "tags": ["yeux"]},
    {"text": "{} secoue-t-{} souvent la tête ou se gratte les oreilles ?", "score_if_yes": 2, "tags": ["oreilles"]},
    {"text": "{} semble-t-{} agité(e) ou stressé(e) récemment ?", "score_if_yes": 3, "tags": ["comportement"]},
    {"text": "Le comportement de {} a-t-{} changé brutalement ?", "score_if_yes": 2, "tags": ["comportement"]}
]

class VetoCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VetoCheck") # Titre de la fenêtre
        self.root.configure(bg=COLOR_BG)
        self.reset() # Lance le premier écran

    def reset(self):
        
        # Réinitialise toutes les variables avant un nouveau diagnostic.
        
        self.animal_type = None
        self.animal_name = ""
        self.animal_age = ""
        self.animal_age_unit = ""
        self.animal_sex = ""
        self.score = 0
        self.question_index = 0
        self.questions = []
        self.symptom_tags = {} # Pour compter les tags dominants
        self.show_profile_form()

    def show_profile_form(self):
        """
        Affiche le formulaire de départ :
        - Nom de l’animal
        - Âge + unité (ans/mois)
        - Sexe
        - Choix Chien/Chat
        """
        for widget in self.root.winfo_children():
            widget.destroy() # Nettoie la fenêtre
        # Affiche le logo, géré via resource_path()
        try:
            logo = Image.open(resource_path("vetocheck_logo.png"))
            logo = logo.resize((200, 200))
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.root, image=logo_img, bg=COLOR_BG)
            logo_label.image = logo_img # Important : garde référence !
            logo_label.pack(pady=(20, 5))
        except:
            pass # Si le logo n’est pas trouvé

        #tk.Label(self.root, text="VetoCheck", font=("Arial", 24, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY).pack(pady=(5, 15))

         # Bloc de champs : nom / âge / sexe
        form_frame = tk.Frame(self.root, bg=COLOR_BG)
        form_frame.pack(pady=5)

        # Nom
        tk.Label(form_frame, text="Nom de l'animal :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.entry_name.grid(row=0, column=1, pady=5)

        # Âge + combobox ans/mois
        tk.Label(form_frame, text="Âge :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_age = tk.Entry(form_frame, font=("Arial", 12), width=10)
        self.entry_age.grid(row=1, column=1, sticky="w", pady=5)

        self.age_unit_var = tk.StringVar(value="ans")
        self.age_unit_combobox = ttk.Combobox(form_frame, textvariable=self.age_unit_var, values=["ans", "mois"], width=8, state="readonly", font=("Arial", 11))
        self.age_unit_combobox.grid(row=1, column=1, sticky="e", pady=5, padx=(0, 40))

        # Sexe
        tk.Label(form_frame, text="Sexe :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.sex_var = tk.StringVar(value="Mâle")
        self.sex_combobox = ttk.Combobox(form_frame, textvariable=self.sex_var, values=["Mâle", "Femelle"], width=20, state="readonly", font=("Arial", 11))
        self.sex_combobox.grid(row=2, column=1, pady=5)

        # ✅ Nouveau : Stérilisé(e)
        tk.Label(form_frame, text="Stérilisé(e) :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.steril_var = tk.StringVar(value="Non")
        self.steril_combobox = ttk.Combobox(
            form_frame, textvariable=self.steril_var,
            values=["Oui", "Non"], width=20, state="readonly", font=("Arial", 11)
        )
        self.steril_combobox.grid(row=3, column=1, pady=5)

        tk.Label(self.root, text="Quel animal souhaitez-vous diagnostiquer ?", font=("Arial", 13, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=20)

        card_style = {
            "font": ("Arial", 18, "bold"),
            "bg": "#e0f7f6",
            "fg": COLOR_PRIMARY,
            "activebackground": "#d0f0ef",
            "activeforeground": COLOR_TEXT,
            "relief": "groove",
            "bd": 2,
            "width": 12,
            "height": 3,
            "cursor": "hand2"
        }

        button_frame = tk.Frame(self.root, bg=COLOR_BG)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🐶\nChien", command=lambda: self.start_quiz("chien"), **card_style).grid(row=0, column=0, padx=30, pady=10)
        tk.Button(button_frame, text="🐱\nChat", command=lambda: self.start_quiz("chat"), **card_style).grid(row=0, column=1, padx=30, pady=10)

        # Petit bouton "?" en haut à droite
        help_button = tk.Label(
            self.root,
            text=" ? ",
            font=("Arial", 12, "bold"),
            bg=COLOR_PRIMARY,
            fg="white",
            cursor="question_arrow"
        )
        # Position : coin haut droit avec un léger décalage
        help_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

        # Texte d'aide à afficher au survol
        help_text = (
            "🐾 VetoCheck est un outil de pré-diagnostic santé animale.\n"
            "Répondez aux questions pour évaluer les signes de votre animal.\n"
            "Recevez des recommandations adaptées.\n"
            "⚠️ Ne remplace pas une visite vétérinaire !"
        )

        # Bind pour afficher/masquer la bulle au survol
        help_button.bind("<Enter>", lambda e: self.show_tooltip(help_button, help_text))
        help_button.bind("<Leave>", lambda e: self.hide_tooltip())


        # Footer branding
        self.footer = tk.Label(
            self.root,
            text="VetoCheck | © 2025 David Salvador | Licensing Demo Maxi Zoo",
            font=("Arial", 9, "italic"),
            fg="#2ca6a4",
            bg=COLOR_BG
        )
        self.footer.pack(side="bottom", pady=5)


    def start_quiz(self, animal_type):
        self.animal_type = animal_type
        self.animal_name = self.entry_name.get().capitalize()
        self.animal_age = self.entry_age.get()
        self.animal_age_unit = self.age_unit_var.get()
        self.animal_sex = self.sex_var.get()
        self.animal_steril = self.steril_var.get()
        self.questions = questions_chien if animal_type == "chien" else questions_chat
        self.score = 0
        self.question_index = 0
        self.symptom_tags = {}
        self.show_question()

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        question = self.questions[self.question_index]

        pronoun = "il" if self.animal_sex == "Mâle" else "elle"
        question_text = question["text"].format(self.animal_name, pronoun)

        info_text = f"{self.animal_name} ({self.animal_age} {self.animal_age_unit}, {self.animal_sex}, Stérilisé(e): {self.animal_steril})"
        tk.Label(self.root, text=info_text, font=("Arial", 12, "italic"), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=5)

        tk.Label(self.root, text=f"Question {self.question_index + 1} sur {len(self.questions)}",
                 font=("Arial", 11), bg=COLOR_BG, fg=COLOR_PRIMARY).pack(pady=2)

        tk.Label(self.root, text=question_text, font=("Arial", 15), wraplength=450,
                 pady=20, fg=COLOR_TEXT, bg=COLOR_BG).pack()

        button_frame = tk.Frame(self.root, bg=COLOR_BG)
        button_frame.pack(pady=10)

        style = {
            "font": ("Arial", 11),
            "bg": COLOR_PRIMARY,
            "fg": "white",
            "activebackground": "#1e7f7e",
            "activeforeground": "white",
            "relief": "flat",
            "width": 12,
            "height": 2,
            "bd": 0
        }

        tk.Button(button_frame, text="Oui", command=lambda: self.answer("yes"), **style).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Non", command=lambda: self.answer("no"), **style).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Je ne sais pas", command=lambda: self.answer("unknown"), **style).grid(row=0, column=2, padx=5)

        self.footer = tk.Label(
            self.root,
            text="VetoCheck | © 2025 David Salvador | Licensing Demo Maxi Zoo",
            font=("Arial", 9, "italic"),
            fg="#2ca6a4",
            bg=COLOR_BG
        )
        self.footer.pack(side="bottom", pady=5)

    def answer(self, response):
        q = self.questions[self.question_index]
        if response == "yes":
            self.score += q.get("score_if_yes", 0)
            for tag in q.get("tags", []):
                self.symptom_tags[tag] = self.symptom_tags.get(tag, 0) + q.get("score_if_yes", 0)
        elif response == "no":
            self.score += q.get("score_if_no", 0)
        elif response == "unknown":
            self.score += q.get("score_if_unknown", 1)

        self.question_index += 1
        if self.question_index < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        if self.score <= 4:
            level = "Vert"
            label = "🟩 Aucun signe inquiétant"
            detail = "Continuez à surveiller votre animal normalement."
            color = "#4CAF50"
        elif 5 <= self.score <= 9:
            level = "Orange"
            label = "🟧 Signes à surveiller"
            detail = "Soyez attentif aux évolutions, consultez si nécessaire."
            color = "#FF9800"
        else:
            level = "Rouge"
            label = "🟥 Risque élevé"
            detail = "Consultez un vétérinaire dès que possible."
            color = "#F44336"

        dominant_need = max(self.symptom_tags, key=self.symptom_tags.get) if self.symptom_tags else "général"
        propositions = RECOMMANDATIONS_INTEL.get(self.animal_type, {}).get(dominant_need, {}).get(level, [])

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Diagnostic terminé", font=("Arial", 16, "bold"), fg=COLOR_PRIMARY, bg=COLOR_BG).pack(pady=15)
        tk.Label(self.root, text=f"{label}", font=("Arial", 14, "bold"), fg=color, bg=COLOR_BG).pack(pady=10)
        tk.Label(self.root, text=detail, font=("Arial", 12), wraplength=450, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=10)

        tk.Label(self.root, text="Recommandations personnalisées Maxi Zoo :", 
                 font=("Arial", 13, "bold"), fg=COLOR_PRIMARY, bg=COLOR_BG).pack(pady=10)

        for produit in propositions:
            produit_label = tk.Label(
                self.root,
                text=f"• {produit['nom']}",
                font=("Arial", 11, "underline"),
                fg="#0056b3",
                cursor="hand2",
                bg=COLOR_BG,
                anchor="w"
            )
            produit_label.pack(fill="x", padx=30, pady=2)
            produit_label.bind("<Enter>", lambda e, lbl=produit_label: lbl.config(fg="#1a75ff"))
            produit_label.bind("<Leave>", lambda e, lbl=produit_label: lbl.config(fg="#0056b3"))
            produit_label.bind("<Button-1>", lambda e, url=produit["lien"]: self.open_url(url))

        # Message stérilisation si >6 mois & non stérilisé
        try:
            age = int(self.animal_age)
            if (self.animal_age_unit == "ans" and age >= 1) or (self.animal_age_unit == "mois" and age > 6):
                if self.animal_steril.lower() == "non":
                    steril_label = tk.Label(self.root, text=f"⚠️ Penser à stériliser {self.animal_name}",
                                            font=("Arial", 10, "italic"), fg="red", bg=COLOR_BG)
                    steril_label.pack(pady=(10, 2))

                    vet_link = tk.Label(self.root, text="Contacter un vétérinaire",
                                        font=("Arial", 10, "underline"), fg="#0056b3",
                                        cursor="hand2", bg=COLOR_BG)
                    vet_link.pack()
                    vet_link.bind("<Enter>", lambda e: vet_link.config(fg="#1a75ff"))
                    vet_link.bind("<Leave>", lambda e: vet_link.config(fg="#0056b3"))
                    vet_link.bind("<Button-1>", lambda e: self.open_url("https://www.maxizoo.fr/services-veterinaire"))
        except:
            pass

        tk.Button(self.root, text="🔁 Recommencer", font=("Arial", 12, "bold"), bg=COLOR_PRIMARY,
                  fg="white", relief="flat", width=20, height=2, command=self.reset).pack(pady=15)

        tk.Button(self.root, text="Quitter", font=("Arial", 11), bg="#cccccc",
                  fg="black", relief="flat", width=12, command=self.root.quit).pack()
        
        if level == "Rouge":
            urgence_label = tk.Label(
                self.root,
                text="⚠️ En cas d’urgence, appelez le 3115 (numéro gratuit)",
                font=("Arial", 12, "bold"),
                fg="red",
                bg=COLOR_BG
            )
            urgence_label.pack(pady=(10, 5))

            urgence_link = tk.Label(
                self.root,
                text="📞 Plus d'infos sur le 3115",
                font=("Arial", 10, "underline"),
                fg="#b30000",
                cursor="hand2",
                bg=COLOR_BG
            )
            urgence_link.pack()
            urgence_link.bind("<Enter>", lambda e: urgence_link.config(fg="#ff0000"))
            urgence_link.bind("<Leave>", lambda e: urgence_link.config(fg="#b30000"))
            urgence_link.bind(
                "<Button-1>",
                lambda e: self.open_url("https://www.urgences-veterinaires.fr/3115.php")
            )
        
        self.footer = tk.Label(
            self.root,
            text="VetoCheck | © 2025 David Salvador | Licensing Demo Maxi Zoo",
            font=("Arial", 9, "italic"),
            fg="#2ca6a4",
            bg=COLOR_BG
        )
        self.footer.pack(side="bottom", pady=5)

    def open_url(self, url):
        webbrowser.open_new(url)

    def show_tooltip(self, widget, text):
        """
        Affiche une bulle d'aide au survol du bouton '?'.
        """
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.config(bg="lightyellow")
        label = tk.Label(
            self.tooltip,
            text=text,
            justify='left',
            bg="lightyellow",
            fg="black",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack(ipadx=5, ipady=2)

        # Position de la bulle près du bouton
        x = widget.winfo_rootx() + 20
        y = widget.winfo_rooty() + 20
        self.tooltip.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self):
        """
        Détruit la bulle d'aide si elle existe.
        """
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()
            self.tooltip = None

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x650")
    app = VetoCheckApp(root)
    root.mainloop()

#pyinstaller --onefile --windowed --icon=vetocheck.ico --add-data "vetocheck_logo.png;." vetocheck.py
