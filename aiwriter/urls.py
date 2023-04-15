from django.urls import path 
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
    
    path('index', index, name='index'),
    
    path('create_research', create_research, name='create_research'),
    
    path('uploadfile/', uploadfile, name='uploadfile'),
    path('importsource/', importsource, name='importsource'),
    path('deletefile/<int:id>/', deletefile, name='deletefile'),
    
    
    
    path('ResearchesView/', ResearchesView.as_view(), name='researchesview'),
    path('research_manager/<str:id>', research_manager, name='research_manager'),
    
    path('Editchapter/<int:research_id>/', Editchapter.as_view(), name='Editchapter'),
    path('Paraphrasing/<int:research_id>/', Paraphrasing.as_view(), name='Paraphrasing'),
    
#    ===============================================================
    # path('topics/<int:chapter_id>/', topics, name='topics'),
    # path('rename_topic/<int:topic_id>/', rename_topic, name='rename_topic'),
    path('save_editor', save_editor, name='save_editor'),

    path('chapters-json/', get_json_chapter_data, name='chapters-json'),
    path('topics-json/<str:chapter>/', get_json_topic_data, name='topics-json'),
    path('editor/<int:id>/',editor, name='editor'),
    
    path('smart_editor/<int:file_id>/', smart_editor, name='smart_editor'),
    path('duplicate_file/<int:file_id>/', duplicate_file, name='duplicate_file'),
    
    path('pdf/<int:file_id>/', pdf, name='pdf'),
   
    
    path('addindex/', addindex, name='addindex'),
    path('addchapter/', addchapter, name='addchapter'),
    path('deletecontent/', deletecontent, name='deletecontent'),
    # path('delete_chapter/', delete_chapter, name='delete_chapter'),
    path('delete_chapter/<int:chapter_id>/', delete_chapter, name='delete_chapter'),
    
    
    # path('get_chapter/', get_chapter, name='get_chapter'),
    
    path('get_topics/', get_topics, name='get_topics'),

#    ===============================================================
    path('researcheditor/<int:research_id>/', ResearchEditor.as_view(), name='researcheditor'),
    path('savetopicform/', SaveTopic.as_view(), name='savetopicform'),
    path('rename_topic/', RenameTopic.as_view(), name='rename_topic'),
    

    
    path('tinymce/<int:research_id>/', TinyMce.as_view(), name='tinymce'),


    path('search_page', search_page, name='search_page'),
    path('project', project, name='project'),
    path('main_view', main_view, name='main_view'),
    path('editor', editor, name='editor'),
    path('document_manager', document_manager, name='document_manager'),
    path('mycontents', mycontents, name='mycontents'),
    path('alltools', alltools, name='alltools'),
    path('dashboard', dashboard, name='dashboard'),
    path('collaboration', collaboration, name='collaboration'),
    path('dashboard', dashboard, name='dashboard'),
    
    path('search_resources', search_resources, name='search_resources'),
    
    # path('delete_topic/<int:topic_id>/', delete_topic, name='delete_subtopic'),
    
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    # path('logout/', user_logout, name='logout'),
    
    path('perform_search/', perform_search, name='perform_search'),
    path('search_history/', search_history, name='search_history'),
    path('search_results/<int:pk>/', search_results, name='search_results'),
    path('search_detail/<int:pk>/', search_detail, name='search_detail'),
    
    # path('display_results/<int:search_id>/', display_results, name='display_results'),
    path('searchanalyzer/<int:search_id>/', searchanalyzer, name='searchanalyzer'),
    path('pdf_summarizer/', pdf_summarizer, name='pdf_summarizer'),
    
    # URL for the project detail page

    # URL for the edit project page

    # URL for saving a chapter
    path('save_chapter/', save_chapter, name='save_chapter'),
    
    

]   
    
    
    