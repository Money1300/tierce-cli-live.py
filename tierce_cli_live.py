
# -*- coding: utf-8 -*-
import random
import csv
import os
import time

chevaux_defaut = [
    (1, "SILVERADO", 18.82),
    (2, "GRINGO", 41.23),
    (3, "TANGO GIRL", 17.06),
    (4, "PEACE RULES", 24.29),
    (5, "GOLDEN QUACKER", 8.09),
    (6, "GRANDE CASA", 32.13),
    (7, "ACES HIGH", 4.33),
    (8, "DESERT EXPRESS", 5.06),
    (9, "SLINGA MALINGA", 7.38),
    (10, "SKYBLUE", 15.02),
    (11, "LANGOUSTINE", 10.65),
    (12, "SUPERWOOD", 29.72),
    (13, "SENNA", 47.41)
]

def normaliser_pondérations(chevaux):
    total_inverse = sum(1 / c[2] for c in chevaux if c[2] > 0)
    return [(c[0], c[1], (1 / c[2]) / total_inverse) for c in chevaux if c[2] > 0]

def tirer_combinaison(chevaux_pondérés):
    pool = chevaux_pondérés[:]
    selection = []
    for _ in range(3):
        choix = random.choices(pool, weights=[c[2] for c in pool], k=1)[0]
        selection.append((choix[0], choix[1]))
        pool = [c for c in pool if c[0] != choix[0]]
    return tuple(selection)

def generer_predictions(chevaux_pondérés, nb=10):
    combinaisons = set()
    essais = 0
    while len(combinaisons) < nb and essais < nb * 10:
        combinaisons.add(tirer_combinaison(chevaux_pondérés))
        essais += 1
    return list(combinaisons)

def sauvegarder_csv(predictions, nom_fichier="predictions.csv"):
    try:
        with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Prédiction", "1er", "2e", "3e"])
            for i, p in enumerate(predictions, 1):
                writer.writerow([f"#{i}", f"{p[0][0]} - {p[0][1]}", f"{p[1][0]} - {p[1][1]}", f"{p[2][0]} - {p[2][1]}"])
        print(f"✅ Fichier sauvegardé : {nom_fichier}")
    except IOError as e:
        print(f"❌ Erreur lors de l'écriture du fichier : {e}")

def afficher_chevaux(chevaux):
    if not chevaux:
        print("⚠️ Aucun cheval enregistré.")
        return
    for c in chevaux:
        print(f"{c[0]:2d}: {c[1]} (cote: {c[2]})")

def cheval_existe(chevaux, num):
    return any(c[0] == num for c in chevaux)

def mode_live(chevaux):
    try:
        pondérés = normaliser_pondérations(chevaux)
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            predictions = generer_predictions(pondérés, 3)
            print("🔁 Prédictions en direct :")
            for i, p in enumerate(predictions, 1):
                print(f"#{i}: {p[0][1]} | {p[1][1]} | {p[2][1]}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("⏹️ Mode live arrêté.")

def menu():
    chevaux = chevaux_defaut[:]
    while True:
        print("\n📋 MENU")
        print("1. Afficher les chevaux")
        print("2. Ajouter un cheval")
        print("3. Supprimer un cheval")
        print("4. Générer prédictions")
        print("5. Mode prédiction en direct")
        print("6. Quitter")

        choix = input("👉 Choix : ").strip()
        if choix == "1":
            afficher_chevaux(chevaux)
        elif choix == "2":
            try:
                num = int(input("Numéro du cheval : "))
                if cheval_existe(chevaux, num):
                    print("⚠️ Numéro déjà utilisé.")
                    continue
                nom = input("Nom du cheval : ").strip()
                cote = float(input("Cote : "))
                if cote <= 0:
                    raise ValueError("Cote invalide.")
                chevaux.append((num, nom, cote))
                print("✅ Cheval ajouté.")
            except Exception as e:
                print(f"❌ Erreur : {e}")
        elif choix == "3":
            try:
                num = int(input("Numéro à supprimer : "))
                if not cheval_existe(chevaux, num):
                    print("❌ Ce cheval n'existe pas.")
                    continue
                chevaux = [c for c in chevaux if c[0] != num]
                print("✅ Supprimé.")
            except:
                print("❌ Entrée invalide.")
        elif choix == "4":
            try:
                if len(chevaux) < 3:
                    print("⚠️ Au moins 3 chevaux requis.")
                    continue
                n = int(input("Nombre de prédictions : "))
                if n <= 0:
                    raise ValueError("Nombre invalide")
                pondérés = normaliser_pondérations(chevaux)
                predictions = generer_predictions(pondérés, n)
                for i, (a, b, c) in enumerate(predictions, 1):
                    print(f"#{i}: 1er: {a[1]} | 2e: {b[1]} | 3e: {c[1]}")
                sauvegarder_csv(predictions)
            except Exception as e:
                print(f"❌ Erreur : {e}")
        elif choix == "5":
            mode_live(chevaux)
        elif choix == "6":
            print("👋 Fin du programme.")
            break
        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    print("🔮 Bienvenue dans le simulateur Tiercé")
    menu()
