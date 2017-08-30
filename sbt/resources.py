"""
Simple API wrapper for SBT
"""

from urllib import parse
from requests import Response

import requests
from django.conf import settings


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

    url: str = settings.SBT_API_URL
    security_token: str = None
    org_code: str = settings.SBT_ORG_CODE

    def __init__(self):
        self.security_token = self.get_security_token()  # at the moment, we just always get a new token

    def get_security_token(self, api_key: str = settings.SBT_API_KEY) -> str:
        """
        This method uses the API Key to obtain a new Security Token
        """

        url: str = ''.join(
            [
                self.url,
                'LoginAPIService.svc/AuthenticateAPIKey?',
                parse.urlencode({'APIKey': api_key})
            ]
        )

        json_data: dict = requests.get(url).json()
        return json_data['AuthenticateAPIKeyResult'].get('SecurityToken')

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
