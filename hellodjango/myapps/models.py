from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=40,blank=True,null=True,verbose_name="昵称")
    age = models.IntegerField(blank=True,null=True,verbose_name="年龄")
    
    class Meta:
        db_table = "person_info"
