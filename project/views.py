from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages


# Create your views here.
def projects(request):
    page = request.GET.get('page')
    results = 3

    projs = Project.objects.all()
    paginator = Paginator(projs, results)
    try:
        projs = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projs = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projs = paginator.page(page)

    page = int(page)

    left_index = int(page) - 3 if page > 3 else 1
    right_index = int(page) + 4 if page < paginator.num_pages - 3 else paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    context = {'projects': projs, 'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'project/projects.html', context)

def project(request, pk):
    proj = Project.objects.get(pk=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = proj
        review.owner = request.user.profile
        review.save()
        proj.get_vote_count()

        messages.success(request, 'Your review was posted successfully!')
        return redirect('project', pk=proj.id)

    context = {'project': proj, 'form': form}
    return render(request, 'project/single-project.html', context)

@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method =="POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.owner = profile
            proj.save()
            return redirect('account')
        
    context = {'form':form}
    return render(request,'project/create-project.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(pk=pk)
    form = ProjectForm(instance=project)

    if request.method =="POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {'form': form, "project" : project}
    return  render(request, "project/form-template.html", context)

@login_required(login_url='login')
def delete_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(pk=pk)

    if request.method == "POST":
        project.delete()
        return redirect('account')

    context = {"object" : project}
    return render(request, 'project/delete.html', context)