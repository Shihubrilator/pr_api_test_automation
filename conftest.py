import pytest
import requests
import pyodbc
import json
import yaml
import pymongo
from bs4 import BeautifulSoup as Soup


def pytest_addoption(parser):
    parser.addoption('--server', action='store', default='dev', help="Choose server: qa or dev")
    parser.addoption("--urltype", action="store", default='1', help="выбор апишного пути. 1 - api/v2/admin/panel/")


def get_config():
    with open("..\\config.yml", "r", encoding='utf8') as ymlfile:
        return yaml.load(ymlfile, Loader=yaml.FullLoader)


def get_db_connect(connection_string):
    conn = pyodbc.connect(connection_string)
    return conn


@pytest.fixture(scope='session')
def config():
    return get_config()


@pytest.fixture(scope='session')
def conn(request, config):
    server = request.config.getoption('server')
    c = get_db_connect(config['sqldb'][server + '_connection_string'])
    yield c
    c.close()


@pytest.fixture(scope='session')
def mongo(request):
    if request.config.getoption('server') == 'qa':
        mongo_client = pymongo.MongoClient("Rhenium:27017")
    else:
        mongo_client = pymongo.MongoClient("mintaka01:50401")
    db = mongo_client.OIConverterNew
    yield db
    mongo_client.close()


@pytest.fixture(scope='session')
def pr_api_path(pytestconfig):
    """переключение api_path"""
    url_type = pytestconfig.getoption('urltype')
    if url_type == '1':
        return 'api/v2/admin/panel/'
    elif url_type == '2':
        pass
    elif url_type == '3':
        pass


@pytest.fixture(scope='session')
def pr_url(config, pr_api_path):
    """лепим основу URL"""
    return config['pr']['domain'] + pr_api_path


@pytest.fixture(scope='session')
def login(pr_url, config):
    """получение куки авторизации"""
    request_url = pr_url + '0/login'
    payload = json.dumps({'Email': config['pr']['login'], 'Password': config['pr']['passwd']})
    headers = {'Accept': config['pr']['headers']['accept'],
               'Content-Type': config['pr']['headers']['content_type']}
    r = requests.post(url=request_url, data=payload, headers=headers)
    return r.cookies.get_dict()['authtoken']


@pytest.fixture()
def pr_headers(login, config):
    """лепим хидер запроса"""
    return {'Accept': config['pr']['headers']['accept'],
            'Cookie': 'authtoken=' + login,
            'Content-Type': config['pr']['headers']['content_type']}


def get_panels_meta():
    """параметрицзация для test_AdminPanel"""
    config = get_config()
    conn = get_db_connect(config['sqldb']['dev_connection_string'])

    cursor = conn.cursor()
    cursor.execute("SELECT Id, CurrencyId, SettingsJSON FROM data.Panels")
    data = cursor.fetchall()

    # id email curr_id curr_symb
    panels_meta = [[], [], []]
    panels_meta[0].append(config['panels']['em']['id'])
    panels_meta[1].append(config['panels']['ob']['id'])
    panels_meta[2].append(config['panels']['oy']['id'])

    for row in data:
        if row[0] == panels_meta[0][0]:
            panels_meta[0].append(json.loads(row[2])['SupportEmail'])
            panels_meta[0].append(row[1])
        if row[0] == panels_meta[1][0]:
            panels_meta[1].append(json.loads(row[2])['SupportEmail'])
            panels_meta[1].append(row[1])
        if row[0] == panels_meta[2][0]:
            panels_meta[2].append(json.loads(row[2])['SupportEmail'])
            panels_meta[2].append(row[1])

    cursor.execute("SELECT Id, AllProperties FROM meta.Objects WHERE ObjectType = 'Currency'")
    data = cursor.fetchall()

    for i in range(len(panels_meta)):
        soup = Soup(dict(data)[panels_meta[i][2]], 'lxml')
        panels_meta[i].append(soup.find('symbol').string)

    conn.close()

    return panels_meta


@pytest.fixture()
def pr_panel_short_label(config):
    conn = get_db_connect(config['sqldb']['dev_connection_string'])

    cursor = conn.cursor()
    cursor.execute('SELECT SettingsJSON FROM data.Panels WHERE Id=' + str(config['panels']['em']['id']))
    data = cursor.fetchall()

    panel_short_label = json.loads(data[0][0])['ShortLabel']

    conn.close()

    return panel_short_label


def id_func(fixture_value):
    """A function for generating ids."""
    t = fixture_value
    return '{},{},{},{}'.format(t[0], t[1], t[2], t[3])


@pytest.fixture(params=get_panels_meta(), ids=id_func)
def panel(request):
    return request.param
