from django.conf.urls import include, url
from django.contrib import admin
from cms import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.loginView),
	url(r'^logout/', views.logoutView),
    url(r'^authenticate/', views.loginPage),
    url(r'^$', views.mainPage),
    url(r'^(\w+)/$', views.getPage),
    url(r'^annotated/(\w+)/$', views.getPageTemplate),
]
