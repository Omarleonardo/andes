"""api_oak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

# Django
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

# Docs
from docs.urls import docs_endpoint

# pokedex app
from apps.pokedex.urls import pokedex_enpoints


urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="docs"),
        name="index",
    ),
    path("admin/", admin.site.urls),
    path("", include((docs_endpoint, "docs"), namespace="docs")),
    path("", include((pokedex_enpoints, "pokedex"), namespace="pokedex")),
]
