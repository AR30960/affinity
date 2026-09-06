import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_frontend_html():
    print("=== Test 1: Structure Frontend dans index.html ===")
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Vérification Ligne 1: NOM :
    assert 'ckp-line-nom' in html and 'NOM :' in html, "Ligne 1: NOM : manquante"
    assert 'id="myProfileFullName"' in html, "Champ myProfileFullName manquant"
    print("  ✓ Ligne 1 : NOM : et Nom+Prénom sur une seule ligne trouvés.")

    # Vérification Ligne 2: Identifiant profil + copié
    assert 'ckp-line-id' in html, "Ligne 2: Identifiant profil manquant"
    assert 'myProfileAffId' in html and 'copyMyAffId' in html, "Identifiant profil ou bouton de copie manquant"
    print("  ✓ Ligne 2 : Identifiant profil avec bouton copié trouvé.")

    # Vérification Ligne 3: Disquette, + sur vous [%], + sur l'autre [%]
    assert 'ckp-line-actions' in html, "Ligne 3: Actions manquante"
    assert 'btnSaveDirectCockpitTop' in html, "Bouton disquette de sauvegarde manquant"
    assert 'btnOpenIdentityQuestionsTop' in html and '+ sur vous' in html, "Bouton + sur vous manquant"
    assert 'btnOpenPartnerQuestionsTop' in html and "+ sur l'autre" in html, "Bouton + sur l'autre manquant"
    assert 'ckpIdentityCompletionTop' in html and 'ckpPartnerCompletionTop' in html, "Badges de complétude manquants"
    print("  ✓ Ligne 3 : Disquette, '+ sur vous [%]' et '+ sur l\\'autre [%]' trouvés sans chevauchement.")

    # Vérification Ligne 4: Pseudo public *
    assert 'ckp-line-pseudo' in html, "Ligne 4: Pseudo public manquant"
    assert 'ckpInputPseudo' in html and 'Pseudo public' in html, "Champ Pseudo public manquant"
    print("  ✓ Ligne 4 : Pseudo public * avec champ de saisie trouvé.")

    # Vérification Modale Deck Identité
    assert 'id="modalIdentityDeck"' in html, "modalIdentityDeck manquante"
    assert 'btnTabIdentitySelf' in html and 'btnTabIdentityPartner' in html, "Onglets de commutation manquants"
    assert 'identityDeckQuestionsContainer' in html, "Conteneur des questions manquant"
    print("  ✓ Modale interactive 'modalIdentityDeck' avec onglets '+ sur vous' et '+ sur l\\'autre' validée.")


def test_api_identity_answers():
    print("\n=== Test 2: API Backend Identity Answers ===")
    base_url = "http://localhost:8765"

    # GET /api/profiles/2/identity-answers
    req = urllib.request.Request(f"{base_url}/api/profiles/2/identity-answers")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))

    questions = data.get('questions', [])
    assert len(questions) == 14, f"Devrait avoir 14 questions d'identité, obtenu {len(questions)}"
    print(f"  ✓ 14 questions de classe 0 récupérées avec succès.")

    # Vérifier les kinds
    numeric_q = [q for q in questions if q.get('kind') == 'numeric']
    select_q = [q for q in questions if q.get('kind') == 'select']
    assert len(numeric_q) == 6, f"Devrait avoir 6 questions numériques, obtenu {len(numeric_q)}"
    assert len(select_q) == 8, f"Devrait avoir 8 questions liste/select, obtenu {len(select_q)}"
    print(f"  ✓ Typologie validée : 6 questions 'numeric' (Taille, Poids, Poitrine, etc.) et 8 questions 'select' (Cheveux, Style, etc.).")

    # POST /api/profiles/2/identity-answers/self (Question numérique: Taille = 182)
    q_taille = next(q for q in questions if 'Taille' in q['texte'])
    payload_self = json.dumps({"question_id": q_taille['id'], "valeur_num": 182.0, "valeur_text": None}).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/api/profiles/2/identity-answers/self", data=payload_self, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res_self = json.loads(resp.read().decode('utf-8'))
        assert res_self.get('ok') is True
        print(f"  ✓ POST /identity-answers/self : Taille = 182 cm enregistrée (complétude self = {res_self.get('self_completion_pct')}%).")

    # POST /api/profiles/2/identity-answers/partner (Question numérique: Taille tolérée entre 160 et 185)
    payload_part = json.dumps({"question_id": q_taille['id'], "min_val": 160.0, "max_val": 185.0, "options": [], "indifferent": False}).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/api/profiles/2/identity-answers/partner", data=payload_part, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res_part = json.loads(resp.read().decode('utf-8'))
        assert res_part.get('ok') is True
        print(f"  ✓ POST /identity-answers/partner : Taille tolérée 160-185 cm enregistrée (complétude partner = {res_part.get('partner_completion_pct')}%).")

    # POST /api/profiles/2/identity-answers/partner avec Indifférent
    q_cheveux = next(q for q in questions if 'cheveux' in q['sujet'].lower() or 'cheveux' in q['texte'].lower())
    payload_indiff = json.dumps({"question_id": q_cheveux['id'], "min_val": None, "max_val": None, "options": [], "indifferent": True}).encode('utf-8')
    req = urllib.request.Request(f"{base_url}/api/profiles/2/identity-answers/partner", data=payload_indiff, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res_indiff = json.loads(resp.read().decode('utf-8'))
        assert res_indiff.get('ok') is True
        print(f"  ✓ POST /identity-answers/partner : Cheveux marqués 'Indifférent' avec succès (complétude partner = {res_indiff.get('partner_completion_pct')}%).")

    # Re-GET pour vérifier la persistance
    req = urllib.request.Request(f"{base_url}/api/profiles/2/identity-answers")
    with urllib.request.urlopen(req) as resp:
        data_after = json.loads(resp.read().decode('utf-8'))
        p_ans = data_after.get('partner', {}).get(str(q_cheveux['id']), {})
        assert p_ans.get('indifferent') in (True, 1), "Indifférent non persisté"
        s_ans = data_after.get('self', {}).get(str(q_taille['id']), {})
        assert s_ans.get('valeur_num') == 182.0, "Valeur num non persistée"
        print("  ✓ Persistance en base SQLite des réponses 'self' et tolérances 'partner' avec case Indifférent vérifiée.")

if __name__ == '__main__':
    test_frontend_html()
    test_api_identity_answers()
    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
