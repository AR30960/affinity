import sqlite3
import os
import json
import server

def run_tests():
    server.init_db()
    conn = server.get_db()
    c = conn.cursor()
    
    # 1. Vérification profil administrateur ar30960 ADM-1
    c.execute("SELECT pseudo, role, code_profil FROM profiles WHERE id = 1")
    admin_prof = c.fetchone()
    assert admin_prof is not None, "Profil 1 introuvable"
    assert admin_prof["pseudo"] == "ar30960", f"Expected pseudo 'ar30960', got '{admin_prof['pseudo']}'"
    assert admin_prof["role"] == "admin", f"Expected role 'admin', got '{admin_prof['role']}'"
    assert admin_prof["code_profil"] == "ADM-1", f"Expected code_profil 'ADM-1', got '{admin_prof['code_profil']}'"
    print("Test 1 Réussi : Profil 1 est ar30960 (ADM-1).")

    # 2. Vérification conversion type MULTI -> M
    c.execute("SELECT COUNT(*) as cnt FROM questions WHERE type = 'MULTI'")
    cnt_multi = c.fetchone()["cnt"]
    assert cnt_multi == 0, f"Trouvé {cnt_multi} questions avec le type 'MULTI' non migré."
    
    c.execute("SELECT COUNT(*) as cnt FROM questions WHERE type = 'M'")
    cnt_m = c.fetchone()["cnt"]
    assert cnt_m > 0, "Aucune question de type 'M' trouvée."
    print(f"Test 2 Réussi : Type M validé ({cnt_m} questions de type M).")

    # 3. Test création d'un nouveau profil invité (guest)
    test_pseudo = "TestGuestUser"
    c.execute("DELETE FROM profiles WHERE pseudo = ?", (test_pseudo,))
    conn.commit()
    
    c.execute("INSERT INTO profiles (pseudo, avatar, role) VALUES (?, 'user', 'guest')", (test_pseudo,))
    new_pid = c.lastrowid
    code_prof = f"AFF-{new_pid}"
    c.execute("UPDATE profiles SET code_profil = ? WHERE id = ?", (code_prof, new_pid))
    c.execute("INSERT INTO identity_cards (profile_id) VALUES (?)", (new_pid,))
    c.execute("INSERT OR REPLACE INTO profile_question_access (profile_id, allowed_packs, allowed_classes, allowed_types) VALUES (?, 'ALL', '[\"1\"]', 'ALL')", (new_pid,))
    conn.commit()
    
    c.execute("SELECT * FROM profiles WHERE id = ?", (new_pid,))
    guest_prof = c.fetchone()
    assert guest_prof["code_profil"] == f"AFF-{new_pid}", f"Code profil erroné: {guest_prof['code_profil']}"
    
    c.execute("SELECT allowed_classes FROM profile_question_access WHERE profile_id = ?", (new_pid,))
    pqa = c.fetchone()
    assert pqa["allowed_classes"] == '["1"]', f"Accès classes invité erroné: {pqa['allowed_classes']}"
    print(f"Test 3 Réussi : Profil invité {test_pseudo} créé avec {code_prof} et restreint à la classe 1.")
    
    # Nettoyage
    c.execute("DELETE FROM profiles WHERE id = ?", (new_pid,))
    conn.commit()
    conn.close()
    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
