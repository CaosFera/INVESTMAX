

from rest_framework import generics, status
from .models import Investments
from .serializers import InvestmentsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import Profile
from rest_framework.views import APIView
from .filters import InvestmentsFilter
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100



class InvestmentsListView(generics.ListAPIView):
    queryset = Investments.objects.all()
    serializer_class = InvestmentsSerializer
    pagination_class = CustomPagination 
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InvestmentsFilter
    permission_classes = [AllowAny] 


class InvestmentDetail(APIView):
    def get(self, request, slug, *args, **kwargs):
        try:
            investment = Investments.objects.get(slug=slug)
        except Investments.DoesNotExist:
            return Response({'detail': 'Investimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InvestmentsSerializer(investment, context={'request': request})
        return Response(serializer.data)

    def post(self, request, slug, *args, **kwargs):       
        try:
            investment = Investments.objects.get(slug=slug)
        except Investments.DoesNotExist:
            return Response({'detail': 'Investimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.get(user=request.user)

        if investment in profile.investment.all():
            return Response({'detail': 'Este investimento já está no seu perfil.'}, status=status.HTTP_400_BAD_REQUEST)

        profile.investment.add(investment)
        return Response({'detail': 'Investimento adicionado ao perfil com sucesso.'}, status=status.HTTP_200_OK)
    
   
    def delete(self, request, slug, *args, **kwargs):   
        try:
            investment = Investments.objects.get(slug=slug)
        except Investments.DoesNotExist:
            return Response({'detail': 'Investimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        profile = Profile.objects.get(user=request.user)

        if investment not in profile.investment.all():
            return Response({'detail': 'Este investimento não está no seu perfil.'}, status=status.HTTP_400_BAD_REQUEST)

        profile.investment.remove(investment)
        return Response({'detail': 'Investimento removido do perfil com sucesso.'}, status=status.HTTP_200_OK)
