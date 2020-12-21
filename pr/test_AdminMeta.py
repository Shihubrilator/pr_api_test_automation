import requests
from bs4 import BeautifulSoup as Soup


def test_GET_MetaCity_200(pr_url, pr_headers, conn, config):
    request_url = pr_url + 'meta/city'
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("select obj.AllProperties, loc.LocalText \
        from meta.Objects obj \
        join data.Localizations loc on obj.Id=loc.ObjectId \
        where obj.Id = " + str(config['test_data']['city_id']) + " and \
        loc.Culture = '" + config['test_data']['culture'] + "'")
    data = cursor.fetchall()
    soup = Soup(data[0][0], 'lxml')
    for el in r_json['Data']:
        if el['Id'] == config['test_data']['city_id']:
            assert el['Name'] == data[0][1]
            assert el['CountryId'] == int(soup.find('countryid').string)
            break


def test_GET_MetaState_200(pr_url, pr_headers, conn, config):
    request_url = pr_url + 'meta/state'
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("select obj.AllProperties, loc.LocalText \
            from meta.Objects obj \
            join data.Localizations loc on obj.Id=loc.ObjectId \
            where obj.Id = " + str(config['test_data']['state_id']) + " and \
            loc.Culture = '" + config['test_data']['culture'] + "'")
    data = cursor.fetchall()
    soup = Soup(data[0][0], 'lxml')
    for el in r_json['Data']:
        if el['Id'] == config['test_data']['state_id']:
            assert el['Name'] == data[0][1]
            assert el['CountryId'] == int(soup.find('countryid').string)
            break


def test_GET_MetaCityFilter_200(pr_url, pr_headers, conn, config):
    param_filter = '?filter=CountryId~eq~' + str(config['test_data']['country_id']) + '~and~Name~startswith~%27%D1%84%27'
    request_url = pr_url + 'meta/city' + param_filter
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("select obj.AllProperties, loc.LocalText \
                from meta.Objects obj \
                join data.Localizations loc on obj.Id=loc.ObjectId \
                where obj.Id = " + str(config['test_data']['state_id']) + " and \
                loc.Culture = '" + config['test_data']['culture'] + "'")
    data = cursor.fetchall()
    for el in r_json['Data']:
        if el['Id'] == config['test_data']['state_id']:
            assert el['Name'] == data[0][1]
            assert el['CountryId'] == config['test_data']['country_id']
            break


def test_GET_Meta_MetatypeId_200(pr_url, pr_headers, config):
    request_url = pr_url + 'meta/city/' + str(config['test_data']['city_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    assert r.json()['Data']['Id'] == config['test_data']['city_id']
    assert r.json()['Result'] == 'ok'


def test_GET_Meta_MetatypeId_400(pr_url, pr_headers):
    request_url = pr_url + 'meta/City/fff'
    r = requests.get(url=request_url, headers=pr_headers)
    assert r.json()['status'] == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'
