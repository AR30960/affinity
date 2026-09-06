import sqlite3
import json

def test_full_filter_behavior():
    print("=== DÉBUT DU TEST DE VALIDATION DES FILTRES ET DE L'AFFICHAGE DES QUESTIONS ===")

    conn = sqlite3.connect('affinity.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Charger les questions de l'API /api/questions (validées)
    cur.execute("""
        SELECT q.*, p.nom as pack_nom,
               parent.texte as parent_texte,
               (SELECT COUNT(*) FROM questions sq WHERE sq.n_quest_lie = q.id AND sq.id != q.id) as subquestions_count
        FROM questions q
        JOIN question_packs p ON q.pack_id = p.id
        LEFT JOIN questions parent ON q.n_quest_lie = parent.id AND q.n_quest_lie != 0
        WHERE (q.status = 'validated' OR q.status IS NULL)
        ORDER BY q.thematique, q.sujet, q.id
    """)
    questions = [dict(r) for r in cur.fetchall()]
    print(f"Total questions validées chargées : {len(questions)}")
    assert len(questions) == 204, f"Attendu 204 questions, obtenu {len(questions)}"

    # Profil admin ar30960
    cur.execute("SELECT * FROM profiles WHERE pseudo = 'ar30960'")
    admin_prof = dict(cur.fetchone())
    print(f"Profil connecté : {admin_prof['pseudo']} (rôle: {admin_prof['role']})")

    # Simulation getActiveProfileEligibleQuestions pour admin
    # Code JS: if (prof.role === 'admin') return state.questions.filter(q => q.classe !== 8 && q.classe !== '8' && q.type !== 'P' && q.type !== 'T');
    admin_eligible = [q for q in questions if q['classe'] != 8 and q['type'] not in ('P', 'T')]
    print(f"Questions éligibles au questionnaire pour l'administrateur : {len(admin_eligible)}")
    assert len(admin_eligible) == 172, f"Attendu 172 questions pour l'admin, obtenu {len(admin_eligible)}"

    # Simulation Questionnaire : filtrage par défaut (ALL / ALL / ALL)
    def filter_questionnaire(eligible, thema='ALL', pack='ALL', classe='ALL', status='ALL', hier='ALL'):
        res = []
        for q in eligible:
            if thema != 'ALL' and str(q['thematique']) != str(thema):
                continue
            if pack != 'ALL' and str(q['pack_id']) != str(pack):
                continue
            if classe != 'ALL' and str(q['classe']) != str(classe):
                continue
            if hier == 'MAIN':
                if q.get('n_quest_lie') and q['n_quest_lie'] != 0 and q['n_quest_lie'] != q['id'] and q['classe'] != 8:
                    continue
            elif hier == 'SUB':
                if not q.get('n_quest_lie') or q['n_quest_lie'] == 0 or q['n_quest_lie'] == q['id'] or q['classe'] == 8:
                    continue
            res.append(q)
        return res

    # 1. Par défaut dans le questionnaire
    q_default = filter_questionnaire(admin_eligible)
    print(f"[OK] Questionnaire par defaut (Admin) : {len(q_default)} questions visibles immediatement")
    assert len(q_default) == 172

    # 2. Sélection de 'Comportement' avec classe='ALL'
    q_comp_all = filter_questionnaire(admin_eligible, thema='Comportement', classe='ALL')
    print(f"[OK] Questionnaire Thematique 'Comportement' (Toutes classes) : {len(q_comp_all)} questions visibles")
    assert len(q_comp_all) == 51, f"Attendu 51, obtenu {len(q_comp_all)}"

    # 3. Changement de filtre classe : Classe 1
    q_comp_c1 = filter_questionnaire(admin_eligible, thema='Comportement', classe='1')
    print(f"[OK] Questionnaire Thematique 'Comportement' + Classe 1 : {len(q_comp_c1)} questions visibles")
    assert len(q_comp_c1) == 42, f"Attendu 42, obtenu {len(q_comp_c1)}"

    # 4. Changement de filtre classe : Classe 2
    q_comp_c2 = filter_questionnaire(admin_eligible, thema='Comportement', classe='2')
    print(f"[OK] Questionnaire Thematique 'Comportement' + Classe 2 : {len(q_comp_c2)} questions visibles")
    assert len(q_comp_c2) == 5, f"Attendu 5, obtenu {len(q_comp_c2)}"

    # 5. Changement de filtre classe : Classe 3
    q_comp_c3 = filter_questionnaire(admin_eligible, thema='Comportement', classe='3')
    print(f"[OK] Questionnaire Thematique 'Comportement' + Classe 3 : {len(q_comp_c3)} questions visibles")
    assert len(q_comp_c3) == 4, f"Attendu 4, obtenu {len(q_comp_c3)}"

    # Simulation Banque de Questions
    def filter_bank(all_qs, thema='ALL', sujet='ALL', classe='ALL', cible='ALL', hier='ALL'):
        res = []
        for q in all_qs:
            if thema != 'ALL' and str(q['thematique']) != str(thema):
                continue
            if sujet != 'ALL' and str(q['sujet']) != str(sujet):
                continue
            if classe != 'ALL' and str(q['classe']) != str(classe):
                continue
            if cible != 'ALL' and str(q['cible']) != str(cible):
                continue
            if hier == 'MAIN':
                if (q.get('n_quest_lie') and q['n_quest_lie'] != 0 and q['n_quest_lie'] != q['id']) and q['classe'] != 8:
                    continue
            elif hier == 'PARENT':
                if not q.get('subquestions_count') or q['subquestions_count'] <= 0:
                    continue
            elif hier == 'SUB':
                if not q.get('n_quest_lie') or q['n_quest_lie'] == 0 or q['n_quest_lie'] == q['id'] or q['classe'] == 8:
                    continue
            res.append(q)
        return res

    # 6. Banque par défaut
    b_default = filter_bank(questions)
    print(f"[OK] Banque de questions par defaut : {len(b_default)} questions visibles")
    assert len(b_default) == 204

    # 7. Banque Thématique 'Comportement' (ALL)
    b_comp_all = filter_bank(questions, thema='Comportement')
    print(f"[OK] Banque Thematique 'Comportement' : {len(b_comp_all)} questions visibles")
    assert len(b_comp_all) == 51

    # 8. Banque Thématique 'Comportement' + Classe 1
    b_comp_c1 = filter_bank(questions, thema='Comportement', classe='1')
    print(f"[OK] Banque Thematique 'Comportement' + Classe 1 : {len(b_comp_c1)} questions visibles")
    assert len(b_comp_c1) == 42

    # 9. Banque Thématique 'Comportement' + Classe 3
    b_comp_c3 = filter_bank(questions, thema='Comportement', classe='3')
    print(f"[OK] Banque Thematique 'Comportement' + Classe 3 : {len(b_comp_c3)} questions visibles")
    assert len(b_comp_c3) == 4

    print("\nTOUTES LES VERIFICATIONS SONT VALIDEES AVEC SUCCES (100%) !")

if __name__ == '__main__':
    test_full_filter_behavior()
