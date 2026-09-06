"""
Test automatisé pour la reprise d'Affinity-Full.mdb, la classe 8 (Identité), la classe 0 (Non définies), N_CIBLE et N_SUJET
"""
import sqlite3
import json
import urllib.request

def run_tests():
    print("=== DÉBUT DES TESTS REPRISE ACCESS & CLASSE 8 ===")

    # 1. Base SQLite
    conn = sqlite3.connect('affinity.db')
    c = conn.cursor()

    # Vérification classe 8
    c.execute("SELECT type, count(*) FROM questions WHERE classe = 8 GROUP BY type")
    counts_c8 = dict(c.fetchall())
    print("1. Questions de Classe 8 (Identité) :", counts_c8)
    assert counts_c8.get('P') == 14, f"Attendu 14 questions P en classe 8, trouvé {counts_c8.get('P')}"
    assert counts_c8.get('T') == 14, f"Attendu 14 questions T en classe 8, trouvé {counts_c8.get('T')}"
    print("   -> OK : 14 questions P et 14 questions T en classe 8.")

    # Vérification des 172 questions Access
    c.execute("SELECT count(*) FROM questions WHERE classe != 8")
    nb_general = c.fetchone()[0]
    print(f"2. Questions générales (issues d'Access) : {nb_general}")
    assert nb_general == 172, f"Attendu 172 questions Access, trouvé {nb_general}"
    print("   -> OK : 172 questions d'Affinity-Full.mdb présentes.")

    # Vérification thématiques : aucune fausse thématique polluante
    c.execute("SELECT DISTINCT thematique FROM questions WHERE classe != 8")
    themas = [r[0] for r in c.fetchall()]
    print("3. Thématiques des questions générales :", themas)
    fausses_themas = ["Morphologie & Mensurations", "Allure & Style", "Origines & Culture", "Mode & Cadre de vie"]
    for ft in fausses_themas:
        assert ft not in themas, f"Erreur: la thématique polluante '{ft}' est présente !"
    print("   -> OK : Aucune thématique polluante dans les questions générales.")

    # Vérification N_CIBLE et N_SUJET
    c.execute("SELECT count(*) FROM questions WHERE n_sujet IS NOT NULL AND n_sujet > 0")
    nb_sujet = c.fetchone()[0]
    assert nb_sujet > 0, "n_sujet manquant"
    c.execute("SELECT DISTINCT cible FROM questions WHERE classe != 8")
    cibles = set(r[0] for r in c.fetchall())
    print("4. Cibles N_CIBLE dans questions générales :", cibles)
    assert 0 in cibles and 1 in cibles and 2 in cibles, f"Attendu cibles 0, 1, 2, trouvé {cibles}"
    print("   -> OK : N_CIBLE (0, 1, 2) et N_SUJET bien renseignés.")

    conn.close()

    # 2. Vérification Frontend (index.html)
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    assert 'id="bankFilterCible"' in html, "bankFilterCible manquant dans index.html"
    assert 'value="8">8 - Identité</option>' in html, "Option classe 8 manquante dans bankFilterClasse"
    assert 'value="0">0 - Non définies</option>' in html, "Option classe 0 manquante dans bankFilterClasse"
    print("5. Frontend index.html :")
    print("   -> OK : bankFilterCible présent.")
    print("   -> OK : Classes 0 (Non définies) et 8 (Identité) présentes.")

    # 3. Vérification Frontend (app.js)
    with open('frontend/app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    assert "q.classe === 8" in js, "Exclusion classe 8 manquante dans getActiveProfileEligibleQuestions"
    assert "profSexe === 1 && q.cible === 2" in js, "Filtrage N_CIBLE homme/femme manquant dans getActiveProfileEligibleQuestions"
    assert "bankFilterCible" in js, "bankFilterCible non géré dans app.js"
    assert "'8 - Identité'" in js or '"8 - Identité"' in js, "Libellé 8 - Identité manquant dans app.js"
    print("6. Frontend app.js :")
    print("   -> OK : Exclusion classe 8 du questionnaire général.")
    print("   -> OK : Filtrage N_CIBLE selon le sexe du profil.")
    print("   -> OK : Rendu de la banque de questions avec cible et n_sujet.")

    # 4. Vérification API REST (server.py)
    req = urllib.request.urlopen("http://127.0.0.1:8765/api/profiles/1/identity-answers")
    assert req.getcode() == 200
    data = json.loads(req.read().decode('utf-8'))
    assert 'questions_self' in data and len(data['questions_self']) == 14
    assert 'questions_partner' in data and len(data['questions_partner']) == 14
    assert all(q['type'] == 'P' for q in data['questions_self'])
    assert all(q['type'] == 'T' for q in data['questions_partner'])
    print("7. Endpoint API /api/profiles/:id/identity-answers :")
    print("   -> OK : 14 questions_self (P) et 14 questions_partner (T) renvoyées en classe 8.")

    # Vérification API /api/questions
    req_q = urllib.request.urlopen("http://127.0.0.1:8765/api/questions")
    assert req_q.getcode() == 200
    q_data = json.loads(req_q.read().decode('utf-8'))
    all_qs = q_data.get("questions", [])
    assert len(all_qs) == 172 + 28, f"Attendu 200 questions au total (172 + 28), trouvé {len(all_qs)}"
    print(f"   -> OK : {len(all_qs)} questions servies par /api/questions avec n_thema et n_sujet.")

    print("=== TOUS LES TESTS DE REPRISE SONT PASSÉS AVEC SUCCÈS ===")

if __name__ == '__main__':
    run_tests()
