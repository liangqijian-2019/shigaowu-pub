
#coding:utf-8
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader,Context
from blog.models import BlogPost
from blog.models import BlogPostForm

from django.shortcuts import render_to_response
from django.template import RequestContext

#create_blogpost
from datetime import datetime
from django.http import HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def archive(request):
    posts = BlogPost.objects.all().order_by('-timestamp')[:5]
    t = loader.get_template("archive.html")
##  c = Context({'posts': posts})
    html = t.render({'posts': posts, 'form': BlogPostForm()})
    return HttpResponse(html,RequestContext(request))
#   return render_to_response('archive.html', {'posts': posts, 'form': BlogPostForm()}, RequestContext(request))

@csrf_exempt
def create_blogpost(request):
    if request.method == 'POST':

#      BlogPost(
#          title = request.POST.get('title'),
#          body = request.POST.get('body'),
#          timestamp = datetime.now(),
#      ).save()

       form = BlogPostForm(request.POST)
       if form.is_valid():
           post = form.save(commit=False)
           post.timestamp=datetime.now()
           post.save()
    return HttpResponseRedirect('/blog/')
