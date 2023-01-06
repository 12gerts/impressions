from django.db import models
from django.shortcuts import reverse
from start.models import Profile
from transliterate.decorators import transliterate_function


@transliterate_function(language_code='ru', reversed=True)
def translit(text):
    return text


def to_slug_from_title(title, username):
    symbols = [',', '.', '!', '&', '?', '+', '~', '{', '}', '(', ')', '\\',
               '/', '*', '@', '$', '^', '<', '>', '№', '\'', '"', ';', ':',
               '`']
    for symbol in symbols:
        title = title.replace(symbol, '')
    return f"{username}-{translit(title).replace(' ', '-')}"



class RememberModel(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    body = models.TextField(blank=True, db_index=True)
    slug = models.CharField(max_length=100, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('remember_detail', kwargs={'slug': self.slug})

    def get_absolute_delete_url(self):
        return reverse('remember_delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = to_slug_from_title(self.title, self.profile.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
