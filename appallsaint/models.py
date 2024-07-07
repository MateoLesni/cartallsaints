from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    categories = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class CategoryItem(models.Model):
        name = models.CharField(max_length=50)
        list = []