INSTALLED_APPS = [
    'provider',
    'provider.oauth2',
    'actionkit_raplet',
    ]

MIDDLEWARE_CLASSES = [
    'actionkit_raplet.oauth.auth_middleware.OAuthMiddleware',
    ]

AUTHENTICATION_BACKENDS = [
    'actionkit_raplet.oauth.auth_backend.OAuthBackend',
    ]

URLCONFS = [
    ("^oauth2/", "actionkit_raplet.oauth.urls", "oauth2"),
    ("^raplet/", "actionkit_raplet.urls"),
    ]

SETTINGS = {
    "OAUTH_REDIRECT_URI_ENFORCE_PREFIX_ONLY": True,
    }
