from django.db import models
import os
# Create your models here.


class PapersModel(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    files = models.FileField(upload_to=os.path.join('static', 'Files'))
    paper_data=models.TextField(null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'PapersModel'