from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse, TestCase

from .provider import SteadyHQProvider


class SteadyHQTests(OAuth2TestsMixin, TestCase):
    provider_id = SteadyHQProvider.id

    def get_mocked_response(self):
        return MockedResponse(200, """
{
  "emailAddress": "raymond.penners@intenct.nl",
  "firstName": "Raymond",
  "lastName": "Penners",
}
""")
