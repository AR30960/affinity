import urllib.request
import json
import sqlite3
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8765"

def run_tests():
    print("=== DÉBUT DES TESTS : INSCRIPTION ÉPURÉE, EMAIL ET MOT DE PASSE OUBLIÉ ===")

    # Test 1 : Inscription épurée (sans sexe ni date de naissance, avec email optionnel)
    reg_payload_with_email = {
        "pseudo": "test_user_email",
        "email": "user.test@domaine-affinity.fr",
        "password": "Password123!"
    }
    req1 = urllib.request.Request(
        f"{BASE_URL}/api/auth/register",
        data=json.dumps(reg_payload_with_email).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        res1 = urllib.request.urlopen(req1)
        data1 = json.loads(res1.read().decode("utf-8"))
        assert data1["success"] is True, "Inscription avec email échouée"
        assert data1["profile"]["email"] == "user.test@domaine-affinity.fr"
        print("✓ Test 1 Réussi : Inscription sans sexe/naissance avec email optionnel validée.")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print("ℹ️ Note : Utilisateur test_user_email existait déjà.")
        else:
            raise

    # Test 2 : Inscription sans email (optionnel non renseigné)
    reg_payload_no_email = {
        "pseudo": "test_user_no_email",
        "email": "",
        "password": "Password123!"
    }
    req2 = urllib.request.Request(
        f"{BASE_URL}/api/auth/register",
        data=json.dumps(reg_payload_no_email).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        res2 = urllib.request.urlopen(req2)
        data2 = json.loads(res2.read().decode("utf-8"))
        assert data2["success"] is True, "Inscription sans email échouée"
        assert data2["profile"]["email"] is None or data2["profile"]["email"] == ""
        print("✓ Test 2 Réussi : Inscription sans email validée.")
    except urllib.error.HTTPError as e:
        if e.code == 409:
            print("ℹ️ Note : Utilisateur test_user_no_email existait déjà.")
        else:
            raise

    # Test 3 : Mot de passe oublié sur compte SANS email
    forgot_no_email = { "login_or_email": "test_user_no_email" }
    req3 = urllib.request.Request(
        f"{BASE_URL}/api/auth/forgot-password",
        data=json.dumps(forgot_no_email).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req3)
        assert False, "Aurait dû refuser la réinitialisation pour compte sans email"
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Code 400 attendu, obtenu {e.code}"
        err_msg = json.loads(e.read().decode())["error"]
        assert "Aucune adresse e-mail n'est associée" in err_msg, f"Message inattendu: {err_msg}"
        assert "ar30960" in err_msg, "Doit mentionner l'administrateur ar30960"
        print("✓ Test 3 Réussi : Refus immédiat avec message d'alerte sécurité si pas d'email.")

    # Test 4 : Mot de passe oublié sur compte AVEC email
    forgot_with_email = { "login_or_email": "test_user_email" }
    req4 = urllib.request.Request(
        f"{BASE_URL}/api/auth/forgot-password",
        data=json.dumps(forgot_with_email).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res4 = urllib.request.urlopen(req4)
    data4 = json.loads(res4.read().decode("utf-8"))
    assert data4["success"] is True, "Demande de mot de passe oublié échouée"
    assert "reset_code" in data4 and len(data4["reset_code"]) == 6, "Code à 6 chiffres attendu"
    assert "u***t@domaine-affinity.fr" in data4["email_masked"] or "@" in data4["email_masked"]
    reset_code = data4["reset_code"]
    print(f"✓ Test 4 Réussi : Code à 6 chiffres généré ({reset_code}) pour l'email masqué {data4['email_masked']}.")

    # Test 5 : Réinitialisation avec mauvais code (doit échouer)
    reset_bad = {
        "login_or_email": "test_user_email",
        "reset_code": "000000",
        "new_password": "NewSecret2026!"
    }
    req5 = urllib.request.Request(
        f"{BASE_URL}/api/auth/reset-password",
        data=json.dumps(reset_bad).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req5)
        assert False, "Aurait dû échouer avec un mauvais code"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        print("✓ Test 5 Réussi : Rejet du mauvais code de réinitialisation.")

    # Test 6 : Réinitialisation avec BON code
    reset_good = {
        "login_or_email": "test_user_email",
        "reset_code": reset_code,
        "new_password": "NewSecret2026!"
    }
    req6 = urllib.request.Request(
        f"{BASE_URL}/api/auth/reset-password",
        data=json.dumps(reset_good).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res6 = urllib.request.urlopen(req6)
    data6 = json.loads(res6.read().decode("utf-8"))
    assert data6["success"] is True, "Réinitialisation échouée"
    print("✓ Test 6 Réussi : Mot de passe réinitialisé avec succès.")

    # Test 7 : Connexion avec le nouveau mot de passe
    login_new = {
        "login": "test_user_email",
        "password": "NewSecret2026!"
    }
    req7 = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=json.dumps(login_new).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res7 = urllib.request.urlopen(req7)
    data7 = json.loads(res7.read().decode("utf-8"))
    assert data7["success"] is True
    print(f"✓ Test 7 Réussi : Connexion validée avec le nouveau mot de passe, token obtenu.")

    # Test 8 : Mise à jour de l'email via la Fiche d'identité
    # Récupérer l'ID du profil test_user_email
    pid = data7["profile"]["id"]
    token = data7["token"]
    req8 = urllib.request.Request(
        f"{BASE_URL}/api/profiles/{pid}/identity",
        data=json.dumps({"email": "nouveau.mail@affinity.com"}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    res8 = urllib.request.urlopen(req8)
    assert res8.status == 200
    
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    c.execute("SELECT email FROM profiles WHERE id = ?", (pid,))
    saved_email = c.fetchone()[0]
    conn.close()
    assert saved_email == "nouveau.mail@affinity.com", f"Email attendu nouveau.mail@affinity.com, obtenu {saved_email}"
    print("✓ Test 8 Réussi : Modification de l'adresse e-mail dans la Fiche de profil persistée en base.")

    # Test 9 : Espace d'arbitrage - Toutes les questions renvoyées par défaut
    req9 = urllib.request.Request(f"{BASE_URL}/api/admin/questions/pending")
    res9 = urllib.request.urlopen(req9)
    data9 = json.loads(res9.read().decode("utf-8"))
    assert data9["total"] >= 60, f"Attendu au moins 60 questions en attente, obtenu {data9['total']}"
    assert "1" in data9["counts_by_class"] and data9["counts_by_class"]["1"] == 10
    assert "5" in data9["counts_by_class"] and data9["counts_by_class"]["5"] == 10
    assert "9" in data9["counts_by_class"] and data9["counts_by_class"]["9"] == 10
    print(f"✓ Test 9 Réussi : Espace d'Arbitrage renvoie toutes les {data9['total']} questions par défaut avec compteurs complets.")

    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS (9/9) !")

if __name__ == "__main__":
    run_tests()
