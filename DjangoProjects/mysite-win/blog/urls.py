#from django.conf.urls.defaults import *
from django.conf.urls import *
import blog.views
urlpatterns = [
    url(r'^$', blog.views.archive,),
    url(r'^create/', blog.views.create_blogpost),
    url(r'^search/$', blog.views.search, name='search'),

]
