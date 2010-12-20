from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from datetime import datetime
from tagging.models import Tag, TaggedItem
from django.views.decorators.csrf import csrf_exempt

from unishare.documents.models import Document, DocumentForm

## Dynamic content

def root(request):
    featureset = Document.objects.values_list('school', flat=True).order_by('school').distinct() 
    return render_to_response('all_schools.html', {'schools': featureset, 'cat': 'main' })

def school(request, school):
    featureset = Document.objects.values_list('course', flat=True).filter(school=school).order_by('course').distinct() 
    return render_to_response('by_school.html', {'classes': featureset, 'cat': 'main', 'school': school })

## Forms ##

def upload(request):
    if request.method == 'POST': # If the form has been submitted...
        form = DocumentForm(request.POST, request.FILES) # A form bound to the POST data
        print form
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # XXX: Check filetypes, etc

            form.save()
            return HttpResponseRedirect('/') # Redirect after POST
        else:
            print "Shiiiiit"
    else:
        form = DocumentForm() # An unbound form

    return render_to_response('upload.html', {
        'form': form,
        'cat': 'upload' 
    })

## Static ##
def about(request):
    return render_to_response('about.html', {'cat': 'about' })

def contact(request):
    return render_to_response('contact.html', {'cat': 'contact' })

