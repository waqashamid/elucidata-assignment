from django.db import models

# Create your models here.

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Data(Base):
    name = models.CharField(null=True, max_length=40)
    file = models.FileField(upload_to='media/')

    def __str__(self):
        return self.name
