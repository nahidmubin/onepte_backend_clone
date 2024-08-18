from django.db import models
from django.contrib.auth.models import User


# Model for Summarize Spoken Text (SST) type question.
class Sst(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    audio_male_voice = models.FileField(upload_to='audio/', null=False, blank=False)
    male_speaker_name = models.CharField(max_length=20, null=False, blank=False)
    audio_female_voice = models.FileField(upload_to='audio/', null=False, blank=False)
    female_speaker_name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.title

# Model to save Sst answers by the users
class Sstuseranswer(models.Model):
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
    

# Model for Re-Order Paragraph type question.
class Ro(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    paragraphs = models.JSONField(default=dict)
    correct_order = models.JSONField(default=list)

    def __str__(self):
        return self.title
    
# Model to save RO answers by the users
class Rouseranswer(models.Model):
    question = models.ForeignKey(Ro, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, related_name='ro_answers_by_user', on_delete=models.CASCADE, blank=False, null=False)
    answer = models.JSONField(default=list)
    score = models.IntegerField(blank=True, null=False,default=0)
    max_score = models.IntegerField(blank=True, null=False,default=0)

    def __str__(self):
        return f"Q: {self.question.title}, A: {self.answer}"