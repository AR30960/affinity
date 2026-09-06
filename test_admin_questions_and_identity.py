import urllib.request
import json
import sqlite3
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

API_BASE = "http://localhost:8765"

def test_classe8_purity():
    print("\n--- TEST 1: Pureté de la Classe 8 (Thématique=Identité, Sujet=Identité, Pas de sujets fictifs) ---")
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    rows = c.execute("SELECT id, thematique, sujet, classe, type, cible, config_reponses FROM questions WHERE classe = 8").fetchall()
    conn.close()

    assert len(rows) > 0, "Aucune question de classe 8 trouvée"
    for r in rows:
        qid, th, sj, cl, tp, cb, cfg = r
        assert th == "Identité", f"Question #{qid} a une thématique '{th}' au lieu de 'Identité'"
        assert sj == "Identité", f"Question #{qid} a un sujet '{sj}' au lieu de 'Identité'"
        assert cl == 8, f"Question #{qid} a classe {cl} au lieu de 8"
        assert tp in ('P', 'T'), f"Question #{qid} a type '{tp}' au lieu de P ou T"
        assert cb in (0, 1, 2), f"Question #{qid} a cible {cb} invalide"
        assert cfg is not None and len(cfg) > 0, f"Question #{qid} n'a pas de config_reponses"
        cfg_obj = json.loads(cfg)
        assert cfg_obj.get("mode") in ("numeric", "select"), f"Question #{qid} a un mode de réponse invalide: {cfg_obj.get('mode')}"
    print(f"✓ {len(rows)} questions de classe 8 vérifiées avec succès (100% Thématique=Identité et Sujet=Identité).")

def test_admin_crud_api():
    print("\n--- TEST 2: API Admin - Création, Modification et Suppression de Question avec Réponses Précises ---")
    # 1. Création
    new_q = {
        "pack_id": 1,
        "classe": 8,
        "type": "P",
        "cible": 0,
        "thematique": "Identité",
        "sujet": "Identité",
        "texte": "Test Question Automatique - Couleur préférée de tenue ?",
        "config_reponses": {
            "mode": "select",
            "options": ["Noir", "Blanc", "Bleu", "Rouge", "Vert", "Autre"]
        }
    }
    req = urllib.request.Request(
        f"{API_BASE}/api/questions",
        data=json.dumps(new_q).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        assert res.get("success") is True
        created_id = res.get("id")
        assert created_id is not None
        print(f"✓ Question créée avec succès via POST /api/questions (ID: #{created_id})")

    # Vérification en base
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    row = c.execute("SELECT id, thematique, sujet, config_reponses FROM questions WHERE id = ?", (created_id,)).fetchone()
    assert row is not None
    assert row[1] == "Identité"
    assert row[2] == "Identité"
    cfg = json.loads(row[3])
    assert cfg["mode"] == "select"
    assert "Noir" in cfg["options"]
    print(f"✓ Données et config_reponses confirmées en base SQLite pour #{created_id}")

    # 2. Modification
    updated_q = {
        "pack_id": 1,
        "classe": 8,
        "type": "P",
        "cible": 1, # passage en cible homme
        "thematique": "Identité",
        "sujet": "Identité",
        "texte": "Test Question Automatique - Longueur de barbe (cm) ?",
        "config_reponses": {
            "mode": "numeric",
            "unit": "cm",
            "min": 0,
            "max": 30,
            "step": 0.5
        }
    }
    req_put = urllib.request.Request(
        f"{API_BASE}/api/questions/{created_id}",
        data=json.dumps(updated_q).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(req_put) as resp:
        res_put = json.loads(resp.read().decode('utf-8'))
        assert res_put.get("success") is True
        print(f"✓ Question modifiée avec succès via PUT /api/questions/{created_id}")

    # Vérification mise à jour en base
    row_mod = c.execute("SELECT cible, config_reponses FROM questions WHERE id = ?", (created_id,)).fetchone()
    assert row_mod[0] == 1 # cible homme
    cfg_mod = json.loads(row_mod[1])
    assert cfg_mod["mode"] == "numeric"
    assert cfg_mod["unit"] == "cm"
    print(f"✓ Mise à jour du mode numérique confirmée en base SQLite")

    # 3. Suppression
    req_del = urllib.request.Request(
        f"{API_BASE}/api/questions/{created_id}",
        method="DELETE"
    )
    with urllib.request.urlopen(req_del) as resp:
        res_del = json.loads(resp.read().decode('utf-8'))
        assert res_del.get("success") is True
        print(f"✓ Question supprimée avec succès via DELETE /api/questions/{created_id}")

    row_del = c.execute("SELECT id FROM questions WHERE id = ?", (created_id,)).fetchone()
    assert row_del is None
    conn.close()
    print(f"✓ Suppression définitive confirmée en base SQLite")

def test_identity_filtering_by_sex():
    print("\n--- TEST 3: Filtrage selon le Sexe du Profil (+ sur moi) & Enrichissement Dynamique ---")
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    
    # S'assurer d'avoir un profil Homme (sexe = 1) et un profil Femme (sexe = 2)
    c.execute("UPDATE identity_cards SET sexe = 1 WHERE profile_id = 1") # Anji Homme
    c.execute("SELECT profile_id FROM identity_cards WHERE sexe = 2 LIMIT 1")
    femme_row = c.fetchone()
    if not femme_row:
        c.execute("UPDATE identity_cards SET sexe = 2 WHERE profile_id = 2")
        femme_id = 2
    else:
        femme_id = femme_row[0]
    conn.commit()
    conn.close()

    # 1. Requête pour Homme (ID 1)
    with urllib.request.urlopen(f"{API_BASE}/api/profiles/1/identity-answers") as resp:
        data_h = json.loads(resp.read().decode('utf-8'))
        qs_self_h = data_h["questions_self"]
        cibles_h = [q.get("cible", 0) for q in qs_self_h]
        assert 2 not in cibles_h, "Un profil homme ne doit pas recevoir de question réservée aux femmes (cible = 2)"
        assert 1 in cibles_h, "Un profil homme doit recevoir les questions spécifiques homme (cible = 1 : barbe/pilosité)"
        # Vérifier enrichissement
        for q in qs_self_h:
            assert "kind" in q and q["kind"] in ("numeric", "select")
            if q["kind"] == "select":
                assert isinstance(q["options"], list) and len(q["options"]) > 0
            if q["kind"] == "numeric":
                assert "min" in q and "max" in q
        print(f"✓ Profil Homme (ID 1) : {len(qs_self_h)} questions éligibles (aucune question femme cible 2, questions barbe incluses).")

    # 2. Requête pour Femme
    with urllib.request.urlopen(f"{API_BASE}/api/profiles/{femme_id}/identity-answers") as resp:
        data_f = json.loads(resp.read().decode('utf-8'))
        qs_self_f = data_f["questions_self"]
        cibles_f = [q.get("cible", 0) for q in qs_self_f]
        assert 1 not in cibles_f, "Un profil femme ne doit pas recevoir de question réservée aux hommes (cible = 1)"
        assert 2 in cibles_f, "Un profil femme doit recevoir les questions spécifiques femme (cible = 2 : bonnet de poitrine)"
        print(f"✓ Profil Femme (ID {femme_id}) : {len(qs_self_f)} questions éligibles (aucune question homme cible 1, questions bonnet incluses).")

if __name__ == "__main__":
    test_classe8_purity()
    test_admin_crud_api()
    test_identity_filtering_by_sex()
    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
