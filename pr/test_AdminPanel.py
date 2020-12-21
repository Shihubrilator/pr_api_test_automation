import requests


def test_GET_AdminPanel_200(pr_url, pr_headers, panel):
    request_url = pr_url
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    for el in r_json['Data']:
        if el['Id'] == panel[0]:
            assert el['PanelSettings']['SupportEmail'] == panel[1]
            assert el['CurrencyId'] == panel[2]
            assert el['CurrencyCode'] == panel[3]
    assert r_json['Result'] == 'ok'


def test_GET_AdminPanelId_200(pr_url, pr_headers, pr_panel_short_label, config):
    request_url = pr_url + str(config['panels']['em']['id'])
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    assert r_json['Data']['Id'] == config['panels']['em']['id']
    assert r_json['Data']['PanelSettings']['ShortLabel'] == pr_panel_short_label
    assert r_json['Result'] == 'ok'
