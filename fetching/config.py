from normalize import QualysProcessing, CrowdstrikeProcessing


BASE_URL = 'https://api.recruiting.app.silk.security/api'
VENDORS = {
    f'{BASE_URL}/qualys/hosts/get': QualysProcessing,
    f'{BASE_URL}/crowdstrike/hosts/get': CrowdstrikeProcessing,
}
API_KEY = 'shared-zevetone@armis.com_357c050d-e4da-432a-a2e5-f61516928717'
HEADERS = {
    'Token': f'{API_KEY}',
    'Accept': 'application/json'
}

MONGODB_URI = 'mongodb://root:example@mongo:27017'
MONGODB_DB_NAME = 'hosts'
MONGODB_ALIAS = 'default'

BATCH_LEN = 1       # for sample purposes