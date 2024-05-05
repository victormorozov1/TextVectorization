import os

PHRASE_MAX_LENGTH = 200

EMBEDDING_FOUND_ANSWER_LEVEL = 0.6
FOLDER_ID = 'b1ge36k3ede9qocova8b'
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN')
GET_IAM_TOKEN_URL = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
EMBEDDING_QUERY_MODEL_URI = f'emb://{FOLDER_ID}/text-search-query/latest'
EMBEDDING_URL = 'https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding'
