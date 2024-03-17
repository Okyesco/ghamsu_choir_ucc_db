from django.db import models
from simple_history.models import HistoricalRecords
from datetime import datetime


# Create your models here.
class Member(models.Model):
    #user_id = models.CharField(max_length=10, primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    level = models.CharField(max_length=255, blank=False, null=False)
    level_of_completion = models.CharField(max_length=255, blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    part = models.CharField(max_length=255, blank=False, null=False)
    programme = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    hall = models.CharField(max_length=255, blank=False, null=False)
    mobile_number = models.CharField(max_length=10, blank=False, null=False)
    whatsapp_number = models.CharField(max_length=10, blank=False, null=False)
    society = models.CharField(max_length=255, blank=False, null=False)
    circuit = models.CharField(max_length=255, blank=False, null=False)
    diocese = models.CharField(max_length=255, blank=False, null=False)
    user_id = models.CharField(max_length=10, primary_key=True, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name}'

    def date_created(self):
        return self.created_at


class BirthdaysThisMonth(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='birthdays_monthly')
    history = HistoricalRecords()



    def __str__(self):
        return f'{self.user.name} - Birthday is this month on - {self.user.birth_date}'

    def name(self):
        return self.user.name

    def birth_date(self):
        return self.user.birth_date

    def level(self):
        return self.user.level

    def part(self):
        return self.user.part

    def mobile_number(self):
        return self.user.mobile_number

    def location(self):
        return self.user.location

    def user_id(self):
        return self.user.user_id


class BirthdaysToday(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='birthdays_today')
    history = HistoricalRecords()



    def __str__(self):
        return f'{self.user.name} - Birthday is this month on - {self.user.birth_date}'

    def user_name(self):
        return self.user.name

    def user_birth_date(self):
        return self.user.birth_date

    def user_level(self):
        return self.user.level

    def user_part(self):
        return self.user.part

    def user_mobile_number(self):
        return self.user.mobile_number

    def user_location(self):
        return self.user.location

    def user_user_id(self):
        return self.user.user_id


class RehearsalAttendance(models.Model):
    date = models.DateField(auto_now_add=True)
    present_user = models.ManyToManyField(Member, related_name='rehearsal_members')
    history = HistoricalRecords()




    def __str__(self):
        return f'{self.present_user.name} - Was Present Today - {self.date}'

    def present_user_name(self):
        return self.present_user.name


class SundayServiceAttendance(models.Model):
    date = models.DateField(auto_now_add=True)
    present_user = models.ManyToManyField(Member, related_name='sunday_members')
    history = HistoricalRecords()


    def __str__(self):
        return f'{self.present_user.name} - Was Present Today - {self.date}'

    def present_user_name(self):
        return self.present_user.name


class MondayPrayerMeetingAttendance(models.Model):
    date = models.DateField(auto_now_add=True)
    present_user = models.ManyToManyField(Member, related_name='monday_members')
    history = HistoricalRecords()


    def __str__(self):
        return f'{self.present_user.name} - Was Present Today - {self.date}'

    def present_user_name(self):
        return self.present_user.name


class OtherAttendance(models.Model):
    date = models.DateField(auto_now_add=True)
    present_user = models.ManyToManyField(Member, related_name='other_members')
    history = HistoricalRecords()


    def __str__(self):
        return f'{self.present_user.name} - Was Present Today - {self.date}'

    def present_user_name(self):
        return self.present_user.name


class Associate(models.Model):
    #user_id = models.CharField(max_length=10, primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    level = models.CharField(max_length=255, blank=False, null=False)
    level_of_completion = models.CharField(max_length=255, blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    part = models.CharField(max_length=255, blank=False, null=False)
    programme = models.CharField(max_length=255, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    hall = models.CharField(max_length=255, blank=False, null=False)
    mobile_number = models.CharField(max_length=10, blank=False, null=False)
    whatsapp_number = models.CharField(max_length=10, blank=False, null=False)
    society = models.CharField(max_length=255, blank=False, null=False)
    circuit = models.CharField(max_length=255, blank=False, null=False)
    diocese = models.CharField(max_length=255, blank=False, null=False)
    user_id = models.CharField(max_length=10, primary_key=True, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.name} - Became an Associate on {self.created_at}'

    def level(self):
        return 'Completed'









