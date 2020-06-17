from django.db import models
# from django_mysql.models import ListTextField
from django.contrib.postgres.fields import ArrayField
import uuid


class Question(models.Model):
#     question_id = models.IntegerField(default=1) 
#     question_id = models.UUIDField(primary_key=True, default=uuid.uuid4)   
    category = models.CharField(max_length=100)
    type_qs = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    ques = models.CharField(max_length=255)
    corr_ans = models.CharField(max_length=100)
    ans = ArrayField(
        models.CharField(max_length=100, blank=True),
        size = 4,
        null=True, 
        blank=True
    )


    def __str__(self):
            return self.ques
    

    def __str__(self):
            return self.ans


    def __str__(self):
            return self.corr_ans
