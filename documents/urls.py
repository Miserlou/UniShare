from django.conf.urls.defaults import *
from unishare.documents.models import Document 

info_dict = {
  'queryset': Document.objects.all(),
}

urlpatterns = patterns('',
      (r'^upload$', 'unishare.documents.views.upload'),
      (r'^victory$', 'unishare.documents.views.victory'),
      (r'^captcha/', include('captcha.urls')),
)
