import requests
import json


def test_GET_AdminWithdrawal_200(pr_url, pr_headers, config, conn):
    param_sort = '?sort='
    param_page = '&page=1'
    param_pagesize = '&pageSize=20'
    param_group = '&group='
    param_filter = '&filter=PanelUserId~eq~' + str(config['test_data']['referrer_id'])
    request_url = pr_url + str(config['panels']['em']['id']) + '/AdminWithdrawal' + param_sort + param_page + \
        param_pagesize + param_group + param_filter
    r = requests.get(url=request_url, headers=pr_headers)
    cursor = conn.cursor()
    data = r.json()['Data'][0]
    cursor.execute("SELECT wr.Id, wr.RequestTypeId, wr.CurrencyId, wr.Amount, wr.Requisites, wr.Updated, usr.NiceName \
                    FROM data.WithdrawalRequests wr \
                    JOIN sec.Users usr ON wr.PanelUserId = usr.Id \
                    where wr.PanelUserId = " + str(config['test_data']['referrer_id']) + " \
                    ORDER BY wr.Id DESC")
    expected_data = cursor.fetchone()
    assert data['Id'] == expected_data[0]
    assert data['RequestTypeId'] == expected_data[1]
    assert data['CurrencyId'] == expected_data[2]
    assert data['Amount'] == expected_data[3]
    phone = data['Requisites']['Phone']
    expected_phone = json.loads(expected_data[4])['Phone']
    assert phone['CountryId'] == expected_phone['CountryId']
    assert phone['CountryCode'] == expected_phone['CountryCode']
    assert phone['Operator'] == expected_phone['Operator']
    assert phone['Number'] == expected_phone['Number'].\
        replace(expected_phone['Number'][0:len(expected_phone['Number'])-4], '****')
    assert data['Updated'][:-1] == expected_data[5].isoformat()
    assert data['PanelUserNiceName'] == expected_data[6]


def test_GET_AdminWithdrawalId_200(pr_url, pr_headers, config, conn):
    request_url = pr_url + str(config['panels']['em']['id']) + \
                  '/adminwithdrawal/' + str(config['test_data']['withdrawal_id'])
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()['Data']
    cursor = conn.cursor()
    cursor.execute("SELECT wr.Id, wr.RequestTypeId, wr.CurrencyId, wr.Amount, wr.Requisites, wr.Updated, usr.NiceName \
                        FROM data.WithdrawalRequests wr \
                        JOIN sec.Users usr ON wr.PanelUserId = usr.Id \
                        where wr.Id = " + str(config['test_data']['withdrawal_id']) + " \
                        ORDER BY wr.Id DESC")
    expected_data = cursor.fetchone()
    assert data['Id'] == expected_data[0]
    assert data['RequestTypeId'] == expected_data[1]
    assert data['CurrencyId'] == expected_data[2]
    assert data['Amount'] == float('{:.2f}'.format(expected_data[3]))
    wallet = data['Requisites']['Wallet']
    expected_wallet = json.loads(expected_data[4])['Wallet']
    assert wallet['CountryId'] == expected_wallet['CountryId']
    assert wallet['Type'] == expected_wallet['Type']
    assert wallet['Number'] == expected_wallet['Number']
    assert data['Updated'][:-1] == expected_data[5].isoformat()
    assert data['PanelUserNiceName'] == expected_data[6]


def test_GET_AdminWithdrawalId_400_IncorrectID(pr_url, pr_headers, config):
    param_wrid = 'incorrect_wrid'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminwithdrawal/' + param_wrid
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['status'] == 400
    assert data['title'] == 'One or more validation errors occurred.'


def test_GET_AdminWithdrawalId_404_NoSuchID(pr_url, pr_headers, config):
    param_wrid = '99999999999'
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminwithdrawal/' + param_wrid
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()
    assert data['Result'] == 'error'
    assert data['Status'] == 404
    assert data['ErrorCode'] == 'notFound'


#вообще дергается в ЛК на странице вывода средств. возвращает правила для вывода.
#хз где лежат эти правила
def test_GET_AdminWithdrawalMethod_200(pr_url, pr_headers, config):
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminwithdrawalmethod'
    r = requests.get(url=request_url, headers=pr_headers)
    data = r.json()['Data']
    for el in data:
        if el['CountryId'] == 1001 and el['Name'] == 'Mobile phone account':
            assert el['MinAccountBalance'] == 500.0000
            break
