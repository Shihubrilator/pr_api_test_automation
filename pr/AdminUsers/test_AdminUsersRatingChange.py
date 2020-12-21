import json
import requests


def test_GET_AdminusersRatingChange_200_NotEmptyData(pr_url, pr_headers, config, conn):
    param_sort = '?sort=Created-desc'
    param_page = '&page=1'
    param_pageSize = '&pageSize=20'
    param_group = '&group='
    param_filter = '&filter=UserId~eq~' + str(config['test_data']['rating_user_id'])
    request_url = pr_url + str(config['panels']['em']['id']) + '/AdminUserRatingChange' + param_sort + param_page + param_pageSize + \
                  param_group + param_filter
    r = requests.get(url=request_url, headers=pr_headers)
    cursor = conn.cursor()
    cursor.execute("SELECT Id, Increment FROM data.RatingChanges \
                    WHERE UserId=" + str(config['test_data']['rating_user_id']))
    data = cursor.fetchall()
    for key in r.json()['Data']:
        if key['Id'] == data[0][0]:
            assert key['Increment'] == data[0][1]
            assert key['UserId'] == config['test_data']['rating_user_id']
            break


def test_GET_AdminuserRasingChange_200_EmptyData(pr_url, pr_headers):
    param_panelId = 'df'
    request_url = pr_url + param_panelId + '/adminuserratingchange'
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    assert isinstance(r_json['Data'], list)
    assert len(r_json['Data']) == 0
    assert r_json['Result'] == 'ok'


def test_POST_AdminuserRatingChangeIdRatingChange_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserratingchange/' + \
                  str(config['test_data']['referrer_id']) + '/ratingchange'
    rating = 41
    payload = json.dumps({
        "Increment": rating,
        "Remark": "autotest_piu_piu"
    })
    r = requests.post(url=request_url, headers=pr_headers, data=payload)
    cursor = conn.cursor()
    cursor.execute("SELECT Rating FROM sec.Users WHERE Id = " + str(config['test_data']['referrer_id']))
    data = cursor.fetchall()
    assert r.json()['Result'] == 'ok'
    assert data[0][0] == rating


def test_POST_AdminuserRatingChangeIdRatingChange_400_InvalidIncrement(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserratingchange/' + \
                  str(config['test_data']['referrer_id']) + '/ratingchange'
    payload = json.dumps({
        "Increment": "test",
        "Remark": "autotest_piu_piu_400"
    })
    r = requests.post(url=request_url, data=payload, headers=pr_headers)
    r_json = r.json()
    assert r_json['status'] == 400
    assert r_json['title'] == 'One or more validation errors occurred.'


def test_POST_AdminuserRatingChangeIdRaitingChange_404_PanelNotFound(pr_url, pr_headers, config):
    param_panelid = ''
    request_url = pr_url + param_panelid + '/adminuserratingchange/' + \
                  str(config['test_data']['referrer_id']) + '/ratingchange'
    payload = json.dumps({
        "Increment": 41,
        "Remark": "autotest_piu_piu_404"
    })
    r = requests.post(url=request_url, data=payload, headers=pr_headers)
    assert r.status_code == 404
