from django.shortcuts import render, redirect
from .models import (Member, RehearsalAttendance, SundayServiceAttendance, MondayPrayerMeetingAttendance,
                     OtherAttendance, BirthdaysToday, BirthdaysThisMonth)
from django.contrib import messages
from datetime import date, timedelta, datetime, time


# Create your views here.
def index(request):
    return render(request, 'index.html')


def form_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        level = request.POST['Level']
        level_of_completion = request.POST['Level_of_completion']
        birth_date = request.POST['dob']
        part = request.POST['parts']
        course = request.POST['program']
        location = request.POST['HostelArea']
        hall = request.POST['hallOfResidence']
        mobile_number = request.POST['activeCallNumber']
        whatsapp_number = request.POST['activeWhatsappNumber']
        society = request.POST['society']
        circuit = request.POST['circuit']
        diocese = request.POST['Diocese']

        parts_list = ('bass', 'alto', 'soprano', 'tenor')
        all_levels = ('100', '200', '300', '400', '500', '600')
        completion_levels = ('400', '600')

        if Member.objects.filter(user_id=mobile_number).exists():
            messages.info(request, f'User with ID {mobile_number} already exists !')
            return redirect('form')
        elif len(mobile_number) < 10 or len(mobile_number) > 10:
            messages.info(request, f'Mobile number should be 10 !')
            return redirect('form')
        elif len(whatsapp_number) < 10 or len(whatsapp_number) > 10:
            messages.info(request, f'Whatsapp number should be 10 !')
            return redirect('form')
        elif part not in parts_list:
            messages.info(request, f'Select Parts You Sing !')
            return redirect('form')
        elif level not in all_levels:
            messages.info(request, f'Level Should Be Between 100 - 600 !')
            return redirect('form')
        elif level_of_completion not in completion_levels:
            messages.info(request, f'Level Of Completion Should Be Either 400 Or 600 !')
            return redirect('form')

        else:
            member: Member = Member()
            member.user_id = mobile_number
            member.name = name.capitalize()
            member.level = level
            member.level_of_completion = level_of_completion
            member.birth_date = birth_date
            member.part = part.capitalize()
            member.programme = course.capitalize()
            member.location = location.capitalize()
            member.hall = hall.capitalize()
            member.mobile_number = mobile_number
            member.whatsapp_number = whatsapp_number
            member.society = society.capitalize()
            member.circuit = circuit.capitalize()
            member.diocese = diocese.capitalize()

            member.save()
            return render(request, 'success.html', {'member': name})

    else:
        return render(request, 'fields.html')


def update_view(request):
    if request.method == 'POST':
        user_id = request.POST['choirsterID']
        user_input = (request.POST['userInput']).capitalize()
        update_field = request.POST['dropdownMenu']

        if Member.objects.filter(user_id=user_id).exists():
            member = Member.objects.get(user_id=user_id)
            if update_field == 'name':
                member.name = user_input
            elif update_field == 'program':
                member.programme = user_input
            elif update_field == 'location':
                member.location = user_input
            elif update_field == 'circuit':
                member.circuit = user_input
            elif update_field == 'activeCallNumber':
                member.mobile_number = user_input
            elif update_field == 'whatsapp_number':
                member.whatsapp_number = user_input
            elif update_field == 'diocese':
                member.diocese = user_input
            else:
                messages.info(request, 'Please Select the field you want to update !')
                return redirect('update')
            member.save()

            return render(request, 'success.html', {'member': member.name})
        else:
            messages.info(request, f'User with ID {user_id} does not exist')
            return redirect('update')
    else:
        return render(request, 'update.html')


def attendance_view(request):
    if request.method == 'POST':
        user_id = request.POST['choirsterID']
        activity = request.POST['Activity']

        try:
            user = Member.objects.get(user_id=user_id)

            if (activity == 'Rehearsal' and datetime.now().weekday() == 5 and RehearsalAttendance.objects.
                    filter(present_user=user).exists()):
                messages.error(request, "Rehearsal Attendance Already Taken By This User")
                # return redirect('attendance')
            elif ((activity == 'Rehearsal' and datetime.now().weekday() == 5) and
                  time(15, 0) <= datetime.now().time() <= time(19, 30)):
                today, created = RehearsalAttendance.objects.get_or_create(date=date.today())
                today.present_user.add(user)
                messages.success(request, "Rehearsal Attendance Taken Successfully")

            elif (activity == 'Prayer_Meeting' and datetime.now().weekday() == 6 and SundayServiceAttendance.objects.
                    filter(present_user=user).exists()):
                messages.error(request, "Prayer Meeting Attendance Already Taken By This User")
                return redirect('attendance')
            elif ((activity == 'Prayer_Meeting' and datetime.now().weekday() == 6) and
                  (time(18, 0) <= datetime.now().time() <= time(20, 30))):
                today, created = SundayServiceAttendance.objects.get_or_create(date=date.today())
                today.present_user.add(user)
                messages.success(request, "Prayer Meeting Attendance Taken Successfully")
                return redirect('attendance')

            elif ((activity == 'Midweek_service' and datetime.now().weekday() == 0) and MondayPrayerMeetingAttendance.
                    objects.filter(present_user=user).exists()):
                messages.error(request, "Midweek Service Attendance Already Taken By This User")
                return redirect('attendance')
            elif ((activity == 'Midweek_service' and datetime.now().weekday() == 0) and
                  (time(18, 30) <= datetime.now().time() <= time(20, 30))):
                today, created = MondayPrayerMeetingAttendance.objects.get_or_create(date=date.today())
                today.present_user.add(user)
                messages.success(request, "Midweek Service Attendance Taken Successfully")

            elif activity == 'Other' and OtherAttendance.objects.filter(present_user=user).exists():
                messages.error(request, "Attendance Already Taken By This User")
                return redirect('attendance')
            elif activity == 'Other' and not (OtherAttendance.objects.filter(present_user=user).exists()):
                today, created = OtherAttendance.objects.get_or_create(date=date.today())
                today.present_user.add(user)
                messages.success(request, "Attendance Taken Successfully")
                return redirect('attendance')

            elif activity == '*':
                messages.error(request, "Invalid Activity Selection")
                return redirect('attendance')
            else:
                messages.error(request, "Attendance Submission Is Currently Closed")
                return redirect('attendance')

        except Member.DoesNotExist:
            messages.error(request, "Invalid User ID")
            return redirect('attendance')

    return render(request, 'attendance.html')


def birthdays_today(request):
    today = date.today()

    birthdays = Member.objects.filter(birth_date__month=today.month, birth_date__day=today.day)
    for member in birthdays:
        birthday = BirthdaysToday()
        birthday.user = member
        birthday.save()


def birthdays_this_month(request):
    today = date.today()

    birthdays = Member.objects.filter(birth_date__month=today.month)
    for member in birthdays:
        birthday = BirthdaysThisMonth()
        birthday.user = member
        birthday.save()
