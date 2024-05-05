import logging
import numpy as np
import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from .constants import EMBEDDING_QUERY_MODEL_URI, EMBEDDING_URL, FOLDER_ID
from .errors import TooManyRequests
from .iam_token_getter import get_token_with_retries
from .models import Phrase

logger = logging.getLogger(__name__)


@retry(
    retry=retry_if_exception_type(TooManyRequests),
    wait=wait_fixed(2),
    stop=stop_after_attempt(3),
    reraise=True,
)
def get_embedding(text: str) -> np.array:
    query_data = {
        'modelUri': EMBEDDING_QUERY_MODEL_URI,
        'text': text,
    }

    response = requests.post(
        EMBEDDING_URL,
        json=query_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {get_token_with_retries()}',
            'x-folder-id': f'{FOLDER_ID}',
        },
    )

    if response.status_code == 429:
        raise TooManyRequests

    response.raise_for_status()

    json_data = response.json()
    logger.debug(f'Received response with data {json_data}')

    return np.array(json_data['embedding'])


def get_or_load_phrase_embedding(phrase: Phrase):
    if phrase.embedding is None:
        phrase.embedding = get_embedding(phrase.content).tolist()
        phrase.save()
    return phrase.embedding
