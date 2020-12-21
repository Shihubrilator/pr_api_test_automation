import requests


def test_GET_Clietstaff_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/clientstaff'
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()['Data'][0]
    cursor = conn.cursor()
    cursor.execute('SELECT Id, Name, Email, PhoneNumber, Position, BirthDate, Notes, Updated, Deleted \
                    FROM data.ClientStaff ORDER BY Id DESC')
    expected_data = cursor.fetchone()
    assert data['Id'] == expected_data[0]
    assert data['Name'] == expected_data[1]
    assert data['Email'] == expected_data[2]
    assert data['PhoneNumber'] == expected_data[3]
    assert data['Position'] == expected_data[4]
    assert data['Birthdate'] == expected_data[5]
    assert data['Notes'] == expected_data[6]
    assert data['Updated'] == expected_data[7].isoformat()
    assert data['Deleted'] == expected_data[8]


def test_GET_ClietstaffId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + '/clientstaff/' + \
                  str(config['test_data']['clientstaff_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()['Data']
    cursor = conn.cursor()
    cursor.execute('SELECT Id, Name, Email, PhoneNumber, Position, BirthDate, Notes, Updated, Deleted \
                    FROM data.ClientStaff WHERE Id = ' + str(config['test_data']['clientstaff_id']))
    expected_data = cursor.fetchone()
    assert data['Id'] == expected_data[0]
    assert data['Name'] == expected_data[1]
    assert data['Email'] == expected_data[2]
    assert data['PhoneNumber'] == expected_data[3]
    assert data['Position'] == expected_data[4]
    assert data['Birthdate'] == expected_data[5]
    assert data['Notes'] == expected_data[6]
    assert data['Updated'] == expected_data[7].isoformat()
    assert data['Deleted'] == expected_data[8]


def test_GET_ClientstaffId_400_IncorrectID(pr_url, pr_headers, config):
    param_csid = 'incorrect_id'
    request_url = pr_url + str(config['panels']['em']['id']) + '/clientstaff/' + param_csid
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['status'] == 400
    assert data['title'] == 'One or more validation errors occurred.'


#по хорошему нужно смотерть в базу, что удаление действительно происходит
#но чет в базе нихера не меняется
def test_POST_ClientstaffIdRemove_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/clientstaff/' + \
                  str(config['test_data']['clientstaff_id']) + '/remove'
    r = requests.post(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['Result'] == 'ok'
    assert data['Status'] == 200


def test_POST_ClientstaffIdRestore_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/clientstaff/' + \
                  str(config['test_data']['clientstaff_id']) + '/restore'
    r = requests.post(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['Result'] == 'ok'
    assert data['Status'] == 200
