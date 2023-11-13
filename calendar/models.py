from django.db import models
from django.utils.translation import gettext_lazy as _


class Calendar(models.Model):
    # Model fields and methods...

    class Meta:
        app_label = 'calendar'
        verbose_name = _("calendar")
        verbose_name_plural = _("calendars")
