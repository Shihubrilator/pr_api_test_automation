import requests
import json


def test_GET_AdminUserInvitation_200(pr_url, pr_headers, config, conn):
    params = {
        'sort': 'Created-desc',
        'page': 1,
        'pageSize': 20,
        'group': '',
        'filter': 'PanelUserId~eq~' + str(config['test_data']['referrer_id'])
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserinvitation'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP(20) inv.Id, sur.Name, inv.SurveyId, scol.SettingsJSON \
                    FROM data.Invitations inv \
                    JOIN data.SurveyCollectors scol ON inv.SurveyId = scol.SurveyId \
                    JOIN data.Surveys sur ON inv.SurveyId = sur.Id \
                    WHERE inv.PanelUserId = " + str(config['test_data']['referrer_id']) + " \
                    ORDER BY inv.Id DESC")
    data = cursor.fetchall()
    SettingsJSON = json.loads(data[0][3])
    min_r = min(rew[1] for rew in SettingsJSON['SurveyRewards'].items())
    max_r = max(rew[1] for rew in SettingsJSON['SurveyRewards'].items())
    reward = str(format(min_r, '.2f'))
    if min_r != max_r:
        reward += ' - ' + str(format(max_r, '.2f'))
    reward += ' баллов'
    for key in r.json()['Data']:
        if key['Id'] == data[0][0]:
            assert key['SurveyName'] == data[0][1] #'Сопельки' #[data].[Surveys] Name
            assert key['SurveyId'] == data[0][2] #190834489 #[data].[Invitations] SurveyId
            assert key['Reward'] == reward#'10.00 - 20.00 баллов' #[data].[SurveyCollectors] SettingsJSON SurveyReward
            break


def test_GET_AdminUserInvitationId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserinvitation/' \
                  + str(config['test_data']['invitation_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("SELECT SurveyId FROM data.Invitations \
                    WHERE Id = " + str(config['test_data']['invitation_id']))
    data = cursor.fetchall()
    assert r_json['Data']['Id'] == config['test_data']['invitation_id']
    assert r_json['Data']['SurveyId'] == data[0][0]


def test_DELETE_AdminUsersInvitationInvitationId(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserinvitation/' \
                  + str(config['test_data']['invitation_id'])
    r = requests.delete(url=request_url, headers=pr_headers)
    assert r.json()['Result'] == 'ok'


def test_POST_AdminUserInvitationIdRestore_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserinvitation/' \
                  + str(config['test_data']['invitation_id']) + '/restore'
    r = requests.post(url=request_url, headers=pr_headers)
    assert r.json()['Result'] == 'ok'


def test_POST_SessionsIdStatus_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/sessions/' \
                  + str(config['test_data']['session_id']) + '/status'
    payload = '{"newStatus": 91}'
    r = requests.post(url=request_url, headers=pr_headers, data=payload)
    assert isinstance(r, requests.Response)
    assert r is not None
    assert r.json()['Data']['FinishStatus'] == 91


def test_POST_AdminUserInvitationIdChangeStatus_400_InvalidJSON(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/sessions/' + \
                  str(config['test_data']['invitation_id']) + '/status'
    payload = '{91}'
    r = requests.post(url=request_url, data=payload, headers=pr_headers)
    assert r.json()['ErrorCode'] == 'Invalid newStatus type'


def test_POST_AdminUserInvitationIdChangeStatus_400_NoSuchId(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/sessions/2331/status'
    payload = '{"newStatus": 91}'
    r = requests.post(url=request_url, data=payload, headers=pr_headers)
    r.json()['ErrorCode'] == 'Unknown Session'
