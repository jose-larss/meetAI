from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")
       
        if not raw_token:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f"Validación del Token falló: {str(e)}")
        
        try:
            user = self.get_user(validated_token)

            # 🔹 Retorna exactamente la tupla que DRF espera
            return user, validated_token
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f"Error al solicitar el usuario: {str(e)}")

