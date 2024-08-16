from django.db import models

#Model for users


# Model for Summarize Spoken Text (SST) type question.
class Sst(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    audio_male_voice = models.FileField(upload_to='audio', null=False, blank=False)
    male_speaker_name = models.CharField(max_length=20, null=False, blank=False)
    audio_female_voice = models.FileField(upload_to='audio', null=False, blank=False)
    female_speaker_name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.title