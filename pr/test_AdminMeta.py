import requests
from datetime import datetime
from bs4 import BeautifulSoup as Soup


def test_GET_MetaCity_200(pr_url, pr_headers, conn, config):
    request_url = pr_url + 'meta/city'
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("select obj.Id, obj.AllProperties, loc.LocalText, loc.LocalDescription, obj.SortOrder, obj.Updated \
                    from meta.Objects obj \
                    join data.Localizations loc on obj.Id=loc.ObjectId \
                    where obj.ObjectType = 'City' and \
                    loc.Culture = '" + config['test_data']['culture'] + "'")
    xpctd_data = cursor.fetchone()
    soup = Soup(xpctd_data[1], 'lxml')
    for data in r_json['Data']:
        if data['Id'] == xpctd_data[0]:
            assert data['CountryId'] == int(soup.find('countryid').string), \
                'CountryId ' + str(data['CountryId']) + '==' + soup.find('countryid').string
            assert data['StateId'] == int(soup.find('parentid').string), \
                'StateId ' + str(data['StateId']) + '==' + soup.find('parentid').string
            assert data['Population'] == float(soup.find('population').string), \
                'Population ' + str(data['Population']) + '==' + soup.find('population').string
            assert data['Name'] == xpctd_data[2], 'City Name ' + data['Name'] + '==' + xpctd_data[2]
            assert data['Description'] == xpctd_data[3], \
                'City Description ' + data['Description'] + '==' + xpctd_data[3]
            assert data['SortOrder'] == xpctd_data[4], 'SortOrder ' + data['SortOrder'] + '==' + xpctd_data[3]
            datetime_object = datetime.strptime(data['Updated'][0:-1], '%Y-%m-%dT%H:%M:%S.%f')
            datetime_str = str(datetime_object.date()) + ' ' + str(datetime_object.time())
            assert datetime_str == str(xpctd_data[5]), 'Updated ' + datetime_str + '==' + str(xpctd_data[5])
            break


def test_GET_MetaState_200(pr_url, pr_headers, conn, config):
    request_url = pr_url + 'meta/state'
    r = requests.get(url=request_url, headers=pr_headers)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("select obj.Id, obj.AllProperties, loc.LocalText, loc.LocalDescription, obj.SortOrder, obj.Updated \
                    from meta.Objects obj \
                    join data.Localizations loc on obj.Id=loc.ObjectId \
                    where obj.ObjectType = 'State' and \
                    loc.Culture = '" + config['test_data']['culture'] + "'")
    xpctd_data = cursor.fetchone()
    soup = Soup(xpctd_data[1], 'lxml')
    for data in r_json['Data']:
        if data['Id'] == xpctd_data[0]:
            assert data['CountryId'] == int(soup.find('countryid').string), \
                'CountryId ' + data['CountryId'] + '==' + soup.find('countryid').string
            assert data['NumCode'] == int(soup.find('numcode').string), \
                'NumCode ' + data['NumCode'] + '==' + soup.find('numcode').string
            assert data['CharCode'] == soup.find('charcode').string, \
                'CharCode ' + data['CharCode'] + '==' + soup.find('charcode').string
            assert data['Name'] == xpctd_data[2], 'Name ' + data['Name'] + '==' + xpctd_data[2]
            assert data['Description'] == xpctd_data[3], 'Description ' + data['Description'] + '==' + xpctd_data[3]
            assert data['SortOrder'] == xpctd_data[4], 'SortOrder ' + data['SortOrder'] + '==' + xpctd_data[4]
            datetime_object = datetime.strptime(data['Updated'][0:-1], '%Y-%m-%dT%H:%M:%S.%f')
            datetime_str = str(datetime_object.date()) + ' ' + str(datetime_object.time())
            assert datetime_str == str(xpctd_data[5]), 'Updated ' + datetime_str + '==' + str(xpctd_data[5])
            break


def test_GET_MetaCityFilter_200(pr_url, pr_headers, conn, config):
    params = {
        'filter': "CountryId~eq~" + str(config['test_data']['country_id']) + "~and~Name~startswith~'ф'"
    }
    request_url = pr_url + 'meta/city'
    r = requests.get(url=request_url, headers=pr_headers, params=params)
    r_json = r.json()
    cursor = conn.cursor()
    cursor.execute("select obj.Id, obj.AllProperties, loc.LocalText, loc.LocalDescription, obj.SortOrder, obj.Updated \
                    from meta.Objects obj \
                    join data.Localizations loc on obj.Id=loc.ObjectId \
                    where obj.ObjectType = 'City' and \
                    loc.Culture = '" + config['test_data']['culture'] + "' and \
                    loc.LocalText like '%ф%' and \
                    obj.AllProperties.value('(/CountryId/text())[1]', 'varchar(max)') = "
                   + str(config['test_data']['country_id']))
    xpctd_data = cursor.fetchone()
    soup = Soup(xpctd_data[1], 'lxml')
    for data in r_json['Data']:
        if data['Id'] == xpctd_data[0]:
            assert data['CountryId'] == int(soup.find('countryid').string), \
                'CountryId ' + str(data['CountryId']) + '==' + soup.find('countryid').string
            assert data['StateId'] == int(soup.find('parentid').string), \
                'StateId ' + str(data['StateId']) + '==' + soup.find('parentid').string
            assert data['Population'] == float(soup.find('population').string), \
                'Population ' + str(data['Population']) + '==' + soup.find('population').string
            assert data['Name'] == xpctd_data[2], 'City Name ' + data['Name'] + '==' + xpctd_data[2]
            assert data['Description'] == xpctd_data[3], \
                'City Description ' + data['Description'] + '==' + xpctd_data[3]
            assert data['SortOrder'] == xpctd_data[4], 'SortOrder ' + data['SortOrder'] + '==' + xpctd_data[3]
            datetime_object = datetime.strptime(data['Updated'][0:-1], '%Y-%m-%dT%H:%M:%S.%f')
            datetime_str = str(datetime_object.date()) + ' ' + str(datetime_object.time())
            assert datetime_str == str(xpctd_data[5]), 'Updated ' + datetime_str + '==' + str(xpctd_data[5])
            break


def test_GET_Meta_MetatypeId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + 'meta/city/' + str(config['test_data']['city_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()['Data']
    cursor = conn.cursor()
    cursor.execute("select obj.Id, obj.AllProperties, loc.LocalText, loc.LocalDescription, obj.SortOrder, obj.Updated \
                    from meta.Objects obj \
                    join data.Localizations loc on obj.Id=loc.ObjectId \
                    where obj.Id = " + str(config['test_data']['city_id']) + " and \
                    loc.Culture = '" + config['test_data']['culture'] + "'")
    xpctd_data = cursor.fetchone()
    soup = Soup(xpctd_data[1], 'lxml')
    assert data['Id'] == xpctd_data[0], 'Id ' + data['Id'] + '==' + xpctd_data[0]
    assert data['CountryId'] == int(soup.find('countryid').string), \
        'CountryId ' + str(data['CountryId']) + '==' + soup.find('countryid').string
    assert data['StateId'] == int(soup.find('parentid').string), \
        'StateId ' + str(data['StateId']) + '==' + soup.find('parentid').string
    assert data['Population'] == float(soup.find('population').string), \
        'Population ' + str(data['Population']) + '==' + soup.find('population').string
    assert data['Name'] == xpctd_data[2], 'City Name ' + data['Name'] + '==' + xpctd_data[2]
    assert data['Description'] == xpctd_data[3], \
        'City Description ' + data['Description'] + '==' + xpctd_data[3]
    assert data['SortOrder'] == xpctd_data[4], 'SortOrder ' + data['SortOrder'] + '==' + xpctd_data[3]
    datetime_object = datetime.strptime(data['Updated'][0:-1], '%Y-%m-%dT%H:%M:%S.%f')
    datetime_str = str(datetime_object.date()) + ' ' + str(datetime_object.time())
    assert datetime_str == str(xpctd_data[5]), 'Updated ' + datetime_str + '==' + str(xpctd_data[5])


def test_GET_Meta_MetatypeId_400(pr_url, pr_headers):
    request_url = pr_url + 'meta/City/fff'
    r = requests.get(url=request_url, headers=pr_headers)
    assert r.json()['status'] == 400
    assert r.json()['title'] == 'One or more validation errors occurred.'
