from django.db import models
from multiselectfield import MultiSelectField
from authenticate.models import User

# Create your models here.

class BookRecords(models.Model):

    title = models.CharField(max_length=100, verbose_name='Title')
    copies_tot = models.IntegerField(default=None)
    copies_avail = models.IntegerField(verbose_name='Available Copies', default=1)
    #is_Fiction = models.BooleanField(default=False)
    #is_NonFiction = not is_Fiction
    ch = (('Drama', 'Drama'), ('Romance', 'Romance'), ('Thriller', 'Thriller'), 
            ('Mystery', 'Mystery'), ('Comedy', 'Comedy'), ('Tragedy', 'Tragedy'),('Autobiography', 'Autobiography'), 
            ('Biography', 'Biography'), ('General-Knowledge', 'General-Knowledge'))
    tags = MultiSelectField(choices = ch, verbose_name='Genre', default=None)
    prev_issuers = models.ManyToManyField(User, related_name='%(class)s_prev')
    curr_issuers = models.ManyToManyField(User, related_name='%(class)s_curr')