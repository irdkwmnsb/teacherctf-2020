from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	is_teacher = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Mark(models.Model):
	subjects = (
		('Математика', ''),
		('Литература', ''),
		('Биология', ''),
		('Физкультура', ''),
		('Minecraft', ''),
		('ctf', '')
	)
	value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(choices=subjects, max_length=20)


class Question(models.Model):
	title = models.CharField(max_length=40)
	text = models.CharField(max_length=200)
	seen = models.BooleanField(default=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE)