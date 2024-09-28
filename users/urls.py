from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import RegisterView
from .views import ProfileView


urlpatterns = [
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),   
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('profile/<slug:slug>/<int:id>/', ProfileView.as_view(), name='profile-detail'),
  
    
]



