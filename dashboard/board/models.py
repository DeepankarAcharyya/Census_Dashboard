from django.db import models

# Create your models here.
class census_data(models.Model):
    country = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    location = models.CharField(max_length=25)
    pop_total = models.PositiveIntegerField()
    pop_males = models.PositiveIntegerField()
    pop_females = models.PositiveIntegerField()
    lit_total = models.PositiveIntegerField()
    lit_males = models.PositiveIntegerField()
    lit_females = models.PositiveIntegerField()
    sex_ratio = models.DecimalField(max_digits=7, decimal_places=2)
    literacy_rate_total = models.DecimalField(max_digits=7, decimal_places=2)
    literacy_rate_males = models.DecimalField(max_digits=7, decimal_places=2)
    literacy_rate_females = models.DecimalField(max_digits=7, decimal_places=2)
