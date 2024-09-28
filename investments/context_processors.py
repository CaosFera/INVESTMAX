

from .models import LogoSite






def logomarca(request):
    logo = LogoSite.objects.first()
    
    return {'logo':logo}