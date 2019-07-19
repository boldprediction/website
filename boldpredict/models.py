from django.db import models
from hashid_field import HashidAutoField




# Create your models here.
class Contrast(models.Model):
    PRIVATE = 'PR'
    PUBLIC = 'PU'
    PRIVACY_CHOICES = [(PRIVATE, 'Private'),(PUBLIC, 'Public')]
    id = HashidAutoField(primary_key=True)
    privacy_choice = models.CharField('Contrast Privacy Settings',choices=PRIVACY_CHOICES, max_length=2,default=PUBLIC) 
    contrast_title = models.TextField('Contrast Title (Optional)', blank=True)
    list1_name = models.TextField('Enter name of Condition 1')
    list1_text = models.TextField('Enter stimulus words separated by a comma')
    baseline_choice = models.BooleanField('Compare to baseline', default=False)
    list2_name = models.TextField('Enter name of Condition 2')
    list2_text = models.TextField ('Enter stimulus words separated by a comma')
    permutation_choice = models.BooleanField('Run permutation/bootstrap test(needs more waiting time)', default=False)
    # experiment_id = models.BigIntegerField('experiment if it exists',default=0)
    # figures_list = models.TextField('Enter name of Condition 1', default = '')
    # MNIstr = models.TextField('model str')
    # subjstr = models.TextField('model str')
    # pmaps = models.TextField('model str')
    # replicated_figure = models.TextField('replicated_image',  default = '')
    # random_roi_file = models.TextField('random_roi_file',  default = '')
