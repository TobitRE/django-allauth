import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import SteadyHQProvider


class SteadyHQAdapter(OAuth2Adapter):
    provider_id = SteadyHQProvider.id
#?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=read&state=RANDOM_STRING

#https://steadyhq.com/de/oauth/authorize?client_id=XXX&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fsteadyhq%2Flogin%2Fcallback%2F&scope=r_emailaddress&response_type=code&state=RWBJi6sADs2u
    access_token_url = 'https://steadyhq.com/api/v1/oauth/token'
    authorize_url = 'https://steadyhq.com/oauth/authorize'
    profile_url = 'https://steadyhq.com/api/v1/users/me'
    # See:
    # https://developers.steadyhq.com/#introduction
    access_token_method = 'GET'

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        return self.get_provider().sociallogin_from_response(
            request, extra_data)

    def get_user_info(self, token):
        fields = self.get_provider().get_profile_fields()
        url = self.profile_url + ':(%s)?format=json' % ','.join(fields)
        resp = requests.get(url,
                            headers={'Authorization': ' '.join(('Bearer',
                                     token.token)), 'x-li-src': 'msdk'})
        resp.raise_for_status()
        return resp.json()


oauth2_login = OAuth2LoginView.adapter_view(SteadyHQAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SteadyHQAdapter)
