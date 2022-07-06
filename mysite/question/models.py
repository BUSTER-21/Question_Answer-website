from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Tags(models.Model):
    tag_word = models.CharField(max_length=55)

    def __str__(self):
        return self.tag_word






# creating class for question 

class Question(models.Model):
    subjects = (
    ('1','Competitive Programming'),
    ('2','Database'),
    ('3','Web Devlopment'),
    ('4','Programming Language'),
    ('5','AI'),
    ('6','Computer Vision'),
    ('7','physics'),
    ('8','Chemistry'),
    ('9','math'),
    ('10','biology'),
    ('11','history'),
    ('12','DeepLearning'),
    ('13','Machine Learning'),
    ('14','Hindi'),
    ('15','english'),
    ('16','Geography'),
    ('17','Politics'),
    ('18','Others'),
    )
    asker = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,help_text='title of question')
    text = models.TextField(help_text='description of question')
    tags = models.ManyToManyField(Tags,help_text='tags for question describing pointed topic dealing with question')
    date_of_ask = models.DateField(default = timezone.now)

    def __str__(self):
        return self.title

# creating class for Answer
class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answer')
    answerer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    date_of_reply = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text