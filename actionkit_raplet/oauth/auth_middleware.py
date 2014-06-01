from django.contrib.auth import authenticate

class OAuthMiddleware(object):

    def process_request(self, request):
        if 'oauth_token' not in request.REQUEST:
            return 
        token = request.REQUEST['oauth_token']
        user = authenticate(access_token=token)
        if user is not None:
            request.user = user
        return 

