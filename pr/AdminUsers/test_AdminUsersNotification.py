import pytest
import requests
import pymongo
#from bson import objectid


@pytest.mark.skip()
def test_GET_AdminUserNotification_200(pr_url, pr_headers, config):
    params = {
        'UserId': config['test_data']['referrer_id'],
        'sort': 'Created-desc',
        'page': 1,
        'pageSize': 20,
        'group': '',
        'filter': ''
    }
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusernotification'
    r = requests.get(url=request_url, headers=pr_headers, params=params)

    #+ Id есть в Messages UserId
    #mongo OIConverterNew MessagesBatchs Template
    clnt = pymongo.MongoClient("Rhenium:27017")
    db = clnt.OIConverterNew
    message = db.Messages.find({"UserId": 900002})
    #result = db.MessagesBatchs.find({"ObjectId": })
    #print(result[0]['Template'])

    clnt.close()

    assert True
