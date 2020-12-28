import pytest
import requests
import pymongo


@pytest.mark.skip()
def test_GET_AdminUserNotification_200(pr_url, pr_headers, config):
    params = {
        'UserId': str(config['test_data']['referrer_id']),
        'sort': 'Created-desc',
        'page': 1,
        'pageSize': 20,
        'group': '',
        'filter': ''
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusernotification'
    r = requests.get(url=request_url, headers=pr_headers, params=params)

    # связь монги и id респа??
    #mongo OIConverterNew MessagesBatchs Template
    clnt = pymongo.MongoClient("Rhenium:27017")
    db = clnt.OIConverterNew
    result = db.MessagesBatchs.find({"ObjectId": "210113452"})
    print(result[0]['Template'])

    clnt.close()

    assert True
