from django.db import models


class CustomManager(models.Manager):
    """
    Custom manager so as not to return deleted objects
    """

    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(deleted=False)


class AbstractBase(models.Model):
    """
    This contains all common object attributes
    Every model will inherit this class to avoid repetition
    Its abstract hence can't be instatiated
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False,
                                  help_text="This is to make sure deletes are not actual deletes")
    active = models.BooleanField(default=True)
    # everything will be used to query deleted objects e.g Model.everything.all()
    everything = models.Manager()
    objects = CustomManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        ordering = ['-updated_at', '-created_at']
        abstract = True
