from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import SiteVisitCounter, UserVisit


@receiver(post_save, sender=User)
def update_site_visits(sender, instance, **kwargs):
    SiteVisitCounter.increment()
    UserVisit.increment_visit_count(instance)
