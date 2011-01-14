from django.conf.urls.defaults import *
from unishare.documents.models import Document 

info_dict = {
  'queryset': Document.objects.all(),
}

urlpatterns = patterns('',
      (r'^upload$', 'unishare.documents.views.upload'),
      (r'^captcha/', include('captcha.urls')),
)
