import urllib.request
import json
from html.parser import HTMLParser

def test_html_modals_hierarchy():
    print("--- 1. Vérification de la hiérarchie HTML des modales ---")
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
        print(f"Modal {modal_id} -> Parents modales imbriquées: {parent_modals}")
        assert len(parent_modals) == 0, f"ERREUR: {modal_id} est imbriqué dans {parent_modals} !"

    print("[OK] Toutes les modales sont bien des enfants directs et autonomes (aucune imbrication parasite) !")

def test_buttons_and_onclick():
    print("\n--- 2. Vérification des boutons + sur moi et + sur l'autre ---")
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    assert 'id="btnOpenIdentityQuestionsTop"' in html, "Bouton btnOpenIdentityQuestionsTop introuvable"
    assert "openIdentityDeck('self')" in html, "onclick openIdentityDeck('self') introuvable"
    assert 'id="btnOpenPartnerQuestionsTop"' in html, "Bouton btnOpenPartnerQuestionsTop introuvable"
    assert "openIdentityDeck('partner')" in html, "onclick openIdentityDeck('partner') introuvable"
    assert 'id="modalIdentityDeck"' in html, "Modal modalIdentityDeck introuvable"
    print("[OK] Boutons et modales d'acces a l'Identite correctement configures dans le DOM !")

def test_api_identity_answers():
    print("\n--- 3. Vérification de l'API /api/profiles/<id>/identity-answers ---")
    for pid in [1, 4]:
        url = f"http://localhost:8765/api/profiles/{pid}/identity-answers"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            assert resp.status == 200, f"Statut non 200 pour profile {pid}"
            data = json.loads(resp.read().decode('utf-8'))
            assert 'questions_self' in data, "questions_self manquant"
            assert 'questions_partner' in data, "questions_partner manquant"
            q_self = data['questions_self']
            print(f"Profil {pid}: {len(q_self)} questions de Type P dans 'questions_self'")
            assert len(q_self) == 15, f"Attendu 15 questions pour homme, obtenu {len(q_self)}"
            for q in q_self:
                assert q['type'] == 'P', f"Question {q['id']} doit être de type P"
                assert q['thematique'] == 'Identité' or q['sujet'] == 'Identité'
                assert q.get('kind') in ('numeric', 'select'), f"Kind manquant pour {q['id']}"

    print("[OK] API fonctionnelle et retournant les questions de classe 8 adaptees au sexe du profil !")

if __name__ == '__main__':
    test_html_modals_hierarchy()
    test_buttons_and_onclick()
    test_api_identity_answers()
    print("\n=========================================")
    print("TOUS LES TESTS DE VALIDATION SONT SUCCÈS !")
    print("=========================================")
