import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "affinity.db")

QUESTIONS_CONFIG = [
    {
        "id_p": 80001, "id_t": 85001, "cible": 0, "dimension": "Taille",
        "texte_p": "Quelle est votre stature et taille exacte en centimètres ?",
        "texte_t": "Quelles sont vos tolérances de taille (stature) chez l'autre ?",
        "config": {"mode": "numeric", "unit": "cm", "min": 100, "max": 230, "step": 1, "default_min": 150, "default_max": 190, "dimension": "Taille"}
    },
    {
        "id_p": 80002, "id_t": 85002, "cible": 0, "dimension": "Poids",
        "texte_p": "Quel est votre poids de forme actuel en kilogrammes ?",
        "texte_t": "Quelles sont vos limites de poids de forme acceptées chez l'autre ?",
        "config": {"mode": "numeric", "unit": "kg", "min": 35, "max": 200, "step": 1, "default_min": 50, "default_max": 90, "dimension": "Poids"}
    },
    {
        "id_p": 80003, "id_t": 85003, "cible": 0, "dimension": "Silhouette",
        "texte_p": "Comment décrivez-vous votre morphologie et silhouette générale ?",
        "texte_t": "Quelles silhouettes appréciez-vous ou tolérez-vous chez l'autre ?",
        "config": {
            "mode": "select", "dimension": "Silhouette",
            "options": ["Mince / Fine", "Athlétique / Sportive", "Élancée", "Normale / Équilibrée", "Enrobée / Ronde", "Musclée", "Forte / Corpulente"]
        }
    },
    {
        "id_p": 80004, "id_t": 85004, "cible": 0, "dimension": "Tour de poitrine",
        "texte_p": "Quel est votre tour de poitrine (mensuration) en centimètres ?",
        "texte_t": "Quelles sont vos tolérances de tour de poitrine chez l'autre ?",
        "config": {"mode": "numeric", "unit": "cm", "min": 50, "max": 160, "step": 1, "default_min": 75, "default_max": 110, "dimension": "Tour de poitrine"}
    },
    {
        "id_p": 80005, "id_t": 85005, "cible": 2, "dimension": "Bonnet de poitrine",
        "texte_p": "Quelle est la taille de votre bonnet de poitrine ?",
        "texte_t": "Quels bonnets de poitrine appréciez-vous ou tolérez-vous chez une partenaire ?",
        "config": {
            "mode": "select", "dimension": "Bonnet de poitrine",
            "options": ["Bonnet A", "Bonnet B", "Bonnet C", "Bonnet D", "Bonnet E", "Bonnet F ou plus"]
        }
    },
    {
        "id_p": 80006, "id_t": 85006, "cible": 0, "dimension": "Tour de taille",
        "texte_p": "Quel est votre tour de taille (mensuration) en centimètres ?",
        "texte_t": "Quelles sont vos tolérances de tour de taille chez l'autre ?",
        "config": {"mode": "numeric", "unit": "cm", "min": 40, "max": 150, "step": 1, "default_min": 60, "default_max": 95, "dimension": "Tour de taille"}
    },
    {
        "id_p": 80007, "id_t": 85007, "cible": 0, "dimension": "Tour de hanches",
        "texte_p": "Quel est votre tour de hanches (mensuration) en centimètres ?",
        "texte_t": "Quelles sont vos tolérances de tour de hanches chez l'autre ?",
        "config": {"mode": "numeric", "unit": "cm", "min": 50, "max": 160, "step": 1, "default_min": 75, "default_max": 115, "dimension": "Tour de hanches"}
    },
    {
        "id_p": 80008, "id_t": 85008, "cible": 0, "dimension": "Pointure",
        "texte_p": "Quelle est votre pointure de chaussures habituelle ?",
        "texte_t": "Quelle plage de pointure tolérez-vous chez l'autre ?",
        "config": {"mode": "numeric", "unit": "", "min": 32, "max": 50, "step": 0.5, "default_min": 36, "default_max": 45, "dimension": "Pointure"}
    },
    {
        "id_p": 80009, "id_t": 85009, "cible": 0, "dimension": "Couleur des yeux",
        "texte_p": "Quelle est la couleur naturelle dominante de vos yeux ?",
        "texte_t": "Quelles couleurs d'yeux appréciez-vous particulièrement chez l'autre ?",
        "config": {
            "mode": "select", "dimension": "Couleur des yeux",
            "options": ["Bleus", "Verts", "Marrons", "Noirs", "Noisette", "Gris", "Vairons"]
        }
    },
    {
        "id_p": 80010, "id_t": 85010, "cible": 0, "dimension": "Couleur des cheveux",
        "texte_p": "Quelle est votre couleur de cheveux actuelle ?",
        "texte_t": "Quelles teintes de cheveux préférez-vous ou acceptez-vous chez l'autre ?",
        "config": {
            "mode": "select", "dimension": "Couleur des cheveux",
            "options": ["Bruns", "Noirs", "Châtains", "Blonds", "Roux", "Gris / Poivre et sel", "Blancs", "Chauve / Rasé", "Colorés / Fantaisie"]
        }
    },
    {
        "id_p": 80011, "id_t": 85011, "cible": 0, "dimension": "Longueur des cheveux",
        "texte_p": "Quelle est la longueur habituelle de votre chevelure ?",
        "texte_t": "Quelles longueurs de cheveux préférez-vous chez l'autre ?",
        "config": {
            "mode": "select", "dimension": "Longueur des cheveux",
            "options": ["Très courts / Rasés", "Courts", "Mi-longs", "Longs", "Très longs"]
        }
    },
    {
        "id_p": 80012, "id_t": 85012, "cible": 1, "dimension": "Pilosité faciale & Barbe",
        "texte_p": "Quel est votre style de pilosité faciale habituel (barbe/moustache) ?",
        "texte_t": "Quel type de barbe ou pilosité faciale préférez-vous chez un homme ?",
        "config": {
            "mode": "select", "dimension": "Pilosité faciale & Barbe",
            "options": ["Rasé de près", "Barbe de 3 jours", "Barbe courte soignée", "Barbe sculptée", "Barbe longue / Fournie", "Moustache", "Bouc"]
        }
    },
    {
        "id_p": 80013, "id_t": 85013, "cible": 0, "dimension": "Style vestimentaire & Allure",
        "texte_p": "Quel style vestimentaire et allure définissent le mieux votre quotidien ?",
        "texte_t": "Quels styles vestimentaires appréciez-vous chez votre partenaire ?",
        "config": {
            "mode": "select", "dimension": "Style vestimentaire & Allure",
            "options": [
                "Décontracté / Casual", "Élégant / Soigné", "Chic / Habillé", "Sportswear / Athlétique",
                "Urbain / Streetwear", "Bohème / Romantique", "Classique / Intemporel", "Rock / Alternatif",
                "Minimaliste", "Autre / Éclectique"
            ]
        }
    },
    {
        "id_p": 80014, "id_t": 85014, "cible": 0, "dimension": "Origines culturelles & géographiques",
        "texte_p": "Quelles sont vos principales origines culturelles et géographiques ?",
        "texte_t": "Quelles origines culturelles êtes-vous prêt(e) à découvrir chez l'autre ?",
        "config": {
            "mode": "select", "dimension": "Origines culturelles & géographiques",
            "options": [
                "Caucasien(ne) / Européen(ne)", "Méditerranéen(ne)", "Maghrébin(ne) / Nord-Africain(ne)",
                "Africain(ne) / Subsaharien(ne)", "Asiatique (Est-Asiatique)", "Sud-Asiatique / Indien(ne)",
                "Proche & Moyen-Orient", "Latino-Américain(ne) / Hispanique", "Métis(se) / Multiculturel(le)", "Autre"
            ]
        }
    },
    {
        "id_p": 80015, "id_t": 85015, "cible": 0, "dimension": "Rythme de vie",
        "texte_p": "Quel est votre rythme de vie prédominant au quotidien ?",
        "texte_t": "Quel rythme de vie recherchez-vous ou tolérez-vous chez l'autre ?",
        "config": {
            "mode": "select", "dimension": "Rythme de vie",
            "options": [
                "Matinal(e) & Lève-tôt", "Nocturne / Couche-tard", "Dynamique & Très actif",
                "Calme, Posé & Régulier", "Casanier & Tranquille", "Spontané & Imprévisible"
            ]
        }
    },
    {
        "id_p": 80016, "id_t": 85016, "cible": 0, "dimension": "Cadre de vie",
        "texte_p": "Dans quel cadre de vie vous épanouissez-vous le plus ?",
        "texte_t": "Quel cadre de vie partagé envisagez-vous avec l'autre ?",
        "config": {
            "mode": "select", "dimension": "Cadre de vie",
            "options": [
                "Grande métropole animée", "Ville moyenne à taille humaine", "Bord de mer / Littoral",
                "Campagne & Pleine nature", "Montagne"
            ]
        }
    }
]

def migrate():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Vérifier si config_reponses existe
    c.execute("PRAGMA table_info(questions)")
    cols = [col[1] for col in c.fetchall()]
    if "config_reponses" not in cols:
        print("Ajout de la colonne config_reponses...")
        c.execute("ALTER TABLE questions ADD COLUMN config_reponses TEXT")
        conn.commit()

    # 2. Supprimer les anciennes questions de classe 8
    c.execute("DELETE FROM questions WHERE classe = 8")
    conn.commit()

    # 3. Insérer les nouvelles questions avec Thématique = Identité, Sujet = Identité
    for item in QUESTIONS_CONFIG:
        cfg_json = json.dumps(item["config"], ensure_ascii=False)
        # Type P
        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet, config_reponses)
            VALUES (?, 1, ?, 8, 'Identité', 'Identité', 'P', ?, 8, 8, ?)
        """, (item["id_p"], item["cible"], item["texte_p"], cfg_json))

        # Type T
        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet, config_reponses)
            VALUES (?, 1, ?, 8, 'Identité', 'Identité', 'T', ?, 8, 8, ?)
        """, (item["id_t"], item["cible"], item["texte_t"], cfg_json))

    conn.commit()
    cnt = c.execute("SELECT count(*) FROM questions WHERE classe = 8").fetchone()[0]
    total = c.execute("SELECT count(*) FROM questions").fetchone()[0]
    print(f"Succès : {cnt} questions de classe 8 insérées. Total des questions dans la base : {total}")
    conn.close()

if __name__ == "__main__":
    migrate()
