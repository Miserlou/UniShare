from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^captcha/', include('captcha.urls')),
     (r'^unishare/', include('unishare.documents.urls')),
     (r'^upload/', 'unishare.documents.views.upload'),
     (r'^about/', 'unishare.documents.views.about'),
     (r'^contact/', 'unishare.documents.views.contact'),
     

    # Uncomment the admin/doc line below to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
     (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'static'}),
     (r'^$', 'unishare.documents.views.root')
)
