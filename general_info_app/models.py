from django.db import models


class Address(models.Model):
    company_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.company_name


class Socialnetwork(models.Model):
    link = models.URLField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.link


class Faqs(models.Model):
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)