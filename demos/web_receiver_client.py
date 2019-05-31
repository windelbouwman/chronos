
""" Client for the web receiver script.


"""

import time
import requests

for x in range(1000):
    print(x)
    requests.post('http://localhost:8883/log', data={'value': 1337, 'value2': x})
    time.sleep(1)
