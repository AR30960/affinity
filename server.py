import http.server
import socketserver
import json
import sqlite3
import os
import sys
import urllib.parse
import math
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

PORT = int(os.environ.get("PORT", 8765))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("AFFINITY_DB_PATH", os.path.join(BASE_DIR, "affinity.db"))
STATIC_DIR = os.path.join(BASE_DIR, "frontend")

CITY_COORDINATES = {
    "paris": (48.8566, 2.3522),
    "lyon": (45.7640, 4.8357),
    "marseille": (43.2965, 5.3698),
    "toulouse": (43.6047, 1.4442),
    "nice": (43.7102, 7.2620),
    "nantes": (47.2184, -1.5536),
    "strasbourg": (48.5734, 7.7521),
    "montpellier": (43.6108, 3.8767),
    "bordeaux": (44.8378, -0.5792),
    "lille": (50.6292, 3.0573),
    "rennes": (48.1173, -1.6778),
    "reims": (49.2583, 4.0317),
    "toulon": (43.1242, 5.9280),
    "saint-etienne": (45.4397, 4.3872),
    "le havre": (49.4944, 0.1079),
    "grenoble": (45.1885, 5.7245),
    "dijon": (47.3220, 5.0415),
    "angers": (47.4784, -0.5632),
    "villeurbanne": (45.7719, 4.8902),
    "nimes": (43.8367, 4.3601),
    "clermont-ferrand": (45.7772, 3.0870),
    "aix-en-provence": (43.5297, 5.4474),
    "brest": (48.3904, -4.4861),
    "tours": (47.3941, 0.6848),
    "amiens": (49.8941, 2.2957),
    "annecy": (45.8992, 6.1294),
    "metz": (49.1193, 6.1757),
    "besancon": (47.2378, 6.0241),
    "perpignan": (42.6887, 2.8948),
    "orleans": (47.9029, 1.9093),
    "caen": (49.1829, -0.3707),
    "mulhouse": (47.7508, 7.3359),
    "rouen": (49.4432, 1.0999),
    "nancy": (48.6921, 6.1844),
    "avignon": (43.9493, 4.8055),
    "poitiers": (46.5802, 0.3404),
    "la rochelle": (46.1603, -1.1511),
    "pau": (43.2951, -0.3708),
    "calais": (50.9513, 1.8587),
    "cannes": (43.5528, 7.0174),
    "antibes": (43.5804, 7.1251),
    "valence": (44.9333, 4.8917),
    "bruxelles": (50.8503, 4.3517),
    "geneve": (46.2044, 6.1432),
    "lausanne": (46.5197, 6.6323),
    "luxembourg": (49.6116, 6.1319),
    "monaco": (43.7384, 7.4246)
}

def calculate_distance_km(city1, city2):
    if not city1 or not city2:
        return None
    c1 = city1.strip().lower()
    c2 = city2.strip().lower()
    if c1 == c2:
        return 0
    
    coord1 = None
    coord2 = None
    for name, pos in CITY_COORDINATES.items():
        if name in c1 or c1 in name:
            coord1 = pos
            break
    for name, pos in CITY_COORDINATES.items():
        if name in c2 or c2 in name:
            coord2 = pos
            break
            
    if not coord1 or not coord2:
        # Fallback estimation déterministe
        return (abs(hash(c1) - hash(c2)) % 420) + 60

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return int(round(6371 * c))

ALLOWED_COUNTRIES = ["France", "UE", "Hors UE"]

CHOIX_RECHERCHE = [
    "Échanges et Amitié",
    "Recherche d’un(e) partenaire",
    "Recherche d'un(e) partenaire",
    "Plus si affinité",
    "Je ne sais pas vraiment"
]

CHOIX_SITUATION_FAMILLE = [
    "Célibataire",
    "En couple",
    "Marié(e)",
    "Pacsé(e)",
    "Séparé(e)",
    "Divorcé(e)",
    "Veuf / Veuve",
    "Compliqué",
    "Autre",
    "Non renseigné"
]

IDENTITY_QUESTIONS_CONFIG = {
    "Stature & Taille (cm)": {
        "mode": "numeric", "unit": "cm", "min": 100, "max": 230, "step": 1,
        "default_min": 150, "default_max": 190, "label": "Taille en centimètres"
    },
    "Taille": {
        "mode": "numeric", "unit": "cm", "min": 100, "max": 230, "step": 1,
        "default_min": 150, "default_max": 190, "label": "Taille en centimètres"
    },
    "Corpulence & Poids de forme": {
        "mode": "numeric", "unit": "kg", "min": 35, "max": 200, "step": 1,
        "default_min": 50, "default_max": 90, "label": "Poids de forme"
    },
    "Poids": {
        "mode": "numeric", "unit": "kg", "min": 35, "max": 200, "step": 1,
        "default_min": 50, "default_max": 90, "label": "Poids de forme"
    },
    "Silhouette & Corpulence": {
        "mode": "select", "options": [
            "Mince / Fine", "Athlétique / Sportive", "Élancée", "Normale / Équilibrée",
            "Enrobée / Ronde", "Musclée", "Forte / Corpulente"
        ], "label": "Silhouette et corpulence générale"
    },
    "Silhouette": {
        "mode": "select", "options": [
            "Mince / Fine", "Athlétique / Sportive", "Élancée", "Normale / Équilibrée",
            "Enrobée / Ronde", "Musclée", "Forte / Corpulente"
        ], "label": "Silhouette et corpulence générale"
    },
    "Tour de poitrine": {
        "mode": "numeric", "unit": "cm", "min": 50, "max": 160, "step": 1,
        "default_min": 75, "default_max": 110, "label": "Tour de poitrine"
    },
    "Tour de taille": {
        "mode": "numeric", "unit": "cm", "min": 40, "max": 150, "step": 1,
        "default_min": 60, "default_max": 95, "label": "Tour de taille"
    },
    "Tour de hanches": {
        "mode": "numeric", "unit": "cm", "min": 50, "max": 160, "step": 1,
        "default_min": 75, "default_max": 115, "label": "Tour de hanches"
    },
    "Pointure de chaussures": {
        "mode": "numeric", "unit": "", "min": 32, "max": 50, "step": 0.5,
        "default_min": 36, "default_max": 44, "label": "Pointure de chaussures"
    },
    "Pointure": {
        "mode": "numeric", "unit": "", "min": 32, "max": 50, "step": 0.5,
        "default_min": 36, "default_max": 44, "label": "Pointure de chaussures"
    },
    "Couleur des yeux": {
        "mode": "select", "options": [
            "Bleus", "Verts", "Marrons", "Noirs", "Noisette", "Gris", "Vairons"
        ], "label": "Couleur naturelle des yeux"
    },
    "Couleur des cheveux": {
        "mode": "select", "options": [
            "Bruns", "Noirs", "Châtains", "Blonds", "Roux",
            "Gris / Poivre et sel", "Blancs", "Chauve / Rasé", "Colorés / Fantaisie"
        ], "label": "Couleur dominante des cheveux"
    },
    "Longueur des cheveux": {
        "mode": "select", "options": [
            "Très courts / Rasés", "Courts", "Mi-longs", "Longs", "Très longs"
        ], "label": "Longueur de la chevelure"
    },
    "Style vestimentaire & Allure": {
        "mode": "select", "options": [
            "Décontracté / Casual", "Élégant / Soigné", "Chic / Habillé", "Sportswear / Athlétique",
            "Urbain / Streetwear", "Bohème / Romantique", "Classique / Intemporel", "Rock / Alternatif",
            "Minimaliste", "Autre / Éclectique"
        ], "label": "Style vestimentaire et allure"
    },
    "Style vestimentaire": {
        "mode": "select", "options": [
            "Décontracté / Casual", "Élégant / Soigné", "Chic / Habillé", "Sportswear / Athlétique",
            "Urbain / Streetwear", "Bohème / Romantique", "Classique / Intemporel", "Rock / Alternatif",
            "Minimaliste", "Autre / Éclectique"
        ], "label": "Style vestimentaire et allure"
    },
    "Origines culturelles & géographiques": {
        "mode": "select", "options": [
            "Caucasien(ne) / Européen(ne)", "Méditerranéen(ne)", "Maghrébin(ne) / Nord-Africain(ne)",
            "Africain(ne) / Subsaharien(ne)", "Asiatique (Est-Asiatique)", "Sud-Asiatique / Indien(ne)",
            "Proche & Moyen-Orient", "Latino-Américain(ne) / Hispanique", "Métis(se) / Multiculturel(le)", "Autre"
        ], "label": "Origines culturelles et géographiques"
    },
    "Origines culturelles": {
        "mode": "select", "options": [
            "Caucasien(ne) / Européen(ne)", "Méditerranéen(ne)", "Maghrébin(ne) / Nord-Africain(ne)",
            "Africain(ne) / Subsaharien(ne)", "Asiatique (Est-Asiatique)", "Sud-Asiatique / Indien(ne)",
            "Proche & Moyen-Orient", "Latino-Américain(ne) / Hispanique", "Métis(se) / Multiculturel(le)", "Autre"
        ], "label": "Origines culturelles et géographiques"
    },
    "Rythme de vie": {
        "mode": "select", "options": [
            "Matinal(e) & Lève-tôt", "Nocturne / Couche-tard", "Dynamique & Très actif",
            "Calme, Posé & Régulier", "Casanier & Tranquille", "Spontané & Imprévisible"
        ], "label": "Rythme de vie au quotidien"
    },
    "Cadre de vie": {
        "mode": "select", "options": [
            "Grande métropole animée", "Ville moyenne à taille humaine", "Bord de mer / Littoral",
            "Campagne & Pleine nature", "Montagne"
        ], "label": "Cadre de vie privilégié"
    }
}

FRENCH_DEPARTMENTS = {
    "01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence", "05": "Hautes-Alpes",
    "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes", "09": "Ariège", "10": "Aube",
    "11": "Aude", "12": "Aveyron", "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal",
    "16": "Charente", "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "2A": "Corse-du-Sud",
    "2B": "Haute-Corse", "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse", "24": "Dordogne",
    "25": "Doubs", "26": "Drôme", "27": "Eure", "28": "Eure-et-Loir", "29": "Finistère",
    "30": "Gard", "31": "Haute-Garonne", "32": "Gers", "33": "Gironde", "34": "Hérault",
    "35": "Ille-et-Vilaine", "36": "Indre", "37": "Indre-et-Loire", "38": "Isère", "39": "Jura",
    "40": "Landes", "41": "Loir-et-Cher", "42": "Loire", "43": "Haute-Loire", "44": "Loire-Atlantique",
    "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne", "48": "Lozère", "49": "Maine-et-Loire",
    "50": "Manche", "51": "Marne", "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle",
    "55": "Meuse", "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord",
    "60": "Oise", "61": "Orne", "62": "Pas-de-Calais", "63": "Puy-de-Dôme", "64": "Pyrénées-Atlantiques",
    "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales", "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône",
    "70": "Haute-Saône", "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie", "74": "Haute-Savoie",
    "75": "Paris", "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines", "79": "Deux-Sèvres",
    "80": "Somme", "81": "Tarn", "82": "Tarn-et-Garonne", "83": "Var", "84": "Vaucluse",
    "85": "Vendée", "86": "Vienne", "87": "Haute-Vienne", "88": "Vosges", "89": "Yonne",
    "90": "Territoire de Belfort", "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis", "94": "Val-de-Marne",
    "95": "Val-d'Oise", "971": "Guadeloupe", "972": "Martinique", "973": "Guyane", "974": "La Réunion", "976": "Mayotte"
}

FRENCH_CITIES_DEPTS = {
    "paris": "75", "marseille": "13", "lyon": "69", "toulouse": "31", "nice": "06",
    "nantes": "44", "montpellier": "34", "strasbourg": "67", "bordeaux": "33", "lille": "59",
    "rennes": "35", "reims": "51", "toulon": "83", "saint-etienne": "42", "le havre": "76",
    "grenoble": "38", "dijon": "21", "angers": "49", "nimes": "30", "villeurbanne": "69",
    "clermont-ferrand": "63", "le mans": "72", "aix-en-provence": "13", "brest": "29", "tours": "37",
    "amiens": "80", "limoges": "87", "annecy": "74", "perpignan": "66", "boulogne-billancourt": "92",
    "metz": "57", "besancon": "25", "orleans": "45", "saint-denis": "93", "argenteuil": "95",
    "rouen": "76", "montreuil": "93", "mulhouse": "68", "caen": "14", "nancy": "54",
    "tourcoing": "59", "roubaix": "59", "nanterre": "92", "vitry-sur-seine": "94", "creteil": "94",
    "avignon": "84", "poitiers": "86", "courbevoie": "92", "versailles": "78", "colombes": "92",
    "asnieres-sur-seine": "92", "aulnay-sous-bois": "93", "saint-maur-des-fosses": "94", "rueil-malmaison": "92",
    "champigny-sur-marne": "94", "aubervilliers": "93", "antibes": "06", "la rochelle": "17", "cannes": "06",
    "calais": "62", "saint-nazaire": "44", "colmar": "68", "dunkerque": "59", "bourges": "18",
    "valence": "26", "quimper": "29", "ajaccio": "2A", "bastia": "2B", "cayenne": "973",
    "fort-de-france": "972", "saint-denis-de-la-reunion": "974", "mamoudzou": "976",
    "neuilly-sur-seine": "92", "levallois-perret": "92", "issy-les-moulineaux": "92", "antony": "92",
    "clichy": "92", "pantin": "93", "bobigny": "93", "bondy": "93", "fontenay-sous-bois": "94",
    "ivry-sur-seine": "94", "villejuif": "94", "maisons-alfort": "94", "cergy": "95", "sarcelles": "95",
    "evry": "91", "corbeil-essonnes": "91", "massy": "91", "meaux": "77", "cheles": "77", "melun": "77",
    "pau": "64", "bayonne": "64", "tarbes": "65", "montauban": "82", "albi": "81", "rodez": "12",
    "carcassonne": "11", "narbonne": "11", "beziers": "34", "sete": "34", "arles": "13",
    "hyeres": "83", "frejus": "83", "grasse": "06", "cagnes-sur-mer": "06", "gap": "05", "digne-les-bains": "04",
    "chambery": "73", "vienne": "38", "roanne": "42", "bourg-en-bresse": "01",
    "auxerre": "89", "nevers": "58", "macon": "71", "chalon-sur-saone": "71", "belfort": "90",
    "vesoul": "70", "lons-le-saunier": "39", "dole": "39", "epinal": "88", "thionville": "57",
    "bar-le-duc": "55", "verdun": "55", "charleville-mezieres": "08", "troyes": "10", "chalons-en-champagne": "51",
    "chaumont": "52", "beauvais": "60", "compiegne": "60", "creil": "60", "laon": "02", "saint-quentin": "02",
    "soissons": "02", "arras": "62", "boulogne-sur-mer": "62", "lens": "62", "douai": "59", "valenciennes": "59",
    "evreux": "27", "dieppe": "76", "cherbourg": "50", "saint-lo": "50", "alencon": "61",
    "chartres": "28", "dreux": "28", "blois": "41", "chateauroux": "36",
    "saint-brieuc": "22", "lorient": "56", "vannes": "56", "saint-malo": "35", "laval": "53",
    "cholet": "49", "la roche-sur-yon": "85", "niort": "79", "angouleme": "16", "saintes": "17",
    "chatellerault": "86", "gueret": "23", "tulle": "19", "brive-la-gaillarde": "19", "perigueux": "24",
    "bergerac": "24", "agen": "47", "villeneuve-sur-lot": "47", "mont-de-marsan": "40", "dax": "40", "auch": "32"
}

def extract_dept_code(dept_str):
    if not dept_str:
        return None
    s = str(dept_str).strip().upper()
    import re, unicodedata
    m = re.match(r'^(\d{2,3}|2A|2B)', s)
    if m and m.group(1) in FRENCH_DEPARTMENTS:
        return m.group(1)
    def clean(t):
        return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')
    c_s = clean(s)
    for code, name in FRENCH_DEPARTMENTS.items():
        if clean(name) == c_s or clean(f"{code} - {name}") == c_s or clean(f"{name} ({code})") == c_s:
            return code
    return None

def validate_france_dept_and_commune(dept_str, commune_str):
    """Vérifie la cohérence entre le département français et la commune renseignée."""
    if not dept_str or not str(dept_str).strip():
        return False, "Le département français est obligatoire lorsque le pays est France.", None
    
    code = extract_dept_code(dept_str)
    if not code or code not in FRENCH_DEPARTMENTS:
        return False, f"Le département '{dept_str}' n'est pas un département français reconnu (sélectionnez un département de 01 à 976).", None
    
    canonical_dept = f"{code} - {FRENCH_DEPARTMENTS[code]}"
    
    if not commune_str or not str(commune_str).strip():
        return True, "", canonical_dept
    
    import re, unicodedata
    def clean(t):
        return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn')
    
    c_clean = clean(str(commune_str).strip())
    
    # Vérification 1 : code postal dans la commune
    cp_match = re.search(r'\b(\d{5})\b', str(commune_str))
    if cp_match:
        cp = cp_match.group(1)
        cp_dept = cp[:3] if cp.startswith(('97', '98')) else cp[:2]
        if cp_dept.startswith('20'):
            if code not in ('2A', '2B'):
                return False, f"Incohérence détectée : le code postal {cp} correspond à la Corse (2A/2B), or vous avez sélectionné '{canonical_dept}'.", canonical_dept
        elif cp_dept != code:
            expected_name = FRENCH_DEPARTMENTS.get(cp_dept, cp_dept)
            return False, f"Incohérence détectée : le code postal {cp} correspond au département {cp_dept} ({expected_name}), or vous avez sélectionné '{canonical_dept}'.", canonical_dept

    # Vérification 2 : Ville répertoriée dans le référentiel des communes
    for city_key, city_dept in FRENCH_CITIES_DEPTS.items():
        if c_clean == city_key or c_clean.startswith(city_key + " ") or c_clean.endswith(" " + city_key):
            if city_dept != code:
                expected_dept_name = FRENCH_DEPARTMENTS.get(city_dept, city_dept)
                return False, f"Incohérence détectée : la commune '{commune_str.strip()}' est rattachée au département {city_dept} ({expected_dept_name}), or vous avez sélectionné '{canonical_dept}'.", canonical_dept
            break

    return True, "", canonical_dept

def is_valid_country(country_name):
    if not country_name or not str(country_name).strip():
        return True, ""
    c_clean = str(country_name).strip()
    import unicodedata
    def strip_accents(text):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    c_norm = strip_accents(c_clean.lower())
    for rc in ALLOWED_COUNTRIES:
        if strip_accents(rc.lower()) == c_norm:
            return True, rc
    return False, None

def validate_birth_date_and_age(birth_date_str):
    if not birth_date_str or not str(birth_date_str).strip():
        return None, None
    s = str(birth_date_str).strip()
    try:
        if "/" in s:
            p = s.split("/")
            d, m, y = int(p[0]), int(p[1]), int(p[2])
            bdate = datetime(y, m, d).date()
        else:
            bdate = datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None, "Format de date de naissance invalide (attendu AAAA-MM-JJ ou JJ/MM/AAAA)."
    
    today = datetime.now().date()
    if bdate > today:
        return None, "La date de naissance ne peut pas être située dans le futur."
    
    age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
    if age < 18:
        return age, "Âge minimum requis : 18 ans pour accéder à la plateforme Affinity."
    if age > 120:
        return age, "Date de naissance incohérente (âge calculé supérieur à 120 ans)."
    
    return age, None

def hash_password(password: str, salt: str = None):
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return salt, hashed

def verify_password(password: str, salt: str, password_hash: str) -> bool:
    if not salt or not password_hash or not password:
        return False
    calc = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return secrets.compare_digest(calc, password_hash)

def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return "adresse e-mail inconnue"
    parts = email.strip().split("@")
    user, domain = parts[0], parts[1]
    if len(user) <= 2:
        masked_user = user[0] + "*"
    else:
        masked_user = user[0] + "*" * min(len(user) - 2, 6) + user[-1]
    return f"{masked_user}@{domain}"

def create_session(profile_id: int) -> str:
    token = secrets.token_hex(32)
    expires = datetime.now(timezone.utc) + timedelta(days=30)
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO sessions (token, profile_id, expires_at) VALUES (?, ?, ?)",
              (token, profile_id, expires.isoformat()))
    conn.commit()
    conn.close()
    return token

def get_session_profile(token: str):
    if not token:
        return None
    conn = get_db()
    c = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()
    row = c.execute("""
        SELECT p.id, p.pseudo, p.code_profil, p.role, p.avatar, p.email
        FROM sessions s
        JOIN profiles p ON s.profile_id = p.id
        WHERE s.token = ? AND s.expires_at > ?
    """, (token, now_str)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def delete_session(token: str):
    if not token:
        return
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Table des profils (Pseudo)
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL UNIQUE,
            code_profil TEXT UNIQUE,
            avatar TEXT DEFAULT 'user',
            role TEXT DEFAULT 'guest', -- 'admin', 'subscriber', 'guest'
            password_hash TEXT,
            salt TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table des sessions actives
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            profile_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        )
    ''')
    conn.commit()
    
    # Migration automatique pour ajouter les colonnes role, code_profil, password_hash, salt, email si elles n'existent pas
    c.execute("PRAGMA table_info(profiles)")
    existing_cols = [col["name"] for col in c.fetchall()]
    if "role" not in existing_cols:
        c.execute("ALTER TABLE profiles ADD COLUMN role TEXT DEFAULT 'guest'")
        conn.commit()
    if "code_profil" not in existing_cols:
        c.execute("ALTER TABLE profiles ADD COLUMN code_profil TEXT")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_profiles_code_profil ON profiles(code_profil)")
        conn.commit()
    if "password_hash" not in existing_cols:
        c.execute("ALTER TABLE profiles ADD COLUMN password_hash TEXT")
        conn.commit()
    if "salt" not in existing_cols:
        c.execute("ALTER TABLE profiles ADD COLUMN salt TEXT")
        conn.commit()
    if "email" not in existing_cols:
        c.execute("ALTER TABLE profiles ADD COLUMN email TEXT")
        conn.commit()

    # Table des demandes de réinitialisation de mot de passe oublié
    c.execute('''
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            reset_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0,
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        )
    ''')
    conn.commit()

    # Initialisation des rôles par défaut et codes profils initiaux
    # Administrateur principal (pseudo ar30960, code_profil ADM-1)
    c.execute("UPDATE profiles SET pseudo = 'ar30960', role = 'admin', code_profil = 'ADM-1' WHERE id = 1")
    c.execute("UPDATE profiles SET role = 'subscriber' WHERE id = 2 AND (role IS NULL OR role = 'guest')")
    c.execute("UPDATE profiles SET role = 'guest' WHERE id IN (3, 4) AND (role IS NULL)")
    
    # Mot de passe par défaut pour l'administrateur ar30960 (Admin2026!)
    c.execute("SELECT id, password_hash, salt FROM profiles WHERE id = 1")
    admin_row = c.fetchone()
    if admin_row and not admin_row["password_hash"]:
        s, h = hash_password("Admin2026!")
        c.execute("UPDATE profiles SET salt = ?, password_hash = ? WHERE id = 1", (s, h))
        conn.commit()

    # Mots de passe initiaux pour les autres profils existants (Affinity2026!)
    c.execute("SELECT id, password_hash FROM profiles WHERE id > 1 AND (password_hash IS NULL OR password_hash = '')")
    for row in c.fetchall():
        s, h = hash_password("Affinity2026!")
        c.execute("UPDATE profiles SET salt = ?, password_hash = ? WHERE id = ?", (s, h, row["id"]))
    conn.commit()
    
    # Génération des codes profils manquants (ADM-x pour admin, AFF-x pour les autres)
    c.execute("SELECT id, role, code_profil FROM profiles")
    all_profs = c.fetchall()
    for prof in all_profs:
        if not prof["code_profil"]:
            prefix = "ADM" if prof["role"] == "admin" else "AFF"
            c.execute("UPDATE profiles SET code_profil = ? WHERE id = ?", (f"{prefix}-{prof['id']}", prof["id"]))
    conn.commit()
    
    # Migration du type de question 'MULTI' vers 'M'
    c.execute("UPDATE questions SET type = 'M' WHERE type = 'MULTI'")
    conn.commit()
    
    # Table des fiches d'identité détaillées (Facultative à la saisie, mais obligatoire pour le calcul d'affinité)
    c.execute('''
        CREATE TABLE IF NOT EXISTS identity_cards (
            profile_id INTEGER PRIMARY KEY,
            nom TEXT,
            prenom TEXT,
            date_naissance TEXT,
            sexe INTEGER DEFAULT 0, -- 0: Tous / Non spécifié, 1: Homme, 2: Femme
            ville TEXT,
            statut TEXT,
            bio TEXT,
            taille INTEGER, -- en cm
            poids INTEGER, -- en kg
            pointure REAL,
            mensurations TEXT,
            origines TEXT,
            couleur_cheveux TEXT,
            style TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
        )
    ''')
    
    # Migration automatique des colonnes morphologiques, d'adresse et de style pour identity_cards
    c.execute("PRAGMA table_info(identity_cards)")
    id_cols = [col["name"] for col in c.fetchall()]
    for col_name, col_type in [
        ("taille", "INTEGER"),
        ("poids", "INTEGER"),
        ("pointure", "REAL"),
        ("mensurations", "TEXT"),
        ("tour_poitrine", "REAL"),
        ("tour_taille", "REAL"),
        ("tour_hanches", "REAL"),
        ("origines", "TEXT"),
        ("couleur_cheveux", "TEXT"),
        ("style", "TEXT"),
        ("aime_chez_moi", "TEXT"),
        ("aime_pas_chez_moi", "TEXT"),
        ("pays_naissance", "TEXT"),
        ("habite_pays", "TEXT"),
        ("habite_region_dept", "TEXT"),
        ("habite_commune", "TEXT"),
        ("travail_pays", "TEXT"),
        ("travail_region_dept", "TEXT"),
        ("travail_commune", "TEXT"),
        ("situation_famille", "TEXT"),
        ("recherche_de", "TEXT")
    ]:
        if col_name not in id_cols:
            c.execute(f"ALTER TABLE identity_cards ADD COLUMN {col_name} {col_type}")
            conn.commit()

    # Migration automatique des données existantes : ville vers habite_commune
    c.execute("UPDATE identity_cards SET habite_commune = ville WHERE (habite_commune IS NULL OR habite_commune = '') AND (ville IS NOT NULL AND ville != '')")
    c.execute("UPDATE identity_cards SET habite_pays = 'France' WHERE habite_commune IS NOT NULL AND habite_commune != '' AND (habite_pays IS NULL OR habite_pays = '')")
    conn.commit()

    # Vérifier l'existence de config_reponses et n_quest_lie dans la table questions
    c.execute("PRAGMA table_info(questions)")
    q_cols = [col["name"] for col in c.fetchall()]
    if "config_reponses" not in q_cols:
        c.execute("ALTER TABLE questions ADD COLUMN config_reponses TEXT")
        conn.commit()
    if "n_quest_lie" not in q_cols:
        c.execute("ALTER TABLE questions ADD COLUMN n_quest_lie INTEGER DEFAULT 0")
        conn.commit()

    # Amorçage des questions de classe 8 (Identité) sans sujets fictifs (Thematique=Identite, Sujet=Identite)
    c.execute("SELECT count(*) as nb FROM questions WHERE classe = 8")
    if c.fetchone()["nb"] == 0:
        import json
        from migrate_classe8_config_reponses import QUESTIONS_CONFIG
        for item in QUESTIONS_CONFIG:
            cfg_json = json.dumps(item["config"], ensure_ascii=False)
            c.execute("""
                INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet, config_reponses)
                VALUES (?, 1, ?, 8, 'Identité', 'Identité', 'P', ?, 8, 8, ?)
            """, (item["id_p"], item["cible"], item["texte_p"], cfg_json))
            c.execute("""
                INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet, config_reponses)
                VALUES (?, 1, ?, 8, 'Identité', 'Identité', 'T', ?, 8, 8, ?)
            """, (item["id_t"], item["cible"], item["texte_t"], cfg_json))
        conn.commit()

    # Tables dédiées aux réponses d'identité : "+ sur vous" (soi) et "+ sur l'autre" (critères & tolérances)
    c.execute('''
        CREATE TABLE IF NOT EXISTS identity_answers_self (
            profile_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            valeur_num REAL,
            valeur_text TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (profile_id, question_id),
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS identity_answers_partner (
            profile_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            min_val REAL,
            max_val REAL,
            options_json TEXT, -- Liste JSON des options tolérées
            indifferent INTEGER DEFAULT 0, -- 1 si l'utilisateur coche "Indifférent"
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (profile_id, question_id),
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()

    # Synchronisation initiale douce : migrer les valeurs physiques existantes de identity_cards vers identity_answers_self si non renseignées
    c.execute("SELECT id, sujet FROM questions WHERE classe = 0")
    q_dict = {row["sujet"]: row["id"] for row in c.fetchall()}
    c.execute("SELECT profile_id, taille, poids, pointure, tour_poitrine, tour_taille, tour_hanches, couleur_cheveux, origines, style FROM identity_cards")
    for card_row in c.fetchall():
        pid = card_row["profile_id"]
        field_mappings = [
            ("Stature & Taille (cm)", card_row["taille"], None),
            ("Corpulence & Poids de forme", card_row["poids"], None),
            ("Pointure de chaussures", card_row["pointure"], None),
            ("Tour de poitrine", card_row["tour_poitrine"], None),
            ("Tour de taille", card_row["tour_taille"], None),
            ("Tour de hanches", card_row["tour_hanches"], None),
            ("Couleur & Nature des cheveux", None, card_row["couleur_cheveux"]),
            ("Origines culturelles", None, card_row["origines"]),
            ("Style vestimentaire & Allure", None, card_row["style"])
        ]
        for subj, v_num, v_txt in field_mappings:
            if subj in q_dict and (v_num is not None or (v_txt and v_txt.strip())):
                qid = q_dict[subj]
                c.execute("""
                    INSERT OR IGNORE INTO identity_answers_self (profile_id, question_id, valeur_num, valeur_text)
                    VALUES (?, ?, ?, ?)
                """, (pid, qid, float(v_num) if v_num is not None else None, str(v_txt).strip() if v_txt else None))
    conn.commit()

    # Table des demandes d'accès aux questions/classes/thématiques adressées à l'administrateur
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_access_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            target_type TEXT NOT NULL, -- 'classe', 'thematique', 'pack'
            target_value TEXT NOT NULL,
            action_type TEXT DEFAULT 'grant', -- 'grant' (demande d'accès) ou 'revoke' (demande de suppression)
            status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            responded_at TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
        )
    ''')
    c.execute("PRAGMA table_info(admin_access_requests)")
    aar_cols = [col["name"] for col in c.fetchall()]
    if "action_type" not in aar_cols:
        c.execute("ALTER TABLE admin_access_requests ADD COLUMN action_type TEXT DEFAULT 'grant'")
        conn.commit()
    
    # Table des autorisations de questionnaires par profil (Jeux/Packs, Classes, Types)
    c.execute('''
        CREATE TABLE IF NOT EXISTS profile_question_access (
            profile_id INTEGER PRIMARY KEY,
            allowed_packs TEXT DEFAULT 'ALL',   -- JSON list ou 'ALL'
            allowed_classes TEXT DEFAULT 'ALL', -- JSON list ou 'ALL'
            allowed_types TEXT DEFAULT 'ALL',   -- JSON list ou 'ALL'
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
        )
    ''')
    
    # Table des demandes de match bilatérales entre abonnés
    c.execute('''
        CREATE TABLE IF NOT EXISTS match_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'declined'
            proposed_classes TEXT DEFAULT 'ALL',
            validated_classes TEXT DEFAULT 'ALL',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            responded_at TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (receiver_id) REFERENCES profiles(id) ON DELETE CASCADE
        )
    ''')
    
    # Table des jeux de questions (Packs / Domaines d'application)
    c.execute('''
        CREATE TABLE IF NOT EXISTS question_packs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            nom TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Table des questions
    # cible : 0-Tous, 1-Homme, 2-Femme
    # classe : 0-Non définies, 1-Standards, 2-Personnelles, 3-Intimes, 4-Privées, 5-A caractère sexuel, 8-Identité, 9-Interdits/Fantasmes
    # type : 'G' (Goûts unique) ou 'MULTI' (V, A, D, P)
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pack_id INTEGER NOT NULL,
            cible INTEGER DEFAULT 0,
            classe INTEGER DEFAULT 1,
            thematique TEXT NOT NULL,
            sujet TEXT NOT NULL,
            type TEXT NOT NULL, -- 'G' ou 'MULTI'
            texte TEXT NOT NULL,
            status TEXT DEFAULT 'validated',
            n_quest_lie INTEGER DEFAULT 0,
            FOREIGN KEY (pack_id) REFERENCES question_packs(id)
        )
    ''')
    
    # S'assurer que le Pack 3 (JEU_3) existe
    c.execute("""
        INSERT OR IGNORE INTO question_packs (id, code, nom, description)
        VALUES (3, 'JEU_3', 'Jeu 3', 'Jeu 3 - Intimité, sensualité et explorations avancées')
    """)

    # Vérification colonne status
    c.execute("PRAGMA table_info(questions)")
    q_col_names = [col[1] for col in c.fetchall()]
    if "status" not in q_col_names:
        c.execute("ALTER TABLE questions ADD COLUMN status TEXT DEFAULT 'validated'")
    
    # Table des réponses
    # axis : 'G', 'V', 'A', 'D', 'P'
    # value : 0 à 9
    c.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            profile_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            axis TEXT NOT NULL,
            value INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (profile_id, question_id, axis),
            FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
    ''')
    
    # Données d'amorçage (Seed data)
    c.execute('SELECT COUNT(*) as count FROM question_packs')
    if c.fetchone()['count'] == 0:
        c.execute('''
            INSERT INTO question_packs (code, nom, description) VALUES 
            ('STANDARD', 'Jeu Général & Découverte', 'Jeu généraliste pour tester les affinités globales, goûts et modes de vie.'),
            ('RENCONTRE', 'Rencontre & Complicité', 'Jeu orienté relations interpersonnelles, projets de vie et intimité.'),
            ('LUDIQUE', 'Soirées & Amis', 'Jeu léger et divertissant pour animer des groupes ou soirées.')
        ''')
        
        # Récupérer l'id du pack standard
        c.execute("SELECT id FROM question_packs WHERE code = 'STANDARD'")
        pack_std_id = c.fetchone()['id']
        c.execute("SELECT id FROM question_packs WHERE code = 'RENCONTRE'")
        pack_ren_id = c.fetchone()['id']
        
        # Questions de base conformes à Affinity.docx
        seed_questions = [
            # Thématique Activités / Sujet Sport (MULTI)
            (pack_std_id, 0, 1, "Activités", "Sport", "MULTI", "La pratique régulière d'un sport ou d'une activité physique intensive."),
            # Thématique Activités / Sujet Lecture (MULTI)
            (pack_std_id, 0, 1, "Activités", "Lecture", "MULTI", "Prendre du temps pour lire des livres, romans ou essais."),
            # Thématique Activités / Sujet Voyages (MULTI)
            (pack_std_id, 0, 1, "Activités", "Voyages", "MULTI", "Voyager à l'étranger et découvrir de nouvelles cultures."),
            # Thématique Goûts / Sujet Gastronomie (G)
            (pack_std_id, 0, 1, "Goûts", "Gastronomie", "G", "Les expériences culinaires raffinées et la découverte de restaurants insolites."),
            # Thématique Goûts / Sujet Cinéma & Séries (G)
            (pack_std_id, 0, 1, "Goûts", "Cinéma & Séries", "G", "Passer des soirées devant des séries, films ou au cinéma."),
            # Thématique Goûts / Sujet Soirées Festives (G)
            (pack_std_id, 0, 1, "Goûts", "Fêtes & Sorties", "G", "Faire la fête tard le soir, aller en club ou en festivals."),
            # Thématique Comportement / Sujet Organisation (MULTI)
            (pack_std_id, 0, 2, "Comportement", "Organisation", "MULTI", "Prévoir et planifier son emploi du temps à l'avance sans imprévus."),
            # Thématique Comportement / Sujet Spontanéité (G)
            (pack_std_id, 0, 2, "Comportement", "Spontanéité", "G", "Décider d'un voyage ou d'une sortie sur un coup de tête."),
            # Thématique Intimité / Sujet Confidences (MULTI)
            (pack_ren_id, 0, 3, "Relations", "Confidences", "MULTI", "Partager facilement ses émotions profondes et ses vulnérabilités."),
            # Thématique Intimité / Sujet Projets de couple (MULTI)
            (pack_ren_id, 0, 3, "Relations", "Projets Communs", "MULTI", "Construire une vie à deux (emménagement, investissements, vision de famille)."),
            # Thématique Privée / Sujet Indépendance (G)
            (pack_ren_id, 0, 4, "Vie Privée", "Indépendance", "G", "Avoir son propre espace et du temps pour soi sans son partenaire."),
            # Thématique Intime / Sujet Tendresse (MULTI)
            (pack_ren_id, 0, 3, "Sensibilité", "Tendresse", "MULTI", "L'importance des gestes affectueux au quotidien (câlins, attention).")
        ]
        
        c.executemany('''
            INSERT INTO questions (pack_id, cible, classe, thematique, sujet, type, texte)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_questions)
        
    conn.commit()
    conn.close()

# ==========================================
# ALGORITHME DE CALCUL D'AFFINITÉ (MOTEUR)
# ==========================================
def calculate_affinity(profile1_id, profile2_id, allowed_classes=None):
    conn = get_db()
    c = conn.cursor()
    
    # 1. Vérifier l'existence des profils
    c.execute("SELECT * FROM profiles WHERE id = ?", (profile1_id,))
    p1 = c.fetchone()
    c.execute("SELECT * FROM profiles WHERE id = ?", (profile2_id,))
    p2 = c.fetchone()
    
    if not p1 or not p2:
        conn.close()
        return {"error": "L'un des profils n'existe pas."}
    
    if profile1_id == profile2_id:
        conn.close()
        return {"error": "Impossible de comparer un profil avec lui-même."}

    # Règle Affinity : un administrateur n'a pas de fiche d'identité et ne peut pas faire l'objet d'un match
    if p1["role"] == "admin" or p2["role"] == "admin":
        conn.close()
        return {
            "error": "ADMIN_NON_MATCHABLE",
            "message": "Un compte administrateur supervise la plateforme et ne peut pas participer à un calcul d'affinité."
        }
    
    # 2. Vérifier que la fiche d'identité est renseignée (RÈGLE ESSENTIELLE D'AFFINITY.DOCX)
    c.execute("SELECT * FROM identity_cards WHERE profile_id = ?", (profile1_id,))
    id1 = c.fetchone()
    c.execute("SELECT * FROM identity_cards WHERE profile_id = ?", (profile2_id,))
    id2 = c.fetchone()
    
    def is_card_valid(card):
        if not card:
            return False
        # Au moins prénom ou nom, et sexe renseigné
        return bool(card["prenom"] or card["nom"])
    
    if not is_card_valid(id1) or not is_card_valid(id2):
        conn.close()
        return {
            "error": "FICHE_MANQUANTE",
            "message": "Selon les règles d'Affinity, chaque profil doit obligatoirement avoir complété sa fiche d'identité pour débloquer le calcul d'affinités.",
            "profile1_complete": is_card_valid(id1),
            "profile2_complete": is_card_valid(id2)
        }
    
    # 3. Récupérer toutes les réponses des deux profils
    c.execute("""
        SELECT a.profile_id, a.question_id, a.axis, a.value, 
               q.thematique, q.sujet, q.classe, q.type, q.texte
        FROM answers a
        JOIN questions q ON a.question_id = q.id
        WHERE a.profile_id IN (?, ?)
    """, (profile1_id, profile2_id))
    rows = c.fetchall()
    conn.close()
    
    # Indexer les réponses par (question_id, axis)
    p1_answers = {}
    p2_answers = {}
    questions_meta = {}
    
    for r in rows:
        qid = r["question_id"]
        axis = r["axis"]
        val = r["value"]
        pid = r["profile_id"]
        questions_meta[qid] = {
            "id": qid,
            "thematique": r["thematique"],
            "sujet": r["sujet"],
            "classe": r["classe"],
            "type": r["type"],
            "texte": r["texte"]
        }
        if pid == profile1_id:
            p1_answers[(qid, axis)] = val
        else:
            p2_answers[(qid, axis)] = val
            
    # Calcul des concordances
    common_questions = set(qid for (qid, _) in p1_answers.keys()).intersection(set(qid for (qid, _) in p2_answers.keys()))

    # Filtrer par classes autorisées / mutuellement validées si spécifié
    if allowed_classes is not None and allowed_classes != "ALL":
        try:
            if isinstance(allowed_classes, str):
                allowed_classes = json.loads(allowed_classes)
            allowed_set = set(int(x) for x in allowed_classes)
            common_questions = set(qid for qid in common_questions if questions_meta[qid]["classe"] in allowed_set)
        except Exception:
            pass
    
    if not common_questions:
        dist = calculate_distance_km(id1["ville"] if id1 else "", id2["ville"] if id2 else "")
        return {
            "score_global": 0,
            "total_questions_communes": 0,
            "distance_km": dist,
            "message": "Aucune question commune dans le périmètre retenu. Remplissez des questionnaires similaires pour calculer l'affinité."
        }
        
    score_details_thematique = {}
    points_de_fusion = []
    zones_de_vigilance = []
    
    total_weights = 0
    accumulated_score = 0
    
    axis_scores = {
        "G": {"sum": 0, "count": 0},
        "V": {"sum": 0, "count": 0},
        "A": {"sum": 0, "count": 0},
        "DP_synergy": {"sum": 0, "count": 0} # Découverte P1 vs Partage P2 et Découverte P2 vs Partage P1
    }
    
    # Fonction de distance d'échelle (0 à 5, 9=Pas du tout/Jamais)
    def normalize_val(v):
        # 0 = pas de réponse -> ignoré
        # 1 à 5 : échelle progressive
        # 9 : pas du tout / jamais / impossible -> valeur 0 sur une échelle de désir/fréquence
        if v == 9:
            return 0.0
        return float(v)

    def compute_axis_similarity(v1, v2):
        if v1 == 0 or v2 == 0:
            return None # non répondu
        n1 = normalize_val(v1)
        n2 = normalize_val(v2)
        # Échelle de 0 à 5 -> écart max 5
        diff = abs(n1 - n2)
        sim = max(0.0, 1.0 - (diff / 5.0))
        return sim

    for qid in common_questions:
        q = questions_meta[qid]
        th = q["thematique"]
        if th not in score_details_thematique:
            score_details_thematique[th] = {"sum": 0.0, "weight": 0.0, "items": []}
            
        q_sim_sum = 0.0
        q_weight = 1.0 # Poids de base
        
        # Les classes intimes/privées ont un poids renforcé pour l'affinité profonde
        if q["classe"] in [3, 4, 5]:
            q_weight = 1.2
            
        q_axes_evaluated = 0
        
        if q["type"] == "G":
            v1 = p1_answers.get((qid, "G"), 0)
            v2 = p2_answers.get((qid, "G"), 0)
            sim = compute_axis_similarity(v1, v2)
            if sim is not None:
                q_sim_sum += sim
                q_axes_evaluated += 1
                axis_scores["G"]["sum"] += sim
                axis_scores["G"]["count"] += 1
                
        elif q["type"] in ("MULTI", "M"):
            # 1. Comparaison Vécu (V)
            v1_v = p1_answers.get((qid, "V"), 0)
            v2_v = p2_answers.get((qid, "V"), 0)
            sim_v = compute_axis_similarity(v1_v, v2_v)
            if sim_v is not None:
                q_sim_sum += sim_v * 0.7 # Vécu passé
                q_axes_evaluated += 0.7
                axis_scores["V"]["sum"] += sim_v
                axis_scores["V"]["count"] += 1

            # 2. Comparaison Actuel (A)
            v1_a = p1_answers.get((qid, "A"), 0)
            v2_a = p2_answers.get((qid, "A"), 0)
            sim_a = compute_axis_similarity(v1_a, v2_a)
            if sim_a is not None:
                q_sim_sum += sim_a * 1.0 # Actuel présent
                q_axes_evaluated += 1.0
                axis_scores["A"]["sum"] += sim_a
                axis_scores["A"]["count"] += 1

            # 3. Synergie croisée Découverte / Partage (D & P) : Cœur de l'algorithme Affinity !
            p1_d = p1_answers.get((qid, "D"), 0)
            p2_p = p2_answers.get((qid, "P"), 0)
            p2_d = p2_answers.get((qid, "D"), 0)
            p1_p = p1_answers.get((qid, "P"), 0)
            
            def eval_dp_pair(desire, share):
                if desire == 0 or share == 0:
                    return None
                nd = normalize_val(desire)
                ns = normalize_val(share)
                # Tension si l'un est gêné ou refuse (1 ou 9) et l'autre exige (5)
                if (desire in [1, 9] and share == 5) or (share in [1, 9] and desire == 5):
                    return 0.1
                # Harmonie si les deux sont positifs (>= 3)
                if nd >= 3 and ns >= 3:
                    return 1.0
                return max(0.0, 1.0 - abs(nd - ns) / 5.0)

            syn1 = eval_dp_pair(p1_d, p2_p)
            syn2 = eval_dp_pair(p2_d, p1_p)
            
            synergies = [s for s in [syn1, syn2] if s is not None]
            if synergies:
                avg_syn = sum(synergies) / len(synergies)
                q_sim_sum += avg_syn * 1.2 # Bonus relationnel
                q_axes_evaluated += 1.2
                axis_scores["DP_synergy"]["sum"] += avg_syn
                axis_scores["DP_synergy"]["count"] += 1

        if q_axes_evaluated > 0:
            q_final_score = q_sim_sum / q_axes_evaluated
            score_details_thematique[th]["sum"] += q_final_score * q_weight
            score_details_thematique[th]["weight"] += q_weight
            
            accumulated_score += q_final_score * q_weight
            total_weights += q_weight
            
            # Détection point de fusion (affinité >= 85%) ou zone de vigilance (<= 35%)
            item_report = {
                "sujet": q["sujet"],
                "thematique": q["thematique"],
                "score": round(q_final_score * 100, 1),
                "texte": q["texte"]
            }
            if q_final_score >= 0.85:
                points_de_fusion.append(item_report)
            elif q_final_score <= 0.35:
                zones_de_vigilance.append(item_report)

    global_score_percent = round((accumulated_score / total_weights) * 100, 1) if total_weights > 0 else 0
    
    # Détail par thématique
    thematiques_report = {}
    for th, data in score_details_thematique.items():
        if data["weight"] > 0:
            thematiques_report[th] = round((data["sum"] / data["weight"]) * 100, 1)

    # Détail par axe temporel/relationnel
    axis_report = {}
    for ax, val in axis_scores.items():
        axis_report[ax] = round((val["sum"] / val["count"]) * 100, 1) if val["count"] > 0 else None

    c1 = (id1["habite_commune"] or id1["ville"] or "") if id1 else ""
    c2 = (id2["habite_commune"] or id2["ville"] or "") if id2 else ""
    dist = calculate_distance_km(c1, c2)

    return {
        "profile1": {"id": p1["id"], "pseudo": p1["pseudo"], "identite": dict(id1)},
        "profile2": {"id": p2["id"], "pseudo": p2["pseudo"], "identite": dict(id2)},
        "score_global": global_score_percent,
        "distance_km": dist,
        "questions_evaluees": len(common_questions),
        "thematiques": thematiques_report,
        "axes": axis_report,
        "points_de_fusion": sorted(points_de_fusion, key=lambda x: x["score"], reverse=True)[:5],
        "zones_de_vigilance": sorted(zones_de_vigilance, key=lambda x: x["score"])[:5]
    }

# ==========================================
# GESTIONNAIRE DE REQUÊTES HTTP / API REST
# ==========================================
class AffinityHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def get_auth_token(self):
        auth_header = self.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:].strip()
        return None

    def get_current_user(self):
        token = self.get_auth_token()
        return get_session_profile(token)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path.startswith("/api/"):
            # Session actuelle de l'utilisateur connecté
            if path == "/api/auth/me":
                user = self.get_current_user()
                if not user:
                    return self._send_json({"error": "Non authentifié"}, 401)
                return self._send_json({"user": user})

            conn = get_db()
            c = conn.cursor()
            
            # --- Référentiel des pays reconnus (France, UE, Hors UE) et départements ---
            if path == "/api/countries":
                conn.close()
                return self._send_json({"countries": ALLOWED_COUNTRIES})

            elif path == "/api/departments":
                conn.close()
                return self._send_json({"departments": [f"{code} - {name}" for code, name in sorted(FRENCH_DEPARTMENTS.items())]})

            # --- Profils ---
            elif path == "/api/profiles":
                c.execute("""
                    SELECT p.id, p.pseudo, p.code_profil, p.avatar, p.role, p.email, p.created_at,
                           i.prenom, i.nom, i.sexe, i.date_naissance, i.ville, i.statut, i.bio,
                           i.situation_famille, i.recherche_de,
                           i.pays_naissance, i.habite_pays, i.habite_region_dept, i.habite_commune,
                           i.travail_pays, i.travail_region_dept, i.travail_commune,
                           i.taille, i.poids, i.pointure, i.tour_poitrine, i.tour_taille, i.tour_hanches, i.mensurations,
                           i.origines, i.couleur_cheveux, i.style, i.aime_chez_moi, i.aime_pas_chez_moi,
                           (CASE WHEN i.prenom IS NOT NULL AND i.prenom != '' THEN 1 ELSE 0 END) as has_identity,
                           (SELECT COUNT(DISTINCT question_id) FROM answers WHERE profile_id = p.id) as answers_count,
                           (SELECT COUNT(DISTINCT a.question_id) FROM answers a JOIN questions q ON a.question_id = q.id WHERE a.profile_id = p.id AND q.classe = 8) as identity_answers_count,
                           (SELECT COUNT(DISTINCT question_id) FROM identity_answers_self WHERE profile_id = p.id AND (valeur_num IS NOT NULL OR (valeur_text IS NOT NULL AND valeur_text != ''))) as identity_self_count,
                           (SELECT COUNT(DISTINCT question_id) FROM identity_answers_partner WHERE profile_id = p.id AND (indifferent = 1 OR (min_val IS NOT NULL AND max_val IS NOT NULL) OR (options_json IS NOT NULL AND options_json != '[]'))) as identity_partner_count,
                           (SELECT COUNT(*) FROM questions WHERE classe = 8) as identity_questions_total,
                           pqa.allowed_packs, pqa.allowed_classes, pqa.allowed_types
                    FROM profiles p
                    LEFT JOIN identity_cards i ON p.id = i.profile_id
                    LEFT JOIN profile_question_access pqa ON p.id = pqa.profile_id
                    ORDER BY p.id ASC
                """)
                raw_profiles = [dict(row) for row in c.fetchall()]
                profiles = []
                for p in raw_profiles:
                    ap = p.get("allowed_packs")
                    ac = p.get("allowed_classes")
                    at = p.get("allowed_types")
                    p["question_access"] = {
                        "allowed_packs": json.loads(ap) if ap and ap != "ALL" else "ALL",
                        "allowed_classes": json.loads(ac) if ac and ac != "ALL" else "ALL",
                        "allowed_types": json.loads(at) if at and at != "ALL" else "ALL"
                    }
                    if p.get("date_naissance"):
                        p_age, _ = validate_birth_date_and_age(p["date_naissance"])
                        p["age"] = p_age
                    else:
                        p["age"] = None
                    p["identity_self_answers_count"] = max(p.get("identity_answers_count", 0), p.get("identity_self_count", 0))
                    p["identity_partner_answers_count"] = p.get("identity_partner_count", 0)
                    profiles.append(p)
                conn.close()
                return self._send_json({"profiles": profiles})
                
            elif path == "/api/admin/access-requests":
                c.execute("""
                    SELECT ar.*, p.pseudo, p.role
                    FROM admin_access_requests ar
                    JOIN profiles p ON ar.profile_id = p.id
                    ORDER BY ar.created_at DESC
                """)
                reqs = [dict(r) for r in c.fetchall()]
                conn.close()
                return self._send_json({"requests": reqs})

            elif path.startswith("/api/profiles/"):
                parts = path.split("/")
                pid = int(parts[3])
                if len(parts) == 4:
                    c.execute("SELECT * FROM profiles WHERE id = ?", (pid,))
                    prof = c.fetchone()
                    conn.close()
                    if prof:
                        return self._send_json(dict(prof))
                    return self._send_json({"error": "Profil introuvable"}, 404)
                elif len(parts) == 5 and parts[4] == "identity":
                    c.execute("SELECT * FROM identity_cards WHERE profile_id = ?", (pid,))
                    card = c.fetchone()
                    conn.close()
                    card_dict = dict(card) if card else {}
                    if card_dict.get("date_naissance"):
                        c_age, _ = validate_birth_date_and_age(card_dict["date_naissance"])
                        card_dict["age"] = c_age
                    return self._send_json(card_dict)
                elif len(parts) == 5 and parts[4] == "catalog-access":
                    c.execute("SELECT * FROM profile_question_access WHERE profile_id = ?", (pid,))
                    pqa = c.fetchone()
                    allowed_packs = json.loads(pqa["allowed_packs"]) if (pqa and pqa["allowed_packs"] and pqa["allowed_packs"] != "ALL") else "ALL"
                    allowed_classes = json.loads(pqa["allowed_classes"]) if (pqa and pqa["allowed_classes"] and pqa["allowed_classes"] != "ALL") else "ALL"

                    # Demandes en attente auprès de l'administrateur
                    c.execute("SELECT target_type, target_value, action_type FROM admin_access_requests WHERE profile_id = ? AND status = 'pending'", (pid,))
                    pending_reqs = [dict(r) for r in c.fetchall()]

                    # Questions déjà répondues par ce profil
                    c.execute("SELECT DISTINCT question_id FROM answers WHERE profile_id = ?", (pid,))
                    answered_qids = set(row["question_id"] for row in c.fetchall())

                    c.execute("SELECT * FROM question_packs ORDER BY id ASC")
                    all_packs = [dict(row) for row in c.fetchall()]
                    packs_res = []
                    for pk in all_packs:
                        has_pk = (allowed_packs == "ALL") or (pk["id"] in allowed_packs)
                        c.execute("SELECT COUNT(*) as cnt FROM questions WHERE pack_id = ?", (pk["id"],))
                        cnt = c.fetchone()["cnt"]

                        # Vérifier s'il y a une demande en attente
                        pk_pending = next((r for r in pending_reqs if r["target_type"] == "pack" and str(r["target_value"]) == str(pk["id"])), None)

                        packs_res.append({
                            "id": pk["id"],
                            "code": pk["code"],
                            "nom": pk["nom"],
                            "description": pk.get("description", ""),
                            "count": cnt,
                            "has_access": has_pk,
                            "has_pending": pk_pending is not None,
                            "pending_action": pk_pending["action_type"] if pk_pending else None
                        })

                    classe_names = {
                        0: "Classe 0 - Non définies",
                        1: "Classe 1 - Standards",
                        2: "Classe 2 - Personnelles",
                        3: "Classe 3 - Intimes",
                        4: "Classe 4 - Privées",
                        5: "Classe 5 - A caractère sexuel",
                        9: "Classe 9 - Interdits / Fantasmes"
                    }
                    c.execute("SELECT DISTINCT classe FROM questions WHERE classe != 8 ORDER BY classe ASC")
                    db_classes = [row["classe"] for row in c.fetchall()]
                    classes_res = []
                    for cl in db_classes:
                        has_cl = (allowed_classes == "ALL") or (cl in allowed_classes)
                        c.execute("SELECT id, thematique, sujet FROM questions WHERE classe = ? ORDER BY thematique ASC", (cl,))
                        q_rows = [dict(r) for r in c.fetchall()]
                        cnt = len(q_rows)
                        answered_in_class = sum(1 for q in q_rows if q["id"] in answered_qids)

                        # Grouper les thématiques de cette classe
                        th_map = {}
                        for q in q_rows:
                            th_name = q["thematique"] or "Divers"
                            if th_name not in th_map:
                                th_map[th_name] = {"thematique": th_name, "total": 0, "answered": 0}
                            th_map[th_name]["total"] += 1
                            if q["id"] in answered_qids:
                                th_map[th_name]["answered"] += 1

                        cl_pending = next((r for r in pending_reqs if r["target_type"] == "classe" and str(r["target_value"]) == str(cl)), None)

                        classes_res.append({
                            "classe": cl,
                            "nom": classe_names.get(cl, f"Classe {cl}"),
                            "label": classe_names.get(cl, f"Classe {cl}"),
                            "count": cnt,
                            "answered_count": answered_in_class,
                            "has_access": has_cl,
                            "has_pending": cl_pending is not None,
                            "pending_action": cl_pending["action_type"] if cl_pending else None,
                            "thematiques": list(th_map.values())
                        })

                    c.execute("SELECT id, thematique, sujet, classe, pack_id FROM questions WHERE classe != 8 ORDER BY thematique ASC, sujet ASC")
                    items = [dict(row) for row in c.fetchall()]
                    thematiques_dict = {}
                    for it in items:
                        th = it["thematique"]
                        if th not in thematiques_dict:
                            thematiques_dict[th] = []
                        has_it = (
                            (allowed_packs == "ALL" or it["pack_id"] in allowed_packs) and
                            (allowed_classes == "ALL" or it["classe"] in allowed_classes)
                        )
                        thematiques_dict[th].append({
                            "id": it["id"],
                            "sujet": it["sujet"],
                            "classe": it["classe"],
                            "classe_label": classe_names.get(it["classe"], f"Classe {it['classe']}"),
                            "pack_id": it["pack_id"],
                            "has_access": has_it,
                            "is_answered": it["id"] in answered_qids
                        })

                    thematiques_res = []
                    for th, q_list in thematiques_dict.items():
                        # Regrouper par sujet
                        subj_map = {}
                        for q in q_list:
                            s_name = q["sujet"]
                            if s_name not in subj_map:
                                subj_map[s_name] = {
                                    "sujet": s_name,
                                    "classe": q["classe"],
                                    "classe_label": q["classe_label"],
                                    "pack_id": q["pack_id"],
                                    "has_access": q["has_access"],
                                    "total_questions": 0,
                                    "answered_questions": 0
                                }
                            subj_map[s_name]["total_questions"] += 1
                            if q["is_answered"]:
                                subj_map[s_name]["answered_questions"] += 1

                        sujets = list(subj_map.values())
                        # Vérifier demande en attente pour les sujets
                        for s in sujets:
                            full_target = f"{th} - {s['sujet']}"
                            s_pending = next((r for r in pending_reqs if r["target_type"] == "thematique" and r["target_value"] == full_target), None)
                            s["has_pending"] = s_pending is not None
                            s["pending_action"] = s_pending["action_type"] if s_pending else None

                        all_access = all(s["has_access"] for s in sujets)
                        some_access = any(s["has_access"] for s in sujets)
                        th_total = sum(s["total_questions"] for s in sujets)
                        th_answered = sum(s["answered_questions"] for s in sujets)

                        thematiques_res.append({
                            "thematique": th,
                            "sujets": sujets,
                            "has_access": all_access,
                            "partial_access": some_access and not all_access,
                            "total_questions": th_total,
                            "answered_questions": th_answered
                        })

                    conn.close()
                    return self._send_json({
                        "profile_id": pid,
                        "packs": packs_res,
                        "classes": classes_res,
                        "thematiques": thematiques_res,
                        "catalog": thematiques_res
                    })
                elif len(parts) == 5 and parts[4] == "access-requests":
                    c.execute("""
                        SELECT * FROM admin_access_requests
                        WHERE profile_id = ?
                        ORDER BY created_at DESC
                    """, (pid,))
                    reqs = [dict(r) for r in c.fetchall()]
                    conn.close()
                    return self._send_json({"requests": reqs})
                elif len(parts) == 5 and parts[4] == "answers":
                    c.execute("""
                        SELECT question_id, axis, value FROM answers WHERE profile_id = ?
                    """, (pid,))
                    answers = [dict(row) for row in c.fetchall()]
                    conn.close()
                    return self._send_json({"answers": answers})
                elif len(parts) == 5 and parts[4] == "identity-answers":
                    c.execute("SELECT * FROM identity_answers_self WHERE profile_id = ?", (pid,))
                    self_rows = [dict(r) for r in c.fetchall()]
                    self_dict = {r["question_id"]: {"valeur_num": r["valeur_num"], "valeur_text": r["valeur_text"]} for r in self_rows}

                    c.execute("SELECT * FROM identity_answers_partner WHERE profile_id = ?", (pid,))
                    partner_rows = [dict(r) for r in c.fetchall()]
                    partner_dict = {
                        r["question_id"]: {
                            "min_val": r["min_val"],
                            "max_val": r["max_val"],
                            "options": json.loads(r["options_json"]) if r["options_json"] else [],
                            "indifferent": bool(r["indifferent"])
                        } for r in partner_rows
                    }

                    # Sexe du profil (stocké dans identity_cards)
                    c.execute("SELECT sexe FROM identity_cards WHERE profile_id = ?", (pid,))
                    prof_row = c.fetchone()
                    prof_sexe = prof_row["sexe"] if prof_row and prof_row["sexe"] is not None else 0

                    # Questions Type P (pour + sur vous / + sur moi) filtrées selon le sexe
                    # Cible 0 = Mixte, 1 = Homme, 2 = Femme
                    if prof_sexe == 1:
                        c.execute("SELECT id, cible, sujet, texte, type, thematique, config_reponses FROM questions WHERE classe = 8 AND type = 'P' AND cible IN (0, 1) ORDER BY id ASC")
                    elif prof_sexe == 2:
                        c.execute("SELECT id, cible, sujet, texte, type, thematique, config_reponses FROM questions WHERE classe = 8 AND type = 'P' AND cible IN (0, 2) ORDER BY id ASC")
                    else:
                        c.execute("SELECT id, cible, sujet, texte, type, thematique, config_reponses FROM questions WHERE classe = 8 AND type = 'P' ORDER BY id ASC")
                    qs_self_rows = c.fetchall()

                    # Questions Type T (pour + sur l'autre) : critères acceptés chez le/la partenaire
                    # Si homme hétérosexuel cherchant femme ou selon son choix : il peut renseigner les critères de tolérance
                    if prof_sexe == 1:
                        c.execute("SELECT id, cible, sujet, texte, type, thematique, config_reponses FROM questions WHERE classe = 8 AND type = 'T' AND cible IN (0, 2) ORDER BY id ASC")
                    elif prof_sexe == 2:
                        c.execute("SELECT id, cible, sujet, texte, type, thematique, config_reponses FROM questions WHERE classe = 8 AND type = 'T' AND cible IN (0, 1) ORDER BY id ASC")
                    else:
                        c.execute("SELECT id, cible, sujet, texte, type, thematique, config_reponses FROM questions WHERE classe = 8 AND type = 'T' ORDER BY id ASC")
                    qs_partner_rows = c.fetchall()

                    def enrich_q(q_row):
                        q_dict = dict(q_row)
                        cfg_raw = q_dict.get("config_reponses")
                        q_cfg = None
                        if cfg_raw:
                            try:
                                q_cfg = json.loads(cfg_raw)
                            except Exception:
                                pass
                        if not q_cfg:
                            q_cfg = IDENTITY_QUESTIONS_CONFIG.get(q_dict.get("sujet", ""), {})

                        q_dict["config"] = q_cfg
                        q_dict["kind"] = q_cfg.get("mode", "select")
                        q_dict["unit"] = q_cfg.get("unit", "")
                        q_dict["min"] = q_cfg.get("min", 0)
                        q_dict["max"] = q_cfg.get("max", 100)
                        q_dict["step"] = q_cfg.get("step", 1)
                        q_dict["default_min"] = q_cfg.get("default_min", q_dict["min"])
                        q_dict["default_max"] = q_cfg.get("default_max", q_dict["max"])
                        q_dict["options"] = q_cfg.get("options", [])
                        q_dict["dimension"] = q_cfg.get("dimension", q_dict.get("texte", ""))
                        return q_dict

                    questions_self = [enrich_q(r) for r in qs_self_rows]
                    questions_partner = [enrich_q(r) for r in qs_partner_rows]

                    total_features_self = len(questions_self)
                    total_features_partner = len(questions_partner)

                    # Comptage des réponses 'self'
                    answered_self = 0
                    for q in questions_self:
                        qid_str = str(q["id"])
                        v = self_dict.get(qid_str)
                        if v and (v.get("valeur_num") is not None or (v.get("valeur_text") and str(v.get("valeur_text")).strip())):
                            answered_self += 1

                    # Comptage des réponses 'partner'
                    answered_partner = 0
                    for q in questions_partner:
                        qid_str = str(q["id"])
                        v = partner_dict.get(qid_str)
                        if v and (v.get("indifferent") or (v.get("min_val") is not None and v.get("max_val") is not None) or (v.get("options") and len(v.get("options")) > 0)):
                            answered_partner += 1

                    pct_self = round((answered_self / total_features_self) * 100) if total_features_self > 0 else 100
                    pct_partner = round((answered_partner / total_features_partner) * 100) if total_features_partner > 0 else 100

                    conn.close()
                    return self._send_json({
                        "profile_id": pid,
                        "self": self_dict,
                        "partner": partner_dict,
                        "questions_self": questions_self,
                        "questions_partner": questions_partner,
                        "questions": questions_self, # Rétro-compatibilité
                        "config": IDENTITY_QUESTIONS_CONFIG,
                        "total_questions": total_features_self,
                        "total_features_self": total_features_self,
                        "total_features_partner": total_features_partner,
                        "answered_self": answered_self,
                        "answered_partner": answered_partner,
                        "completion_self": pct_self,
                        "completion_partner": pct_partner,
                        "self_completion_pct": pct_self,
                        "partner_completion_pct": pct_partner
                    })
                elif len(parts) == 5 and parts[4] == "question-access":
                    c.execute("SELECT * FROM profile_question_access WHERE profile_id = ?", (pid,))
                    pqa = c.fetchone()
                    conn.close()
                    if pqa:
                        ap = pqa["allowed_packs"]
                        ac = pqa["allowed_classes"]
                        at = pqa["allowed_types"]
                        return self._send_json({
                            "profile_id": pid,
                            "allowed_packs": json.loads(ap) if ap and ap != "ALL" else "ALL",
                            "allowed_classes": json.loads(ac) if ac and ac != "ALL" else "ALL",
                            "allowed_types": json.loads(at) if at and at != "ALL" else "ALL"
                        })
                    else:
                        return self._send_json({
                            "profile_id": pid,
                            "allowed_packs": "ALL",
                            "allowed_classes": "ALL",
                            "allowed_types": "ALL"
                        })
                elif len(parts) == 5 and parts[4] == "match-requests":
                    # Demandes reçues par ce profil
                    c.execute("""
                        SELECT mr.*, p.pseudo as sender_pseudo, p.avatar as sender_avatar, p.role as sender_role,
                               i.prenom as sender_prenom, i.nom as sender_nom, i.ville as sender_ville,
                               i.statut as sender_statut, i.bio as sender_bio
                        FROM match_requests mr
                        JOIN profiles p ON mr.sender_id = p.id
                        LEFT JOIN identity_cards i ON mr.sender_id = i.profile_id
                        WHERE mr.receiver_id = ?
                        ORDER BY mr.created_at DESC
                    """, (pid,))
                    raw_received = [dict(row) for row in c.fetchall()]

                    # Demandes envoyées par ce profil
                    c.execute("""
                        SELECT mr.*, p.pseudo as receiver_pseudo, p.avatar as receiver_avatar, p.role as receiver_role,
                               i.prenom as receiver_prenom, i.nom as receiver_nom, i.ville as receiver_ville,
                               i.statut as receiver_statut, i.bio as receiver_bio
                        FROM match_requests mr
                        JOIN profiles p ON mr.receiver_id = p.id
                        LEFT JOIN identity_cards i ON mr.receiver_id = i.profile_id
                        WHERE mr.sender_id = ?
                        ORDER BY mr.created_at DESC
                    """, (pid,))
                    raw_sent = [dict(row) for row in c.fetchall()]

                    c.execute("SELECT ville FROM identity_cards WHERE profile_id = ?", (pid,))
                    my_card = c.fetchone()
                    my_ville = my_card["ville"] if my_card else ""

                    received = []
                    for r in raw_received:
                        dist = calculate_distance_km(my_ville, r.get("sender_ville", ""))
                        r["distance_km"] = dist
                        try:
                            r["proposed_classes"] = json.loads(r["proposed_classes"]) if r["proposed_classes"] != "ALL" else "ALL"
                            r["validated_classes"] = json.loads(r["validated_classes"]) if r["validated_classes"] != "ALL" else "ALL"
                        except Exception:
                            pass
                        received.append(r)

                    sent = []
                    for s in raw_sent:
                        dist = calculate_distance_km(my_ville, s.get("receiver_ville", ""))
                        s["distance_km"] = dist
                        try:
                            s["proposed_classes"] = json.loads(s["proposed_classes"]) if s["proposed_classes"] != "ALL" else "ALL"
                            s["validated_classes"] = json.loads(s["validated_classes"]) if s["validated_classes"] != "ALL" else "ALL"
                        except Exception:
                            pass
                        if s["status"] == "accepted":
                            try:
                                aff = calculate_affinity(s["sender_id"], s["receiver_id"], s["validated_classes"])
                                s["score_global"] = aff.get("score_global", 0)
                                s["affinity_result"] = aff
                            except Exception:
                                pass
                        sent.append(s)

                    conn.close()
                    return self._send_json({"received": received, "sent": sent})

            # --- Calcul Distance entre Villes ---
            elif path == "/api/distance":
                query_params = urllib.parse.parse_qs(parsed.query)
                c1 = query_params.get("ville1", [""])[0]
                c2 = query_params.get("ville2", [""])[0]
                dist = calculate_distance_km(c1, c2)
                conn.close()
                return self._send_json({"ville1": c1, "ville2": c2, "distance_km": dist})

            # --- Jeux / Packs ---
            elif path == "/api/packs":
                c.execute("SELECT * FROM question_packs ORDER BY id ASC")
                packs = [dict(row) for row in c.fetchall()]
                conn.close()
                return self._send_json({"packs": packs})

            # --- Questions et sous-questions liées ---
            elif path.startswith("/api/questions/") and path.endswith("/subquestions"):
                qid = int(path.split("/")[3])
                c.execute("""
                    SELECT q.*, p.nom as pack_nom,
                           parent.texte as parent_texte,
                           (SELECT COUNT(*) FROM questions sq WHERE sq.n_quest_lie = q.id AND sq.id != q.id) as subquestions_count
                    FROM questions q
                    JOIN question_packs p ON q.pack_id = p.id
                    LEFT JOIN questions parent ON q.n_quest_lie = parent.id AND q.n_quest_lie != 0
                    WHERE q.n_quest_lie = ? AND q.id != ?
                    ORDER BY q.id ASC
                """, (qid, qid))
                sub_qs = [dict(row) for row in c.fetchall()]
                conn.close()
                return self._send_json({"parent_id": qid, "subquestions": sub_qs, "total": len(sub_qs)})

            # --- Questions ---
            elif path == "/api/questions":
                query_params = urllib.parse.parse_qs(parsed.query)
                requested_status = query_params.get("status", [None])[0]
                filter_parent = query_params.get("parent_id", [None])[0]

                base_select = """
                    SELECT q.*, p.nom as pack_nom,
                           parent.texte as parent_texte,
                           (SELECT COUNT(*) FROM questions sq WHERE sq.n_quest_lie = q.id AND sq.id != q.id) as subquestions_count
                    FROM questions q
                    LEFT JOIN question_packs p ON q.pack_id = p.id
                    LEFT JOIN questions parent ON q.n_quest_lie = parent.id AND q.n_quest_lie != 0
                """
                if filter_parent is not None:
                    sql = base_select + " WHERE q.n_quest_lie = ? ORDER BY q.id ASC"
                    c.execute(sql, (int(filter_parent),))
                elif requested_status == "all":
                    sql = base_select + " ORDER BY q.thematique, q.sujet, q.id"
                    c.execute(sql)
                elif requested_status == "pending_review":
                    sql = base_select + " WHERE q.status = 'pending_review' ORDER BY q.classe, q.id"
                    c.execute(sql)
                else:
                    sql = base_select + " WHERE (q.status = 'validated' OR q.status IS NULL) ORDER BY q.thematique, q.sujet, q.id"
                    c.execute(sql)
                questions = [dict(row) for row in c.fetchall()]
                conn.close()
                return self._send_json({"questions": questions})

            # --- Questions en attente de validation (Jeu 3, propositions) ---
            elif path == "/api/admin/questions/pending":
                query_params = urllib.parse.parse_qs(parsed.query)
                cl_param = query_params.get("classe", [None])[0]
                if cl_param:
                    c.execute("""
                        SELECT q.*, p.nom as pack_nom 
                        FROM questions q
                        LEFT JOIN question_packs p ON q.pack_id = p.id
                        WHERE q.status = 'pending_review' AND q.classe = ?
                        ORDER BY q.id ASC
                    """, (int(cl_param),))
                else:
                    c.execute("""
                        SELECT q.*, p.nom as pack_nom 
                        FROM questions q
                        LEFT JOIN question_packs p ON q.pack_id = p.id
                        WHERE q.status = 'pending_review'
                        ORDER BY q.classe ASC, q.id ASC
                    """)
                pending_qs = [dict(row) for row in c.fetchall()]
                
                # Décompte par classe dynamique
                c.execute("SELECT classe, COUNT(*) as cnt FROM questions WHERE status = 'pending_review' GROUP BY classe")
                counts_by_class = {str(row["classe"]): row["cnt"] for row in c.fetchall()}
                c.execute("SELECT COUNT(*) as cnt FROM questions WHERE status = 'pending_review' AND classe = 5")
                c5_cnt = c.fetchone()["cnt"]
                c.execute("SELECT COUNT(*) as cnt FROM questions WHERE status = 'pending_review' AND classe = 9")
                c9_cnt = c.fetchone()["cnt"]
                conn.close()
                return self._send_json({
                    "questions": pending_qs,
                    "pending_questions": pending_qs,
                    "total": len(pending_qs),
                    "counts_by_class": counts_by_class,
                    "count_classe_5": c5_cnt,
                    "count_classe_9": c9_cnt
                })

            # --- Statistiques Globales ---
            elif path == "/api/stats":
                c.execute("SELECT COUNT(*) as nb_profiles FROM profiles")
                nb_p = c.fetchone()["nb_profiles"]
                c.execute("SELECT COUNT(*) as nb_questions FROM questions")
                nb_q = c.fetchone()["nb_questions"]
                c.execute("SELECT COUNT(*) as nb_answers FROM answers")
                nb_a = c.fetchone()["nb_answers"]
                conn.close()
                return self._send_json({
                    "profiles_count": nb_p,
                    "questions_count": nb_q,
                    "answers_count": nb_a
                })

            conn.close()
            return self._send_json({"error": "Endpoint non trouvé"}, 404)
            
        # Sinon servir les fichiers statiques de l'interface
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        conn = get_db()
        c = conn.cursor()
        
        # --- AUTHENTIFICATION & SÉCURITÉ DES SESSIONS ---
        if path == "/api/auth/login":
            login = str(data.get("login", "")).strip()
            password = str(data.get("password", "")).strip()
            if not login or not password:
                conn.close()
                return self._send_json({"error": "Identifiant et mot de passe requis."}, 400)
            
            c.execute("""
                SELECT id, pseudo, code_profil, role, avatar, email, password_hash, salt
                FROM profiles
                WHERE LOWER(pseudo) = LOWER(?) OR LOWER(code_profil) = LOWER(?) OR (email IS NOT NULL AND LOWER(email) = LOWER(?))
            """, (login, login, login))
            prof = c.fetchone()
            if not prof:
                conn.close()
                return self._send_json({"error": "Identifiant ou mot de passe incorrect."}, 401)
            
            if not verify_password(password, prof["salt"], prof["password_hash"]):
                conn.close()
                return self._send_json({"error": "Identifiant ou mot de passe incorrect."}, 401)
            
            token = create_session(prof["id"])
            prof_dict = {
                "id": prof["id"],
                "pseudo": prof["pseudo"],
                "code_profil": prof["code_profil"],
                "role": prof["role"],
                "avatar": prof["avatar"],
                "email": prof["email"]
            }
            conn.close()
            return self._send_json({"success": True, "token": token, "profile": prof_dict})

        elif path == "/api/auth/register":
            pseudo = str(data.get("pseudo", "")).strip()
            password = str(data.get("password", "")).strip()
            email = str(data.get("email", "")).strip() or None
            
            if not pseudo:
                conn.close()
                return self._send_json({"error": "Le pseudo est obligatoire."}, 400)
            if not password or len(password) < 4:
                conn.close()
                return self._send_json({"error": "Le mot de passe doit contenir au moins 4 caractères."}, 400)
            
            salt, p_hash = hash_password(password)
            try:
                c.execute("INSERT INTO profiles (pseudo, avatar, role, password_hash, salt, email) VALUES (?, 'user', 'guest', ?, ?, ?)",
                          (pseudo, p_hash, salt, email))
                pid = c.lastrowid
                code_prof = f"AFF-{pid}"
                c.execute("UPDATE profiles SET code_profil = ? WHERE id = ?", (code_prof, pid))
                c.execute("INSERT INTO identity_cards (profile_id) VALUES (?)", (pid,))
                c.execute("INSERT OR REPLACE INTO profile_question_access (profile_id, allowed_packs, allowed_classes, allowed_types) VALUES (?, 'ALL', '[\"1\"]', 'ALL')", (pid,))
                conn.commit()
                token = create_session(pid)
                prof_dict = {
                    "id": pid,
                    "pseudo": pseudo,
                    "code_profil": code_prof,
                    "role": "guest",
                    "avatar": "user",
                    "email": email
                }
                conn.close()
                return self._send_json({"success": True, "token": token, "profile": prof_dict}, 201)
            except sqlite3.IntegrityError:
                conn.close()
                return self._send_json({"error": "Ce pseudo existe déjà. Veuillez en choisir un autre."}, 409)

        elif path == "/api/auth/forgot-password":
            login_or_email = str(data.get("login_or_email", "")).strip()
            if not login_or_email:
                conn.close()
                return self._send_json({"error": "Veuillez saisir votre pseudo, code profil ou adresse e-mail."}, 400)
            
            c.execute("""
                SELECT id, pseudo, code_profil, email
                FROM profiles
                WHERE LOWER(pseudo) = LOWER(?) OR LOWER(code_profil) = LOWER(?) OR (email IS NOT NULL AND LOWER(email) = LOWER(?))
            """, (login_or_email, login_or_email, login_or_email))
            prof = c.fetchone()
            if not prof:
                conn.close()
                return self._send_json({"error": "Aucun profil trouvé avec cet identifiant ou cette adresse e-mail."}, 404)
            
            user_email = (prof["email"] or "").strip()
            if not user_email:
                conn.close()
                return self._send_json({
                    "error": "Aucune adresse e-mail n'est associée à ce compte. Conformément aux règles de sécurité, la réinitialisation automatique est impossible sans e-mail renseigné. Veuillez contacter l'administrateur (ar30960)."
                }, 400)
            
            # Génération du code temporaire sécurisé à 6 chiffres
            reset_code = f"{secrets.randbelow(900000) + 100000}"
            expires_at = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()
            
            c.execute("INSERT INTO password_resets (profile_id, reset_code, expires_at) VALUES (?, ?, ?)",
                      (prof["id"], reset_code, expires_at))
            conn.commit()
            conn.close()
            
            masked = mask_email(user_email)
            return self._send_json({
                "success": True,
                "profile_id": prof["id"],
                "pseudo": prof["pseudo"],
                "email_masked": masked,
                "reset_code": reset_code,
                "message": f"Un code de réinitialisation sécurisé à 6 chiffres a été généré pour {masked}."
            })

        elif path == "/api/auth/reset-password":
            login_or_email = str(data.get("login_or_email", "")).strip()
            reset_code = str(data.get("reset_code", "")).strip()
            new_password = str(data.get("new_password", "")).strip()
            
            if not login_or_email or not reset_code or not new_password:
                conn.close()
                return self._send_json({"error": "Identifiant, code de réinitialisation et nouveau mot de passe requis."}, 400)
            if len(new_password) < 4:
                conn.close()
                return self._send_json({"error": "Le nouveau mot de passe doit comporter au moins 4 caractères."}, 400)
                
            c.execute("""
                SELECT id, pseudo, code_profil, email
                FROM profiles
                WHERE LOWER(pseudo) = LOWER(?) OR LOWER(code_profil) = LOWER(?) OR (email IS NOT NULL AND LOWER(email) = LOWER(?))
            """, (login_or_email, login_or_email, login_or_email))
            prof = c.fetchone()
            if not prof:
                conn.close()
                return self._send_json({"error": "Profil introuvable."}, 404)
                
            now_str = datetime.now(timezone.utc).isoformat()
            c.execute("""
                SELECT id, expires_at, used
                FROM password_resets
                WHERE profile_id = ? AND reset_code = ? AND used = 0 AND expires_at > ?
                ORDER BY id DESC LIMIT 1
            """, (prof["id"], reset_code, now_str))
            reset_entry = c.fetchone()
            if not reset_entry:
                conn.close()
                return self._send_json({"error": "Code de réinitialisation invalide ou expiré. Veuillez refaire une demande."}, 400)
                
            salt, p_hash = hash_password(new_password)
            c.execute("UPDATE profiles SET password_hash = ?, salt = ? WHERE id = ?", (p_hash, salt, prof["id"]))
            c.execute("UPDATE password_resets SET used = 1 WHERE id = ?", (reset_entry["id"],))
            c.execute("DELETE FROM sessions WHERE profile_id = ?", (prof["id"],))
            conn.commit()
            conn.close()
            return self._send_json({
                "success": True,
                "message": "Votre mot de passe a été réinitialisé avec succès ! Vous pouvez maintenant vous connecter."
            })

        elif path == "/api/auth/logout":
            token = self.get_auth_token()
            if token:
                delete_session(token)
            conn.close()
            return self._send_json({"success": True})

        elif path == "/api/auth/change-password":
            user = self.get_current_user()
            if not user:
                conn.close()
                return self._send_json({"error": "Authentification requise."}, 401)
            old_pwd = str(data.get("old_password", ""))
            new_pwd = str(data.get("new_password", "")).strip()
            if len(new_pwd) < 4:
                conn.close()
                return self._send_json({"error": "Le nouveau mot de passe doit comporter au moins 4 caractères."}, 400)
            c.execute("SELECT password_hash, salt FROM profiles WHERE id = ?", (user["id"],))
            prow = c.fetchone()
            if not prow or not verify_password(old_pwd, prow["salt"], prow["password_hash"]):
                conn.close()
                return self._send_json({"error": "Ancien mot de passe incorrect."}, 403)
            s, h = hash_password(new_pwd)
            c.execute("UPDATE profiles SET salt = ?, password_hash = ? WHERE id = ?", (s, h, user["id"]))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "message": "Mot de passe mis à jour avec succès."})

        elif path == "/api/admin/reset-password":
            user = self.get_current_user()
            if not user or user.get("role") != "admin":
                conn.close()
                return self._send_json({"error": "Action réservée à l'administrateur."}, 403)
            target_id = data.get("profile_id")
            new_pwd = str(data.get("new_password", "")).strip()
            if not target_id or len(new_pwd) < 4:
                conn.close()
                return self._send_json({"error": "Profil cible et mot de passe (min 4 caractères) requis."}, 400)
            s, h = hash_password(new_pwd)
            c.execute("UPDATE profiles SET salt = ?, password_hash = ? WHERE id = ?", (s, h, target_id))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "message": f"Mot de passe réinitialisé pour le profil #{target_id}."})

        # Création de profil
        elif path == "/api/profiles":
            pseudo = data.get("pseudo", "").strip()
            if not pseudo:
                conn.close()
                return self._send_json({"error": "Le pseudo est requis."}, 400)
            avatar = data.get("avatar", "user")
            try:
                c.execute("INSERT INTO profiles (pseudo, avatar, role) VALUES (?, ?, 'guest')", (pseudo, avatar))
                pid = c.lastrowid
                code_prof = f"AFF-{pid}"
                c.execute("UPDATE profiles SET code_profil = ? WHERE id = ?", (code_prof, pid))
                c.execute("INSERT INTO identity_cards (profile_id) VALUES (?)", (pid,))
                # Accès par défaut pour les nouveaux profils invités : classe 1 (Standards) uniquement
                c.execute("INSERT OR REPLACE INTO profile_question_access (profile_id, allowed_packs, allowed_classes, allowed_types) VALUES (?, 'ALL', '[\"1\"]', 'ALL')", (pid,))
                conn.commit()
                conn.close()
                return self._send_json({"success": True, "id": pid, "pseudo": pseudo, "code_profil": code_prof, "role": "guest"}, 201)
            except sqlite3.IntegrityError:
                conn.close()
                return self._send_json({"error": "Ce pseudo existe déjà."}, 409)

        # Mise à jour de la fiche d'identité
        elif path.startswith("/api/profiles/") and path.endswith("/identity"):
            pid = int(path.split("/")[3])
            
            # Mise à jour du pseudo si renseigné
            new_pseudo = data.get("pseudo")
            if new_pseudo and str(new_pseudo).strip():
                try:
                    c.execute("UPDATE profiles SET pseudo = ? WHERE id = ?", (str(new_pseudo).strip(), pid))
                except sqlite3.IntegrityError:
                    pass

            # Mise à jour de l'adresse e-mail si transmise
            if "email" in data:
                new_email = str(data.get("email", "")).strip() or None
                c.execute("UPDATE profiles SET email = ? WHERE id = ?", (new_email, pid))

            # 1. Validation de la date de naissance et cohérence de l'âge
            date_naiss = str(data.get("date_naissance", "")).strip() if data.get("date_naissance") else ""
            if date_naiss:
                c_age, age_err = validate_birth_date_and_age(date_naiss)
                if age_err:
                    conn.close()
                    return self._send_json({"error": age_err}, 400)

            # 2. Validation d'existence des pays (limité à France, UE, Hors UE)
            pays_naiss = str(data.get("pays_naissance", "")).strip() if data.get("pays_naissance") else ""
            if pays_naiss:
                is_ok, canonical = is_valid_country(pays_naiss)
                if not is_ok:
                    conn.close()
                    return self._send_json({"error": f"Le pays de naissance '{pays_naiss}' doit être sélectionné parmi : France, UE, Hors UE."}, 400)
                pays_naiss = canonical

            hab_pays = str(data.get("habite_pays", "")).strip() if data.get("habite_pays") else ""
            if hab_pays:
                is_ok, canonical = is_valid_country(hab_pays)
                if not is_ok:
                    conn.close()
                    return self._send_json({"error": f"Le pays de résidence '{hab_pays}' doit être sélectionné parmi : France, UE, Hors UE."}, 400)
                hab_pays = canonical

            hab_commune = str(data.get("habite_commune", "")).strip() if data.get("habite_commune") else ""
            hab_reg_dept = str(data.get("habite_region_dept", "")).strip() if data.get("habite_region_dept") else ""
            
            # Cohérence par défaut si commune saisie sans pays
            if hab_commune and not hab_pays:
                hab_pays = "France"

            # 3. Si Pays == France, limiter et vérifier le département et la cohérence avec la commune
            if hab_pays == "France":
                is_ok, err_msg, canonical_dept = validate_france_dept_and_commune(hab_reg_dept, hab_commune)
                if not is_ok:
                    conn.close()
                    return self._send_json({"error": err_msg}, 400)
                if canonical_dept:
                    hab_reg_dept = canonical_dept

            trav_commune = str(data.get("travail_commune", "")).strip() if data.get("travail_commune") else ""
            trav_reg_dept = str(data.get("travail_region_dept", "")).strip() if data.get("travail_region_dept") else ""
            trav_pays = str(data.get("travail_pays", "")).strip() if data.get("travail_pays") else ""

            ville_val = hab_commune or str(data.get("ville", "")).strip()

            # Calcul synthétique de mensurations si les tours individuels sont saisis
            tp = float(data["tour_poitrine"]) if data.get("tour_poitrine") not in (None, "") else None
            tt = float(data["tour_taille"]) if data.get("tour_taille") not in (None, "") else None
            th = float(data["tour_hanches"]) if data.get("tour_hanches") not in (None, "") else None

            mens_val = data.get("mensurations", "")
            if (not mens_val or mens_val == "") and (tp or tt or th):
                mens_val = f"{int(tp) if tp else '-'}-{int(tt) if tt else '-'}-{int(th) if th else '-'}"

            # Validation du champ 'À la recherche de'
            recherche_val = str(data.get("recherche_de", "")).strip() if data.get("recherche_de") else ""
            if recherche_val:
                norm_val = recherche_val.replace("'", "’")
                match_choice = next((c for c in CHOIX_RECHERCHE if c.replace("'", "’") == norm_val), None)
                if not match_choice:
                    conn.close()
                    return self._send_json({"error": "Choix invalide pour 'À la recherche de'. Choix attendus : Échanges et Amitié, Recherche d’un(e) partenaire, Plus si affinité, Je ne sais pas vraiment."}, 400)
                recherche_val = match_choice

            sit_famille_val = str(data.get("situation_famille", "")).strip() if data.get("situation_famille") else (str(data.get("statut", "")).strip() if data.get("statut") else "")

            c.execute("""
                INSERT INTO identity_cards (
                    profile_id, nom, prenom, date_naissance, sexe, ville, statut, bio,
                    situation_famille, recherche_de,
                    pays_naissance, habite_pays, habite_region_dept, habite_commune,
                    travail_pays, travail_region_dept, travail_commune,
                    taille, poids, pointure, tour_poitrine, tour_taille, tour_hanches, mensurations,
                    origines, couleur_cheveux, style, aime_chez_moi, aime_pas_chez_moi, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(profile_id) DO UPDATE SET
                    nom = excluded.nom,
                    prenom = excluded.prenom,
                    date_naissance = excluded.date_naissance,
                    sexe = excluded.sexe,
                    ville = excluded.ville,
                    statut = excluded.statut,
                    bio = excluded.bio,
                    situation_famille = excluded.situation_famille,
                    recherche_de = excluded.recherche_de,
                    pays_naissance = excluded.pays_naissance,
                    habite_pays = excluded.habite_pays,
                    habite_region_dept = excluded.habite_region_dept,
                    habite_commune = excluded.habite_commune,
                    travail_pays = excluded.travail_pays,
                    travail_region_dept = excluded.travail_region_dept,
                    travail_commune = excluded.travail_commune,
                    taille = excluded.taille,
                    poids = excluded.poids,
                    pointure = excluded.pointure,
                    tour_poitrine = excluded.tour_poitrine,
                    tour_taille = excluded.tour_taille,
                    tour_hanches = excluded.tour_hanches,
                    mensurations = excluded.mensurations,
                    origines = excluded.origines,
                    couleur_cheveux = excluded.couleur_cheveux,
                    style = excluded.style,
                    aime_chez_moi = excluded.aime_chez_moi,
                    aime_pas_chez_moi = excluded.aime_pas_chez_moi,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                pid,
                data.get("nom", ""),
                data.get("prenom", ""),
                date_naiss,
                int(data.get("sexe", 0)),
                ville_val,
                sit_famille_val,
                data.get("bio", ""),
                sit_famille_val,
                recherche_val,
                pays_naiss,
                hab_pays,
                hab_reg_dept,
                hab_commune,
                trav_pays,
                trav_reg_dept,
                trav_commune,
                int(data["taille"]) if data.get("taille") not in (None, "") else None,
                int(data["poids"]) if data.get("poids") not in (None, "") else None,
                float(data["pointure"]) if data.get("pointure") not in (None, "") else None,
                tp,
                tt,
                th,
                mens_val,
                data.get("origines", ""),
                data.get("couleur_cheveux", ""),
                data.get("style", ""),
                data.get("aime_chez_moi", ""),
                data.get("aime_pas_chez_moi", "")
            ))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "message": "Fiche d'identité mise à jour avec succès."})

        # Enregistrement des réponses d'identité "+ sur vous" (soi)
        elif path.startswith("/api/profiles/") and path.endswith("/identity-answers/self"):
            pid = int(path.split("/")[3])
            c.execute("SELECT role FROM profiles WHERE id = ?", (pid,))
            prof_row = c.fetchone()
            if prof_row and prof_row["role"] == "admin":
                conn.close()
                return self._send_json({"error": "Un administrateur ne répond pas aux questionnaires."}, 403)

            if "answers" in data and isinstance(data["answers"], list):
                answers_list = data["answers"]
            elif "question_id" in data:
                answers_list = [data]
            else:
                answers_list = []

            for ans in answers_list:
                qid = ans.get("question_id")
                v_num = ans.get("valeur_num")
                v_txt = ans.get("valeur_text")
                if qid:
                    c.execute("""
                        INSERT INTO identity_answers_self (profile_id, question_id, valeur_num, valeur_text, updated_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(profile_id, question_id) DO UPDATE SET
                            valeur_num = excluded.valeur_num,
                            valeur_text = excluded.valeur_text,
                            updated_at = CURRENT_TIMESTAMP
                    """, (pid, qid, float(v_num) if v_num not in (None, "") else None, str(v_txt).strip() if v_txt else None))
            conn.commit()

            # Calcul du pourcentage de complétude mis à jour (sur les 14 caractéristiques de classe 8)
            c.execute("SELECT COUNT(*) as total FROM questions WHERE classe = 8 AND type = 'P'")
            tot_q = c.fetchone()["total"] or 14
            c.execute("""
                SELECT COUNT(DISTINCT q.sujet) as cnt 
                FROM identity_answers_self a
                JOIN questions q ON a.question_id = q.id
                WHERE a.profile_id = ? AND (a.valeur_num IS NOT NULL OR (a.valeur_text IS NOT NULL AND a.valeur_text != ''))
            """, (pid,))
            ans_count = c.fetchone()["cnt"]
            pct = round((ans_count / tot_q) * 100) if tot_q > 0 else 100

            conn.close()
            return self._send_json({
                "success": True,
                "ok": True,
                "saved": len(answers_list),
                "answered": ans_count,
                "total": tot_q,
                "completion": pct,
                "self_completion_pct": pct
            })

        # Enregistrement des critères d'identité "+ sur l'autre" (tolérances partenaire)
        elif path.startswith("/api/profiles/") and path.endswith("/identity-answers/partner"):
            pid = int(path.split("/")[3])
            c.execute("SELECT role FROM profiles WHERE id = ?", (pid,))
            prof_row = c.fetchone()
            if prof_row and prof_row["role"] == "admin":
                conn.close()
                return self._send_json({"error": "Un administrateur ne répond pas aux questionnaires."}, 403)

            if "criteria" in data and isinstance(data["criteria"], list):
                criteria_list = data["criteria"]
            elif "question_id" in data:
                criteria_list = [data]
            else:
                criteria_list = []

            for crit in criteria_list:
                qid = crit.get("question_id")
                min_v = crit.get("min_val")
                max_v = crit.get("max_val")
                opts = crit.get("options", [])
                indiff = 1 if crit.get("indifferent") else 0
                if qid:
                    opts_json = json.dumps(opts) if isinstance(opts, list) else json.dumps([])
                    c.execute("""
                        INSERT INTO identity_answers_partner (profile_id, question_id, min_val, max_val, options_json, indifferent, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(profile_id, question_id) DO UPDATE SET
                            min_val = excluded.min_val,
                            max_val = excluded.max_val,
                            options_json = excluded.options_json,
                            indifferent = excluded.indifferent,
                            updated_at = CURRENT_TIMESTAMP
                    """, (pid, qid, float(min_v) if min_v not in (None, "") else None, float(max_v) if max_v not in (None, "") else None, opts_json, indiff))
            conn.commit()

            # Calcul du pourcentage de complétude partenaire mis à jour (sur les 14 caractéristiques de classe 8)
            c.execute("SELECT COUNT(*) as total FROM questions WHERE classe = 8 AND type = 'T'")
            tot_q = c.fetchone()["total"] or 14
            c.execute("""
                SELECT COUNT(DISTINCT q.sujet) as cnt 
                FROM identity_answers_partner a
                JOIN questions q ON a.question_id = q.id
                WHERE a.profile_id = ? AND (a.indifferent = 1 OR (a.min_val IS NOT NULL AND a.max_val IS NOT NULL) OR (a.options_json IS NOT NULL AND a.options_json != '[]'))
            """, (pid,))
            ans_count = c.fetchone()["cnt"]
            pct = round((ans_count / tot_q) * 100) if tot_q > 0 else 100

            conn.close()
            return self._send_json({
                "success": True,
                "ok": True,
                "saved": len(criteria_list),
                "answered": ans_count,
                "total": tot_q,
                "completion": pct,
                "partner_completion_pct": pct
            })

        # Création d'une demande d'accès ou de suppression à l'administrateur
        elif path == "/api/access-requests":
            pid = data.get("profile_id")
            target_type = data.get("target_type", "classe")
            target_value = data.get("target_value", "")
            action_type = data.get("action_type", "grant") # 'grant' (demande d'accès) ou 'revoke' (demande de suppression)
            if not pid or not target_value:
                conn.close()
                return self._send_json({"error": "Paramètres manquants."}, 400)
            if target_type == "classe":
                val_str = str(target_value).strip()
                if val_str in ("1", "Classe 1", "Classe 1 - Standards") and action_type == "revoke":
                    conn.close()
                    return self._send_json({"error": "La Classe 1 - Standards est toujours accordée et ne peut pas être retirée."}, 400)
                if val_str in ("8", "Classe 8", "Classe 8 - Identité"):
                    conn.close()
                    return self._send_json({"error": "La Classe 8 - Identité est accessible exclusivement via + sur moi et ne peut pas être retirée."}, 400)
            c.execute("""
                INSERT INTO admin_access_requests (profile_id, target_type, target_value, action_type, status)
                VALUES (?, ?, ?, ?, 'pending')
            """, (pid, target_type, str(target_value), action_type))
            req_id = c.lastrowid
            conn.commit()
            conn.close()
            msg = "Demande d'accès transmise à l'administrateur." if action_type == "grant" else "Demande de suppression d'accès transmise à l'administrateur."
            return self._send_json({"success": True, "id": req_id, "action_type": action_type, "message": msg}, 201)

        # Enregistrement de réponses au questionnaire
        elif path == "/api/answers":
            profile_id = data.get("profile_id")
            answers_list = data.get("answers", [])
            if not profile_id or not answers_list:
                conn.close()
                return self._send_json({"error": "Données incomplètes."}, 400)

            c.execute("SELECT role FROM profiles WHERE id = ?", (profile_id,))
            prof_row = c.fetchone()
            if prof_row and prof_row["role"] == "admin":
                conn.close()
                return self._send_json({"error": "Un administrateur ne répond pas aux questionnaires."}, 403)
                
            for ans in answers_list:
                c.execute("""
                    INSERT INTO answers (profile_id, question_id, axis, value)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(profile_id, question_id, axis) DO UPDATE SET
                        value = excluded.value,
                        created_at = CURRENT_TIMESTAMP
                """, (profile_id, ans["question_id"], ans["axis"], ans["value"]))
                
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "saved": len(answers_list)})

        # Calcul d'affinité (Réservé aux Abonnés et Administrateurs)
        elif path == "/api/affinity/calculate":
            p1_id = data.get("profile1_id")
            p2_id = data.get("profile2_id")
            if not p1_id or not p2_id:
                conn.close()
                return self._send_json({"error": "profile1_id et profile2_id requis."}, 400)
            
            c.execute("SELECT role FROM profiles WHERE id = ?", (p1_id,))
            prof_row = c.fetchone()
            if not prof_row:
                conn.close()
                return self._send_json({"error": "Profil demandeur introuvable."}, 404)
            
            user_role = prof_row["role"] if "role" in prof_row.keys() and prof_row["role"] else "guest"
            simulated_role = data.get("simulated_role")
            if user_role == "admin" and simulated_role in ["subscriber", "guest"]:
                user_role = simulated_role

            if user_role not in ["subscriber", "admin"]:
                conn.close()
                return self._send_json({
                    "error": "ACCES_RESTREINT",
                    "message": "Le calculateur d'affinité est réservé aux membres abonnés et administrateurs. Contactez l'administrateur pour activer votre abonnement."
                }, 403)
            
            conn.close()
            allowed_classes = data.get("allowed_classes", None)
            result = calculate_affinity(p1_id, p2_id, allowed_classes)
            status = 400 if "error" in result and result.get("error") == "FICHE_MANQUANTE" else 200
            return self._send_json(result, status)

        # Création d'une demande de match bilatérale
        elif path == "/api/match-requests":
            sender_id = data.get("sender_id")
            receiver_id = data.get("receiver_id")
            proposed_classes = data.get("proposed_classes", "ALL")
            if isinstance(proposed_classes, list):
                proposed_classes = json.dumps(proposed_classes)
            
            if not sender_id or not receiver_id:
                conn.close()
                return self._send_json({"error": "sender_id et receiver_id requis."}, 400)
            if int(sender_id) == int(receiver_id):
                conn.close()
                return self._send_json({"error": "Impossible d'envoyer une demande de match à soi-même."}, 400)
                
            # Vérifier rôles du demandeur et du destinataire
            c.execute("SELECT role FROM profiles WHERE id = ?", (sender_id,))
            p_sender = c.fetchone()
            if not p_sender or p_sender["role"] in ["guest", "admin"]:
                conn.close()
                return self._send_json({"error": "Les demandes de match sont réservées exclusivement aux membres Abonnés (hors administrateurs)."}, 403)

            c.execute("SELECT role FROM profiles WHERE id = ?", (receiver_id,))
            p_receiver = c.fetchone()
            if not p_receiver or p_receiver["role"] == "admin":
                conn.close()
                return self._send_json({"error": "Impossible d'envoyer une demande de match à un compte administrateur."}, 400)

            c.execute("""
                INSERT INTO match_requests (sender_id, receiver_id, status, proposed_classes, validated_classes)
                VALUES (?, ?, 'pending', ?, 'ALL')
            """, (sender_id, receiver_id, proposed_classes))
            req_id = c.lastrowid
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "id": req_id, "message": "Demande de match transmise avec succès !"}, 201)

        # Modification d'une question existante (POST fallback)
        elif path.startswith("/api/questions/") and len(path.split("/")) == 4:
            qid = int(path.split("/")[3])
            n_quest_lie = int(data.get("n_quest_lie", 0))
            c.execute("""
                UPDATE questions SET
                    thematique = ?,
                    sujet = ?,
                    classe = ?,
                    type = ?,
                    cible = ?,
                    texte = ?,
                    n_quest_lie = ?
                WHERE id = ?
            """, (
                data.get("thematique", "").strip(),
                data.get("sujet", "").strip(),
                int(data.get("classe", 1)),
                data.get("type", "MULTI"),
                int(data.get("cible", 0)),
                data.get("texte", "").strip(),
                n_quest_lie,
                qid
            ))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "message": "Question modifiée avec succès."})

        # Création de nouvelle question
        elif path == "/api/questions":
            cfg = data.get("config_reponses")
            cfg_str = json.dumps(cfg, ensure_ascii=False) if isinstance(cfg, (dict, list)) else (cfg if isinstance(cfg, str) else None)
            
            classe_val = int(data.get("classe", 1))
            type_val = data.get("type", "MULTI")
            if type_val == "MULTI":
                type_val = "M"
            n_quest_lie = int(data.get("n_quest_lie", 0))

            c.execute("""
                INSERT INTO questions (pack_id, cible, classe, thematique, sujet, type, texte, config_reponses, n_quest_lie)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get("pack_id", 1),
                int(data.get("cible", 0)),
                classe_val,
                data.get("thematique", "Identité" if classe_val == 8 else "").strip(),
                data.get("sujet", "Identité" if classe_val == 8 else "").strip(),
                type_val,
                data.get("texte", "").strip(),
                cfg_str,
                n_quest_lie
            ))
            qid = c.lastrowid
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "id": qid, "message": "Question créée avec succès."}, 201)

        # Validation d'une question en attente (avec choix optionnel du jeu / pack)
        elif path.startswith("/api/admin/questions/") and path.endswith("/validate"):
            parts = path.split("/")
            qid = int(parts[4])
            pack_id = data.get("pack_id")
            if pack_id is not None:
                c.execute("UPDATE questions SET status = 'validated', pack_id = ? WHERE id = ?", (int(pack_id), qid))
            else:
                c.execute("UPDATE questions SET status = 'validated' WHERE id = ?", (qid,))
            if c.rowcount == 0:
                conn.close()
                return self._send_json({"error": "Question introuvable."}, 404)
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "id": qid, "message": f"Question #{qid} validée et activée avec succès !"})

        # Validation par lot de questions en attente (avec choix optionnel du jeu / pack)
        elif path == "/api/admin/questions/validate-batch":
            action = data.get("action", "")
            ids_list = data.get("ids", [])
            pack_id = data.get("pack_id")
            
            if pack_id is not None:
                pack_val = int(pack_id)
                if action == "all":
                    c.execute("UPDATE questions SET status = 'validated', pack_id = ? WHERE status = 'pending_review'", (pack_val,))
                elif action.startswith("classe_"):
                    cl = int(action.split("_")[1])
                    c.execute("UPDATE questions SET status = 'validated', pack_id = ? WHERE status = 'pending_review' AND classe = ?", (pack_val, cl))
                elif ids_list:
                    placeholders = ",".join("?" for _ in ids_list)
                    c.execute(f"UPDATE questions SET status = 'validated', pack_id = ? WHERE id IN ({placeholders})", (pack_val,) + tuple(ids_list))
                else:
                    conn.close()
                    return self._send_json({"error": "Action ou liste d'identifiants requise."}, 400)
            else:
                if action == "all":
                    c.execute("UPDATE questions SET status = 'validated' WHERE status = 'pending_review'")
                elif action.startswith("classe_"):
                    cl = int(action.split("_")[1])
                    c.execute("UPDATE questions SET status = 'validated' WHERE status = 'pending_review' AND classe = ?", (cl,))
                elif ids_list:
                    placeholders = ",".join("?" for _ in ids_list)
                    c.execute(f"UPDATE questions SET status = 'validated' WHERE id IN ({placeholders})", tuple(ids_list))
                else:
                    conn.close()
                    return self._send_json({"error": "Action ou liste d'identifiants requise."}, 400)
            
            cnt = c.rowcount
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "count": cnt, "message": f"{cnt} question(s) validée(s) avec succès !"})

        conn.close()
        return self._send_json({"error": "Endpoint non trouvé"}, 404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        conn = get_db()
        c = conn.cursor()
        
        # Mise à jour du rôle d'un profil (Attribution par Administrateur)
        if path.startswith("/api/profiles/") and path.endswith("/role"):
            pid = int(path.split("/")[3])
            new_role = data.get("role", "").strip().lower()
            if new_role not in ["admin", "subscriber", "guest"]:
                conn.close()
                return self._send_json({"error": "Rôle invalide. Rôles permis : admin, subscriber, guest"}, 400)
            
            c.execute("UPDATE profiles SET role = ? WHERE id = ?", (new_role, pid))
            if c.rowcount == 0:
                conn.close()
                return self._send_json({"error": "Profil introuvable."}, 404)
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "message": f"Rôle mis à jour avec succès : {new_role}", "role": new_role})

        # Mise à jour des autorisations de questionnaires (Packs, Classes, Types) par Administrateur
        elif path.startswith("/api/profiles/") and path.endswith("/question-access"):
            pid = int(path.split("/")[3])
            raw_packs = data.get("allowed_packs", "ALL")
            raw_classes = data.get("allowed_classes", "ALL")
            raw_types = data.get("allowed_types", "ALL")
            
            str_packs = json.dumps(raw_packs) if isinstance(raw_packs, list) else "ALL"
            str_classes = json.dumps(raw_classes) if isinstance(raw_classes, list) else "ALL"
            str_types = json.dumps(raw_types) if isinstance(raw_types, list) else "ALL"

            c.execute("""
                INSERT INTO profile_question_access (profile_id, allowed_packs, allowed_classes, allowed_types, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(profile_id) DO UPDATE SET
                    allowed_packs = excluded.allowed_packs,
                    allowed_classes = excluded.allowed_classes,
                    allowed_types = excluded.allowed_types,
                    updated_at = CURRENT_TIMESTAMP
            """, (pid, str_packs, str_classes, str_types))
            conn.commit()
            conn.close()
            return self._send_json({
                "success": True,
                "message": "Périmètre de questionnaires mis à jour avec succès.",
                "question_access": {
                    "profile_id": pid,
                    "allowed_packs": raw_packs,
                    "allowed_classes": raw_classes,
                    "allowed_types": raw_types
                }
            })

        # Réponse à une demande de match (Acceptation / Refus avec classes convenues)
        elif path.startswith("/api/match-requests/") and path.endswith("/respond"):
            req_id = int(path.split("/")[3])
            action = data.get("action", "").lower()
            validated_classes = data.get("validated_classes", "ALL")
            if isinstance(validated_classes, list):
                validated_classes = json.dumps(validated_classes)
                
            new_status = "accepted" if action in ("accept", "accepted") else "declined"
            c.execute("""
                UPDATE match_requests
                SET status = ?, validated_classes = ?, responded_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_status, validated_classes, req_id))
            if c.rowcount == 0:
                conn.close()
                return self._send_json({"error": "Demande de match introuvable."}, 404)
            conn.commit()

            # Si accepté, calculer immédiatement le résultat d'affinité pour retour direct
            aff_result = None
            if new_status == "accepted":
                c.execute("SELECT sender_id, receiver_id FROM match_requests WHERE id = ?", (req_id,))
                row = c.fetchone()
                if row:
                    s_id, r_id = row
                    val_cl = None
                    try:
                        val_cl = json.loads(validated_classes) if validated_classes != "ALL" else None
                    except:
                        pass
                    aff_result = calculate_affinity(s_id, r_id, allowed_classes=val_cl)

            conn.close()
            val_cl_parsed = json.loads(validated_classes) if validated_classes != "ALL" else "ALL"
            resp_data = {
                "success": True,
                "status": new_status,
                "validated_classes": val_cl_parsed,
                "message": f"Demande de match {new_status} avec succès."
            }
            if aff_result:
                resp_data["affinity_result"] = aff_result
            return self._send_json(resp_data)

        # Réponse administrateur à une demande d'accès (Approbation / Refus)
        elif path.startswith("/api/access-requests/") and path.endswith("/respond"):
            req_id = int(path.split("/")[3])
            action = data.get("action", "").lower()
            new_status = "approved" if action in ("approve", "approved") else "rejected"

            c.execute("SELECT * FROM admin_access_requests WHERE id = ?", (req_id,))
            req = c.fetchone()
            if not req:
                conn.close()
                return self._send_json({"error": "Demande introuvable."}, 404)

            c.execute("""
                UPDATE admin_access_requests
                SET status = ?, responded_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_status, req_id))

            # Si approuvée, accorder ou retirer automatiquement le droit dans profile_question_access
            if new_status == "approved":
                pid = req["profile_id"]
                target_type = req["target_type"]
                target_value = req["target_value"]
                action_type = req["action_type"] if "action_type" in req.keys() and req["action_type"] else "grant"

                c.execute("SELECT allowed_packs, allowed_classes FROM profile_question_access WHERE profile_id = ?", (pid,))
                pqa = c.fetchone()
                raw_cls = pqa["allowed_classes"] if (pqa and pqa["allowed_classes"]) else "ALL"
                raw_pks = pqa["allowed_packs"] if (pqa and pqa["allowed_packs"]) else "ALL"

                if target_type == "classe":
                    import re
                    m = re.search(r'\d+', str(target_value))
                    if m:
                        cl_num = int(m.group(0))
                        c.execute("SELECT DISTINCT classe FROM questions")
                        all_classes_db = [r["classe"] for r in c.fetchall()]
                        if action_type == "revoke":
                            curr = list(all_classes_db) if raw_cls == "ALL" else list(json.loads(raw_cls))
                            if cl_num in curr and cl_num != 1:
                                curr.remove(cl_num)
                            c.execute("""
                                INSERT INTO profile_question_access (profile_id, allowed_classes) VALUES (?, ?)
                                ON CONFLICT(profile_id) DO UPDATE SET allowed_classes = excluded.allowed_classes, updated_at = CURRENT_TIMESTAMP
                            """, (pid, json.dumps(curr)))
                        else: # grant
                            if raw_cls != "ALL":
                                curr = list(json.loads(raw_cls))
                                if cl_num not in curr:
                                    curr.append(cl_num)
                                    curr.sort()
                                c.execute("""
                                    INSERT INTO profile_question_access (profile_id, allowed_classes) VALUES (?, ?)
                                    ON CONFLICT(profile_id) DO UPDATE SET allowed_classes = excluded.allowed_classes, updated_at = CURRENT_TIMESTAMP
                                """, (pid, json.dumps(curr)))

                elif target_type == "pack":
                    try:
                        import re
                        m = re.search(r'\d+', str(target_value))
                        pk_id = int(m.group(0)) if m else int(target_value)
                        c.execute("SELECT id FROM question_packs")
                        all_packs_db = [r["id"] for r in c.fetchall()]
                        if action_type == "revoke":
                            curr = list(all_packs_db) if raw_pks == "ALL" else list(json.loads(raw_pks))
                            if pk_id in curr:
                                curr.remove(pk_id)
                            c.execute("""
                                INSERT INTO profile_question_access (profile_id, allowed_packs) VALUES (?, ?)
                                ON CONFLICT(profile_id) DO UPDATE SET allowed_packs = excluded.allowed_packs, updated_at = CURRENT_TIMESTAMP
                            """, (pid, json.dumps(curr)))
                        else: # grant
                            if raw_pks != "ALL":
                                curr = list(json.loads(raw_pks))
                                if pk_id not in curr:
                                    curr.append(pk_id)
                                    curr.sort()
                                c.execute("""
                                    INSERT INTO profile_question_access (profile_id, allowed_packs) VALUES (?, ?)
                                    ON CONFLICT(profile_id) DO UPDATE SET allowed_packs = excluded.allowed_packs, updated_at = CURRENT_TIMESTAMP
                                """, (pid, json.dumps(curr)))
                    except:
                        pass

            conn.commit()
            conn.close()
            return self._send_json({"success": True, "status": new_status, "message": f"Demande {new_status} avec succès."})

        elif path.startswith("/api/questions/"):
            qid = int(path.split("/")[3])
            cfg = data.get("config_reponses")
            cfg_str = json.dumps(cfg, ensure_ascii=False) if isinstance(cfg, (dict, list)) else (cfg if isinstance(cfg, str) else None)
            
            classe_val = int(data.get("classe", 1))
            type_val = data.get("type", "MULTI")
            if type_val == "MULTI":
                type_val = "M"
            n_quest_lie = int(data.get("n_quest_lie", 0))

            c.execute("""
                UPDATE questions SET
                    thematique = ?,
                    sujet = ?,
                    classe = ?,
                    type = ?,
                    cible = ?,
                    texte = ?,
                    config_reponses = ?,
                    n_quest_lie = ?
                WHERE id = ?
            """, (
                data.get("thematique", "Identité" if classe_val == 8 else "").strip(),
                data.get("sujet", "Identité" if classe_val == 8 else "").strip(),
                classe_val,
                type_val,
                int(data.get("cible", 0)),
                data.get("texte", "").strip(),
                cfg_str,
                n_quest_lie,
                qid
            ))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "message": "Question modifiée avec succès."})
            
        conn.close()
        return self._send_json({"error": "Endpoint non trouvé"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/profiles/"):
            pid = int(path.split("/")[3])
            conn = get_db()
            c = conn.cursor()
            c.execute("DELETE FROM profiles WHERE id = ?", (pid,))
            c.execute("DELETE FROM identity_cards WHERE profile_id = ?", (pid,))
            c.execute("DELETE FROM answers WHERE profile_id = ?", (pid,))
            c.execute("DELETE FROM identity_answers_self WHERE profile_id = ?", (pid,))
            c.execute("DELETE FROM identity_answers_partner WHERE profile_id = ?", (pid,))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "deleted_id": pid})
        elif path.startswith("/api/questions/"):
            qid = int(path.split("/")[3])
            conn = get_db()
            c = conn.cursor()
            c.execute("DELETE FROM questions WHERE id = ?", (qid,))
            c.execute("DELETE FROM answers WHERE question_id = ?", (qid,))
            c.execute("DELETE FROM identity_answers_self WHERE question_id = ?", (qid,))
            c.execute("DELETE FROM identity_answers_partner WHERE question_id = ?", (qid,))
            conn.commit()
            conn.close()
            return self._send_json({"success": True, "deleted_id": qid})
        return self._send_json({"error": "Non supporté"}, 404)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

def run():
    init_db()
    print(f"=== AFFINITY SERVEUR PRÊT ===")
    print(f"Écoute sur http://localhost:{PORT}")
    server = ThreadedTCPServer(("", PORT), AffinityHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
