import requests


def test_GET_AdminUserReferral_200(pr_url, pr_headers, config, conn):
    param_sort = '?sort=Id-desc'
    param_page = '&page=1'
    param_pageSize = '&pageSize=20'
    param_filter = '&filter=ReferredByUserId~eq~' + str(config['test_data']['referrer_id'])
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserreferral' + param_sort + param_page + \
                  param_pageSize + param_filter
    r = requests.get(url=request_url, headers=pr_headers)
    cursor = conn.cursor()
    cursor.execute("SELECT ReferralNiceName, ReferralEmail, ReferralId, Domain \
                   FROM data.PanelUserReferrals WHERE Id = " + str(config['test_data']['referral_id']))
    data = cursor.fetchall()
    expected_email = data[0][1].replace('@'+data[0][3], '')
    expected_email = expected_email.replace(str(expected_email[2:len(expected_email)-1]), '***')
    for key in r.json()['Data']:
        if key['Id'] == config['test_data']['referral_id']:
            assert key['ReferralNiceName'] == data[0][0]
            assert key['ReferralEmail'] == expected_email+'@'+data[0][3]
            assert key['ReferralId'] == data[0][2]
            break
