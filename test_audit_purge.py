"""
Script de test automatisé (HTTP pur) pour la purge et la suppression unitaire
du journal d'audit (user_actions_history).
"""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8765"
sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    print("--- Démarrage des tests HTTP de purge et suppression d'audit ---")

    # 1. Vérification du journal d'audit actuel
    req = urllib.request.Request(f"{BASE_URL}/api/admin/user-actions-history?limit=10")
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        total_initial = data.get("total_count", 0)
        items = data.get("items", [])
        print(f"Total initial d'actions enregistrées : {total_initial}")
        assert len(items) > 0, "L'historique contient des entrées"
        test_id = items[0]["id"]
        print(f"Action ciblée pour suppression unitaire : #{test_id} ({items[0].get('summary')})")

    # 2. Test d'estimation de purge (dry_run: True) en mode 'older_than_days'
    payload_dry = {
        "mode": "older_than_days",
        "days": 0, # Toutes les entrées antérieures à aujourd'hui
        "dry_run": True
    }
    req_dry = urllib.request.Request(
        f"{BASE_URL}/api/admin/user-actions-history/purge",
        data=json.dumps(payload_dry).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_dry, timeout=10) as resp:
        dry_res = json.loads(resp.read().decode('utf-8'))
        print(f"Estimation (dry_run: True, mode: older_than_days) : {dry_res}")
        assert dry_res.get("success") is True
        assert dry_res.get("dry_run") is True
        assert dry_res.get("matching_count") >= 1

    # 3. Test d'estimation en mode 'filtered'
    payload_dry_filt = {
        "mode": "filtered",
        "category": "reponse",
        "dry_run": True
    }
    req_dry_filt = urllib.request.Request(
        f"{BASE_URL}/api/admin/user-actions-history/purge",
        data=json.dumps(payload_dry_filt).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_dry_filt, timeout=10) as resp:
        dry_filt_res = json.loads(resp.read().decode('utf-8'))
        print(f"Estimation (dry_run: True, mode: filtered) : {dry_filt_res}")
        assert dry_filt_res.get("success") is True
        assert dry_filt_res.get("matching_count") >= 0

    # 4. Test de suppression unitaire (DELETE /api/admin/user-actions-history/<id>)
    req_del = urllib.request.Request(
        f"{BASE_URL}/api/admin/user-actions-history/{test_id}",
        method="DELETE"
    )
    with urllib.request.urlopen(req_del, timeout=10) as resp:
        del_res = json.loads(resp.read().decode('utf-8'))
        print(f"Suppression unitaire de #{test_id} : {del_res}")
        assert del_res.get("success") is True
        assert del_res.get("deleted_id") == test_id
        assert del_res.get("deleted_count") == 1

    # Vérification que #{test_id} a bien été retiré
    req_check = urllib.request.Request(f"{BASE_URL}/api/admin/user-actions-history?limit=10")
    with urllib.request.urlopen(req_check, timeout=10) as resp:
        check_data = json.loads(resp.read().decode('utf-8'))
        remaining_ids = [it["id"] for it in check_data.get("items", [])]
        assert test_id not in remaining_ids, f"L'ID #{test_id} est encore présent"

    # 5. Test de purge réelle avec création de sauvegarde automatique de sécurité
    # Cibler un critère précis pour purger en sécurité :
    # ex: mode filtered sur un mot précis ou un profil
    payload_purge = {
        "mode": "older_than_days",
        "days": 3650, # Actions de plus de 10 ans (ne supprimera rien ou très peu, mais déclenchera le cycle complet avec backup si count > 0)
        "dry_run": False,
        "create_backup": True
    }
    req_purge = urllib.request.Request(
        f"{BASE_URL}/api/admin/user-actions-history/purge",
        data=json.dumps(payload_purge).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_purge, timeout=15) as resp:
        purge_res = json.loads(resp.read().decode('utf-8'))
        print(f"Exécution de la purge (mode: older_than_days 3650) : {purge_res}")
        assert purge_res.get("success") is True
        assert "deleted_count" in purge_res

    # 6. Test de purge avec match réel (mode 'filtered' avec critère pseudo)
    first_item = check_data["items"][0]
    search_pseudo = first_item.get("pseudo") or "AR30"
    print(f"Purge ciblée sur le membre : '{search_pseudo}'")

    payload_purge_real = {
        "mode": "filtered",
        "pseudo": search_pseudo,
        "dry_run": False,
        "create_backup": True
    }
    req_purge_real = urllib.request.Request(
        f"{BASE_URL}/api/admin/user-actions-history/purge",
        data=json.dumps(payload_purge_real).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_purge_real, timeout=15) as resp:
        real_purge_res = json.loads(resp.read().decode('utf-8'))
        print(f"Résultat purge réelle ciblée : {real_purge_res}")
        assert real_purge_res.get("success") is True
        assert real_purge_res.get("deleted_count") >= 1
        assert real_purge_res.get("backup_created") is True
        assert real_purge_res.get("backup_file") is not None
        print(f"✅ Sauvegarde de sécurité créée avant purge : {real_purge_res.get('backup_file')}")

    # 7. Vérification de l'inscription de l'action de purge dans le journal d'audit (AUDIT_PURGE)
    req_audit = urllib.request.Request(f"{BASE_URL}/api/admin/user-actions-history?limit=5")
    with urllib.request.urlopen(req_audit, timeout=10) as resp:
        audit_data = json.loads(resp.read().decode('utf-8'))
        audit_types = [it.get("action_type") for it in audit_data.get("items", [])]
        print(f"Types d'actions récentes dans l'audit : {audit_types}")
        assert "AUDIT_PURGE" in audit_types, "L'action de purge AUDIT_PURGE doit être inscrite dans le journal d'audit"

    print("\n🎉 TOUS LES TESTS DE PURGE ET DE SUPPRESSION UNITAIRE SONT PARFAITEMENT VALIDES !")
    return True

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
