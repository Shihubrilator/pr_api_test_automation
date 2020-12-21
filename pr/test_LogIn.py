import requests
import json


def test_POST_LogIn_500_InvalidEmailPassword(pr_url, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/login'
    payload = json.dumps({'Email': config['pr']['login'],
                          'Password': config['pr']['passwd']})
    headers = {'Accept': config['pr']['headers']['accept'],
               'Content-Type': config['pr']['headers']['content_type']}
    r = requests.post(url=request_url, data=payload, headers=headers)
    assert r.json()['Result'] == 'error'
    assert r.json()['ErrorDescription'] == 'Invalid email or password.'


def test_POST_LogIn_200(pr_url, config, conn):
    request_url = pr_url + '0/login'
    payload = json.dumps({'Email': config['pr']['login'],
                          'Password': config['pr']['passwd']})
    headers = {'Accept': config['pr']['headers']['accept'],
               'Content-Type': config['pr']['headers']['content_type']}
    r = requests.post(url=request_url, data=payload, headers=headers)
    cursor = conn.cursor()
    cursor.execute("SELECT Id, Culture FROM sec.Users where Email='" + config['pr']['login'] + "'")
    data = cursor.fetchall()
    assert r.json()['Result'] == 'ok'
    assert r.json()['Data']['Id'] == data[0][0]
    assert r.json()['Data']['Settings']['Culture'] == data[0][1]


def test_DELETE_LogOut_200(pr_url, config, pr_headers):
    request_url = pr_url + str(config['panels']['em']['id']) + '/login'
    r = requests.delete(url=request_url, headers=pr_headers)
    assert r.json()['Result'] == 'ok'
