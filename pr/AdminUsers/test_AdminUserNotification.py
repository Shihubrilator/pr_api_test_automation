import requests
import pymongo

#связь монги и id респа??
def test_GET_AdminUserNotification_200(pr_url, pr_headers, config):
    param_userid = '?UserId=' + str(config['test_data']['referrer_id'])
    param_sort = '&sort=Created-desc'
    param_page = '&page=1'
    param_pagesize = '&pageSize=20'
    param_group = '&group='
    param_filter = '&filter='
    request_url = pr_url + str(config['panels']['em']['id']) + '/adminusernotification' + param_userid + param_sort + \
        param_page + param_pagesize + param_group + param_filter
    r = requests.get(url=request_url, headers=pr_headers)

    #mongo OIConverterNew MessagesBatchs Template
    clnt = pymongo.MongoClient("Rhenium:27017")
    db = clnt.OIConverterNew
    result = db.MessagesBatchs.find({"ObjectId": "210113452"})
    print(result[0]['Template'])

    clnt.close()
