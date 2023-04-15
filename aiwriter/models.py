import requests
from django.db import models
# -============PDF=====
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import FileResponse
# ====
import PyPDF2
from io import StringIO
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.text import slugify
# from ckeditor_uploader.fields import RichTextUploadingField 
from tinymce.models import HTMLField  


# =====================================
class Field(models.Model):
    name = models.CharField(null=True, blank=True,max_length=500)
    def __str__(self):
        return self.name  
    
     
     
class UploadedFile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True, default='New Document')
    doc = models.FileField(upload_to='user_uploads/docx/' , blank=True, null=True)
    pdf = models.FileField(upload_to='user_uploads/pdf/' , blank=True, null=True)
    # raw_doc = RichTextUploadingField(null=True, blank=True)
    parties = models.CharField(max_length=100, blank=True, null=True)
    term = models.CharField(max_length=1000, blank=True, null=True)
    liabilitycap = models.CharField(max_length=1000, blank=True, null=True)
    consideration = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField (blank=True, null=True)
    effectivedate = models.DateField(max_length=1000,blank=True, null=True)
    expirydate = models.DateField(max_length=1000,blank=True, null=True)
    status = models.CharField(max_length=100,blank=True, null=True)
    comment = models.TextField(max_length=255, blank=True, null=True)
    renewal = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title    
     
     

class GoogleScholarFile(models.Model):
    title = models.CharField(max_length=200)
    snippet = models.CharField(max_length=500)
    url = models.URLField()
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField (blank=True, null=True)

    def download_pdf(self):
        """
        Download the pdf file at the URL and save it to the pdf_file field
        """
        if self.url.endswith('.pdf'):
            response = requests.get(self.url)
            self.pdf_file.save(self.filename, ContentFile(response.content), save=True)

    def extract_pdf_content(self):
        """
        Extract the content of the pdf file and save it to the content field
        """
        if self.pdf_file:
            with open(self.pdf_file.path, 'rb') as file:
                pdf = PyPDF2.PdfFileReader(file)
                self.content = '\n'.join(page.extractText() for page in pdf.pages)
            self.save()
            
    def __str__(self):
        return self.title 
     
     
     
class Research(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, blank=True)
    uploadedfile = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, blank=True, null=True)
    googlefile = models.ForeignKey(GoogleScholarFile, on_delete=models.CASCADE , blank=True, null=True)
    research_title = models.CharField(max_length=500)
    body = HTMLField(null=True, blank=True)
    references = models.TextField(null=True, blank=True)
    description = models.CharField(max_length= 100,null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.research_title
    
    


    
class Chapter(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    def __str__(self):
        return self.name  
        
class Index(models.Model):
    name = models.CharField(max_length=500)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='subtopics')
    def __str__(self):
        return self.name  


class Content(models.Model):
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='contents')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.index}: {self.content[:50]}"


 
    
    

# =============================




class Company(models.Model):
    company_name = models.CharField(max_length=150, null=True)
    company_uuid = models.CharField(null=True,blank=True, max_length=100)
    email = models.EmailField(null=True)
    url = models.URLField(null=True)
    
    class Meta:
        db_table = 'company'
        managed = True
        verbose_name = 'company'
        verbose_name_plural = 'company'

    def __str__(self):
        return self.company_name  
    


    
class ProfileDetail(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    p_img = models.ImageField(upload_to='profile', default='profile/avatar.png', blank=True, null=True)

    class Meta:
        db_table = 'profiledetail'
        managed = True
        verbose_name = 'profileDetail'
        verbose_name_plural = 'profileDetails'

    def __str__(self):
        return self.username.username
    
    
class DemoUser(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    fullname = models.CharField(max_length=150, null=True)
    url = models.URLField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=150, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    date_expired = models.DateTimeField(blank=True, null=True)
    profile_pic = models.ImageField(default='default.jpg')

    class Meta:
        db_table = 'demouser'
        managed = True
        verbose_name = 'demouser'
        verbose_name_plural = 'demo profiles'

    def __str__(self):
        return self.username.username