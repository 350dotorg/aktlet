from django.conf import settings
from django.db import connections 
from django.http import HttpResponse
from django.template import Template, Context
from django.utils.datastructures import SortedDict
import json

from actionkit_raplet.models import Configuration

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        SortedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def raplet(request):

    if request.GET.get("show") == "metadata":
        data = metadata(request)
    else:

        if request.user.is_anonymous():
            return HttpResponse("forbidden") #@@TODO

        data = base_user_data(request)

    data = json.dumps(data)
    if 'callback' in request.GET:
        return HttpResponse("%s(%s);" % (request.GET['callback'], data), content_type="text/javascript")
    return HttpResponse(json.dumps(data), content_type="application/json")

def base_user_data(request):

    config = Configuration.objects.get(slug="")

    email = request.GET['email']

    ak = connections['ak'].cursor()

    ak.execute(config.sql, [email])
    try:
        results = dictfetchall(ak)[0]
    except IndexError:
        results = None

    if results is None:
        return {
            "status": 404,
            }

    data = {
        "html": Template(config.html).render(Context(results)),
        "css": config.css,
        #            "js": "alert('Hello world!');",
        "status": 200
        }
    return data

def metadata(request):
    data = {
        'name': "%s Actionkit Raplet" % settings.SITE_NAME,
        'description': "Display Actionkit data for %s" % settings.SITE_NAME,
        'welcome_text': "Welcome!",
        'icon_url': settings.SITE_LOGO_URL,
        'preview_url': settings.SITE_LOGO_URL,
        'provider_name': settings.SITE_NAME,
        'provider_url': settings.ACTIONKIT_API_HOST,
        'config_url': "https://%s/oauth2/authorize/" % settings.SITE_DOMAIN,
        }
    return data
