import requests
import json


def test_GET_CollectorTemplates_200(pr_url, pr_headers, config, conn):
    params = {
        'page': 1,
        'pageSize': 20,
        'filter': 'Deleted~eq~false~and~SurveyId~eq~' + str(config['test_data']['ct_proj_id'])
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectorTemplates'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    data = r.json()['Data'][0]
    cursor = conn.cursor()
    cursor.execute('SELECT sct.Id, sct.PanelId, sct.Name, sct.SurveyId, pnl.Name, srv.State\
                    from data.SurveyCollectorTemplates sct\
                    join data.Panels pnl on sct.PanelId = pnl.Id\
                    join data.Surveys srv on sct.SurveyId = srv.Id\
                    where sct.SurveyId = ' + str(config['test_data']['ct_proj_id']) + ' order by sct.Id desc')
    expected_data = cursor.fetchone()
    assert data['Id'] == expected_data[0], 'Expected "{}", but Id is "{}"'.format(expected_data[0], r.json()['Id'])
    assert data['PanelId'] == expected_data[1], \
        'Expected "{}", but PanelId is "{}"'.format(expected_data[1], r.json()['PanelId'])
    assert data['Name'] == expected_data[2], \
        'Expected "{}", but Name is "{}"'.format(expected_data[2], r.json()['Name'])
    assert data['SurveyId'] == expected_data[3], \
        'Expected "{}", but SurveyId is "{}"'.format(expected_data[3], r.json()['SurveyId'])
    assert data['PanelName'] == expected_data[4], \
        'Expected "{}", but PanelName is "{}"'.format(expected_data[4], r.json()['PanelName'])
    assert data['SurveyState'] == expected_data[5], \
        'Expected "{}", but SurveyState is "{}"'.format(expected_data[5], r.json()['SurveyState'])


def test_GET_CollectorTemplatesId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectortemplates/' + \
                  str(config['test_data']['ct_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    cursor = conn.cursor()
    cursor.execute('select sct.Id, sct.SurveyId, sct.PanelId, sct.ValidationType, sct.Name, sct.AutoFill, sct.Deleted,\
                    pnl.Name, srv.InnerName, srv.SettingsJSON, sct.SettingsJSON, srv.State\
                    from data.SurveyCollectorTemplates sct\
                    join data.Surveys srv on sct.SurveyId = srv.Id\
                    join data.Panels pnl on sct.PanelId = pnl.Id\
                    where sct.Id = ' + str(config['test_data']['ct_id']))
    xpctd_data = cursor.fetchone()
    data = r.json()['Data']
    assert data['Id'] == xpctd_data[0], 'Expected "{}", but "{}"'.format(xpctd_data[0], data['Id'])
    assert data['SurveyId'] == xpctd_data[1], 'Expected "{}", but "{}"'.format(xpctd_data[1], data['SurveyId'])
    assert data['PanelId'] == xpctd_data[2], 'Expected "{}", but "{}"'.format(xpctd_data[2], data['PanelId'])
    assert data['ValidationType'] == xpctd_data[3], \
        'Expected "{}", but "{}"'.format(xpctd_data[3], data['ValidationType'])
    assert data['Name'] == xpctd_data[4], 'Expected "{}", but "{}"'.format(xpctd_data[4], data['Name'])
    assert data['AutoFill'] == xpctd_data[5], 'Expected "{}", but "{}"'.format(xpctd_data[5], data['AutoFill'])
    assert data['Deleted'] == xpctd_data[6], 'Expected "{}", but "{}"'.format(xpctd_data[6], data['Deleted'])
    assert data['PanelName'] == xpctd_data[7], 'Expected "{}", but "{}"'.format(xpctd_data[7], data['PanelName'])
    assert data['SurveyName'] == xpctd_data[8], 'Expected "{}", but "{}"'.format(xpctd_data[8], data['SurveyName'])
    assert data['ShowCaptcha'] == json.loads(xpctd_data[9])['ShowCaptcha'], \
        'Expected "{}", but "{}"'.format(json.loads(xpctd_data[9])['ShowCaptcha'], data['ShowCaptcha'])
    assert data['AllowDuplicates'] == json.loads(xpctd_data[10])['AllowDuplicates'], \
        'Expected "{}", but "{}"'.format(json.loads(xpctd_data[10])['AllowDuplicates'], data['AllowDuplicates'])
    assert json.loads(data['SurveyRewards']) == json.loads(xpctd_data[10])['SurveyRewards'], \
        'Expected "{}", but "{}"'.format(json.loads(xpctd_data[10])['SurveyRewards'], data['SurveyRewards'])
    assert data['InvitationTemplate'] == json.loads(xpctd_data[10])['InvitationTemplate'], \
        'Expected "{}", but "{}"'.format(json.loads(xpctd_data[10])['InvitationTemplate'], data['InvitationTemplate'])
    assert data['ReminderTemplate'] == json.loads(xpctd_data[10])['ReminderTemplate'], \
        'Expected "{}", but "{}"'.format(json.loads(xpctd_data[10])['ReminderTemplate'], data['ReminderTemplate'])
    assert data['SurveyState'] == xpctd_data[11], 'Expected "{}", but "{}"'.format(xpctd_data[11], data['SurveyState'])
    #assert data['IsValid'] - что это, зачем и откуда беоется?
    #ErrorMessage и ParsedString - что это, зачем и откуда беоется?


def test_GET_CollectorTemplatesId_400_IncorrectID(pr_url, pr_headers, config):
    param_ctid = 'incorrect_ctid'
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectortemplates/' + param_ctid
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['status'] == 400
    assert data['title'] == 'One or more validation errors occurred.'


def test_GET_CollectorTemplatesId_404_NoSuchID(pr_url, pr_headers, config):
    param_ctid = '1'
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectortemplates/' + param_ctid
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['Status'] == 404


def test_POST_CollectorTemplates_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectortemplates'
    payload = {
        "Name": "NewmanTestCollector",
        "SurveyId": config['test_data']['ct_proj_id_post']
    }
    r = requests.post(url=request_url, data=json.dumps(payload), headers=pr_headers)
    data = r.json()['Data']
    cursor = conn.cursor()
    cursor.execute('select Id, SurveyId, PanelId, ValidationType, Name, AutoFill, Deleted, SettingsJSON\
                    from data.SurveyCollectorTemplates\
                    where SurveyId = ' + str(config['test_data']['ct_proj_id_post']) + ' order by Id desc')
    xpctd_data = cursor.fetchone()
    assert data['Id'] == xpctd_data[0]
    assert data['SurveyId'] == xpctd_data[1]
    assert data['PanelId'] == xpctd_data[2]
    assert data['ValidationType'] == xpctd_data[3]
    assert data['Name'] == xpctd_data[4]
    assert data['AutoFill'] == xpctd_data[5]
    assert data['Deleted'] == xpctd_data[6]
    assert json.loads(data['SurveyRewards']) == json.loads(xpctd_data[7])['SurveyRewards']


def test_POST_CollectorTemplates_400_SurveyArchived(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectortemplates'
    payload = {
        "Name": "NewmanTestCollector",
        "SurveyId": config['test_data']['ct_proj_id_arch']
    }
    r = requests.post(url=request_url, data=json.dumps(payload), headers=pr_headers)
    data = r.json()
    assert data['Result'] == 'error'
    assert data['Status'] == 400
    assert data['ErrorCode'] == 'surveyArchived'
