from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.forms import ModelForm
from datetime import datetime
from django import forms
from django.conf import settings
from tagging.fields import TagField
from tagging.models import Tag
from captcha.fields import CaptchaField

ulpath = 'unishare/uploads/recordings/'
attachment_file_storage = FileSystemStorage(location='/var/www/unishare/unishare/uploads', base_url='documents')

# Create your models here.
class Document(models.Model):

    # Document specific
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    year = models.CharField(max_length='200', blank=True)
    semester = models.CharField(max_length='200', blank=True)
    school = models.CharField(max_length='200', blank=False)
    course = models.CharField(max_length='200', blank=False)
    professor = models.CharField(max_length='200', blank=False)

    # Files specific
    local_file = models.CharField(max_length='200', blank=True)
    doc_file = models.FileField(upload_to='recordings', storage=attachment_file_storage)
    file_loc = models.CharField(max_length='500', blank=True)
    mimetype = models.CharField(max_length='500', blank=True)

    # Meta specific
    date = models.DateTimeField('date uploaded', blank=True, default=datetime.now())
    approved = models.BooleanField(default=True, blank=True)
    featured = models.BooleanField(default=False, blank=True)

    tags = TagField()

    def save(self):
        super(Document, self).save()

        # New recording, let me know about it
        #if not self.approved:
        #    send_mail('New recording: ' + self.name, 'Public: \n ' + self.public_description + 'Private: \n' +         self.private_description, 'bigvagitabluntz420@gmail.com', ['rich@anomos.info'], fail_silently=False)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

class DocumentForm(ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Document

    #def __init__(self, bound_object=None, *args, **kwargs):
    #    super(RecordingForm, self).__init__(*args, **kwargs)
    #    self.bound_object = bound_object
    #    self.is_updating = False
    #    if self.bound_object:
    #        self.is_updating = True

    def clean(self):
        if self.cleaned_data.get('doc_file',None).size > 209715200:
            raise forms.ValidationError("File too big, son")
        return self.cleaned_data

    def save(self):
        self.bound_object = Document()
        uploaded_file = self.cleaned_data['doc_file']
        import re
        stored_name = re.sub(r'[^a-zA-Z0-9._]+', '-', uploaded_file.name)
        self.bound_object.rec_file.save(stored_name, uploaded_file)
        self.bound_object.mimetype = uploaded_file.content_type
        self.bound_object.name = self.cleaned_data['name']
        self.bound_object.description = self.cleaned_data['description']
        self.bound_object.year = self.cleaned_data['year']
        self.bound_object.semester = self.cleaned_data['semester']
        self.bound_object.school = self.cleaned_data['school']
        self.bound_object.course = self.cleaned_data['course']
        self.bound_object.professor = self.cleaned_data['professor']
        self.bound_object.location = self.cleaned_data['location']
        self.bound_object.date = datetime.now()
        self.bound_object.file_loc = settings.UPLOAD_ROOT + stored_name
        self.bound_object.save() 
