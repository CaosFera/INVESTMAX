

from .models import Profile






def photo_profile(request):
    photo = Profile.objects.first()
    
    return {'photo':photo}
