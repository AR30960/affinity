import urllib.request
import json

def test_modify():
    qid = 31100
    update_data = {
        'thematique': 'Activités',
        'sujet': 'Domestiques',
        'classe': 1,
        'type': 'MULTI',
        'cible': 0,
        'texte': 'Faire la cuisine et concocter de bons petits plats'
    }
    req = urllib.request.Request(
        f'http://localhost:8765/api/questions/{qid}',
        data=json.dumps(update_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print('Réponse modification:', res)

    # Vérification
    res2 = urllib.request.urlopen('http://localhost:8765/api/questions')
    data2 = json.loads(res2.read().decode('utf-8'))
    modified_q = [q for q in data2['questions'] if q['id'] == qid][0]
    print(f"Vérification question #{qid}:", modified_q['texte'])

if __name__ == '__main__':
    test_modify()
