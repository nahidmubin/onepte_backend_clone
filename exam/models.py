from django.db import models
from django.contrib.auth.models import User


class Sst(models.Model):
    """Sst model resembles Summarize Spoken Text (SST) type question.
    It saves title, audio of male and female speaker, and the speakers name."""

    title = models.CharField(max_length=150, null=False, blank=False)
    audio_male_voice = models.FileField(upload_to='audio/', null=False, blank=False)
    male_speaker_name = models.CharField(max_length=20, null=False, blank=False)
    audio_female_voice = models.FileField(upload_to='audio/', null=False, blank=False)
    female_speaker_name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.title


class Sstanswer(models.Model):
    """Sstanswer Model saves answer of a SST type question by the user.
    It relates a question from the Sst table and a user from the User table. It
    saves score in several category and finally saves the total score. All the
    practice history of sst type question of a user can be accessed by the
    related_name parameter."""
    
    question = models.ForeignKey(Sst, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, related_name='sst_answers_by_user', on_delete=models.CASCADE, blank=False, null=False)
    answer = models.TextField(blank=False, null=False)
    content_score = models.IntegerField(blank=True, null=False, default=0)
    form_score = models.IntegerField(blank=True, null=False, default=0)
    grammar_score = models.IntegerField(blank=True, null=False, default=0)
    vocabulary_score = models.IntegerField(blank=True, null=False, default=0)
    spelling_score = models.IntegerField(blank=True, null=False, default=0)
    total_score = models.IntegerField(blank=True, null=False,default=0)


    def __str__(self):
        return f"Q: {self.question.title}, A: {self.answer[0:50]}"
    

class Ro(models.Model):
    """Ro model resembles Re-Order Paragraph(RO) type question.
    It saves a title, unordered paragraphs and the correct order of the paragraphs."""

    title = models.CharField(max_length=150, null=False, blank=False)
    paragraphs = models.JSONField(default=dict)
    correct_order = models.JSONField(default=list)

    def __str__(self):
        return self.title
    

class Roanswer(models.Model):
    """Roanswer Model saves answer of a RO type question by the user.
    It relates a question from the Ro table and a user from the User table. It
    saves the maximum score and score depending on the question and answer. All
    the practice history of ro type question of a user can be accessed by the
    related_name parameter."""

    question = models.ForeignKey(Ro, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, related_name='ro_answers_by_user', on_delete=models.CASCADE, blank=False, null=False)
    answer = models.JSONField(default=list)
    score = models.IntegerField(blank=True, null=False,default=0)
    max_score = models.IntegerField(blank=True, null=False,default=0)

    def __str__(self):
        return f"Q: {self.question.title}, A: {self.answer}"    


class Mcq(models.Model):
    """Mcq model resembles Reading Multiple Choice (Multiple) (RMMCQ) type
    question. It saves a title, a passage, options and the correct choices."""

    title = models.CharField(max_length=150, null=False, blank=False)
    passage = models.TextField(null=False, blank=False)
    options = models.JSONField(default=dict)
    correct_choice = models.JSONField(default=list)

    def __str__(self):
        return self.title
    

class Mcqanswer(models.Model):
    """Mcqanswer Model saves answer of a Reading Multiple Choice (Multiple) (RMMCQ)
    type question by the user. It relates a question from the Mcq table and an
    user from the User table. It saves the maximum score and score depending on
    the question and answer. All the practice history of Mcq type question of a
    user can be accessed by the related_name parameter."""

    question = models.ForeignKey(Mcq, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, related_name='mcq_answers_by_user', on_delete=models.CASCADE, blank=False, null=False)
    answer = models.JSONField(default=list)
    score = models.IntegerField(blank=True, null=False,default=0)
    max_score = models.IntegerField(blank=True, null=False,default=0)

    def __str__(self):
        return f"Q: {self.question.title}, A: {self.answer}"