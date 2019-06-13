from django.db import models

# Create your models here.
class Contrast(models.Model):
    image_location = models.CharField(max_length=200)

    # def __str__(self):
    #     return str(self.id)+" "+self.post_text+" ("+str(self.post_date_time)+")"
    def dump(self):
        return {
            'pk' : self.id,
            'image_location' : self.image_location
        }
