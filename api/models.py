from django.db import models


class Code(models.Model):
    """The model of code. Inherited from models.Model."""
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=12, blank=False)
