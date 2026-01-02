from os import access

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from task_manager.serializers.users import UserCreateSerializer

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"

def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie(
        key=ACCESS_COOKIE,
        value=access,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=refresh,
        httponly=True,
        samesite="Lax",
    )

def clear_auth_cookies(response: Response):
    response.delete_cookie(ACCESS_COOKIE)
    response.delete_cookie(REFRESH_COOKIE)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_str = str(refresh)

        response = Response(
            {
                "access": access,
                "refresh": refresh_str,
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(response, access, refresh_str)

        return response

class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)

        if not refresh_token:
            return Response(
                {"detail": "Refresh token cookie not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            new_refresh = str(refresh)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "access": new_access,
                "refresh": new_refresh,
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(response, new_access, new_refresh)
        return response

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)

        if refresh_token:

            token = RefreshToken(refresh_token)
            token.blacklist()

            # try:
            #     token = RefreshToken(refresh_token)
            #     token.blacklist()
            # except Exception:
            #     return Response(
            #         {"detail": "Invalid refresh token"},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            response = Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_200_OK,
            )
            clear_auth_cookies(response)
            return response



