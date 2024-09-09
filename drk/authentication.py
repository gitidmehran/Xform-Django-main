import logging
from django.contrib.auth.models import AnonymousUser
from keycloak import KeycloakOpenID
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

KEYCLOAK_OPENID = KeycloakOpenID(
    server_url="https://keycloak-qa.vitalanalytics.net/",
    client_id="backend",
    realm_name="laravel",
    client_secret_key="NBjvuQ6SLQSKjdDedaV9ZkIFHRoxdIk3"
)

class TokenNoopUser(AnonymousUser):
    """
    Django Rest Framework needs an user to consider authenticated
    """

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info

    @property
    def is_authenticated(self):
        return True


class KeyCloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # logger.info(request)
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed("No token provided")

        try:
            _, token = token.split(" ")
            # logger.info("Received token: %s", token)
            user_info = KEYCLOAK_OPENID.userinfo(token)
            # logger.info("User info: %s", user_info)
        except Exception as e:
            # logger.exception("Error during authentication: %s", str(e))
            raise AuthenticationFailed("Authentication failed")

        return (TokenNoopUser(user_info=user_info), None)
