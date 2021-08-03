import requests
import pymongo
from bson.objectid import ObjectId


#@pytest.mark.skip()
def test_GET_AdminUserNotification_200(pr_url, pr_headers, config, mongo):
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
    data = r.json()['Data']

    message = mongo.Messages.find({"UserId": config['test_data']['referrer_id']}).limit(1)[0]
    batch = mongo.MessagesBatchs.find({'_id': ObjectId(message['BatchId'])})[0]

    preview_text = batch['Template']
    preview_text = preview_text.replace('{UserName}', message['TemplateParameters']['UserName'])
    preview_text = preview_text.replace('{AcceptUrl}', message['TemplateParameters']['AcceptUrl'])
    preview_text = preview_text.replace('{UnsubscribeUrl}', message['TemplateParameters']['UnsubscribeUrl'])
    preview_text = preview_text.replace('{RejectUrl}', message['TemplateParameters']['RejectUrl'])

    assert len(data) == params['pageSize']
    assert data[0]['Id'] == str(message['_id'])
    assert data[0]['Created'] == batch['Created'].isoformat()[:-3] + 'Z'
    assert data[0]['Channel'] == batch['Channel']
    assert data[0]['NotificationEvent'] == batch['NotificationEventId']
    assert data[0]['SendingDateTime'] == batch['Created'].isoformat()[:-3] + 'Z'
    assert data[0]['PreviewText'] == preview_text
    assert data[0]['PreviewSubject'] == batch['AdditionalParameters']['subject']
