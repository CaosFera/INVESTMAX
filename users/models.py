from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from investments.models import Investments
from .managers import CustomUserManager
from django.core.exceptions import ValidationError

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()    

class Profile(models.Model):
    photo = models.ImageField('Photo', upload_to='users/images/', blank=True, null=True, default='users/images/user_deafault.png')
    slug = models.SlugField('Slug', max_length=200, blank=False, editable=False)
    created = models.DateTimeField('Created', auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField('Updated', auto_now=True, blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='users')
    investment = models.ManyToManyField(Investments,  related_name='investments')
    

    def __str__(self):
        return self.user.email
    
    def get_absolute_url(self):
        return reverse('users:users_detail', args=[self.slug, self.id])

    def clean(self):
        super().clean()
        if self.investment.exists():
            raise ValidationError("This user already has this investment.")



def profile_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.user.full_name or instance.user.email)

pre_save.connect(profile_pre_save, sender=Profile)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

