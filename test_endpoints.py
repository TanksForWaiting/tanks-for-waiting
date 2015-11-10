import requests
get, post, put, delete = requests.get, requests.post, requests.put, requests.delete
firebase_url = "https://tanks-for-waiting.firebaseio.com"
local_url = "http://localhost:8000/api/"
heroku_url = "cryptic-citadel-5628.herokuapp.com/api/"

def test_post_player():
    player = post(local_url + 'players/')
    assert player.status_code == 201
    assert len(player.json()['player_id']) == 36

def test_post_game():
    player = post(local_url + 'players/')
    player_id = player.json()['player_id']
    new_game = post(local_url + 'games/', data={'player_id': player_id})
    check_game = get(firebase_url + '/games/{}.json'.format(new_game.json()['game_id']))
    assert player.status_code == 201
    assert new_game.status_code == 201
    assert check_game.status_code == 200
    assert len(player.json()['player_id']) == 36
    assert len(new_game.json()['game_id']) == 36
    assert new_game.json()['players'][0] == player_id
    # assert len(check_game.json()['tanks']) == 1
    assert len(check_game.json()['targets']) == 5



def test_get():
    player = get(local_url + 'players/')
    game = get(local_url + 'games/')
    assert player.status_code == 200
    assert game.status_code == 200

def test_fail_destroy_target():
    player = post(local_url + 'players/').json()
    player_id = player['player_id']
    game = post(local_url + 'games/', data={'player_id': player_id}).json()
    targets = get(firebase_url + '/games/{}.json'.format(game['game_id']))
    target_id = [key for key in targets.json()['targets']][0]
    fail_delete = delete(local_url + 'games/{}/targets/{}/'.format(game['game_id'], target_id))
    board = get(firebase_url + '/games/{}.json'.format(game['game_id'])).json()
    assert fail_delete.status_code == 403
    assert target_id in board['targets']

def test_player_destroy_target():
    player = post(local_url + 'players/').json()
    player_id = player['player_id']
    game = post(local_url + 'games/', data={'player_id': player_id}).json()
    targets = get(firebase_url +'/games/{}.json'.format(game['game_id'])).json()
    target_id = [key for key in targets['targets']][0]
    target = targets['targets'][str(target_id)]
    put(firebase_url + '/games/{}/tanks/{}/x.json'.format(game['game_id'],player_id), data=str(target['x']))
    put(firebase_url + '/games/{}/tanks/{}/y.json'.format(game['game_id'],player_id), data=str(target['y']))
    delete_target = delete(local_url + 'games/{}/targets/{}/'.format(game['game_id'], target_id), json=player_id)
    check_data = get(firebase_url + '/games/{}.json'.format(game['game_id'])).json()
    assert target_id not in check_data['targets']
    assert delete_target.status_code == 200
    assert len(check_data['targets']) == 5
