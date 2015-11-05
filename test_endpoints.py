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
    assert p.status_code == 201
    assert g.status_code == 201
    assert len(p.json()['player_id']) == 36
    assert len(g.json()['game_id']) == 36
    assert g.json()['players'][0] == player_id


def test_get():
    p = requests.get('http://localhost:8000/api/players/')
    g = requests.get('http://localhost:8000/api/games/')
    assert p.status_code == 200
    assert g.status_code == 200