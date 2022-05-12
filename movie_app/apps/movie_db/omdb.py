import urllib.request
from urllib.error import HTTPError
from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_503_SERVICE_UNAVAILABLE


class OMDB(object):
    def __init__(self, omdb_api_url: str, omdb_api_key: str):
        self.client_url = f'{omdb_api_url}?apikey={omdb_api_key}'

    def retrieve_description(self, movie_title: str) -> str:
        # If it was API for official use I would take care about OMDB API daily limit 1000 requests/day
        # or just buy full OMDB API without limit.
        # For actual purposes I think it's impossible to pass the limit. I'm a fan of YAGNI philosophy.
        try:
            # I used urllib to not implement more project dependencies but I prefer requests lib
            description = urllib.request.urlopen(f'{self.client_url}&t={movie_title}').read().decode('utf-8')
            return description
        except HTTPError as e:
            code = e.getcode()
            if code == HTTP_401_UNAUTHORIZED:
                raise NotAuthenticated()
            elif code == HTTP_503_SERVICE_UNAVAILABLE:
                raise APIException()
