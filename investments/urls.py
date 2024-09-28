from django.urls import path
from .views import InvestmentsListView, InvestmentDetail

urlpatterns = [
    path('investments/', InvestmentsListView.as_view(), name='investments-list'),
    path('investments/<slug:slug>/', InvestmentDetail.as_view(), name='investments-detail'),
    
]
