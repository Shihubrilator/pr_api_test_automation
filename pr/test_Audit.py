import requests


def test_GET_Audit_200(pr_url, pr_headers, config):
    param_rel = '?relatedTo=' + str(config['test_data']['project_id'])
    param_format = '&format=json'
    request_url = pr_url + str(config['panels']['em']['id']) + '/audit' + param_rel + param_format
    r = requests.get(url=request_url, headers=pr_headers)
    assert isinstance(r.json()['Data'], list)
    assert len(r.json()['Data']) > 0
