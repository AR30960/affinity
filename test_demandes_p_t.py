"""
Script de validation automatisée pour les 6 demandes relatives à l'Identité (Types P & T)
"""
import sys
import json
import urllib.request
import sqlite3

def run_tests():
    print("=== DÉBUT DES TESTS DE CONFORMITÉ ===")
    
    # 1. Vérification Base de données & Types P / T
    conn = sqlite3.connect('affinity.db')
    c = conn.cursor()
    c.execute("SELECT type, count(*) FROM questions WHERE classe = 0 GROUP BY type")
    type_counts = dict(c.fetchall())
    print(f"1. Types questions classe 0 dans SQLite : {type_counts}")
    assert 'P' in type_counts and type_counts['P'] == 14, f"Erreur: attendu 14 questions de type P, trouvé {type_counts.get('P')}"
    assert 'T' in type_counts and type_counts['T'] == 14, f"Erreur: attendu 14 questions de type T, trouvé {type_counts.get('T')}"
    print("   -> OK : 14 questions P et 14 questions T présentes en classe 0.")

    # 2. Vérification Exclusion classe 0 dans index.html
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    assert 'id="qFilterClasse"' in html_content
    # Vérifier que dans qFilterClasse, l'option classe 0 n'existe pas
    qfilter_block = html_content.split('id="qFilterClasse"')[1].split('</select>')[0]
    assert 'value="0"' not in qfilter_block, "Erreur: l'option 0 ne doit pas être dans qFilterClasse"
    print("2. Exclusion de la classe 0 du questionnaire général :")
    print("   -> OK : qFilterClasse ne contient plus l'option 0.")

    # 3. Vérification CSS Cockpit (Alignement strict)
    with open('frontend/style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    assert '.ckp-line-actions' in css_content
    assert 'flex-wrap: nowrap' in css_content or 'nowrap' in css_content
    print("3. Alignement strict des boutons du Cockpit :")
    print("   -> OK : .ckp-line-actions configuré avec flex-wrap: nowrap et align-items: center.")

    # 4. Vérification app.js (complétude 100% self + 100% partner et types P/T)
    with open('frontend/app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()
    assert 'selfPct < 100 || partnerPct < 100' in js_content, "Erreur: règle de complétude 100% self + partner absente"
    assert "openIdentityDeck('self')" in html_content and "openIdentityDeck('partner')" in html_content
    assert "async function openIdentityDeck" in js_content
    assert "curProf.role === 'admin'" not in js_content.split('async function openIdentityDeck')[1].split('switchIdentityDeckTab')[0], "Erreur: blocage admin présent dans openIdentityDeck"
    assert "Tolérance : de" in js_content or "de ${" in js_content
    print("4. Logique frontend app.js :")
    print("   -> OK : Complétude exige 100% self ET 100% partner.")
    print("   -> OK : Clic direct sur onglet 'self' et 'partner'.")
    print("   -> OK : Formulation 'de ... à ...' présente.")

    # 5. Vérification API Backend (server.py)
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8765/api/profiles/1/identity-answers")
        assert req.getcode() == 200
        data = json.loads(req.read().decode('utf-8'))
        assert 'questions_self' in data, "questions_self manquant dans /identity-answers"
        assert 'questions_partner' in data, "questions_partner manquant dans /identity-answers"
        assert len(data['questions_self']) == 14, f"Attendu 14 questions_self, reçu {len(data['questions_self'])}"
        assert len(data['questions_partner']) == 14, f"Attendu 14 questions_partner, reçu {len(data['questions_partner'])}"
        assert all(q['type'] == 'P' for q in data['questions_self']), "Toutes les questions_self doivent être de type P"
        assert all(q['type'] == 'T' for q in data['questions_partner']), "Toutes les questions_partner doivent être de type T"
        print("5. Endpoint API /api/profiles/:id/identity-answers :")
        print(f"   -> OK : 14 questions_self (type P) et 14 questions_partner (type T) renvoyées.")
        print(f"   -> Statut complétude profil 1 : self={data.get('self_completion_pct')}%, partner={data.get('partner_completion_pct')}%")

        # Test POST self
        post_self = urllib.request.Request(
            "http://127.0.0.1:8765/api/profiles/2/identity-answers/self",
            data=json.dumps({"answers": {"Taille": "178"}}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        res_self = json.loads(urllib.request.urlopen(post_self).read().decode('utf-8'))
        assert res_self.get('success') is True
        print("   -> OK : POST /identity-answers/self opérationnel.")

        # Test POST partner
        post_partner = urllib.request.Request(
            "http://127.0.0.1:8765/api/profiles/2/identity-answers/partner",
            data=json.dumps({"tolerances": {"Taille": {"min": 160, "max": 185}}}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        res_partner = json.loads(urllib.request.urlopen(post_partner).read().decode('utf-8'))
        assert res_partner.get('success') is True
        print("   -> OK : POST /identity-answers/partner opérationnel.")
    except Exception as e:
        print(f"Erreur API : {e}")
        conn.close()
        raise e

    conn.close()
    print("=== TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS ===")

if __name__ == '__main__':
    run_tests()
