import requests


def get_db_data(conn, script: str, fetchall=True):
    cursor = conn.cursor()
    cursor.execute(script)
    if fetchall:
        return cursor.fetchall()
    else:
        return cursor.fetchone()

def test_GET_AdminUserInvitationStatsId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminuserinvitationstats/' \
                  + str(config['test_data']['referrer_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    script = 'SELECT status, count(status) ' \
             'FROM data.Invitations ' \
             'where PanelUserId = {} ' \
             'group by Status'.format(config['test_data']['referrer_id'])
    data = get_db_data(conn, script)
    counts = dict.fromkeys(['Completed', 'Ignored', 'NotCompleted', 'Other', 'Rejected', 'TotalInvitations',
                           'TotalOtherSessions', 'TotalPanelistSessions', 'TotalSessions'], 0)
    for code, count in data:
        if code == 0:
            counts['Ignored'] = count
        elif code == 21:
            counts['Rejected'] = count
    assert r.status_code == 200, 'Request is not OK, status is {}'.format(r.status_code)
    assert r_json['Data']['UserId'] == config['test_data']['referrer_id']
    assert r_json['Data']['Ignored'] == counts['Ignored']
    assert r_json['Data']['Rejected'] == counts['Rejected']

    #completed 91 - ??
    #NotCompleted - ?? = ignored?
    #Other - ??
    #TotalInvitations - sum(0 + 21 + 31 + 91 + 94)
    #TotalOtherSessions ??
    #TotalPanelistSessions ??
    #TotalSessions - panelist + other ??

