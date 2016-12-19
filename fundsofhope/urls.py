"""fundsofhope URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.generic import RedirectView

from fundsofhope import settings
from fundsofhope import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/fundsofhope')),
    url(r'^admin/', admin.site.urls),
    url(r'^ngo/', views.ngo, name='ngos'),
    # url(r'^(?P<project_id>\w{0,50})/upload/', upload_pic),
    # url(r'^saved/', views.upload_pic, name='saved'),
    url(r'^user/signup/', views.signup, name='signup'),
    url(r'^user/account/', views.account, name='account'),
    url(r'^project/donate/', views.donate, name='donate'),
    url(r'^project/', views.project, name='projects'),
    url(r'^trending/', views.trending, name='trending'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
