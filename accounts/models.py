from django.db import models

# Create your models here.
class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.TextField(db_column='USERNAME') # Field name made low
    password = models.TextField(db_column='PASSWORD') # Field name made low
    class Meta:
        managed = True
        db_table = 'Accounts'
        ordering = ['id']
    def __str__(self):
        return self.name