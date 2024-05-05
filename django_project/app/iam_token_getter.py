import datetime
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .constants import GET_IAM_TOKEN_URL, OAUTH_TOKEN

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
last_update: datetime.datetime | None = None
iam_token: str | None = None


def get_token() -> str:
    global last_update, iam_token

    if last_update is None or datetime.datetime.now() - last_update > datetime.timedelta(hours=1):
        logging.info(f'Updating iam token')
        response = requests.post(GET_IAM_TOKEN_URL, json={'yandexPassportOauthToken': OAUTH_TOKEN})
        response.raise_for_status()
        iam_token = response.json()['iamToken']
        last_update = datetime.datetime.now()
        logger.info('iam_token successfully updated')

    return iam_token


@retry(
    retry=retry_if_exception_type(requests.HTTPError),
    wait=wait_exponential(max=100),
    stop=stop_after_attempt(100),
    reraise=True,
)
def get_token_with_retries():
    global iam_token

    try:
        return get_token()
    except requests.HTTPError as e:
        logger.error(f'Received error {e} during updating iam token')
        if iam_token is not None:
            logger.warning('Still use old version of iam_token')
            return iam_token
        else:
            logger.critical('No iam_token!')
            raise
