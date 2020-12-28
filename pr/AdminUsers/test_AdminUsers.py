import json
import requests


def test_Adminusers_200(pr_url, pr_headers, config, conn):
    params = {
        'sort': '',
        'page': 1,
        'pageSize': 20,
        'group': '',
        'filter': 'Id~eq~' + str(config['test_data']['user_id']) + '~and~Status~eq~0' #190868777
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("SELECT NiceName, PanelId FROM sec.Users WHERE Id = " + str(config['test_data']['user_id']))
    data = cursor.fetchall()
    for el in r_json['Data']:
        if el['Id'] == config['test_data']['user_id']:
            assert el['NiceName'] == data[0][0]
            assert el['PanelId'] == data[0][1]
            break


def test_GET_Adminusers_403_ForbiddenWrongAuth(pr_url, pr_headers):
    param_panelId = 'w1www'
    request_url = pr_url + param_panelId + '/adminusers'
    r = requests.get(url=request_url, headers=pr_headers)
    assert r.json()['ErrorCode'] == 'forbidden'


def test_GET_AdminusersID_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + str(config['test_data']['user_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Data']['UserToken'] is None


def test_GET_AdminusersID_400_InvalidId(pr_url, pr_headers, config):
    param_adminusersid = 'ttt'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + param_adminusersid
    r = requests.get(url=request_url, headers=pr_headers)
    assert r.status_code == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'


def test_POST_AdminusersIdDeactivate_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + \
                  str(config['test_data']['user_id']) + '/deactivate'
    r = requests.post(url=request_url, headers=pr_headers)
    assert r is not None
    assert isinstance(r, requests.Response)
    assert r.status_code == 200


def test_POST_AdminusersIdDeactivate_400_Invalid(pr_url, pr_headers, config):
    param_adminusersid = 'wwww'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + \
                  param_adminusersid + '/deactivate'
    r = requests.post(url=request_url, headers=pr_headers)
    assert r.status_code == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'


def test_POST_AdminusersIdDeactivate_404_UserNotExist(pr_url, pr_headers, config):
    param_adminusersid = '1'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + \
                  param_adminusersid + '/deactivate'
    r = requests.post(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Status'] == 404


def test_POST_AdminusersIdActivate_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + \
                  str(config['test_data']['user_id']) + '/activate'
    r = requests.post(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Status'] == 200


def test_POST_AdminusersIdActivate_400_InvalidID(pr_url, pr_headers, config):
    param_id = 'ddd'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + param_id + '/activate'
    r = requests.post(url=request_url, headers=pr_headers)
    assert r.status_code == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'


def test_POST_AdminusersIdActivate_404_UserNotExist(pr_url, pr_headers, config):
    param_id = '2'
    requests_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + param_id + '/activate'
    r = requests.post(url=requests_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Status'] == 404


def test_POST_AdminusersIdRemove_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + \
                  str(config['test_data']['user_id']) + '/remove'
    r = requests.post(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.status_code == 200


def test_POST_AdminusersIdRemove_400_InvalidID(pr_url, pr_headers, config):
    param_id = 'ddd'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + param_id + '/remove'
    r = requests.post(url=request_url, headers=pr_headers)
    assert r.status_code == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'


def test_POST_AdminusersIdRemove_404_UserNotExist(pr_url, pr_headers, config):
    param_id = '186380786'
    request_url = pr_url + str(config['panels']['em']['id']) + '/admonusers/' + param_id + '/remove'
    r = requests.post(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.status_code == 404


def test_POST_AdminusersIdRestore_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + \
                  str(config['test_data']['user_id']) + '/restore'
    r = requests.post(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.status_code == 200


def test_POST_AdminusersIdRestore_400_InvalidID(pr_url, pr_headers, config):
    param_id = 'wwwww'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + param_id + '/restore'
    r = requests.post(url=request_url, headers=pr_headers)
    assert r.json()['status'] == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'


def test_POST_AdminusersIdRestore_404_UserNotExist(pr_url, pr_headers, config):
    param_id = '0009'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/' + param_id + '/restore'
    r = requests.post(url=request_url, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Status'] == 404


def test_GET_AdminusersLegacyIsemailavailable_200_true(pr_url, pr_headers, config):
    params = {
        'email': '31575530621@yandex.ru'
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/legacy/isemailavailable'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Data']['result'] == 'Ok'


def test_GET_AdminusersLegacyIsemailavailable_200_InvalidEmail(pr_url, pr_headers, config):
    params = {
        'email': '111'
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/legacy/isemailavailable'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Data']['result'] == 'Invalid'


def test_GET_AdminusersLegacyIsemailavailable_200_ForbiddenDomain(pr_url, pr_headers, config):
    params = {
        'email': '111@yopmail.com'
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/legacy/isemailavailable'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    assert r.json()['Data']['result'] == 'Invalid'


def test_GET_AdminusersLegacyIsemailavailable_200_NotAvailableEmail(pr_url, pr_headers, config):
    params = {
        'email': config['test_data']['existing_email']
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusers/legacy/isemailavailable'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    assert isinstance(r.json(), dict)
    assert r is not None
    assert r.json()['Data']['result'] == 'NotAvailable'


'''
#?????? ШО ЗА ДИЧЬ???????
def test_GET_AdminusersLegacyIsemailavailable_403_WrongPanelID(pr_url, pr_headers, pr_panelId):
    params = {
        'fulldata': 'false'
    }
    request_url = pr_url + str(pr_panelId) + '/adminusers/bulk/export'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    assert isinstance(r, requests.Response)
    assert r is not None
    r.json()['Status'] == 403
'''


def test_PUT_AdminUserProfileId_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserprofile/' + str(config['test_data']['user_id'])
    payload = json.dumps(config['test_data']['json'])
    r = requests.put(url=request_url, data=payload, headers=pr_headers)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Result'] == 'ok'
