from urllib.parse import urljoin

FLAG = 'grey{fake_flag}'

ERROR = 'danger'
SUCCESS = 'success'
JUDGE0_BASE_URL = 'http://crashpython-server-1:2358'
JUDGE0_SUBMIT_URL = urljoin(
    JUDGE0_BASE_URL, '/submissions/?base64_encoded=true&wait=false')


DECODE_KEYS = [
    'stdout',
    'stderr',
    'message',
]

BANNED_WORDS = [
    'os',
    'eval',
    'exec',
    'subprocess',
    'threading',
    'multiprocessing',
    'raise',
    'quit',
    'sys',
    'stdout',
    'stderr',
    'x',
]
