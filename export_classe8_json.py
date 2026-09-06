import sqlite3
import json

conn = sqlite3.connect('affinity.db')
c = conn.cursor()
c.execute('SELECT id, pack_id, cible, classe, thematique, sujet, type, texte, config_reponses FROM questions WHERE classe = 8 ORDER BY id ASC')
rows = c.fetchall()

questions = []
for r in rows:
    cfg = json.loads(r[8]) if r[8] else {}
    questions.append({
        "id": r[0],
        "pack_id": r[1],
        "cible": r[2],
        "classe": r[3],
        "thematique": r[4],
        "sujet": r[5],
        "type": r[6],
        "texte": r[7],
        "config": cfg
    })

conn.close()

with open('classe8_questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Exporté {len(questions)} questions classe 8 vers classe8_questions.json")
