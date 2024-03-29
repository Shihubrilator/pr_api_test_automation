import requests


def test_GET_AdminUsersCharge_200(pr_url, pr_headers, config, conn):
    params = {
        'page': 1,
        'pageSize': 20,
        'filter': 'PanelUserId~eq~' + str(config['test_data']['referrer_id'])
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusercharge'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    cursor = conn.cursor()
    cursor.execute("SELECT TOP (20) Id, Value, CurrentRelatedObjectId \
                    FROM data.Charges WHERE PanelUserId = " + str(config['test_data']['referrer_id']) + " \
                    ORDER BY Id DESC")
    data = cursor.fetchall()
    for key in r.json()['Data']:
        if key['Id'] == data[0][0]:
            assert key['Amount'] == str(round(data[0][1], 2))+' баллов'#'9.00 баллов'
            assert key['CurrentRelatedObjectId'] == data[0][2]#1161700
            break
