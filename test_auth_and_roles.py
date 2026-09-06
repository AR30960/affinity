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
    print("=== DÉBUT DES TESTS AUTHENTIFICATION & RÔLES ===")

    # Test 1 : Vérification compte admin ar30960 dans SQLite
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    c.execute("SELECT id, pseudo, code_profil, role, password_hash, salt FROM profiles WHERE id = 1")
    admin_row = c.fetchone()
    assert admin_row is not None, "Profil 1 introuvable"
    assert admin_row[1] == "ar30960", f"Pseudo attendu 'ar30960', obtenu: {admin_row[1]}"
    assert admin_row[2] == "ADM-1", f"Code profil attendu 'ADM-1', obtenu: {admin_row[2]}"
    assert admin_row[3] == "admin", f"Rôle attendu 'admin', obtenu: {admin_row[3]}"
    print("✓ Test 1 Réussi : Profil 1 est bien ar30960 (ADM-1, admin).")

    # Test 2 : Connexion Admin échouée (mauvais mot de passe)
    req_bad = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=json.dumps({"login": "ar30960", "password": "MauvaisMotDePasse!"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req_bad)
        assert False, "La connexion aurait dû échouer avec un mauvais mot de passe"
    except urllib.error.HTTPError as e:
        assert e.code == 401, f"Code 401 attendu, obtenu {e.code}"
        print("✓ Test 2 Réussi : Connexion refusée avec code 401 pour mauvais mot de passe.")

    # Test 3 : Connexion Admin réussie (Admin2026!)
    req_ok = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=json.dumps({"login": "ar30960", "password": "Admin2026!"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req_ok)
    data = json.loads(res.read().decode("utf-8"))
    assert data.get("success") is True, "Connexion admin échouée"
    token = data.get("token")
    assert token and len(token) >= 32, "Jeton de session invalide"
    assert data["profile"]["role"] == "admin"
    print(f"✓ Test 3 Réussi : Connexion réussie pour ar30960, jeton reçu.")

    # Test 4 : Vérification session active via /api/auth/me
    req_me = urllib.request.Request(
        f"{BASE_URL}/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    res_me = urllib.request.urlopen(req_me)
    data_me = json.loads(res_me.read().decode("utf-8"))
    assert data_me["user"]["pseudo"] == "ar30960"
    print("✓ Test 4 Réussi : /api/auth/me valide le profil ar30960 avec le jeton Bearer.")

    # Test 5 : Inscription d'un nouveau profil invité
    unique_pseudo = "TestGuestWeb"
    c.execute("DELETE FROM profiles WHERE pseudo = ?", (unique_pseudo,))
    conn.commit()
    conn.close()

    req_reg = urllib.request.Request(
        f"{BASE_URL}/api/auth/register",
        data=json.dumps({
            "pseudo": unique_pseudo,
            "password": "Password123!",
            "sexe": 1,
            "date_naissance": "1995-06-15"
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res_reg = urllib.request.urlopen(req_reg)
    data_reg = json.loads(res_reg.read().decode("utf-8"))
    assert data_reg.get("success") is True
    assert data_reg["profile"]["role"] == "guest"
    guest_token = data_reg.get("token")
    print("✓ Test 5 Réussi : Nouveau profil invité TestGuestWeb inscrit avec rôle 'guest'.")

    # Test 6 : Déconnexion du jeton
    req_logout = urllib.request.Request(
        f"{BASE_URL}/api/auth/logout",
        data=b"{}",
        headers={"Authorization": f"Bearer {guest_token}", "Content-Type": "application/json"}
    )
    urllib.request.urlopen(req_logout)
    # Après déconnexion, /api/auth/me doit renvoyer 401
    try:
        req_check = urllib.request.Request(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {guest_token}"}
        )
        urllib.request.urlopen(req_check)
        assert False, "Le jeton révoqué aurait dû être rejeté"
    except urllib.error.HTTPError as e:
        assert e.code == 401
        print("✓ Test 6 Réussi : Déconnexion effective, jeton révoqué.")

    # Test 7 : Vérification des questions synthétiques (Classes 1, 2, 3, 4, 5, 9)
    conn = sqlite3.connect("affinity.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions WHERE id BETWEEN 50001 AND 50100 OR id BETWEEN 90001 AND 90050")
    old_ai_count = c.fetchone()[0]
    assert old_ai_count == 0, f"Les anciennes questions IA doivent être supprimées (trouvé: {old_ai_count})"
    
    for cl in [1, 2, 3, 4, 5, 9]:
        c.execute("SELECT COUNT(*) FROM questions WHERE classe = ? AND id >= 10000", (cl,))
        cnt = c.fetchone()[0]
        assert cnt >= 10, f"Classe {cl} devrait avoir au moins 10 questions directes (obtenu: {cnt})"
    print("✓ Test 7 Réussi : 100% des anciennes questions longues supprimées, 10 questions directes par classe présentes.")
    conn.close()

    print("\n TOUS LES TESTS AUTHENTIFICATION & QUESTIONS ONT RÉUSSI AVEC SUCCÈS !")

if __name__ == "__main__":
    run_tests()
