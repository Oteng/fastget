from __future__ import unicode_literals

current_header = 0
headers = [
    'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
]


def get_next_user_agent():
    """
    :return: returns the a different user agent for a requests
    """
    global current_header
    current_header = (current_header + 1) % 3
    return headers[current_header]
