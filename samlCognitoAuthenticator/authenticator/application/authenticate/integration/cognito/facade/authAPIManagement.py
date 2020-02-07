import logging
import urllib.parse
from http.client import HTTPSConnection
from base64 import b64encode
import json

from application.generic.base.constants.exceptionConstants import *
from application.generic.base.exception.businessExceptions import *
from application.generic.base.exception.exceptionUtility import ExceptionUtility


class OAuthManager:
    logger = logging.getLogger(__name__)

    def __init__(self, client_id, client_secret, redirect_uri, domain, region):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.domain = domain
        self.region = region

        self.token_endpoint = None
        self.token_path = None

    def set_token_endpoint(self):
        self.token_endpoint = "{0}.auth.{1}.amazoncognito.com".format(self.domain, self.region)
        self.token_path = "/oauth2/token"

    def post_token_endpoint_request(self, authorization_code):
        self.logger.debug("Sending POST Request for TOKEN Endpoint to AWS....")

        try:
            headers = {
                "Authorization": "Basic {0}".format(self.encode_auth_header()),
                "Content-type": "application/x-www-form-urlencoded",
            }

            query = urllib.parse.urlencode({
                        "grant_type": "authorization_code",
                        "client_id": self.client_id,
                        "code": authorization_code,
                        "redirect_uri": self.redirect_uri,
                    }
            )

            con = HTTPSConnection(self.token_endpoint)
            con.request("POST", self.token_path, body=query, headers=headers)
            response = con.getresponse()

            self.logger.debug("Response Code Received: {0}".format(response.status))

            if response.status == 200 or response.status == 400:
                res_data = str(response.read().decode('utf-8'))
                data = json.loads(res_data)
                return response.status, data

            return None, None
        except Exception as ex:
            self.logger.error("Exception occurred in Auth API Management : {}".format(ex))
            raise ExceptionUtility.create_exception_detail(ExceptionConstants.CODE_AUTH_API_MGMT_EXCEPTION,
                                                           ExceptionConstants.USERMESSAGE_AUTH_API_MGMT_EXCEPTION,
                                                           str(ex),
                                                           AuthAPIManagementException.__name__)

    def encode_auth_header(self):
        # authorization header through Basic HTTP authorization using format client_id:secret
        encoded_auth_header = "{0}:{1}".format(self.client_id, self.client_secret)
        return b64encode(bytes(encoded_auth_header, "utf-8")).decode("ascii")
