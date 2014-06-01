from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from provider.oauth2.views import (Authorize, Redirect, 
                                   AccessTokenView)
import urlparse

class Authorize(Authorize):
    def get_redirect_url(self, request):
        return reverse('oauth2:access_token')

class AccessTokenView(AccessTokenView):

    template_name = 'actionkit_raplet/oauth/access_token.html' 

    def get(self, request):
        data = self.get_data(request)
        code = self.get_data(request, "code")
        client = self.get_data(request, "client")
        grant = self.get_authorization_code_grant(
            request, {'code': code}, client)

        return self.render_to_response({'grant': grant})

    def access_token_response(self, access_token):
        request = self.request
        data = self.get_data(request)
        client = self.get_data(request, "client")
        redirect_uri = data.get("redirect_uri", None) or client.redirect_uri

        parsed = urlparse.urlparse(redirect_uri)

        query = QueryDict('', mutable=True)

        if 'state' in data and data['state']:
            query['state'] = data['state']

        query['access_token'] = access_token.token

        # rapportive wants the data passed back in fragment, not query string
        parsed = parsed[:4] + ('', query.urlencode()) 

        redirect_uri = urlparse.ParseResult(*parsed).geturl()

        self.clear_data(request)

        return HttpResponseRedirect(redirect_uri)

