from django import forms
from .models import *
# from tinymce.widgets import TinyMCE
# class ProjectForm(forms.ModelForm):
#     chapter_choices = [(i, str(i)) for i in range(1, 21)]
#     chapter = forms.ModelChoiceField(queryset=Chapter.objects.all(), empty_label=None, widget=forms.RadioSelect(choices=chapter_choices))

#     class Meta:
#         model = Research
#         fields = ['topic', 'field', 'body', 'references', 'chapter']
#         widgets = {
#             'body': forms.Textarea(attrs={'rows': 10}),
#             'references': forms.Textarea(attrs={'rows': 5}),
#         }


    
# class TaskForm(forms.ModelForm):
#     class Meta:
#         model =  Index
#         fields = ['name']
        
#         widget ={
#             name : forms.TextInput(attrs={'class': 'form-control'})
#         }



# class MyForm(forms.Form):
#     my_field = forms.CharField(widget=TinyMCE())
