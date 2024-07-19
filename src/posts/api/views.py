import json
from rest_framework import viewsets
from ..models import Post
from .serializers import PostModelSerializer
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    print("Request Data:", request.data)
    # refresh_token = request.headers.get('Authorization', '').split(' ')[-1]
    # print(refresh_token)
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if user is None or not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    @action(detail=True, methods=['POST'])
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            message = 'Post unliked'
        else:
            post.likes.add(user)
            message = 'Post liked'
        post.save()
        return Response({'status': message})

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request):
        try:
            # refresh_token = request.headers.get('Authorization', '').split(' ')[-1]
            refresh_token = request.data.get('refresh')
            print(refresh_token)
            if not refresh_token:
                return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Create RefreshToken instance
            token = RefreshToken(refresh_token)

            # Find the OutstandingToken instance
            try:
                outstanding_token = OutstandingToken.objects.get(token=refresh_token)
            except OutstandingToken.DoesNotExist:
                return Response({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            # Add the token to the blacklist
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response({'detail': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
class PasswordResetView(APIView):
    def post(self, request):
        username = request.data.get('username')
        new_password = request.data.get('newPassword')
        if not username or not new_password:
            return JsonResponse({'error': 'Username and new password are required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this username does not exist'}, status=404)

        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password reset successful'}, status=200)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        body = data.get('content')
        user = request.user

        if not title or not body:
            return JsonResponse({'error': 'Title and content are required'}, status=400)

        post = Post.objects.create(title=title, body=body, author=user)
        return JsonResponse({'message': 'Post created successfully', 'post': post.id})

    return JsonResponse({'error': 'Invalid request method'}, status=405)
    