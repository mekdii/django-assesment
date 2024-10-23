from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from .serializers import CustomLoginSerializer, CustomRegisterSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save(self.request)
            refresh = RefreshToken.for_user(user)
            response_data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'role': user.role
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({"email": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)





class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def get_response(self):
        user = self.serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        role = user.role

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'role': role
        }
        return Response(response_data)
