from rest_framework import serializers
from .models import Profile, CustomUser, Investments
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from investments.serializers import InvestmentsSerializer  # Importe o InvestmentsSerializer




"""

CustomUser = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False, max_length=30)
    last_name = serializers.CharField(required=False, max_length=30)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        Profile.objects.create(user=user)        
        return user



class CustomLoginSerializer(serializers.Serializer):
    username = None 
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        # Extrai os dados do request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Autentica o usuário com o email e senha fornecidos
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if user is None:
                raise AuthenticationFailed(_('Invalid email or password.'))
            if not user.is_active:
                raise AuthenticationFailed(_('User account is disabled.'))
        else:
            raise AuthenticationFailed(_('Must include "email" and "password".'))

        attrs['user'] = user
        return attrs

"""

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined']  


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    profile_url = serializers.SerializerMethodField()
    investment = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user','id', 'slug', 'profile_url', 'investment'] 

    def get_profile_url(self, obj):
        # Pega o request do contexto do serializer
        request = self.context.get('request')
        # Constrói a URL absoluta usando o request e os campos slug e id
        return request.build_absolute_uri(f'/users/profile/{obj.slug}/{obj.id}/')

    def get_investment(self, obj):
        investments = obj.investment.all()
        serializer = InvestmentsSerializer(investments, many=True, context=self.context)
        return serializer.data