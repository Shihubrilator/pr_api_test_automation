import requests
import json


def test_POST_LogIn_500_InvalidEmailPassword(pr_url, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/login'
    payload = json.dumps({'Email': config['pr']['login'],
                          'Password': config['pr']['passwd']})
    headers = {'Accept': config['pr']['headers']['accept'],
               'Content-Type': config['pr']['headers']['content_type']}
    r = requests.post(url=request_url, data=payload, headers=headers)
    assert r.json()['Result'] == 'error', 'Expected "error", but result is "{}"'.format(r.json()['Result'])
    assert r.json()['ErrorDescription'] == 'Invalid email or password.', \
        'Expected "Invalid email or password.", but ErrorDescription is "{}"'.format(r.json()['ErrorDescription'])


def test_POST_LogIn_200(pr_url, config, conn):
    request_url = pr_url + '0/login'
    payload = json.dumps({'Email': config['pr']['login'],
                          'Password': config['pr']['passwd']})
    headers = {'Accept': config['pr']['headers']['accept'],
               'Content-Type': config['pr']['headers']['content_type']}
    r = requests.post(url=request_url, data=payload, headers=headers)
    cursor = conn.cursor()
    cursor.execute("SELECT Id, Culture FROM sec.Users where Email = '" + config['pr']['login'] + "'")
    data = cursor.fetchall()
    assert r.json()['Result'] == 'ok', 'Expected "ok", but result is "{}"'.format(r.json()['Result'])
    assert r.json()['Data']['Id'] == data[0][0], \
        'Expected "{}", but Id is "{}"'.format(data[0][0], r.json()['Data']['Id'])
    assert r.json()['Data']['Settings']['Culture'] == data[0][1], \
        'Expected "{}", but Culture is "{}"'.format(data[0][1], r.json()['Data']['Settings']['Culture'])


def test_DELETE_LogOut_200(pr_url, config, pr_headers):
    request_url = pr_url + str(config['panels']['em']['id']) + '/login'
    r = requests.delete(url=request_url, headers=pr_headers)
    assert r.json()['Result'] == 'ok', 'Expected "ok", but result is "{}"'.format(r.json()['Result'])
