from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_quote$', views.add_quote),
    url(r'^quotes/(?P<id>\d+)$', views.profile),
    url(r'^quotes/(?P<id>\d+)/edit$', views.edit_quote),
    url(r'^quotes/(?P<id>\d+)/update$', views.update_quote),
    url(r'^quotes/(?P<id>\d+)/favorite$', views.favorite_quote), 
    url(r'^quotes/(?P<id>\d+)/remove_favorite$', views.remove_favorite),
    url(r'^quotes/(?P<id>\d+)/delete$', views.delete_quote),
    url(r'^logout$', views.logout),
]