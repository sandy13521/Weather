from django.db import models

# Create your models here.
class city(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField()
    temp = models.FloatField()
    des = models.CharField(max_length=50, default="")
    icon = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
