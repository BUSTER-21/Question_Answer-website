from django.shortcuts import render,redirect
from .models import Question,Answer,Tags
from django.contrib.auth.models import User
from .forms import QuestionForm,AnswerForm,TagsForm
from django.shortcuts import get_object_or_404

# Create your views here.
def question_list(request):
    u = User.objects.all()[:5]
    questions = Question.objects.all()
    return render(request,'question_list.html',{'questions':questions,'ranker':u})

def question_new(request):
    u = User.objects.all()[:5]
    questions = Question.objects.all()[:5]
    if request.method == 'POST':
        form1 = QuestionForm(request.POST)
        form2 = TagsForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            question = form1.save(commit=False)
            question.asker = request.user
            question.save()
            form2.save()
            return redirect('question_list')
    else:
        form1 = QuestionForm()
        form2 = TagsForm()
    return render(request,'question_edit.html',{'ranker':u,'questions':questions,'form1':form1,'form2':form2})

def question_detail(request,pk):
    u = User.objects.all()[:5]
    questions = Question.objects.all()[:5]
    quest = get_object_or_404(Question,pk=pk)
    same_user = False
    if(request.user == quest.asker):
        same_user = True
    return render(request,'question_detail.html',{'questions':questions,'ranker':u,'quest':quest,'same_user':same_user})