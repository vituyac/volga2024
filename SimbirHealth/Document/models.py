from django.db import models
from Hospital.models import Hospital, Room
from Account.models import User
    
    
class History(models.Model):
    date = models.DateTimeField()
    pacientId = models.ForeignKey(User, on_delete=models.CASCADE)
    hospitalId = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_history')
    doctorId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hospital_doc')
    room = models.CharField(max_length=255, blank=False, null=False)
    data = models.CharField(max_length=512, blank=False, null=False)

    def __str__(self):
        return f'{self.pacientId}'
    
from django.utils import timezone

class FirstConfig(models.Model):
    is_made = models.BooleanField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    
