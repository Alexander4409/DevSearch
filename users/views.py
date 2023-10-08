from .models import Profile, User
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import search_profiles
# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "username does not exist")

    return render(request, 'users/login_register.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, "You are logged out! ")
    return redirect('profiles')


def profiles(request):
    profs, search_query = search_profiles(request)

    context = {'profiles': profs, 'search_query': search_query}
    return render(request, 'users/index.html', context)


def register_user(request):
    page = "register"
    form = CustomUserCreationForm
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower().strip()
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred during registration!')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def user_profile(reqest, pk):
    profile = Profile.objects.get(pk=pk)
    top_skills = profile.skill_set.exclude( description__exact="")
    other_skills = profile.skill_set.filter( description__exact="")
    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
    }
    return render(reqest, 'users/profile.html',context)


@login_required(login_url='login')
def user_account(request):
    prof = request.user.profile
    skills = prof.skill_set.all()
    projects = prof.project_set.all()
    context = {
        'profile': prof,
        'skills': skills,
        'projects': projects,
    }
    return render(request, "users/account.html", context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            messages.success(request,"Account edited successfully! ")
            return redirect("account")

    context = {'form': form}
    return render(request, "users/profile_form.html", context)

@login_required(login_url='login')
def create_skill(reqest):
    profile = reqest.user.profile
    form = SkillForm()
    if reqest.method == "POST":
        form = SkillForm(reqest.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            messages.success(reqest,'Skill was added successfully')
            return redirect('account')

    context = {'form': form}
    return render(reqest, "users/skill_form.html", context)

@login_required(login_url='login')
def update_skill(reqest,pk):
    profile = reqest.user.profile
    skill = profile.skill_set.get(pk=pk)
    form = SkillForm(instance=skill)

    if reqest.method == "POST":
        form = SkillForm(reqest.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(reqest, 'Skill was update successfully')

            return redirect('account')

    context = {'form': form}
    return render(reqest, "users/skill_form.html", context)

@login_required(login_url='login')
def delete_skill (reqest,pk):
    profile = reqest.user.profile
    skill = profile.skill_set.get(pk=pk)

    if reqest.method == "POST":
        skill.delete()
        return redirect('account')

    context = {'object': skill}
    return render(reqest, "project/delete.html", context)

@login_required(login_url='login')
def inbox(reqest):
    profile = reqest.user.profile
    user_messages = profile.messages.all()
    unread_count = user_messages.filter(is_read=False).count()
    context = {'user_messages': user_messages,
               'unread_count': unread_count}
    return render(reqest,'users/inbox.html', context)

@login_required(login_url='login')
def view_message(request,pk):
    profile = request.user.profile
    message = profile.messages.get(pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request,'users/message.html', context)


def create_message(request,pk):
    recipient = Profile.objects.get(pk=pk)
    form =MessageForm()
    sender =None
    if request.user.is_authenticated:
        del form.fields['name']
        del form.fields['email']
        sender = request.user.profile

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.success(request, "your message successfully sent!")
            message.save()

            return redirect('user_profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request,'users/message_form.html', context)

