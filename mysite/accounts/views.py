from django.shortcuts import render,redirect,get_object_or_404

from django.http import HttpResponse
from .forms import SignUpForm
from .forms import LoginForm,UserDetailForm,StudentDetailForm
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from question.models import Question

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

# importing models for fetching the query

from .models import Student,Ssconnector,Subject,Subject,Quotes,Batch
from blog.models import Post

# importing connection for performing the raw sql queries

from django.db import connection


# creating function for signup
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data['password1']
            confirm_password = form.cleaned_data["confirm_password"]
            agree_term = form.cleaned_data["agree_term"]
            if agree_term:
                if password1 == confirm_password:
                    if User.objects.filter(username=username).exists():
                        messages.info(request,'username taken')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request,"Email already exists")
                    else:
                        user = User.objects.create_user(username=username,email=email,password=password1)
                        user.is_active = False
                        user.save()
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your blog account.'
                        message = render_to_string('acc_active_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':account_activation_token.make_token(user),
                        })
                        to_email = form.cleaned_data.get('email')
                        email = EmailMessage(
                                    mail_subject, message, to=[to_email]
                        )
                        email.send()
                        return HttpResponse('Please confirm your email address to complete the registration')
                else:
                    messages.error(request,"confiramtion password doesn't match")
            else:
                messages.info(request,"It seems that you had not agreed to the terms and conditions")
        else:
            messages.error(request,"please check again")
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})

# creating function for login
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = User.objects.get(email=email.lower()).username
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('/')
            else:
                messages.error(request,'invalid credentials')
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})


 
def logout(request):
    auth.logout(request)
    return redirect('/')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        # return redirect('home')
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


# function for profile_detail 

def my_custom_sql():
    with connection.cursor() as c:
        c.execute()

@login_required
def profile_detail(request,pk):

    profile = get_object_or_404(User,pk=pk)
    u = User.objects.all()
    posts = Post.objects.filter(published_date__isnull = False,author__pk = pk).order_by('created_date')
    questions = Question.objects.filter(asker__pk=pk).order_by('date_of_ask')
    program_dict = {'U':'Undergraduate','M':'Masters','H':'HighSchool','N':'Nurcher'}
    std = program_dict[profile.student.program]
    confirm_user = False
    if request.user == profile:
        confirm_user = True
    return render(request,'profile_detail.html',{'profile':profile,'ranker':u,'std':std,'posts':posts,'confirm_user':confirm_user,'questions':questions})
@login_required
def profile_list(request):
    u = User.objects.all()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    program_dict = {'U':'Undergraduate','M':'Masters','H':'HighSchool','N':'Nurcher'}
    program = 'UnderGraduate'
    #program = [program_dict[t.student.program] for t in u]
    return render(request,'profile.html',{'ranker':u,'std':program,'posts':posts})

# function for profile detailing

@login_required
def profile_edit(request , pk):
    u = User.objects.all()[:5]
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')[:5]
    post = get_object_or_404(User,pk = pk)
    student = get_object_or_404(Student,user__pk = pk)
    confirm_user = False
    if request.method == "POST":
        form1 = StudentDetailForm(request.POST,instance=student)
        form2 = UserDetailForm(request.POST,instance=post)
        if form1.is_valid() and form2.is_valid():
            post1 = form1.save(commit = False)
            post1.save()
            post2 = form2.save(commit=False)
            post2.save()
            return redirect('profile_detail',pk=post.pk)
    else:
        form1 = StudentDetailForm(instance = student)
        form2 = UserDetailForm(instance=post)
    return render(request ,'profile_edit.html',{'form1':form1,'form2':form2,'ranker':u,'posts':posts})
