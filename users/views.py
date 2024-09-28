from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, id):
        # Tenta obter o objeto usando slug e id, retorna 404 se não encontrar
        profile = get_object_or_404(Profile, slug=slug, id=id)
        
        # Instancia o serializer usando o perfil encontrado e passa o contexto da requisição
        serializer = self.serializer_class(profile, context={'request': request})

        # Retorna os dados serializados
        return Response(serializer.data, status=status.HTTP_200_OK)
