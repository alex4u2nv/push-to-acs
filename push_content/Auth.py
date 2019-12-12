import logging
import time

import requests




class Authenticate:
    jwt = None
    token_time = None
    token_timeout = None
    username = None
    password = None
    refresh_token = None
    time_buffer = 10  # seconds
    aims = None

    def __init__(self, base_url, username, password):
        self.username = username
        self.password = password
        base_url = base_url.strip('/')
        self.aims = "{base_url}/auth".format(base_url=base_url)

    def set_resp(self, resp, auth_url):
        """ Handle response from AIMS """
        if resp.status_code == 200:
            resp_json = resp.json()
            self.jwt = resp_json["access_token"]
            self.token_time = time.time()
            self.token_timeout = (resp_json["expires_in"] - self.time_buffer)
            self.refresh_token = resp_json['refresh_token']
            return self.jwt
        else:
            logging.error("Couldn't authenticate to {auth_url}".format(auth_url=auth_url))
            logging.error(
                "Error is: \nCode: {code}\nError: {error}".format(code=resp.status_code, error=resp.text))
            return None

    def request_auth(self, auth_url, payload: dict):
        """ Request an authentication token from AIMS """
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'user-agent': 'python'}
        try:
            resp = requests.post(auth_url, headers=headers,
                                 data=payload)
        except requests.exceptions.RequestException as e:
            logging.error("Could not get a token at {auth_url}".format(auth_url=auth_url))
            logging.error(e)
            return None
        else:
            return self.set_resp(resp=resp, auth_url=auth_url)

    def get_jwt(self):
        auth_url = "{aims}/realms/alfresco/protocol/openid-connect/token".format(aims=self.aims)
        if self.refresh_token is None:
            payload = dict(username=self.username,
                           password=self.password,
                           grant_type='password',
                           client_id='admin-cli')
            return self.request_auth(auth_url=auth_url, payload=payload)
        else:
            elapsed_time = time.time() - self.token_time
            if elapsed_time < self.token_timeout:
                return self.jwt
            refresh_payload = dict(
                grant_type='refresh_token',
                refresh_token=self.refresh_token,
                client_id='admin-cli'
            )
            return self.request_auth(auth_url=auth_url, payload=refresh_payload)
