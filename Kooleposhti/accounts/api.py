from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                    return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    # permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

