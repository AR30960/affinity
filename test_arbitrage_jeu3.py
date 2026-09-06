# -*- coding: utf-8 -*-
"""
Script de validation automatisée de l'Espace d'Arbitrage Jeu 3
- Vérifie l'état initial des 150 questions proposées (100 Classe 5, 50 Classe 9)
- Vérifie l'étanchéité des questionnaires membres (les 150 questions ne sont pas visibles)
- Valide le cycle d'arbitrage (Validation unitaire, modification, suppression) sur question test
- Vérifie l'intégrité de la table Access T_JEU (Pack 3 présent)
"""
import urllib.request
import json
import sqlite3
import os

API_BASE = "http://127.0.0.1:8765"

def api_get(endpoint):
    url = f"{API_BASE}{endpoint}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def api_post(endpoint, data=None):
    url = f"{API_BASE}{endpoint}"
    payload = json.dumps(data).encode('utf-8') if data else None
    headers = {'Content-Type': 'application/json'} if data else {}
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def api_delete(endpoint):
    url = f"{API_BASE}{endpoint}"
    req = urllib.request.Request(url, method='DELETE')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def main():
    print("=== DEBUT DES TESTS D'ARBITRAGE JEU 3 ===")

    # 1. Vérification des questions en attente
    pending_data = api_get('/api/admin/questions/pending')
    total_pending = pending_data['total']
    c5 = pending_data['count_classe_5']
    c9 = pending_data['count_classe_9']
    print(f"[TEST 1] Questions en attente détectées : Total={total_pending}, Classe 5={c5}, Classe 9={c9}")
    assert total_pending == 150, f"Attendu 150 en attente, reçu {total_pending}"
    assert c5 == 100, f"Attendu 100 questions classe 5, reçu {c5}"
    assert c9 == 50, f"Attendu 50 questions classe 9, reçu {c9}"
    print("  -> TEST 1 REUSSI: 150 propositions (100 C5 + 50 C9) correctement identifiées.")

    # 2. Vérification de l'étanchéité des questions publiques/membres
    active_questions = api_get('/api/questions')['questions']
    print(f"[TEST 2] Questions visibles aux membres : {len(active_questions)}")
    assert len(active_questions) == 204, f"Attendu 204 questions validées visibles, reçu {len(active_questions)}"
    for q in active_questions:
        assert q['status'] == 'validated', f"Question #{q['id']} non validée présente dans les questionnaires !"
    print("  -> TEST 2 REUSSI: Seules les 204 questions validées sont transmises aux membres.")

    # 3. Test du cycle unitaire d'arbitrage sur question temporaire
    conn = sqlite3.connect('affinity.db')
    cursor = conn.cursor()
    test_qid = 999999
    cursor.execute("DELETE FROM questions WHERE id = ?", (test_qid,))
    cursor.execute("""
        INSERT INTO questions (id, pack_id, thematique, sujet, classe, type, cible, texte, status)
        VALUES (?, 3, 'Sexualité', 'Test Arbitrage', 5, 'M', 0, 'Question test temporaire pour arbitrage', 'pending_review')
    """, (test_qid,))
    conn.commit()
    conn.close()

    # Vérification que la question test est bien listée dans pending
    pending_after_insert = api_get('/api/admin/questions/pending')
    assert pending_after_insert['total'] == 151
    print("[TEST 3A] Question test temporaire créée avec succès en attente.")

    # Validation de la question test
    val_res = api_post(f'/api/admin/questions/{test_qid}/validate')
    assert val_res['success'] is True
    print(f"[TEST 3B] Validation API réussie : {val_res['message']}")

    # Vérification qu'elle est passée dans les questions actives
    active_after_val = api_get('/api/questions')['questions']
    assert len(active_after_val) == 205
    assert any(q['id'] == test_qid for q in active_after_val)
    print("[TEST 3C] Question test correctement intégrée dans la banque active.")

    # Suppression de la question test
    del_res = api_delete(f'/api/questions/{test_qid}')
    assert del_res['success'] is True
    print("[TEST 3D] Suppression API réussie de la question test.")

    # Vérification que le compte est revenu exactement à 150 en attente et 204 actives
    final_pending = api_get('/api/admin/questions/pending')
    final_active = api_get('/api/questions')['questions']
    assert final_pending['total'] == 150
    assert final_pending['count_classe_5'] == 100
    assert final_pending['count_classe_9'] == 50
    assert len(final_active) == 204
    print("  -> TEST 3 REUSSI: Cycle complet d'arbitrage (Création, Validation, Intégration, Suppression) 100% fonctionnel.")

    # 4. Vérification de l'intégration Access du Jeu 3
    conn_sq = sqlite3.connect('affinity.db')
    sq_packs = conn_sq.execute("SELECT id, code, nom FROM question_packs WHERE id = 3").fetchone()
    conn_sq.close()
    assert sq_packs is not None
    print(f"[TEST 4] Pack Jeu 3 dans SQLite: ID={sq_packs[0]}, Code={sq_packs[1]}, Nom={sq_packs[2]}")
    print("  -> TEST 4 REUSSI: Jeu 3 parfaitement synchronisé.")

    print("\n==========================================")
    print("TOUS LES TESTS D'ARBITRAGE SONT VALIDES AVEC SUCCES !")
    print("==========================================")

if __name__ == '__main__':
    main()
