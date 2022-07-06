
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    course_name = models.CharField(unique=True, max_length=50,help_text='specialization')
    subject = models.ForeignKey('Subject', models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.subject}({self.course_name})'




class Ssconnector(models.Model):
    work = (
        ('S','Student'),
        ('M','Mentor'),
        ('O','Organizer')
    )
    ss_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True)
    subbatch = models.ForeignKey('Subbatch', models.DO_NOTHING, blank=True, null=True)
    role = models.CharField(default='S',max_length=1,help_text='user role',choices=work,blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.subject}({self.course_name})'




class Student(models.Model):
    USER_STATUS = (
        ('M','Masters'),
        ('U', 'UnderGraduate'),
        ('H', 'HighSchool'),
        ('F', 'Foundation'),
        ('N', 'Nurcher')
    )

    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/')
    points = models.IntegerField(blank=True, null=True)
    ratings = models.FloatField(blank=True, null=True,editable=False)
    program = models.CharField(max_length=1, blank=True,default='H',choices=USER_STATUS,help_text='user qualification')
    date_of_birth = models.DateField(null=True,blank=True)
    total_upvote = models.IntegerField(blank=True,null=True)
    total_view = models.IntegerField(blank=True,null=True)
    is_mentor = models.BooleanField(default=False,verbose_name='want to become a mentor')
    describe_yourself = models.TextField(help_text='describe_yourself',blank=True,max_length=255)
    opinion = models.TextField(help_text="know your opnion",blank=True,max_length=255,default="No matter what your dream , it will come true.")

    class Meta:
        ordering = ['points']
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.student_id} ({self.user.username})'
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('user-detail', args=[str(self.student_id)])


class Subbatch(models.Model):
    SUBBATCH_STATUS = (
        ('M','Masters'),
        ('U', 'UnderGraduate'),
        ('H', 'HighSchool'),
        ('F', 'Foundation'),
        ('N', 'Nurcher')
    )
    subbatch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=55)
    batch = models.ManyToManyField(Batch,help_text = 'contents to be taught')
    level = models.CharField(max_length=1,blank=True,default='H',choices=SUBBATCH_STATUS,help_text='level of subbatch')
    description = models.TextField(max_length=255,null=True,blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('subbatch-detail', args=[str(self.subbatch_id)])



class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    sub_name = models.CharField(unique=True, max_length=40)

    def __str__(self):
        """String for representing the Model object."""
        return self.sub_name


class Quotes(models.Model):
    quotes_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    quotes = models.TextField(help_text="enter your thoughts of the day",max_length=255,null=True,default="No matter what you dream, It will come true.")
    created_time = models.TimeField(default=timezone.now)
    author = models.CharField(help_text='author of quotes',max_length=55,blank=True)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return self.quotes
