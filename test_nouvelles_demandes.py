import urllib.request
import json
import re
from html.parser import HTMLParser

def test_dom_modals():
    print("--- 1. Vérification de la structure DOM et des modales ---")
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    class HierarchyChecker(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.modals = {}
            
        def handle_starttag(self, tag, attrs):
            if tag in ('meta', 'link', 'input', 'img', 'br', 'hr'):
                return
            attrs_dict = dict(attrs)
            classes = attrs_dict.get('class', '').split()
            el_id = attrs_dict.get('id', '')
            if 'modal-backdrop' in classes and el_id:
                self.stack.append((tag, el_id))
                parent_modals = [i for t, i in self.stack[:-1] if i]
                self.modals[el_id] = parent_modals
            else:
                self.stack.append((tag, ''))

        def handle_endtag(self, tag):
            if tag in ('meta', 'link', 'input', 'img', 'br', 'hr'):
                return
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    self.stack.pop(i)
                    break

    checker = HierarchyChecker()
    checker.feed(content)

    for modal_id, parent_modals in checker.modals.items():
        print(f"Modal {modal_id} -> Parents imbriques: {parent_modals}")
        assert len(parent_modals) == 0, f"ERREUR: {modal_id} imbriqué dans {parent_modals}"

    print("[OK] Toutes les modales sont directes et autonomes.")

def test_nouvelle_question_elements():
    print("\n--- 2. Vérification des sélecteurs Thématique/Sujet et de la gestion des réponses ---")
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    assert 'id="editQThematiqueSelect"' in html, "editQThematiqueSelect manquant"
    assert 'id="editQSujetSelect"' in html, "editQSujetSelect manquant"
    assert 'id="infoTypeMulti"' in html, "infoTypeMulti manquant"
    assert 'id="infoTypeGouts"' in html, "infoTypeGouts manquant"
    assert 'id="boxConfigIdentityAnswers"' in html, "boxConfigIdentityAnswers manquant"

    with open('frontend/app.js', 'r', encoding='utf-8') as f:
        js = f.read()

    assert 'function populateModalThematiques' in js, "populateModalThematiques manquante"
    assert 'function updateModalSujetsDropdown' in js, "updateModalSujetsDropdown manquante"
    assert 'function onEditQThematiqueSelectChange' in js, "onEditQThematiqueSelectChange manquante"
    assert 'function onEditQSujetSelectChange' in js, "onEditQSujetSelectChange manquante"
    assert 'Questionnaire "+ sur l\'autre" incomplet' in js, "Libellé Questionnaire + sur l'autre incomplet manquant"

    print("[OK] Sélecteurs de thématique et sujet et adaptation des réponses selon le type validés.")

def test_api_crud_question_types():
    print("\n--- 3. Vérification API: Création, modification et suppression selon les types ---")
    # Test Type P (Précis)
    payload_p = {
        "thematique": "Identité",
        "sujet": "Identité",
        "classe": 8,
        "type": "P",
        "cible": 0,
        "texte": "Test automatisé Type P - Stature exacte",
        "config_reponses": {
            "mode": "numeric",
            "unit": "cm",
            "min": 120,
            "max": 220,
            "step": 1
        }
    }
    req = urllib.request.Request(
        "http://localhost:8765/api/questions",
        data=json.dumps(payload_p).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        qid = res['id']
        print(f"Question Type P créée avec ID #{qid}")

    # Test Type T (Tolérance)
    payload_t = {
        "thematique": "Identité",
        "sujet": "Identité",
        "classe": 8,
        "type": "T",
        "cible": 0,
        "texte": "Test automatisé Type T - Tolérance stature",
        "config_reponses": {
            "mode": "numeric",
            "unit": "cm",
            "min": 150,
            "max": 190,
            "step": 1
        }
    }
    req_put = urllib.request.Request(
        f"http://localhost:8765/api/questions/{qid}",
        data=json.dumps(payload_t).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(req_put) as resp:
        res_put = json.loads(resp.read().decode('utf-8'))
        print(f"Question #{qid} mise à jour en Type T: {res_put.get('success')}")

    # Suppression de nettoyage
    req_del = urllib.request.Request(
        f"http://localhost:8765/api/questions/{qid}",
        method="DELETE"
    )
    with urllib.request.urlopen(req_del) as resp:
        res_del = json.loads(resp.read().decode('utf-8'))
        print(f"Question #{qid} supprimée: {res_del.get('success')}")

    print("[OK] API CRUD pour les types de questions vérifiée avec succès.")

if __name__ == '__main__':
    test_dom_modals()
    test_nouvelle_question_elements()
    test_api_crud_question_types()
    print("\n================================================")
    print("TOUS LES NOUVEAUX TESTS SONT PASSÉS AVEC SUCCÈS !")
    print("================================================")
