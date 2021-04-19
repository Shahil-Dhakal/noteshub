# Core Django imports
from django.db import models
from django.utils.text import slugify

# package imports
from core.models import TimeStampedModel


class Post(TimeStampedModel):
    """
    Base class to define our Post model and its properties
    """
    title = models.CharField(max_length=50)
    title_slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=200)
    file_field = models.FileField(upload_to='user_uploads/', null=True)

    def save(self, *args, **kwargs):
        """ 
        Override the default save function to add a slug from the title
        """
        # if there's no slug provided then assign a slug using the object's name
        if not self.title_slug:
            self.title_slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns a representation of a post object,
        which's displayed in admin page
        """
        return self.title
    
