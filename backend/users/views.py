from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, ExpiredTokenError
from rest_framework_simplejwt.views import TokenRefreshView

from users.serializers import RegisterUserSerializer, LoginUserSerializer, CustomUserSerializer



@api_view(["POST"])
@authentication_classes([])   # 🔥 CLAVE
@permission_classes([])
def refresh_token_view(request):
    # obtener refresh token desde http_only
    refresh_token = request.COOKIES.get("refresh_token")
 
    if not refresh_token:
        return Response({"error": "Refresh token no ha sido provisto"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # validar y crear nuevo access token
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response({"message": "El access token ha sido refrescado satisfactoriamente"}, status=status.HTTP_200_OK)
        #setear cookie http_only
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            max_age = 60 * 2 #60 * 60 * 24  # 1 día
        )

        return response
    except InvalidToken:
        response = Response({"error": "Token invalidado"}, status=status.HTTP_401_UNAUTHORIZED)

        response.delete_cookie(
            "refresh_token", 
            path="/",  
            samesite="None",
            )
        response.delete_cookie(
            "access_token", 
            path="/",
            samesite="None",
            )

        return response

"""
class CookieTokenRefreshView(APIView): #es igual a que herede de TokenRefreshView sin las 2 listas vacias
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ...

    def post(self, request, *args, **kwargs):

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token no ha sido provisto"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({"message": "Access token ha sido refrescado satisfactoriamente"}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
                path="/",
                max_age = 60 * 2 #60 * 60 * 24  # 1 día
            )
            return response
        
        except InvalidToken:
            response = Response({"error": "Token invalidado"}, status=status.HTTP_401_UNAUTHORIZED)

            response.delete_cookie(
                "refresh_token", 
                path="/",  
                samesite="None",
                )
            response.delete_cookie(
                "access_token", 
                path="/",
                samesite="None",
                )

            return response
"""


@api_view(["POST"])
def logout_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
    
        except Exception as e:
            return Response({"error": "Token inválido" + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    response =  Response({"message": "Se ha deslogado satisfactoriamente"}, status=status.HTTP_200_OK)

    response.delete_cookie(
        "access_token",    
        path="/",
        samesite="None",
        )
    response.delete_cookie(
        "refresh_token",    
        path="/",
        samesite="None",
        )

    return response


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    
    if request.method == "GET":
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method in ["PUT", "PATCH"]:
        serializer = CustomUserSerializer(
            user, 
            data=request.data, 
            partial = (request.method=="PATCH")
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user_view(request):
    serializer = LoginUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data

        # 🔥 Crear sesión para Django Admin
        #login(request, user)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Guardar la sesión
        #request.session.save()

        response = Response({"user": CustomUserSerializer(user).data},status=status.HTTP_200_OK)

        # Enviar cookies JWT (si quieres)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            max_age = 60 * 2 #60 * 60 * 24  # 1 día
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
            max_age = 60 * 2 #60 * 60 * 24  # 1 día
        )

        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def registration_user_view(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)