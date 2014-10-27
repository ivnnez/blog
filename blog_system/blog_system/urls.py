from django.conf.urls import patterns, include, url
from blog_system import settings
from blog.feeds import EntradasFeed
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^categorias/(?P<id_categoria>\d+)/$', 'blog.views.categorias', name='categorias'),
	#url(r'^categorias/$', 'blog.views.categorias', name='categorias'),
	url(r'^base/$', 'blog.views.base', name='base'),
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^demo/$', 'blog.views.demo', name='demo'),
    # url(r'^blog/(?P<slug>[-\w]+)/$', 'blog.views.blog', name='blog'),
    url(r'^blog/(?P<id_blog>\d+)/$', 'blog.views.blog', name='blog'),
    #url(r'^comentar/(?P<id_blog>\d+)/$', 'blog.views.comentar', name='comentar'),
    url(r'^contacto/$','blog.views.contacto_view',name='vista_contacto'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^feeds/$', EntradasFeed()),
)
