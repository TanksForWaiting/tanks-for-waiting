import requests


def test_post_player():
    p = requests.post('http://localhost:8000/api/players/')
    assert p.status_code == 201
    assert len(p.json()['player_id']) == 36

def test_post_game():
    p = requests.post('http://localhost:8000/api/players/')
    player_id = p.json()['player_id']
    g = requests.post('http://localhost:8000/api/games/',
                      data={'player_id': player_id})
    r = requests.get('https://tanks-for-waiting.firebaseio.com/games/{}.json'.format(g.json()['game_id']))
    assert p.status_code == 201
    assert g.status_code == 201
    assert r.status_code == 200
    assert len(p.json()['player_id']) == 36
    assert len(g.json()['game_id']) == 36
    assert g.json()['players'][0] == player_id
    assert len(r.json()['tanks']) == 1
    assert len(r.json()['targets']) == 5



def test_get():
    p = requests.get('http://localhost:8000/api/players/')
    g = requests.get('http://localhost:8000/api/games/')
    assert p.status_code == 200
    assert g.status_code == 200

def test_destroy_target():
    p = requests.post('http://localhost:8000/api/players/')
    player_id = p.json()['player_id']
    g = requests.post('http://localhost:8000/api/games/',
                      data={'player_id': player_id})
    r = requests.get('https://tanks-for-waiting.firebaseio.com/games/{}.json'.format(g.json()['game_id']))
    target_id = [key for key in r.json()['targets']][0]
    d = requests.delete('http://localhost:8000/api/games/{}/targets/{}/'.format(g.json()['game_id'], target_id))
    n = requests.get('https://tanks-for-waiting.firebaseio.com/games/{}.json'.format(g.json()['game_id']))
    assert d.status_code == 200
    # assert target_id not in n.json()['targets'].keys()
