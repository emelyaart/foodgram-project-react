from rest_framework.views import APIView
from rest_framework import parsers, renderers
from .serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class AuthToken(APIView):
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser,
                      parsers.JSONParser)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
