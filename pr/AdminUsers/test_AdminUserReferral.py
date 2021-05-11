import requests


def test_GET_AdminUserReferral_200(pr_url, pr_headers, config, conn):
    params = {
        'sort': 'Id-desc',
        'page': 1,
        'pageSize': 20,
        'filter': 'ReferredByUserId~eq~' + str(config['test_data']['referrer_id'])
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserreferral'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    cursor = conn.cursor()
    cursor.execute("SELECT ReferralNiceName, ReferralEmail, ReferralId, Domain \
                   FROM data.PanelUserReferrals WHERE Id = " + str(config['test_data']['referral_id']) \
                   + "order by Id desc")
    xpctd_data = cursor.fetchall()
    expected_email = xpctd_data[0][1][0:xpctd_data[0][1].find('@')]
    expected_email = expected_email.replace(str(expected_email[2:len(expected_email)-1]), '***')
    data = r.json()['Data'][0]
    assert data['ReferralNiceName'] == xpctd_data[0][0], 'ReferralNiceName is "' + xpctd_data[0][0] + \
                                                         '", but expected "' + data['ReferralNiceName'] + '"'
    assert data['ReferralEmail'] == expected_email+'@'+xpctd_data[0][3]
    assert data['ReferralId'] == xpctd_data[0][2]
