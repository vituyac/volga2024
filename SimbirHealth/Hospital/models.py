from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    address = models.CharField(max_length=255, blank=False, null=False)
    contactPhone = models.CharField(max_length=255, blank=False, null=False)
    
class Room(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=255, blank=False, null=False, unique=False)

    def __str__(self):
        return f'{self.number}'
