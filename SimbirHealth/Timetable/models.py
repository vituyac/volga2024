from django.db import models
from Hospital.models import Hospital, Room
from Account.models import User
    
    
class Timetable(models.Model):
    hospitalId = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctorId = models.ForeignKey(User, on_delete=models.CASCADE)
    fr = models.DateTimeField(verbose_name='from')
    to = models.DateTimeField()
    room = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f'{self.number}'
    
class Ticket(models.Model):
    timetableId = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

