from django.shortcuts import render, redirect, get_object_or_404
from PyPDF2 import PdfReader
import requests
import uuid
import pandas as pd
import csv
from aiwriter.models import *
from .forms import *
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
import os
from shutil import copyfile
from django.core.files.base import ContentFile
import docx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import mammoth
import boto3
import io
from docx import Document
from docx2python import docx2python 
from htmldocx import HtmlToDocx
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

# Create your views here.

def deletefile(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        id = request.POST['id']
        file = UploadedFile.objects.get(id=id)
        file.delete()
    return redirect(url)
   



def duplicate_file(file_id):
    # Get the file object with the given ID
    file = UploadedFile.objects.get(id=file_id)

    # Get the file path
    file_path = file.file.path

    # Get the file extension
    file_ext = file.file.name.split('.')[-1]

    # Make a copy of the file with a different name
    new_file_path = file_path.replace(f".{file_ext}", f"_copy.{file_ext}")
    copyfile(file_path, new_file_path)

    # Create a new file object for the copied file and save it to the database
    new_file = UploadedFile(title=f"{file.title} (Copy)", file=ContentFile(open(new_file_path, 'rb').read()), owner=file.owner)
    new_file.save()

    # Return the ID of the new file object
    return new_file.id

      
        
def uploadfile(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            title, ext = os.path.splitext(file.name)
            count = 0
            while True:
                if count == 0:
                    file_title = title
                else:
                    file_title = f"{title}({count})"
                if not UploadedFile.objects.filter(title=file_title).exists():
                    break
                count += 1
            if ext == '.docx':
                UploadedFile.objects.get_or_create(doc=file, title=file_title, defaults={'date_created': timezone.now()})
                messages.success(request, 'Invalid file type !')
                
                return redirect(url)

            elif ext == '.pdf':
                UploadedFile.objects.get_or_create(pdf=file, title=file_title, defaults={'date_created': timezone.now()})
                messages.success(request, 'Invalid file type !')
                
                return redirect(url)

            else:
                messages.error(request, 'Invalid file type !')
                return redirect(url)
        else:
            return JsonResponse({'success': False, 'message': 'Please select a file to upload.'})
    return render(request, 'landing.html')

def importsource(request):
    url = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            title, ext = os.path.splitext(file.name)
            count = 0
            while True:
                if count == 0:
                    file_title = title
                else:
                    file_title = f"{title}({count})"
                if not UploadedFile.objects.filter(title=file_title).exists():
                    break
                count += 1
                
           

            if ext == '.docx':
                newfile = UploadedFile.objects.create(doc=file, title=file_title, date_created=timezone.now())
                return redirect(smart_editor, newfile.id)

            else:
                ext == '.pdf'
                newfile = UploadedFile.objects.create(pdf=file, title=file_title, date_created=timezone.now())
                return redirect(smart_editor, newfile.id)
            
        else:
            messages.error(request, 'Please select a file to upload. !')
            return redirect(url)
    return redirect(url)




def create_research(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        research_title = request.POST['research_title']
        description = request.POST['description']
        field_id = request.POST['field']
        field = Field.objects.get(id=field_id)
        research = Research.objects.create(
            research_title=research_title,
            description=description,
            field=field,
        )
        research.save()
    return redirect(url)
        



def main_view(request):
    chapters = Chapter.objects.all()
    selected_chapter = None
    topics = None

    if 'chapter_id' in request.GET:
        chapter_id = request.GET['chapter_id']
        selected_chapter = Chapter.objects.get(id=chapter_id)
        topics = Index.objects.filter(chapter=selected_chapter)

    return render(request, 'research/main.html', {
        'chapters': chapters,
        'selected_chapter': selected_chapter,
        'topics': topics,
    })




def get_json_chapter_data(request):
    qs_val = list(Chapter.objects.values())
    return JsonResponse({'data': qs_val})

def get_json_topic_data(request, *args, **kwargs):
    selected_chapter = kwargs.get('chapter')
    obj_topics = list(Index.objects.filter(chapter__name=selected_chapter).values())
    return JsonResponse({'data': obj_topics})

def get_topics(request, *args, **kwargs):
    selected_chapter = kwargs.get('chapter_id')
    obj_topics = list(Index.objects.filter(chapter__name=selected_chapter).values())
    return JsonResponse({'data': obj_topics})

# ===============================================================
        
class ResearchesView(View):
    def get(self, request, *args, **kwargs):
        fields = Field.objects.all()
        
        researches = Research.objects.all()

        context = {
            'researches': researches,
            'fields': fields,
        }
        
        return render(request, 'research/research.html', context)
    
def research_manager(request, id):
    research = Research.objects.get(id=id)
    context = {
        'research': research,
    }
    return render(request, 'research/research_manager.html', context)





class Editchapter(View):
    def get(self, request, research_id):
        uploaded_files = UploadedFile.objects.all().order_by('-date_created')
        results = GoogleScholarFile.objects.all().order_by('-date_created')
        
        research = get_object_or_404(Research, id=research_id)
        chapters = Chapter.objects.all().filter(research=research)
        selected_chapter_id = request.GET.get('chapter_id')
        
        
        
        topics = []
        if selected_chapter_id:
            selected_chapter = get_object_or_404(Chapter, id=selected_chapter_id, research=research)
            topics = Index.objects.all().filter(chapter=selected_chapter)
        else:
            selected_chapter = chapters.first()
            topics = Index.objects.all().filter(chapter=selected_chapter)
            
        request.session.get('research') == research
        request.session.get('chapters')  == chapters
        request.session.get('selected_chapter')  == selected_chapter
        request.session.get('topics') == topics 
        context = {
            'research': research,
            'chapters': chapters,
            'selected_chapter': selected_chapter,
            'topics': topics,
            
            'uploaded_files': uploaded_files,
            'results': results,
        }
        return render(request, 'research/edit_chapters.html', context)


# ======================================================================================
    


class SaveTopic(View):
    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        topicid = request.POST.get('topicid')
        try:
            index = Index.objects.get(id=topicid)
            content_obj, created = Content.objects.get_or_create(index=index, content=content)
            if not created:
                content_obj.content = content
            content_obj.created_at = timezone.now()
            content_obj.save()
            resp = {'status': 'success', 'content_id': content_obj.id}
        except Exception as e:
            print(e)
            resp = {'status': 'failed'}
        
        return JsonResponse(resp)

    
class RenameTopic(View):
    def post(self, request):
        topic_id = request.POST.get('topic_id')
        new_name = request.POST.get('new_name')
        topic = get_object_or_404(Index, id=topic_id)
        topic.name = new_name
        topic.save()
        return JsonResponse({'status': 'success'})
    
def addindex(request):
    if request.method == 'POST':
        chapter_id = request.POST.get('chapter_id')
        topic_name = request.POST.get('topic_name')
        # topic_description = request.POST.get('description')

        chapter = get_object_or_404(Chapter, id=chapter_id)

        # Create a new topic in the selected chapter
        Index.objects.create(name=topic_name, chapter=chapter)

        return JsonResponse({'created': True})
    return JsonResponse({'created': False})

def addchapter(request):
    if request.method == 'POST':
        chapter_name = request.POST.get('name')
        research = request.POST.get('research')
        # topic_description = request.POST.get('description')

        print(research)
        # Create a new topic in the selected chapter
        Chapter.objects.create(research_id=research, name=chapter_name)

        return JsonResponse({'created': True})
    return JsonResponse({'created': False})

def delete_chapter(request, chapter_id):
    print(chapter_id)
    if request.method == 'DELETE':
        try:
            chapter = Chapter.objects.get(id=chapter_id)
            chapter.delete()
            return JsonResponse({'deleted': True})
        except Chapter.DoesNotExist:
            return JsonResponse({'deleted': False})










# @csrf_exempt
# def deletecontent(request):
#     if request.method == 'DELETE':
#         content_id = request.POST.get('contentid')
#         try:
#             content = Content.objects.get(id=content_id)
#             content.delete()
#             return JsonResponse({'status': 'success'})
#         except Content.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Content does not exist.'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def deletecontent(request):
    if request.method == 'DELETE':
        content_id = request.POST.get('contentid')
        try:
            content = Content.objects.get(id=int(content_id))
            content.delete()
            return JsonResponse({'status': 'success'})
        except (Content.DoesNotExist, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Content does not exist or ID is invalid.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

#  =========================================   
class ResearchEditor(View):
    def get(self, request, *args, **kwargs):
        research_id = kwargs['research_id']
        research = Research.objects.get(id=research_id)
        context = {
            'research': research,
        }
        return render(request, 'research/researcheditor.html', context)

def save_editor(request):
    if request.method == 'POST':
        research_id = request.POST['research_id']
        body = request.POST['body']
        # Check if a research object with the same title exists
        research = Research.objects.get(research_id=research_id)
        # Update the body of the existing object
        research.body = body
        research.save()

        
        return HttpResponse({'status': 'success'})





class TinyMce(View):
    def get(self, request, *args, **kwargs):
        research_id = kwargs['research_id']
        research = Research.objects.get(id=research_id)
        context = {
            'research': research,
        }
        return render(request, 'research/tinymce.html', context)    
   
      

    

class Paraphrasing(View):
    def get(self, request, research_id):
        uploaded_files = UploadedFile.objects.all().order_by('-date_created')
        results = GoogleScholarFile.objects.all().order_by('-date_created')
        
        research = get_object_or_404(Research, id=research_id)
        chapters = Chapter.objects.all().filter(research=research)
        selected_chapter_id = request.GET.get('chapter_id')
        topics = []
        if selected_chapter_id:
            selected_chapter = get_object_or_404(Chapter, id=selected_chapter_id, research=research)
            topics = Index.objects.all().filter(chapter=selected_chapter)
        else:
            selected_chapter = chapters.first()
            topics = Index.objects.all().filter(chapter=selected_chapter)
        context = {
            'research': research,
            'chapters': chapters,
            'selected_chapter': selected_chapter,
            'topics': topics,
            
            'uploaded_files': uploaded_files,
            'results': results,
        }
        return render(request, 'research/paraphrasing.html', context)
    
    
def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def landing(request):
    return render(request, 'landing.html')

def register(request):
    return render(request, 'research/register.html')

def research(request):
    return render(request, 'research/research.html')

def pdf(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    if file.pdf:
        with open(file.pdf.path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline;filename={file.title}.pdf'
            return response


def editor(request, id):
    file = UploadedFile.objects.get(id=id)
    # Your code here
    return render(request, 'research/editor.html', {'file': file})


def extract_rtf(doc):
    data = {}
    data["paragraphs"] = []
    for para in doc.paragraphs:
        para_data = {}
        para_data["text"] = para.text
        para_data["style"] = para.style.name
        if para.alignment == WD_PARAGRAPH_ALIGNMENT.LEFT:
            para_data["alignment"] = "left"
        elif para.alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            para_data["alignment"] = "center"
        elif para.alignment == WD_PARAGRAPH_ALIGNMENT.RIGHT:
            para_data["alignment"] = "right"
        para_data["runs"] = []
        for run in para.runs:
            run_data = {}
            run_data["text"] = run.text
            run_data["bold"] = run.bold
            run_data["italic"] = run.italic
            run_data["underline"] = run.underline
            run_data["color"] = run.font.color.rgb
            if run.font.size is not None:
                run_data["size"] = run.font.size.pt
            else:
                run_data["size"] = None
            para_data["runs"].append(run_data)
        data["paragraphs"].append(para_data)
    return json.dumps(data)


def smart_editor(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    content = ''
    
    if file.pdf: # Read PDF content
        with open(file.pdf.path, 'rb') as pdf_file:
            pdf_data = io.BytesIO(pdf_file.read())
        pdf_reader = PdfReader(pdf_data)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            content += page.extract_text()  
            
    if file.doc: # Read DOCX content
        doc = docx2python(file.doc.path)
        json_data = json.dumps(doc.body)
        content = json.loads(json_data)

    research_id = request.session.get('research')
    if research_id:
        research = Research.objects.get(id=research_id)
        file.researches.add(research)
        file.linked = True
        file.save()

    context = {
        'file': file,
        'content': content,
    }
    return render(request, 'research/smart_editor.html', context)



def search_page(request):
    return render(request, 'research/search_page.html')

def project(request):
    return render(request, 'research/project.html')

def alltools(request):
    return render(request, 'research/alltools.html')



# ====================================================
   
    


def document_manager(request):
    files = UploadedFile.objects.all().order_by('-date_created')
    context = {
        'files': files,
    }
    
    return render(request, 'document_manager.html', context)

def mycontents(request):
    return render(request, 'mycontents.html')


def search_resources(request):
    return render(request, 'research/search_resources.html')



def dashboard(request):
    return render(request, 'dashboard.html')


def collaboration(request):
    messages = CollaborationMessage.objects.filter(group='collaboration').order_by('timestamp')
    return render(request, 'collaboration.html', {'messages': messages})

def dashboard(request):
    return render(request, 'dashboard.html')











# def post_message(request):
#     message = request.POST.get('message', '')
#     # Code to save the message to the database goes here
#     # ...
#     # Send the message to the collaboration group
#     from asgiref.sync import async_to_sync
#     from channels.layers import get_channel_layer

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'collaboration',
#         {
#             'type': 'chat_message',
#             'message': message
#         }
#     )
#     return HttpResponse('Message sent')



# @login_required
# def chat_room(request):
#     messages = Message.objects.order_by('-timestamp').all()
#     return render(request, 'chat_room.html', {'messages': messages})

def pdf_summarizer(request):
    return render(request, 'pdf_summarizer.html')


def save_chapter(request):
    if request.method == 'POST' and request.is_ajax():
        chapter_id = request.POST.get('chapter_id')
        chapter_content = request.POST.get('chapter_content')
        
        # Get the chapter object by id
        chapter = Chapter.objects.get(id=chapter_id)
        
        # Update the chapter content
        chapter.content = chapter_content
        chapter.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})



# =============================================
# Search
# ===============
# import requests
# import json

# from serpapi import GoogleSearch

# params = {
#   "engine": "google_scholar",
#   "q": "biology",
#   "api_key": "6c3ee40b5c5be9e4b533d695500d9e3d61ee184ab14babad48a431831c4cb618"
# }

# search = GoogleSearch(params)
# results = search.get_dict()
# organic_results = results["organic_results"]




import requests
import json
from django.shortcuts import render

def perform_search(request):
    if request.method == 'POST':
        query = request.POST.get('query', '') # Extract the search query from the POST data
        if query:
            url = "https://google.serper.dev/search"
            payload = {
                "q": query # Use the user's search query as the search term
            }
            headers = {
                'X-API-KEY': '66594230b3c772333e296d7d24e376c084f27f1b',
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response.raise_for_status() # Raise an exception if the HTTP response status is an error code (e.g. 400 or 500)
                results = response.json() # Parse the JSON response into a Python dictionary
            except requests.exceptions.RequestException as e:
                # Handle network errors, API errors, or other exceptions that might occur during the request
                return render(request, 'search_error.html', {'error_message': str(e)})
            return render(request, 'research/search_resources.html', {'results': results})
    # If the request is not a POST request, or the query parameter is missing, render a template with the search form
    return render(request, 'research/search_resources.html')


    
    
    
    
    
    
    
    
    
    # """
    # Search for information on the query and return search results
    # """
    # url = "https://google.serper.dev/search"
    # payload = {
    #     "q": query,
    #     "gl": "us",
    #     "hl": "en",
    #     "autocorrect": True 
    # }
    # headers = {
    #     'X-API-KEY': '66594230b3c772333e296d7d24e376c084f27f1b',
    #     'Content-Type': 'application/json',
    #     'User-Agent': 'My Python App'
    # }
    # # send the post request to the API and get the response
    # response = requests.post(url, headers=headers, json=payload)
    # response.raise_for_status() # raise an error if the response is not successful
    
    # create a list of SearchResult objects
    search_results_list = []
    for result in search_results['results']:
        search_result = SearchResult.objects.create(
            title=result['title'],
            snippet=result['snippet'],
            url=result['link']
        )
        search_results_list.append(search_result)

    # # send the post request to the API and get the response
    # response = requests.post(url, headers=headers, json=payload)
    # response.raise_for_status() # raise an error if the response is not successful
    # search_results = response.json()
    
    # # return the search results as a JSON response
    # return JsonResponse(search_results)

# def save_to_csv(data, filename):
#     """
#     Save the search results to a CSV file
#     """
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['title', 'snippet', 'link']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for item in data:
#             writer.writerow(item)
            
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',')
#         for result in results:
#             writer.writerow(result.values())

# def perform_search_and_save_results(query, filename):
#     search, created = Project.objects.get_or_create(title=query)
#     if created:
#         # only perform the search if a new search object was created
#         data = perform_search(query)
#         save_to_csv(data, filename)
#         search.completed = True
#         search.save()
    

    #     # loop through the results and create a SearchResult object for each item
    #     query = Project.objects.get(title=query)
    #     for item in data.get('peopleAlsoAsk', []) + data.get('organic', []):
    #         result = SearchResult.objects.create(
    #             search_id=search_id, 
    #             search=query, 
    #             title=item.get('title', ''), 
    #             snippet=item.get('snippet', ''), 
    #             url=item.get('link', ''),
    #         )
    #         result.save()
        
    #     return redirect('search_results', pk=search.pk)
    # return render(request, 'search.html')

# =============================
# 


# =============================
def search_results(request, pk):
    search = GoogleScholarFile.objects.get(pk=pk)
    results = GoogleScholarFile.objects.all()
    return render(request, 'search_results.html', {'results': results})

# ======================
def search_history(request):
    searches = GoogleScholarFile.objects.all()
    return render(request, 'search_history.html', {'searches': searches})

def search_detail(request, pk):
    search = get_object_or_404(GoogleScholarFile, pk=pk)
    return render(request, 'search_detail.html', {'search': search})

def searchanalyzer(request, search_id):
    search = GoogleScholarFile.objects.get(id=search_id)
    results = search.results.all()
    results_with_pdf = results.filter(pdf_file__isnull=False)
    other_results = results.filter(pdf_file__isnull=True)
    
    return render(request, 'searchanalyzer.html', {
        'search': search,
        'results_with_pdf': results_with_pdf,
        'other_results': other_results,
    })
    


# # def search_results(request, pk):
# #     search = Search.objects.get(pk=pk)
# #     results = search.results.all()

# #     # Pagination
# #     paginator = Paginator(results, 10) # Show 10 results per page
# #     page = request.GET.get('page')
# #     try:
# #         results = paginator.page(page)
# #     except PageNotAnInteger:
# #         # If page is not an integer, deliver first page.
# #         results = paginator.page(1)
# #     except EmptyPage:
# #         # If page is out of range (e.g. 9999), deliver last page of results.
# #         results = paginator.page(paginator.num_pages)

# #     # Filter
# #     filter_by = request.GET.get('filter_by')
# #     if filter_by == 'date':
# #         results = results.order_by('-date')
# #     elif filter_by == 'relevance':
# #         results = results.order_by('-relevance')
# #     elif filter_by == 'source':
# #         results = results.order_by('source')
    
# #     return render(request, 'search_results.html', {'results': results})
  
    


  
    




# import openai

# openai.api_key = "YOUR_API_KEY"

# def summarize_text(text):
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt="Please summarize the following text: " + text,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
#     message = response["choices"][0]["text"].strip()
#     return message

# def extract_pdf_content(file):
#     # Code to extract text from PDF file
#     # For example, using PyPDF2:
#     with open(file, "rb") as pdf_file:
#         pdf_reader = PyPDF2.PdfFileReader(pdf_file)
#         num_pages = pdf_reader.numPages
#         text = ""
#         for page_num in range(num_pages):
#             page = pdf_reader.getPage(page_num)
#             text += page.extractText()
#     return text

# pdf_file = "path/to/pdf/file.pdf"
# pdf_content = extract_pdf_content(pdf_file)
# summary = summarize_text(pdf_content)
# print(summary)


# import requests
# from django.core.files.base import ContentFile
# from myapp.models import Document

# def download_and_save_pdf(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         document = Document()
#         document.pdf.save('file.pdf', ContentFile(response.content))
#         document.save()
#         return document
#     else:
#         return None
import io
import requests
from django.core.files.base import ContentFile
from django.db import models
from PyPDF2 import PdfFileReader

# class MyModel(models.Model):
#     pdf_file = models.FileField(upload_to='pdf_files')
#     pdf_text = models.TextField(blank=True)

#     def download_pdf_and_extract_text(self, url):
#         # Download the PDF file from the given URL
#         response = requests.get(url)
#         if response.status_code == 200:
#             # Save the PDF file to the database as a file field
#             self.pdf_file.save('my_file.pdf', ContentFile(response.content))

#             # Extract the text from the PDF using PyPDF2
#             pdf_data = io.BytesIO(response.content)
#             pdf_reader = PdfFileReader(pdf_data)
#             text = ''
#             for page_num in range(pdf_reader.getNumPages()):
#                 page = pdf_reader.getPage(page_num)
#                 text += page.extractText()

#             # Save the extracted text to the database
#             self.pdf_text = text
#             self.save()
#         else:
#             raise Exception('Failed to download PDF file')

# my_instance = MyModel.objects.get(id=1)
# my_instance.download_pdf_and_extract_text('http://example.com/my_file.pdf')


# # ==============================================
# # =========================================



# # import threading

# # def search_function_1():
# #     # Your code for the first search function

# # def search_function_2():
# #     # Your code for the second search function

# # thread1 = threading.Thread(target=search_function_1)
# # thread2 = threading.Thread(target=search_function_2)

# # thread1.start()
# # thread2.start()

# # thread1.join()
# # thread2.join()
# # ==========================
# # import concurrent.futures

# # def search(query):
# #     # Code for the existing search function

# # def alternative_search(query):
# #     # Code for the pubmed search function


# # def parallel_search(query):
# #     with concurrent.futures.ThreadPoolExecutor() as executor:
# #         google_scholar_future = executor.submit(search, query)
# #         pubmed_future = executor.submit(alternative_search, query)
# #         google_scholar_results = google_scholar_future.result()
# #         pubmed_results = pubmed_future.result()

# #         all_results = google_scholar_results + pubmed_results
# #         search = Search.objects.create(query=query)
# #         search.results.set(all_results)

# # if request.method == 'POST':
# #     query = request.POST.get('query')
# #     parallel_search(query)
# #     # rest of the code



#         # MED SEARCH PUB
# # -=================================



# # import requests
# # from io import BytesIO
# # from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# # from pdfminer.converter import TextConverter
# # from pdfminer.layout import LAParams
# # from pdfminer.pdfpage import PDFPage

# # def search_pubmed(query):
# #     # API endpoint to search in Pubmed
# #     endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
# #     parameters = {
# #         "db": "pubmed",
# #         "term": query,
# #         "retmax": "100",
# #         "retmode": "xml"
# #     }

# #     # Make API request
# #     response = requests.get(endpoint, params=parameters)
# #     response.raise_for_status()
# #     xml_data = response.text

# #     # Extract publication ids from the API response
# #     root = ET.fromstring(xml_data)
# #     ids = root.findall("./IdList/Id")
# #     ids = [id.text for id in ids]

# #     # API endpoint to retrieve publication details
# #     details_endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
# #     details_parameters = {
# #         "db": "pubmed",
# #         "id": ",".join(ids),
# #         "retmode": "xml"
# #     }

# #     # Make API request to retrieve publication details
# #     details_response = requests.get(details_endpoint, params=details_parameters)
# #     details_response.raise_for_status()
# #     details_xml_data = details_response.text

# #     # Extract publication details from the API response
# #     details_root = ET.fromstring(details_xml_data)
# #     articles = details_root.findall("./PubmedArticle")

# #     # Store publication links and PDFs
# #     results = []
# #     for article in articles:
# #         link = article.find("./PubmedData/ArticleIdList/ArticleId[@IdType='doi']").text
# #         link = f"https://doi.org/{link}"
# #         result = SearchResult(link=link)

# #         # Try to download and store the PDF file
# #         try:
# #             response = requests.get(link)
# #             if response.headers.get("content-type") == "application/pdf":
# #                 result.pdf_file.save(link.split("/")[-1], ContentFile(response.content), save=True)
# #         except:
# #             result.pdf_file = None

# #         results.append(result)
# #     SearchResult.objects.bulk_create(results)

# # ======================


# # import requests
# # from io import BytesIO
# # from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# # from pdfminer.converter import TextConverter
# # from pdfminer.layout import LAParams
# # from pdfminer.pdfpage import PDFPage

# # def search_pubmed(query):
# #     # API endpoint to search in Pubmed
# #     endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
# #     parameters = {
# #         "db": "pubmed",
# #         "term": query,
# #         "retmax": "100",
# #         "retmode": "xml"
# #     }

# #     # Make API request
# #     response = requests.get(endpoint, params=parameters)
# #     response.raise_for_status()
# #     xml_data = response.text

# #     # Extract publication ids from the API response
# #     root = ET.fromstring(xml_data)
# #     ids = root.findall("./IdList/Id")
# #     ids = [id.text for id in ids]

# #     # API endpoint to retrieve publication details
# #     details_endpoint = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
# #     details_parameters = {
# #         "db": "pubmed",
# #         "id": ",".join(ids),
# #         "retmode": "xml"
# #     }

# #     # Make API request to retrieve publication details
# #     details_response = requests.get(details_endpoint, params=details_parameters)
# #     details_response.raise_for_status()
# #     details_xml_data = details_response.text

# #     # Extract publication details from the API response
# #     details_root = ET.fromstring(details_xml_data)
# #     articles = details_root.findall("./PubmedArticle")

# #     # Store publication links and PDFs
# #     results = []
# #     for article in articles:
# #         link = article.find("./PubmedData/ArticleIdList/ArticleId[@IdType='doi']").text
# #         link = f"https://doi.org/{link}"
# #         result = SearchResult(link=link)

# #         # Try to download and store the PDF file
# #         try:
# #             response = requests.get(link)
# #             if response.headers.get("content-type") == "application/pdf":
# #                 result.pdf_file.save(link.split("/")[-1], ContentFile(response.content), save=True)
# #         except:
# #             result.pdf_file = None

# #         results.append(result)
# #     SearchResult.objects.bulk_create(results)

# # ==========================
# # import requests
# # from bs4 import BeautifulSoup

# # def search_pubmed(query):
# #     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
# #     params = {
# #         "db": "pubmed",
# #         "term": query,
# #         "retmax": 100
# #     }
# #     response = requests.get(base_url, params=params)
# #     response.raise_for_status()
# #     soup = BeautifulSoup(response.content, "xml")
# #     pubmed_ids = soup.find_all("Id")
# #     pubmed_ids = [pid.text for pid in pubmed_ids]
# #     return pubmed_ids

# # ===========================


