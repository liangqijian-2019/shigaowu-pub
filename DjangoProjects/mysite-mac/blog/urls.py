#from django.conf.urls.defaults import *
from django.conf.urls import *
import blog.views
import django.views.generic
urlpatterns = [
#   url(r'^$', django.views.generic.TemplateView ,{'url':'/blog/'}),
    url(r'^$', blog.views.archive),
    url(r'^create/', blog.views.create_blogpost)
]
