from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from task.models import Tasks, CompletedTasks
from company.models import Team, Staff, Company, TaskType, Admins, Unknown
@login_required(login_url="/login/")
def index(request):
    all_task = Tasks.objects.all()
    all_task_count = all_task.count()
    completed = all_task.filter(is_completed=True)
    completed_count = completed.count()
    uncompleted = all_task.filter(is_completed=False)
    overall_rating = float((completed_count/all_task_count)*100)
    company = Company.objects.all()






    mydict = {"all_task": all_task, 'completed': completed, 'uncompleted': uncompleted,
            'overall_rating': overall_rating, 'company': company} 
    return render(request, "index.html", context=mydict)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))