import requests


def test_GET_Audit_200(pr_url, pr_headers, config):
    params = {
        'relatedTo': str(config['test_data']['project_id']),
        'format': 'json'
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/audit'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    try:
        assert isinstance(r.json()['Data'], list)
        assert len(r.json()['Data']) > 0
    except:
        assert False, "Случился самшит"
