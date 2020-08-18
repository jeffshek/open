import logging

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from rest_auth.registration.views import SocialLoginView
from rest_auth.serializers import LoginSerializer, JWTSerializer
from rest_auth.views import LoginView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from open.users.serializers import (
    UserCreateSerializer,
    UserTokenSerializer,
    UserReadSerializer,
    UserDeleteSerializer,
)

User = get_user_model()

logger = logging.getLogger(__name__)


class EmptyView(APIView):
    """
    Empty View that returns nothing because django-all-auth tries to resolve a form, but we don't use forms
    since this is only an API ...
    """

    authentication_classes = ()
    permission_classes = ()

    def get(self, *args):
        return Response()


class LoginNoCSRFAPIView(LoginView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = LoginSerializer

    def post(self, *args):
        # leave for debugging temporarily
        return super().post(*args)

    def get_response_serializer(self):
        # override default response serializer to also include user and token (this is used by redux to set userinfo)
        if getattr(settings, "REST_USE_JWT", False):
            response_serializer = JWTSerializer
        else:
            response_serializer = UserTokenSerializer
        return response_serializer


class RegisterNoCSRFAPIView(APIView):
    # from stackoverflow
    # for registration forms, don't want/need an auth class
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)
        response_serializer = UserTokenSerializer(token)
        return Response(status=201, data=response_serializer.data)


class UserDetailsView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserReadSerializer(user)
        return Response(serializer.data)


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GITHUB
    client_class = OAuth2Client


class UserDeleteView(APIView):
    model_class = User

    def delete(self, request, uuid):
        context = {"request": request}
        serializer = UserDeleteSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        # many paranoia checks, i don't want someone to be deleted by accident / malice
        instance = request.user
        valid_request = instance.uuid == uuid
        if not valid_request:
            raise Http404

        label = (
            f"DELETED | {self.model_class} | ID {instance.id} deleted by {request.user}"
        )
        logger.error(label)
        instance.delete()

        return Response(status=204)
