from os import getenv

from dotenv import load_dotenv

load_dotenv()

PAT_KEY = getenv('PAT', None)
assert PAT_KEY

print(PAT_KEY, 'CONFIG.PY')