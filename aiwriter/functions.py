import os
import openai
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
import re
from aiwriter.models import *
from .models import Project, Field, Chapter
from .forms import ProjectForm
import threading

openai.api_key = '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'

# ..........................................

def generate(request):
    result = []
    if request.method == "GET":
        type = request.GET.get("type")
        return render(request, 'facebook-ads.html', {"type":type})

    elif request.method == 'POST':
        project_id = request.POST.get("id")
        my_project = Project.objects.get(pk=project_id)
        
        topic = my_project.topic
        section_chapter = request.POST.get("section")
        field = my_project.field
        sources = request.POST.get("sources")
        rewrite_text = request.POST.get("rewrite")
        if (tone == None):
            tone = "default"
        language = "English"

        if (rewrite_text):
            result = generate(rewrite_text)
            return render(request, "generatebody.html", {"result": result, "type": "rewrite", 'topic':topic})
        
        err = False
        if (section_chapter == None):
            err = "topic field is required"
        elif (topic == None):
            err = "product discription os required"
        elif (sources == None):
            err = "please choose a particular researchformat"
        
        if err:
            return render(request, "aiwriter.hhtml", {"err": err})
        else:
            result = write_section(section_chapter, topic, field, sources)
            if len(result) > 0:
                # messages.error(request,"Oops, we could not generate any blog ideas for you , please try again")
                # my_project = Project.objects.get(pk=project_id)

                # define the regular expression to match the run of references
                pattern = r"(?:refrence|refrences|\[\d+\])+"

                # find the starting position of the run of references
                start_pos = re.search(pattern, result).start()

                # cut the string from the starting position
                text_before_refrences = result[:start_pos]
                refrences = result[start_pos:]
                
                my_project.body += text_before_refrences
                my_project.refrences += refrences

                # save the text before references and references in separate fields in a model
                my_project.save()
                
                return redirect('aiwriter')
    
        return render (request, 'facebook-ads.html' , {'result':result, 'type':"template", 'topic':topic})


# ==================================================

def write_section(section_chapter, topic, field, sources):
    prompt = ""
    research_result = []

    if section_chapter == "Introduction":
        prompt=f"Introduction:\nTo engage the reader, use an attention-grabbing fact or a thought-provoking statement related to {topic} in {field}, sourced from {sources}.\nClearly state the purpose and scope of the study, highlighting its importance in the context of {field}.\nProvide background information on the topic, defining any key terms or concepts, drawing on {sources} to establish the foundation for the study.\nEnd with a focused research question or hypothesis related to {topic}, indicating what the study intends to answer, with the help of insights provided by {sources}.\nList all sources used in APA format to credit and validate the research.\n",
    
    elif section_chapter == "Literature Review":
        prompt=f"Literature Review:\nOrganize the review according to themes or topics related to {topic} in {field} using {sources} to identify the most relevant and up-to-date research.Review the existing literature on {topic} in {field}, identifying key concepts, theories, and empirical studies related to the research question, and summarizing the main findings and arguments.\nCritically evaluate the strengths and weaknesses of the literature, and highlight any gaps or inconsistencies that the study aims to address.\nAnalyze the existing research on each topic, drawing on {sources} to compare and contrast different approaches, identifying gaps or inconsistencies in the literature.\nExplain how the current study will contribute to the field, referring to {sources} for context and support.\nSummarize the key findings of the literature review and explain how they will inform the current study, with the help of the foundation provided by {sources}.\nList all sources used in APA format to credit and validate the research.\n",
    
    elif section_chapter == "Background and Context":
        prompt=f"Background:\nProvide a historical background of the research topic in {field}, using {sources}.\nDiscuss the evolution of the research topic and its relevance to current research.\nAnalyze the key research studies that have contributed to the current state of knowledge in the field, with the help of {sources}.\nList all sources used in APA format to credit and validate the research.\n",
    
    elif section_chapter == "Hypotheses":
        prompt=f"Hypothesis:\nFormulate a testable hypothesis related to {topic} in {field}, based on insights from {sources}.\nState the null and alternative hypotheses and explain how they will be tested, drawing on {sources} to establish the basis for the study.\nProvide a rationale for the chosen hypothesis, using {sources} to support the reasoning behind the proposed test.\nEnd with a prediction of the expected results of the study, based on the hypothesis and insights from {sources}.\nList all sources used in APA format to credit and validate the research.\n",
    
    elif section_chapter == "Research Questions":
        prompt = f"Identify and articulate the research questions related to {topic} in {field}, drawing on {sources} to establish the significance and relevance of the topic.\nFormulate the research questions in a clear and concise manner, ensuring that they are specific, measurable, achievable, relevant, and time-bound (SMART) to guide the research process.\n"
    
    elif section_chapter == "Findings and Analysis":
        prompt = f"Present the findings of the study in a clear and organized manner, using tables, graphs, or other visual aids as appropriate to represent the data collected on {topic} in {field}, with the help of {sources}.\nAnalyze the collected data, describing the patterns, trends, and relationships that were observed, drawing on {sources} to provide context and support for the results.\n"

    elif section_chapter == "Background and Context":
        prompt = f"Provide a historical background of the research topic in {field}, using {sources}.\nDiscuss the evolution of the research topic and its relevance to current research.\nAnalyze the key research studies that have contributed to the current state of knowledge in the field.\n"
    
    elif section_chapter == "Theoretical Framework":
        prompt = f"Identify and discuss the theoretical framework that will be used to guide the study of {topic} in {field}, drawing on {sources} to establish the relevance and appropriateness of the chosen framework.\n"
    
    elif section_chapter == "Research Questions or Hypotheses":
        prompt = f"Formulate the research questions or hypotheses that will guide the study of {topic} in {field}, based on {sources} to ensure that the questions or hypotheses are relevant, significant, and feasible.\n"
    
    elif section_chapter == "Significance of the Study":
        prompt = f"Explain the significance of the study of {topic} in {field}, drawing on {sources} to establish the relevance and importance of the research.\n"
    
    elif section_chapter == "Limitations and Delimitations":
        prompt = f"Discuss the limitations and delimitations of the study of {topic} in {field}, referencing {sources} to identify potential issues or constraints that may affect the research.\n"
    
    elif section_chapter == "Research Design":
        prompt = f"Provide a clear and detailed description of the research design that will be used to study {topic} in {field}, using {sources} to ensure that the design is appropriate for answering the research question.\n"
    
    elif section_chapter == "Sampling Method":
        prompt = f"Explain the sampling method that will be used to select participants for the study of {topic} in {field}, drawing on {sources} to establish the appropriateness and validity of the chosen method.\n"
    
    elif section_chapter == "Data Collection Tools":
        prompt = f"Describe the data collection tools that will be used to gather information about {topic} in {field}, based on {sources} to ensure that the tools are appropriate and reliable.\n"
    
    elif section_chapter == "Data Analysis Techniques":
        prompt = f"Explain the data analysis techniques that will be used to analyze the data collected on {topic} in {field}, using {sources} to establish the appropriateness and validity of the chosen techniques.\n"
    
    elif section_chapter == "Ethical Considerations":
        prompt = f"Discuss the ethical considerations that will be addressed in the study of {topic} in {field}, based on {sources} to ensure that the research is conducted in a responsible and ethical manner.\n"
    
    elif section_chapter == "Validity and Reliability":
        prompt = f"Explain how validity and reliability will be ensured in the study of {topic} in {field}, drawing on {sources} to establish the strength of the research.\n"
    
    elif section_chapter == "Findings and Analysis":
        prompt = f"Present the findings of the study in a clear and organized manner, using tables, graphs, or other visual aids as appropriate to represent the data collected on {topic} in {field}, with the help of {sources}.\nAnalyze the collected data, describing the patterns, trends, and relationships that were observed, drawing on {sources} to provide context and support for the results.\n"
    
    elif section_chapter == "Conclusions and Future Directions":
        prompt = f"Draw conclusions from the results of the study of {topic} in {field}, explaining how they contribute to the existing knowledge in the field, referencing {sources} to establish the strength of the findings.\nDiscuss any limitations or future directions for research related to {topic} in {field}, drawing on {sources} to identify areas for further study and improvement.\n"
        
    elif section_chapter == "Conclusion":
        prompt=f"Conclusion:\nRestate the purpose and research question, highlighting the key findings related to {topic} in {field}, based on {sources}.\nProvide a summary of the results and their implications for the field, drawing on {sources} to establish the significance of the study.\nDiscuss any limitations or challenges encountered in the study, referencing {sources} to provide context for the issues faced.\nRecommend future research directions, based on {sources}, to build upon the current study and further advance knowledge in the field.\nEnd with a final statement that emphasizes the importance of the study in relation to {field}, drawing on {sources} to support the significance of the research.\nList all sources used in APA format to credit and validate the research.\n"
        + f"Summarize the main findings and conclusions of the study related to {topic} in {field}, emphasizing their significance and contribution to the field, using {sources}.\nDiscuss the implications of the study for future research and its practical applications in {field}, drawing on {sources} to identify potential areas for development and growth.\nEnd with a final statement that emphasizes the significance of the study and its contribution to the existing knowledge of {topic} in {field}, referencing {sources} to establish the strength of the research.\n",
    
    elif section_chapter == "Methodology":
        prompt=f"Provide a clear and detailed description of the research design, including the sampling method, data collection tools, and data analysis techniques that will be used to study {topic} in {field}, using {sources}. Justify the choice of methodology and explain how it is appropriate for answering the research question, citing {sources} to provide evidence for the chosen approach. Discuss any potential ethical concerns and explain how they will be addressed, based on {sources} to ensure a responsible and ethical study. End with a summary of the key features of the methodology, indicating how it will ensure the reliability and validity of the study, with the help of {sources} to establish the strength of the methodology. List all sources used in APA format to credit and validate the research. Describe the research design, methods, and procedures used to collect and analyze data on {topic} in {field}, providing a clear and detailed explanation of the sampling, data collection, and data analysis techniques. Justify the choice of methods and procedures, and discuss any potential limitations or biases that may affect the validity and reliability of the study."
    
    elif section_chapter == "Discussion":
        prompt=f"Discussion:\nInterpret and explain the significance of the results related to {topic} in {field}, using {sources} to provide context and support for the analysis.\nExplain how the findings contribute to the existing knowledge of {topic} in {field}, referencing {sources} to establish the strength of the conclusions.\nDiscuss any unexpected or contradictory results, and explain their possible causes and implications, drawing on {sources} to provide support and explanations.\nIdentify any limitations or shortcomings of the study, and suggest areas for improvement or future research, using {sources} to provide insights into the gaps in knowledge.\nEnd with a concise summary of the key findings and their implications for the field of {field}.\nList all sources used in APA format to credit and validate the research.\n",
    
    elif section_chapter == "Results":
        prompt=f"Results:\nPresent the findings of the study on {topic} in {field} in a clear and organized manner, using tables, graphs, or other visual aids as appropriate to represent the data collected, with the help of {sources}.\nAnalyze the collected data, describing the patterns, trends, and relationships that were observed, drawing on {sources} to provide context and support for the results.\nDraw conclusions from the results and explain how they contribute to the existing knowledge of {topic} in {field}, referencing {sources} to establish the strength of the findings.\nDiscuss any limitations or future directions for research related to {topic} in {field}, drawing on {sources} to identify areas for further study and improvement.\nList all sources used in APA format to credit and validate the research.\n",

    else:
        prompt = f"write {section_chapter} extensively, based on the {topic} in the field of {field} :\n"
        

    response = openai.Completion.create(
        engine="text-davinci-002",
        temperature=0.5,
        prompt= prompt,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        # stop=["\n\n"]
    )
    if 'choices' in response:
        if len(response['choices']) > 0:
            res = response['choices'][0]['text']
        else:
            return []
    else:
        return []

    a_list = res.split('\n')
    if len(a_list) > 0:
        for tins in a_list:
            research_result.append(tins)
    else:
        return []

    return research_result
# =====================================================

# Set up OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Define function 1
def function1():
    prompt = "YOUR_PROMPT_FOR_FUNCTION_1"
    response = openai.Completion.create(engine="YOUR_ENGINE_NAME", prompt=prompt)
    # Process the response from OpenAI API

# Define function 2
def function2():
    prompt = "YOUR_PROMPT_FOR_FUNCTION_2"
    response = openai.Completion.create(engine="YOUR_ENGINE_NAME", prompt=prompt)
    # Process the response from OpenAI API

# Define function 3
def function3():
    prompt = "YOUR_PROMPT_FOR_FUNCTION_3"
    response = openai.Completion.create(engine="YOUR_ENGINE_NAME", prompt=prompt)
    # Process the response from OpenAI API

# Define function 4
def function4():
    prompt = "YOUR_PROMPT_FOR_FUNCTION_4"
    response = openai.Completion.create(engine="YOUR_ENGINE_NAME", prompt=prompt)
    # Process the response from OpenAI API
    


def run_functions(request):
    if request.method == "POST":
        activate_function1 = request.POST.get("function1", False)
        activate_function2 = request.POST.get("function2", False)
        activate_function3 = request.POST.get("function3", False)
        
        # Create a list of functions to run based on user input
        functions_to_run = []
        if activate_function1:
            functions_to_run.append(function1)
        if activate_function2:
            functions_to_run.append(function2)
        if activate_function3:
            functions_to_run.append(function3)

        # Create a list of threads, one for each function
        threads = [threading.Thread(target=f) for f in functions_to_run]

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        return render(request, "success.html")
    else:
        return render(request, "function_form.html")




    # <form method="POST" action="{% url 'run_functions' %}">
    #   {% csrf_token %}
    #   <label>
    #     <input type="checkbox" name="function1" value="True" {% if function1 %}checked{% endif %}>
    #     Function 1
    #   </label>
    #   <br>
    #   <label>
    #     <input type="checkbox" name="function2" value="True" {% if function2 %}checked{% endif %}>
    #     Function 2
    #   </label>
    #   <br>
    #   <label>
    #     <input type="checkbox" name="function3" value="True" {% if function3 %}checked{% endif %}>
    #     Function 3
    #   </label>
    #   <br>
    #   <label>
    #     <input type="checkbox" name="function4" value="True" {% if function4 %}checked{% endif %}>
    #     Function 4
    #   </label>
    #   <br>
    #   <button type="submit">Run Selected Functions</button>
    # </form>
