from unittest import TestCase
from fitbit import Fitbit
import copy
import json
import mock
import requests_mock


class TestFitbitSupport(TestCase):
    client_kwargs = {
        'client_id': '22D42B',
        'client_secret': '0982b100f5c82fafae5f3a91f5fc1742',
        'redirect_uri': 'http://127.0.0.1:8000/en/user/fitbit/login',
        'scope': 'weight'
    }

    def test_authorize_token_url(self):
        # authorize_token_url calls auth and returns URL
        fb = Fitbit(**self.client_kwargs)
        retval = fb.client.authorize_token_url()
        self.assertEqual(retval[0], 'https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=22D42B&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fen%2Fuser%2Ffitbit%2Flogin&scope=activity+nutrition+heartrate+location+nutrition+profile+settings+sleep+social+weight&state=' + retval[1])

    def test_fetch_access_token(self):
        # tests the fetching of access token using code and redirect_URL
        fb = Fitbit(**self.client_kwargs)
        fake_code = "fake_code"
        with requests_mock.mock() as m:
            m.post(fb.client.access_token_url, text=json.dumps({
                'access_token': 'fake_return_access_token',
                'refresh_token': 'fake_return_refresh_token'
            }))
            retval = fb.client.fetch_access_token(fake_code)
        self.assertEqual("fake_return_access_token", retval['access_token'])
        self.assertEqual("fake_return_refresh_token", retval['refresh_token'])

    def test_refresh_token(self):
        # test of refresh function
        kwargs = copy.copy(self.client_kwargs)
        kwargs['access_token'] = 'fake_access_token'
        kwargs['refresh_token'] = 'fake_refresh_token'
        kwargs['refresh_cb'] = lambda x: None
        fb = Fitbit(**kwargs)
        with requests_mock.mock() as m:
            m.post(fb.client.refresh_token_url, text=json.dumps({
                'access_token': 'fake_return_access_token',
                'refresh_token': 'fake_return_refresh_token'
            }))
            retval = fb.client.refresh_token()
        self.assertEqual("fake_return_access_token", retval['access_token'])
        self.assertEqual("fake_return_refresh_token", retval['refresh_token'])


if __name__ == '__main__':
    unittest.main()
