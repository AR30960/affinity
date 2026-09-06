import sqlite3
import json

def migrate():
    conn = sqlite3.connect('affinity.db')
    c = conn.cursor()

    # Trouver le pack STANDARD
    c.execute("SELECT id FROM question_packs WHERE code = 'STANDARD'")
    row = c.fetchone()
    pack_id = row[0] if row else 1

    # Liste des 14 caractéristiques d'identité
    # (sujet, thematique, mode, unit, min, max, step, options, texte_self, texte_partner)
    features = [
        (
            "Stature & Taille (cm)",
            "Morphologie & Mensurations",
            "numeric", "cm", 100, 230, 1, [],
            "Quelle est votre taille exacte en centimètres ?",
            "Quelle taille tolérez-vous chez votre partenaire ?"
        ),
        (
            "Corpulence & Poids de forme",
            "Morphologie & Mensurations",
            "numeric", "kg", 35, 200, 1, [],
            "Quel est votre poids de forme habituel en kilogrammes ?",
            "Quel poids tolérez-vous chez votre partenaire ?"
        ),
        (
            "Silhouette & Corpulence",
            "Morphologie & Mensurations",
            "select", "", 0, 0, 0,
            ["Mince / Fine", "Athlétique / Sportive", "Élancée", "Normale / Équilibrée", "Enrobée / Ronde", "Musclée", "Forte / Corpulente"],
            "Quelle silhouette correspond le mieux à votre morphologie ?",
            "Quelles silhouettes tolérez-vous ou préférez-vous chez votre partenaire ?"
        ),
        (
            "Tour de poitrine",
            "Morphologie & Mensurations",
            "numeric", "cm", 50, 160, 1, [],
            "Quel est votre tour de poitrine (ou carrure de buste) en cm ?",
            "Quel tour de poitrine ou carrure tolérez-vous chez l'autre ?"
        ),
        (
            "Tour de taille",
            "Morphologie & Mensurations",
            "numeric", "cm", 40, 150, 1, [],
            "Quel est votre tour de taille en cm ?",
            "Quel tour de taille tolérez-vous chez votre partenaire ?"
        ),
        (
            "Tour de hanches",
            "Morphologie & Mensurations",
            "numeric", "cm", 50, 160, 1, [],
            "Quel est votre tour de hanches en cm ?",
            "Quel tour de hanches tolérez-vous chez votre partenaire ?"
        ),
        (
            "Pointure de chaussures",
            "Morphologie & Mensurations",
            "numeric", "", 32, 50, 0.5, [],
            "Quelle est votre pointure de chaussures habituelle ?",
            "Quelle pointure tolérez-vous chez votre partenaire ?"
        ),
        (
            "Couleur des yeux",
            "Allure & Style",
            "select", "", 0, 0, 0,
            ["Bleus", "Verts", "Marrons", "Noirs", "Noisette", "Gris", "Vairons"],
            "Quelle est la couleur naturelle de vos yeux ?",
            "Quelles couleurs d'yeux tolérez-vous ou préférez-vous chez l'autre ?"
        ),
        (
            "Couleur des cheveux",
            "Allure & Style",
            "select", "", 0, 0, 0,
            ["Bruns", "Noirs", "Châtains", "Blonds", "Roux", "Gris / Poivre et sel", "Blancs", "Chauve / Rasé", "Colorés / Fantaisie"],
            "Quelle est la couleur dominante de votre chevelure ?",
            "Quelles teintes de cheveux tolérez-vous chez votre partenaire ?"
        ),
        (
            "Longueur des cheveux",
            "Allure & Style",
            "select", "", 0, 0, 0,
            ["Très courts / Rasés", "Courts", "Mi-longs", "Longs", "Très longs"],
            "Quelle est la longueur actuelle de vos cheveux ?",
            "Quelles longueurs de cheveux tolérez-vous chez votre partenaire ?"
        ),
        (
            "Style vestimentaire & Allure",
            "Allure & Style",
            "select", "", 0, 0, 0,
            ["Décontracté / Casual", "Élégant / Soigné", "Chic / Habillé", "Sportswear / Athlétique", "Urbain / Streetwear", "Bohème / Romantique", "Classique / Intemporel", "Rock / Alternatif", "Minimaliste", "Autre / Éclectique"],
            "Quel style vestimentaire et quelle allure vous caractérisent le plus ?",
            "Quels styles vestimentaires tolérez-vous chez votre partenaire ?"
        ),
        (
            "Origines culturelles & géographiques",
            "Origines & Culture",
            "select", "", 0, 0, 0,
            ["Caucasien(ne) / Européen(ne)", "Méditerranéen(ne)", "Maghrébin(ne) / Nord-Africain(ne)", "Africain(ne) / Subsaharien(ne)", "Asiatique (Est-Asiatique)", "Sud-Asiatique / Indien(ne)", "Proche & Moyen-Orient", "Latino-Américain(ne) / Hispanique", "Métis(se) / Multiculturel(le)", "Autre"],
            "Quelles sont vos origines culturelles et géographiques prédominantes ?",
            "Quelles origines culturelles tolérez-vous ou recherchez-vous chez l'autre ?"
        ),
        (
            "Rythme de vie",
            "Mode & Cadre de vie",
            "select", "", 0, 0, 0,
            ["Matinal(e) & Lève-tôt", "Nocturne / Couche-tard", "Dynamique & Très actif", "Calme, Posé & Régulier", "Casanier & Tranquille", "Spontané & Imprévisible"],
            "Comment décririez-vous votre rythme de vie au quotidien ?",
            "Quels rythmes de vie tolérez-vous chez votre partenaire ?"
        ),
        (
            "Cadre de vie",
            "Mode & Cadre de vie",
            "select", "", 0, 0, 0,
            ["Grande métropole animée", "Ville moyenne à taille humaine", "Bord de mer / Littoral", "Campagne & Pleine nature", "Montagne"],
            "Dans quel cadre de vie vous épanouissez-vous le mieux ?",
            "Quels cadres de vie tolérez-vous pour votre quotidien commun ?"
        )
    ]

    # Supprimer les anciennes questions de classe 0 qui étaient en type M ou G
    c.execute("DELETE FROM questions WHERE classe = 0")

    # Réinsérer les questions propres de Type P (Précis) et Type T (Tolérance)
    for feat in features:
        sujet, thematique, mode, unit, v_min, v_max, step, options, texte_self, texte_partner = feat
        # 1. Question Type P (pour + sur vous)
        c.execute("""
            INSERT INTO questions (pack_id, cible, classe, thematique, sujet, type, texte)
            VALUES (?, 0, 0, ?, ?, 'P', ?)
        """, (pack_id, thematique, sujet, texte_self))

        # 2. Question Type T (pour + sur l'autre)
        c.execute("""
            INSERT INTO questions (pack_id, cible, classe, thematique, sujet, type, texte)
            VALUES (?, 0, 0, ?, ?, 'T', ?)
        """, (pack_id, thematique, sujet, texte_partner))

    conn.commit()

    c.execute("SELECT count(*), type FROM questions WHERE classe = 0 GROUP BY type")
    print("Nouvelles questions de classe 0 dans la base :")
    for r in c.fetchall():
        print(f"  Type {r[1]}: {r[0]} questions")

    conn.close()

if __name__ == '__main__':
    migrate()
