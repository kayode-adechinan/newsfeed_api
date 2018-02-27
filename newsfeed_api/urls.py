"""newsfeed_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import  routers
from post import views

from django.conf.urls.static import static
from django.conf import settings

from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter()
router.register("users", views.UserView)
router.register("posts", views.PostView)
router.register("attachments", views.AttachmentView)
router.register("profiles", views.ProfileView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls)),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('search-post/<str:query>/', views.SearchList.as_view()),
    path('search-user-posts/<int:userID>/', views.SearchUserPost.as_view()),
    path('reset-user-password/<int:pk>/', views.UserPasswordReset.as_view())

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)