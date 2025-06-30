
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Couleurs
COLOR_BG = "#ffffff"
COLOR_PRIMARY = "#2ca6a4"
COLOR_TEXT = "#1b4f4e"

# Questions chien
questions_chien = [
    {"text": "{} vomit-{} fréquemment ?", "score_if_yes": 3},
    {"text": "Refuse-t-{} de manger depuis plus de 24h ?", "score_if_yes": 2},
    {"text": "Boit-{} normalement ?", "score_if_yes": 0, "score_if_no": 2},
    {"text": "Présente-t-{} de la diarrhée ou du sang dans les selles ?", "score_if_yes": 4},
    {"text": "Semble-t-{} triste ou amorphe ?", "score_if_yes": 2},
    {"text": "A-t-{} des difficultés à marcher ou se lever ?", "score_if_yes": 2},
    {"text": "Respire-t-{} rapidement ou bruyamment ?", "score_if_yes": 3},
    {"text": "Tousse-t-{} fréquemment ?", "score_if_yes": 2},
    {"text": "Présente-t-{} une perte de poids visible ?", "score_if_yes": 3},
    {"text": "Son comportement a-t-{} changé brutalement ?", "score_if_yes": 2},
    {"text": "{} se gratte-t-{} intensément ou présente-t-{} des zones sans poils visibles ? ", "score_if_yes": 3},
    {"text": "Avez-vous constaté une mauvaise haleine persistante ou un écoulement inhabituel au niveau des dents ?", "score_if_yes": 2},
    {"text": "{} secoue-t-{} fréquemment la tête ou se gratte-t-{} les oreilles ?", "score_if_yes": 3},
    {"text": "Présente-t-{} des rougeurs ou des inflammations visibles au niveau des yeux ou de la peau ?", "score_if_yes": 3},
    {"text": "{} montre-t-{} une agressivité inhabituelle ou une irritabilité soudaine ?", "score_if_yes": 2},
    {"text": "Avez-vous observé une augmentation significative ou inhabituelle de la soif récemment ? ", "score_if_yes": 3},
    {"text": "{} urine-t-{} fréquemment ou présente-t-{} des difficultés lors de la miction ?", "score_if_yes": 3},
    {"text": "A-t-{} eu récemment un contact avec des tiques ou présente-t-{} des parasites visibles ?", "score_if_yes": 4}
]

# Questions chat
questions_chat = [
    {"text": "{} vomit-{} fréquemment ?", "score_if_yes": 3},
    {"text": "Refuse-t-{} de manger depuis plus de 24h ?", "score_if_yes": 2},
    {"text": "Boit-{} normalement ?", "score_if_yes": 0, "score_if_no": 2},
    {"text": "A-t-{} des selles anormales ou sanglantes ?", "score_if_yes": 4},
    {"text": "Semble-t-{} caché, amorphe ou replié ?", "score_if_yes": 2},
    {"text": "Présente-t-{} des boiteries ou mouvements douloureux ?", "score_if_yes": 2},
    {"text": "Fait-{} des bruits anormaux en respirant ?", "score_if_yes": 3},
    {"text": "A-t-{} maigri visiblement ces derniers jours ?", "score_if_yes": 3},
    {"text": "Utilise-t-{} normalement sa litière ?", "score_if_no": 2},
    {"text": "{} présente-t-{} des démangeaisons intenses ou des zones dégarnies de poils ?", "score_if_yes": 3},
    {"text": "Avez-vous constaté une odeur inhabituelle ou un écoulement autour de sa gueule ou de ses dents ?", "score_if_yes": 2},
    {"text": "{} éternue-t-{} fréquemment ou présente-t-{} un écoulement nasal ou oculaire ?", "score_if_yes": 3},
    {"text": "{} a-t-{} une respiration sifflante ou montre-t-{} des difficultés à respirer ?", "score_if_yes": 4},
    {"text": "{} se toilette-t-{} de façon excessive au point de provoquer des lésions cutanées ?", "score_if_yes": 2},
    {"text": "Avez-vous observé une fréquence inhabituelle de passage à la litière ou des difficultés à uriner ?", "score_if_yes": 4},
    {"text": "{} montre-t-{} des signes inhabituels d’agressivité ou d’anxiété soudains ?", "score_if_yes": 2},
    {"text": "Avez-vous remarqué une prise de poids soudaine et excessive ou un gonflement abdominal inhabituel ?", "score_if_yes": 3}
]

class VetoCheckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VetoCheck")
        self.root.configure(bg=COLOR_BG)
        self.reset()

    def reset(self):
        self.animal_type = None
        self.animal_name = ""
        self.animal_age = ""
        self.score = 0
        self.question_index = 0
        self.questions = []
        self.show_profile_form()

    def show_profile_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        try:
            logo = Image.open("vetocheck_logo.png")
            logo = logo.resize((120, 120))
            logo_img = ImageTk.PhotoImage(logo)
            logo_label = tk.Label(self.root, image=logo_img, bg=COLOR_BG)
            logo_label.image = logo_img
            logo_label.pack(pady=(20, 5))
        except:
            pass

        tk.Label(self.root, text="VetoCheck", font=("Arial", 24, "bold"), bg=COLOR_BG, fg=COLOR_PRIMARY).pack(pady=(5, 15))
        tk.Label(self.root, text="Analyse préventive de santé animale", font=("Arial", 12, "italic"),
                 bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=(0, 15))

        form_frame = tk.Frame(self.root, bg=COLOR_BG)
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Nom de l'animal :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.entry_name.grid(row=0, column=1, pady=5)

        # Champ pour l'âge (nombre uniquement)
        tk.Label(form_frame, text="Âge :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT)\
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_age = tk.Entry(form_frame, font=("Arial", 12), width=15)
        self.entry_age.grid(row=1, column=1, sticky="w", pady=5)

        # Choix entre "ans" et "mois"
        self.age_unit_var = tk.StringVar(value="ans")
        age_options = ["ans", "mois"]
        self.age_unit_menu = tk.OptionMenu(form_frame, self.age_unit_var, *age_options)
        self.age_unit_menu.config(font=("Arial", 12), width=7)
        self.age_unit_menu.grid(row=1, column=1, sticky="e", pady=5)


        tk.Label(form_frame, text="Sexe :", font=("Arial", 12), bg=COLOR_BG, fg=COLOR_TEXT)\
            .grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.sex_var = tk.StringVar(value="Mâle")

        sex_options = ["Mâle", "Femelle"]
        self.entry_sex = tk.OptionMenu(form_frame, self.sex_var, *sex_options)
        self.entry_sex.config(width=23, font=("Arial", 12))
        self.entry_sex.grid(row=3, column=1, pady=5)


        tk.Label(self.root, text="Quel animal souhaitez-vous diagnostiquer ?",
                 font=("Arial", 13, "bold"), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=20)

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

    def start_quiz(self, animal_type):
        self.animal_type = animal_type
        self.animal_name = self.entry_name.get().capitalize()
        self.animal_age = self.entry_age.get()
        self.animal_age_unit = self.age_unit_var.get()  # Ajout de l'unité
        self.animal_sex = self.sex_var.get()  # Ajout du sexe
        self.questions = questions_chien if animal_type == "chien" else questions_chat
        self.score = 0
        self.question_index = 0
        self.show_question()


    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        question = self.questions[self.question_index]

        # Affichage des infos de l'animal
        tk.Label(self.root, text=f"{self.animal_name} ({self.animal_age} {self.animal_age_unit}, {self.animal_sex})",
                font=("Arial", 12, "italic"), bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=5)

        tk.Label(self.root, text=f"Question {self.question_index + 1} sur {len(self.questions)}",
                font=("Arial", 11), bg=COLOR_BG, fg=COLOR_PRIMARY).pack(pady=2)

        # Définition du pronom selon le sexe
        pronoun = "il" if self.animal_sex == "Mâle" else "elle"
        question_text = question["text"].format(self.animal_name, pronoun)

        # Affichage question formatée
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

    def answer(self, response):
        q = self.questions[self.question_index]
        if response == "yes":
            self.score += q.get("score_if_yes", 0)
        elif response == "no":
            self.score += q.get("score_if_no", 0)
        elif response == "unknown":
            self.score += q.get("score_if_unknown", 1)  # valeur par défaut en cas d'incertitude

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

        with open("vetocheck_historique.txt", "a", encoding="utf-8") as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{self.animal_name} ({self.animal_age} {self.animal_age_unit}) - "
                f"Score: {self.score} - Niveau: {level}\n")


        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Diagnostic terminé", font=("Arial", 16, "bold"), fg=COLOR_PRIMARY, bg=COLOR_BG).pack(pady=15)
        tk.Label(self.root, text=f"{label}", font=("Arial", 14, "bold"), fg=color, bg=COLOR_BG).pack(pady=10)
        tk.Label(self.root, text=detail, font=("Arial", 12), wraplength=450, bg=COLOR_BG, fg=COLOR_TEXT).pack(pady=10)

        tk.Button(self.root, text="🔁 Recommencer", font=("Arial", 12, "bold"), bg=COLOR_PRIMARY,
                  fg="white", relief="flat", width=20, height=2, command=self.reset).pack(pady=15)

        tk.Button(self.root, text="Quitter", font=("Arial", 11), bg="#cccccc",
                  fg="black", relief="flat", width=12, command=self.root.quit).pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = VetoCheckApp(root)
    root.mainloop()
