"""eligibility_rules_server URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rules_server.views import RulesetView, RulingsView

schema_view = get_schema_view(
    openapi.Info(
        title="Eligibility API",
        default_version='v1',
        description="Helps agencies process program eligibility applications",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="catherine.devlin@gsa.gov"),
        license=openapi.License(name="Public Domain"),
    ),
    # validators=['flex', 'ssv'],
    public=True,
)

urlpatterns = [
    url(r'^swagger(?P<format>.json|.yaml)$',
        schema_view.without_ui(cache_timeout=None),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'),
    url(r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=None),
        name='schema-redoc'), ...
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rulings/<str:program>/<str:entity>/', RulingsView.as_view()),
    path('rulings/<str:program>/<str:entity>/rules/', RulesetView.as_view()),
    url(r'^swagger(?P<format>.json|.yaml)$',
        schema_view.without_ui(cache_timeout=None),
        name='schema-json'),
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=None),
        name='schema-swagger-ui'),
]
