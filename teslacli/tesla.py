from __future__ import absolute_import, print_function

import requests


class Tesla(object):
    HEADERS = {
        'Content-Type': 'application/json'
    }

    def __init__(self, base_url='https://owner-api.teslamotors.com'):
        self._base_url = base_url
        self._auth_token = None

    def login(self, username, password, client_id, client_secret):
        resp = requests.post(
            self._get_url('/oauth/token'),
            headers=self._get_headers(),
            json={
                'grant_type': 'password',
                'client_id': client_id,
                'client_secret': client_secret,
                'email': username,
                'password': password,
            }
        )
        resp.raise_for_status()

        self._auth_token = resp.json().get('access_token')
        return self._auth_token

    def fetch_vehicles(self):
        return self._get('/api/1/vehicles')

    def unlock_doors(self, vehicle_id):
        return self._post('/api/1/vehicles/{0}/command/door_unlock'.format(vehicle_id))

    def lock_doors(self, vehicle_id):
        return self._post('/api/1/vehicles/{0}/command/door_lock'.format(vehicle_id))

    def wake(self, vehicle_id):
        return self._post('/api/1/vehicles/{0}/wake_up'.format(vehicle_id))

    
    def _get(self, uri):
        resp = requests.get(self._get_url('/api/1/vehicles'), headers=self._get_headers())
        resp.raise_for_status()

        return resp.json().get('response')

    def _post(self, uri):
        resp = requests.post(self._get_url(uri), headers=self._get_headers(), **kwargs)
        resp.raise_for_status()

        return resp.json().get('response')

    def _get_url(self, uri):
        return '{0}{1}'.format(self._base_url, uri)

    def _get_headers(self):
        headers = {}
        headers.update(self.HEADERS)

        if self._auth_token:
            headers.update({
                'Authorization': 'Bearer {0}'.format(self._auth_token)
            })

        return headers