from django.db import models
import datetime

class data_update(models.Model):
    time_stamp = models.DateTimeField()

    def __str__(self):
        return str(self.time_stamp)

class athlete(models.Model):
    id = models.BigIntegerField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    access_token = models.CharField(max_length=45)

    def __str__(self):
        return self.firstname + " " + self.lastname

class activity(models.Model):
    id = models.BigIntegerField(primary_key=True)
    athlete_id = models.ForeignKey(athlete,on_delete=models.CASCADE,)
    name = models.CharField(max_length=140)
    distance = models.FloatField()
    moving_time = models.DurationField()
    elapsed_time = models.DurationField()
    total_elevation_gain = models.FloatField()
    type = models.CharField(max_length=30)
    start_date_local = models.DateTimeField()
    average_speed = models.FloatField()
    calories = models.IntegerField(null=True, blank=True)
    photos = models.URLField(null=True, blank=True)
    cumulative_elevation = models.FloatField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)

    def is_this_month(self, month=None):
        if not month:
            month = datetime.datetime.today()._month
        if self.start_date_local._month == month:
            return True
        else:
            return False

    def __str__(self):
        return self.name
