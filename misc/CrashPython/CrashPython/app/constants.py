from urllib.parse import urljoin

FLAG = 'grey{pyth0n-cv3-2021-3177_0r_n0t?_cd924ee8df15912dd55c718685517d24}'

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
