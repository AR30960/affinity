import sqlite3
import subprocess
import json

def get_access_links():
    ps_cmd = """
    $dbPath = 'C:\\_AR\\Antigravity\\_Devia\\ARP001\\Affinity-Full.mdb'
    $pwd = 'quest1234'
    $connStr = "Provider=Microsoft.ACE.OLEDB.16.0;Data Source=$dbPath;Jet OLEDB:Database Password=$pwd;"
    $conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = 'SELECT N_QUEST, N_QUEST_LIE FROM [T_QUEST]'
    $ad = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    [void]$ad.Fill($dt)
    $rows = @()
    foreach ($r in $dt.Rows) {
        $rows += @{ n_quest = [int]$r['N_QUEST']; n_quest_lie = [int]$r['N_QUEST_LIE'] }
    }
    $conn.Close()
    $rows | ConvertTo-Json -Compress
    """
    res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True)
    if res.returncode != 0:
        print("Erreur powershell:", res.stderr)
        return []
    try:
        return json.loads(res.stdout.strip())
    except Exception as e:
        print("Erreur parsing JSON:", e)
        return []

links = get_access_links()
print(f"Trouvé {len(links)} entrées dans T_QUEST d'Access.")

conn = sqlite3.connect("affinity.db")
c = conn.cursor()

# Vérifier si la colonne existe
c.execute("PRAGMA table_info(questions)")
cols = [r[1] for r in c.fetchall()]
if "n_quest_lie" not in cols:
    c.execute("ALTER TABLE questions ADD COLUMN n_quest_lie INTEGER DEFAULT 0")
    print("Colonne n_quest_lie ajoutée à questions.")
else:
    print("Colonne n_quest_lie déjà présente.")

updated = 0
for item in links:
    qid = item["n_quest"]
    qlie = item["n_quest_lie"]
    c.execute("UPDATE questions SET n_quest_lie = ? WHERE id = ?", (qlie, qid))
    if c.rowcount > 0 and qlie != 0:
        updated += 1

conn.commit()
print(f"Mise à jour terminée. {updated} questions ont maintenant un n_quest_lie <> 0.")

# Vérifions les statistiques dans sqlite
c.execute("SELECT COUNT(*) FROM questions WHERE n_quest_lie != 0")
cnt = c.fetchone()[0]
print(f"Total questions avec n_quest_lie != 0 dans SQLite: {cnt}")

# Affichons quelques exemples
c.execute("""
    SELECT q.id, q.texte, q.n_quest_lie, p.texte as parent_texte
    FROM questions q
    LEFT JOIN questions p ON q.n_quest_lie = p.id
    WHERE q.n_quest_lie != 0
    LIMIT 15
""")
print("\n--- EXEMPLES DE QUESTIONS LIÉES ---")
for r in c.fetchall():
    print(f"#{r[0]} ({r[1][:30]}...) -> Liée à #{r[2]} ({str(r[3])[:30]}...)")

conn.close()
