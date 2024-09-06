from django.db import models

class TrialSession(models.Model):
    location = models.CharField(max_length=3)  # Локация BH, KW, KSA
    trainer_name = models.CharField(max_length=100)
    session_count = models.IntegerField()
    date = models.DateField()

# Пример отображения данных в шаблоне
# views.py
from django.shortcuts import render
from .models import TrialSession

def trial_sessions_view(request):
    sessions = TrialSession.objects.all()
    return render(request, 'sessions.html', {'sessions': sessions})