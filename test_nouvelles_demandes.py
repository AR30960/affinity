import urllib.request
import urllib.parse
import json
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_URL = "http://127.0.0.1:8765"

def http_get(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        data = resp.read().decode('utf-8')
        return resp.status, json.loads(data)

def http_post(url, payload, headers=None):
    data = json.dumps(payload).encode('utf-8')
    h = {'Content-Type': 'application/json'}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return e.code, json.loads(body) if body else {}

def test_validation_and_bank():
    print("\n--- Test 1 : Validation de questions et présence dans la banque active ---")
    status, data = http_get(f"{BASE_URL}/api/questions")
    assert status == 200, f"Erreur GET /api/questions: {status}"
    initial_qs = data["questions"]
    initial_count = len(initial_qs)
    print(f"Nombre initial de questions dans la banque active : {initial_count}")

    status_pend, data_pend = http_get(f"{BASE_URL}/api/admin/questions/pending")
    assert status_pend == 200, f"Erreur GET pending: {status_pend}"
    pending_qs = data_pend["questions"]
    print(f"Nombre de questions en attente d'arbitrage : {len(pending_qs)}")

    if len(pending_qs) > 0:
        target_q = pending_qs[0]
        qid = target_q["id"]
        print(f"Validation unitaire de la question #{qid} ({target_q['thematique']} - {target_q['sujet']}) dans le Jeu 3...")
        status_val, data_val = http_post(f"{BASE_URL}/api/admin/questions/{qid}/validate", {"pack_id": 3})
        assert status_val == 200, f"Erreur validation: {status_val} - {data_val}"
        print(f"Validation unitaire réussie: {data_val}")

        status_after, data_after = http_get(f"{BASE_URL}/api/questions")
        assert status_after == 200
        after_qs = data_after["questions"]
        found = any(q["id"] == qid for q in after_qs)
        assert found, f"La question #{qid} validée n'a pas été trouvée dans la banque active !"
        print(f"✅ SUCCÈS : La question #{qid} est immédiatement présente et visible dans la banque active ({len(after_qs)} questions) !")

def test_registration_without_email_and_profile_email():
    print("\n--- Test 2 : Inscription sans email & Ajout email dans Mon Profil ---")
    test_pseudo = "MembreSansEmailTest"
    test_pwd = "monSecret123"
    test_email = "membre.test@affinity.com"

    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    c.execute("DELETE FROM profiles WHERE pseudo = ?", (test_pseudo,))
    conn.commit()
    conn.close()

    # 1. Inscription avec uniquement pseudo et mot de passe (sans email)
    status_reg, data_reg = http_post(f"{BASE_URL}/api/auth/register", {
        "pseudo": test_pseudo,
        "password": test_pwd
    })
    assert status_reg == 201, f"Erreur inscription: {status_reg} - {data_reg}"
    profile = data_reg["profile"]
    pid = profile["id"]
    token = data_reg["token"]
    print(f"✅ Inscription réussie sans e-mail pour #{pid} ({profile['pseudo']}) - Rôle: {profile['role']}")
    assert profile.get("email") is None or profile.get("email") == "", "L'e-mail ne devrait pas être renseigné à l'inscription !"

    # 2. Sauvegarde de l'adresse email dans Mon Profil (POST /api/profiles/:id/identity)
    headers = {"Authorization": f"Bearer {token}"}
    status_id, data_id = http_post(f"{BASE_URL}/api/profiles/{pid}/identity", {
        "pseudo": test_pseudo,
        "email": test_email,
        "prenom": "Jean",
        "nom": "Dupont",
        "sexe": 1,
        "date_naissance": "1990-05-15",
        "habite_pays": "France",
        "habite_region_dept": "75 - Paris",
        "habite_commune": "Paris",
        "recherche_de": "Échanges et Amitié",
        "bio": "Membre passionné de relations sincères."
    }, headers=headers)
    assert status_id == 200, f"Erreur sauvegarde profil: {status_id} - {data_id}"
    print(f"✅ Enregistrement dans Mon Profil réussi avec e-mail {test_email} !")

    # 3. Vérifier que le profil a bien l'email enregistré
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    c.execute("SELECT email FROM profiles WHERE id = ?", (pid,))
    saved_email = c.fetchone()[0]
    conn.close()
    assert saved_email == test_email, f"L'email en base {saved_email} ne correspond pas à {test_email}"
    print(f"✅ SUCCÈS : L'email {saved_email} est bien enregistré dans le profil #{pid} !")

    # 4. Tester la récupération de mot de passe avec cet e-mail
    status_forgot, data_forgot = http_post(f"{BASE_URL}/api/auth/forgot-password", {
        "login_or_email": test_email
    })
    assert status_forgot == 200, f"Erreur forgot-password: {status_forgot} - {data_forgot}"
    assert data_forgot["success"] is True
    print(f"✅ SUCCÈS : Mot de passe oublié fonctionne avec l'email renseigné dans Mon Profil ! Code généré: {data_forgot['reset_code']}")

if __name__ == "__main__":
    test_validation_and_bank()
    test_registration_without_email_and_profile_email()
    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
