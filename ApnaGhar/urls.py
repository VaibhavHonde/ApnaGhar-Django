"""
URL configuration for AptDB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include  # <--- Added 'include' here
from django.contrib.auth import views as auth_views
import app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),
    # Property management
    path('properties/', views.my_properties, name='my_properties'),
    path('properties/add/', views.add_property, name='add_property'),
    path('properties/<int:apt_id>/edit/', views.edit_property, name='edit_property'),
    path('properties/<int:apt_id>/delete/', views.delete_property, name='delete_property'),
    path('properties/<int:apt_id>/add-image/', views.add_image, name='add_image'),
    path('properties/image/<int:image_id>/delete/', views.delete_image, name='delete_image'),
    # also expose login at /login/ for convenience
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),  # <--- Add this new line!
    path('', views.index, name='index'),
    path('browseall/', views.browse_all, name='browse_all'),
    path('searchapts/', views.search_apts, name='search_apts'),
    path('view/<int:id>/', views.view_apt, name='view_apt'),
]
