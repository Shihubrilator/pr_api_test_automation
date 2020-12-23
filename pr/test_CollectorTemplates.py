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
    assert data['Id'] == expected_data[0]
    assert data['PanelId'] == expected_data[1]
    assert data['Name'] == expected_data[2]
    assert data['SurveyId'] == expected_data[3]
    assert data['PanelName'] == expected_data[4]
    assert data['SurveyState'] == expected_data[5]


def test_GET_CollectorTemplatesId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/collectortemplates/' + \
                  str(config['test_data']['ct_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()['Data']
    cursor = conn.cursor()
    cursor.execute('select sct.Id, sct.SurveyId, sct.PanelId, sct.ValidationType, sct.Name, sct.AutoFill, sct.Deleted,\
                    pnl.Name, srv.InnerName, srv.SettingsJSON, sct.SettingsJSON, srv.State\
                    from data.SurveyCollectorTemplates sct\
                    join data.Surveys srv on sct.SurveyId = srv.Id\
                    join data.Panels pnl on sct.PanelId = pnl.Id\
                    where sct.Id = ' + str(config['test_data']['ct_id']))
    xpctd_data = cursor.fetchone()
    assert data['Id'] == xpctd_data[0]
    assert data['SurveyId'] == xpctd_data[1]
    assert data['PanelId'] == xpctd_data[2]
    assert data['ValidationType'] == xpctd_data[3]
    assert data['Name'] == xpctd_data[4]
    assert data['AutoFill'] == xpctd_data[5]
    assert data['Deleted'] == xpctd_data[6]
    assert data['PanelName'] == xpctd_data[7]
    assert data['SurveyName'] == xpctd_data[8]
    assert data['ShowCaptcha'] == json.loads(xpctd_data[9])['ShowCaptcha']
    #assert data['AllowDuplicates'] - хз где живет в базе
    assert json.loads(data['SurveyRewards']) == json.loads(xpctd_data[10])['SurveyRewards']
    assert data['InvitationTemplate'] == json.loads(xpctd_data[10])['InvitationTemplate']
    assert data['ReminderTemplate'] == json.loads(xpctd_data[10])['ReminderTemplate']
    assert data['SurveyState'] == xpctd_data[11]
    #assert data['IsValid'] - хз где живет в базе
    #ErrorMessage и ParsedString - хз где живут в базе


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
