"""casestock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('home', views.index, name='index'),
    path('products', views.products, name='products'),
    path('add-case', views.addCase, name='add-case'),
    path('add-design', views.addDesign, name='addDesign'),
    path('add-phone', views.addPhone, name='add-phone'),
    path('edit-stock', views.editStock, name='edit-stock'),
    path('designs-<type>', views.searchCase, name='search'),
    path('design-<ctype>-<dtype>', views.searchDesign, name='searchdesign'),
    path('shopiz-admin-login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('edit-case-<ctype>', views.editCasePage, name='editCasePage'),
    path('admin-design-view-<ctype>', views.adminViewDesign, name='adminViewCase')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
