from django.db import models
from django_mysql.models import ListTextField


class Question(models.Model):
    category = models.CharField(max_length=100)
    type_qs = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100)
    ques = models.CharField(max_length=255)
    corr_ans = models.CharField(max_length=100)
    ans = ListTextField(
        base_field = models.CharField(max_length=100),
        size = 4,
        max_length = (4 * 101)
    )


    def __str__(self):
            return self.ques
