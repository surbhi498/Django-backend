from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutView, PasswordResetView, PostViewSet, SignUpView, create_post, login_view
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('create-post/', create_post, name='create_post'),
    path('', include(router.urls)),
]