from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url('^$',
        'actionkit_raplet.views.raplet',
        name='raplet'),
)
