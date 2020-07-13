from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView


from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.serializers import LoginSerializer
from rest_auth.views import LoginView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from open.users.serializers import UserCreateSerializer, UserTokenSerializer

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class LoginNoCSRFAPIView(LoginView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = LoginSerializer


class RegisterNoCSRFAPIView(APIView):
    # from stackoverflow
    # for sign up fields, don't want/need an auth class
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)
        response_serializer = UserTokenSerializer(token)
        return Response(response_serializer.data)


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GITHUB
    client_class = OAuth2Client
