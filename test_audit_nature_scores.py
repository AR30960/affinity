import unittest
import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:8765"

class TestUserActivityHistoryAudit(unittest.TestCase):
    def test_audit_history_format_and_nature(self):
        # 1. Vérifier la récupération de l'historique
        req = urllib.request.Request(f"{BASE_URL}/api/admin/user-actions-history?limit=10")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            self.assertIn("items", data)
            items = data["items"]
            self.assertGreater(len(items), 0)

            # Vérifier qu'aucun item ne contient "/9" dans ses libellés d'axes ou de scores
            for it in items:
                # Vérifier la présence du champ nature
                self.assertIn("nature", it)
                self.assertIn(it["nature"], ["1ère saisie", "Modification"])
                
                # Vérifier que details_json ne contient pas de "/9"
                if it.get("details_json"):
                    det = json.loads(it["details_json"])
                    if "axes" in det and isinstance(det["axes"], dict):
                        for ax, val in det["axes"].items():
                            self.assertNotEqual(val, "/9")

        # 2. Test d'une 1ère saisie sur une question pour un profil de test (ex: profil 25 Alyssa sur question 10107)
        test_qid = 10107
        # Vérifions si le profil 25 a déjà répondu
        req_answers = urllib.request.Request(f"{BASE_URL}/api/questions/answers?profile_id=25")
        try:
            with urllib.request.urlopen(req_answers, timeout=5) as resp:
                pass
        except Exception:
            pass

        # Première passe : mettre des valeurs de référence
        payload_step1 = {
            "profile_id": 25,
            "answers": [
                {"question_id": 31400, "axis": "V", "value": 2}, # Régulièrement (2)
                {"question_id": 31400, "axis": "A", "value": 1}, # Peu (1)
                {"question_id": 31400, "axis": "D", "value": 3}, # Ne gêne pas (3)
                {"question_id": 31400, "axis": "P", "value": 3}  # Ne gêne pas (3)
            ]
        }
        req_post1 = urllib.request.Request(
            f"{BASE_URL}/api/answers",
            data=json.dumps(payload_step1).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_post1, timeout=5) as resp:
            pass

        # Deuxième passe : modifier ces valeurs
        payload_step2 = {
            "profile_id": 25,
            "answers": [
                {"question_id": 31400, "axis": "V", "value": 4}, # 2 -> 4 (Très souvent)
                {"question_id": 31400, "axis": "A", "value": 3}, # 1 -> 3 (Souvent)
                {"question_id": 31400, "axis": "D", "value": 3}, # 3 -> 3 (inchangé)
                {"question_id": 31400, "axis": "P", "value": 7}  # 3 -> 7 (Prioritaire)
            ]
        }
        req_post2 = urllib.request.Request(
            f"{BASE_URL}/api/answers",
            data=json.dumps(payload_step2).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_post2, timeout=5) as resp:
            res2 = json.loads(resp.read().decode())
            self.assertTrue(res2.get("success"))

        # Vérifier l'historique pour cette modification
        req_h2 = urllib.request.Request(f"{BASE_URL}/api/admin/user-actions-history?limit=1")
        with urllib.request.urlopen(req_h2, timeout=5) as resp:
            h2 = json.loads(resp.read().decode())["items"][0]
            self.assertEqual(h2["nature"], "Modification")
            self.assertEqual(h2["action_category"], "modification")
            self.assertIn("➔", h2["summary"])
            # Doit contenir ancienne et nouvelle valeur
            self.assertIn("Régulièrement (2) ➔ Très souvent (4)", h2["summary"])
            self.assertIn("Peu (1) ➔ Souvent (3)", h2["summary"])
            self.assertIn("Ne gêne pas (3) ➔ Prioritaire (7)", h2["summary"])
            self.assertNotIn("/9", h2["summary"])

            # Vérifier les détails JSON
            det2 = json.loads(h2["details_json"])
            self.assertEqual(det2["nature"], "Modification")
            self.assertIn("changes", det2)
            self.assertEqual(det2["changes"]["V"]["old"], 2)
            self.assertEqual(det2["changes"]["V"]["new"], 4)
            self.assertEqual(det2["changes"]["A"]["old"], 1)
            self.assertEqual(det2["changes"]["A"]["new"], 3)
            self.assertEqual(det2["changes"]["P"]["old"], 3)
            self.assertEqual(det2["changes"]["P"]["new"], 7)

        print("\n[OK] Test d'audit, libellés explicites, et modification avec ancienne et nouvelle valeur validé avec succès !")

if __name__ == "__main__":
    unittest.main()
