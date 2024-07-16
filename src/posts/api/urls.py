from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, SignUpView, login_view
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]