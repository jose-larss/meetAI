from django.urls import path


from users.views import registration_user_view, login_user_view, me_view, logout_view, refresh_token_view

urlpatterns = [
    path('registro/', registration_user_view, name="registro_view"),
    path('login/', login_user_view, name="login_view"),
    path('me/', me_view, name="me_view"),
    path('logout/', logout_view, name="logout_view"),
    path('refresh/', refresh_token_view, name="refresh_view"),
]