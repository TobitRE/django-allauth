from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import SteadyHQProvider


urlpatterns = default_urlpatterns(SteadyHQProvider)
