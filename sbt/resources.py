"""
Simple API wrapper for SBT
"""

from urllib import parse
from requests import Response

import requests


class APIBase(object):
    """
    Base implementation to connect to an API endpoint
    """
    url: str = None
    endpoint: str = None

    def join(self):
        return f'{self.url}{self.endpoint}'

    def _post(self, data: dict):
        absolute_url = self.join()
        return requests.post(absolute_url, json=data)

    def _get(self, params=None):
        absolute_url = self.join()
        return requests.get(absolute_url, params=params)


class SBTAPI(APIBase):
    """
    Base for SBT API
    """

    url: str = 'https://{env}.solutionsbytext.com/SBT.App.SetUp/RSServices/'
    api_key: str = None
    security_token: str = None
    org_code: str = None
    self.use_test = None

    def __init__(self, api_key: str, org_code: str, security_token: str = None, use_test: bool = True):
        self.api_key = api_key
        self.org_code = org_code
        self.security_token = security_token
        self.use_test = use_test
        

    def get_security_token(self, api_key: str = None) -> str:
        """
        This method uses the API Key to obtain a new Security Token
        """
        api_key =  api_key if api_key else self.api_key
        env: str = 'test' if self.use_test else 'ui'
        url: str = ''.join(
            [
                self.url.format(env),
                'LoginAPIService.svc/AuthenticateAPIKey?',
                parse.urlencode({'APIKey': api_key})
            ]
        )

        json_data: dict = requests.get(url).json()
        self.security_token = json_data['AuthenticateAPIKeyResult'].get('SecurityToken')
        return self.security_token

    def get_default_data(self, data: dict) -> dict:
        """
        Almost every call to SBT requires an Org Code and a Security Token;
        so this sets up those defaults.
        """
        defaults = {
            'securityToken': self.security_token,
            'orgCode': self.org_code
        }

        defaults.update(**data)

        return defaults

    def get(self, data: dict) -> Response:
        """
        Implements the GET HTTP verb for all requests
        """
        return self._get(
            params=self.get_default_data(data)
        )

    def post(self, data: dict) -> Response:
        """
        Implements the POST HTTP verb for all requests
        """
        return self._post(
            data=self.get_default_data(data)
        )

"""
Actual API Interface 
"""


class Carrier(SBTAPI):
    """
    https://www.solutionsbytext.com/api-support/api-documentation/get-carrier-lookup/46/
    """
    endpoint = 'GeneralRSService.svc/GetCarrierLookup'


class RequireVBT(SBTAPI):
    """
    https://www.solutionsbytext.com/api-support/api-documentation/require-vbt/23/
    """
    endpoint = 'MessageRSService.svc/RequireVBT'


class RequestVBT(SBTAPI):
    """
    https://www.solutionsbytext.com/api-support/api-documentation/request-vbt/22/
    """
    endpoint = 'MessageRSService.svc/RequestVBT'


class SendTemplateMessage(SBTAPI):
    """
    https://www.solutionsbytext.com/api-support/api-documentation/send-template-message/25/
    """
    endpoint = 'MessageRSService.svc/SendTemplateMessage'


class GetMessageStatus(SBTAPI):
    """
    https://www.solutionsbytext.com/api-support/api-documentation/get-message-status/32/
    """
    endpoint = 'MessageRSService.svc/GetMessageStatus'
