from django.db import models

class ErrorReport(models.Model):
    code = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)