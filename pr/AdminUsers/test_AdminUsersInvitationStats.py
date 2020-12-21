import requests


def test_GET_AdminUserInvitationStatsId_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserinvitationstats/' + str(config['test_data']['referrer_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    assert r_json['Data']['UserId'] == config['test_data']['referrer_id']
