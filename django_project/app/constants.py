import os

PHRASE_MAX_LENGTH = 200

EMBEDDING_FOUND_ANSWER_LEVEL = 0.6
FOLDER_ID = 'b1ge36k3ede9qocova8b'
IAM_TOKEN = os.environ.get('IAM_TOKEN')
EMBEDDING_QUERY_MODEL_URI = f'emb://{FOLDER_ID}/text-search-query/latest'
EMBEDDING_URL = 'https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding'
EMBEDDING_HEADERS = {
    'Content-Type': 'application/json', 'Authorization': f'Bearer {IAM_TOKEN}', 'x-folder-id': f'{FOLDER_ID}',
}
