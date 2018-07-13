from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import (
    ProviderAccount,
    ProviderException,
)
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class SteadyHQAccount(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('publicProfileUrl')

    def get_avatar_url(self):
        # try to return the higher res picture-urls::(original) first
        try:
            return self.account.extra_data['pictureUrls']['values'][0]
        except Exception:
            # if we can't get higher res for any reason, we'll just return the
            # low res
            pass
        return self.account.extra_data.get('pictureUrl')

    def to_str(self):
        dflt = super(SteadyHQAccount, self).to_str()
        name = self.account.extra_data.get('name', dflt)
        first_name = self.account.extra_data.get('firstName', None)
        last_name = self.account.extra_data.get('lastName', None)
        if first_name and last_name:
            name = first_name + ' ' + last_name
        return name


class SteadyHQProvider(OAuth2Provider):
    id = 'steadyhq'
    # Name is displayed to ordinary users -- don't include protocol
    name = 'SteadyHQ'
    account_class = SteadyHQAccount

    def extract_uid(self, data):
        if 'id' not in data:
            raise ProviderException(
                'SteadyHQ encountered an internal error while logging in. \
                Please try again.'
            )
        return str(data['id'])

    def get_profile_fields(self):
        default_fields = ['id',
                          'first-name',
                          'last-name',
                          'email',
                          'has-password',]
        fields = self.get_settings().get('PROFILE_FIELDS',
                                         default_fields)
        return fields

    def get_default_scope(self):
        scope = []
        if app_settings.QUERY_EMAIL:
            scope.append('r_emailaddress')
        return scope

    def extract_common_fields(self, data):
        return dict(email=data.get('emailAddress'),
                    first_name=data.get('firstName'),
                    last_name=data.get('lastName'))


provider_classes = [SteadyHQProvider]
