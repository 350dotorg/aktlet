from django.contrib.auth.models import User
from provider.oauth2.models import AccessToken

class OAuthBackend(object):

    def authenticate(self, access_token=None):
        try:
            token = AccessToken.objects.select_related("user").get(
                token=access_token)
        except AccessToken.DoesNotExist:
            return None
        return token.user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
