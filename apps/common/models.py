from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Something(BaseModel):
    title = models.CharField(max_length=122, verbose_name=_("title"))
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Something'
        verbose_name_plural = "Something"
