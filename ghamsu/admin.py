from django.contrib import admin
from .models import (Member, SundayServiceAttendance, RehearsalAttendance, MondayPrayerMeetingAttendance,
                     OtherAttendance, BirthdaysThisMonth, BirthdaysToday, Associate)
from simple_history.admin import SimpleHistoryAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db.models import Q
from django.utils.timezone import now
from django.http import HttpResponseRedirect


admin.site.site_header = 'GHAMSU UCC CHOIR'
admin.site.site_title = 'GHAMSU UCC CHOIR'
admin.site.index_title = 'GHAMSU UCC CHOIR ADMINISTRATION'


class MemberResource(resources.ModelResource):
    class Meta:
        model = Member
        fields = ['name', 'birth_date', 'level', 'level_of_completion', 'part', 'mobile_number', 'location']


@admin.register(Member)
class MemberAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    prepopulated_fields = {"user_id": ("mobile_number",)}
    actions = ['update_birthdays']
    list_display = ['name', 'birth_date', 'level', 'part', 'mobile_number', 'location']
    list_per_page = 25
    list_filter = ['part', 'level',  'location']
    search_fields = ('name__icontains', 'mobile_number__icontains', 'level__icontains', 'location__icontains',)
    ordering = ['name', 'level']
    #readonly_fields = ()
    resource_classes = [MemberResource]

    @admin.action(description="Update Birthdays")
    def update_birthdays(self, request, queryset):
        today = now().date()

        birthdays_today = Member.objects.filter(
            Q(birth_date__month=today.month) & Q(birth_date__day=today.day)
        )

        for member in birthdays_today:
            if not BirthdaysToday.objects.filter(user=member).exists():
                birthday = BirthdaysToday(user=member)
                birthday.save()

        birthdays_month = Member.objects.filter(birth_date__month=today.month)

        for member in birthdays_month:
            if not BirthdaysThisMonth.objects.filter(user=member).exists():
                birthday = BirthdaysThisMonth(user=member)
                birthday.save()

        self.message_user(request, "Birthdays updated successfully")

    change_form_template = "button_form.html"

    def response_change(self, request, obj):
        if "_promote-members" in request.POST:
            users = Member.objects.all()
            for user in users:
                if int(user.level) < int(user.level_of_completion):
                    user.level = int(user.level) + 100
                    user.save()
                elif int(user.level) == int(user.level_of_completion):
                    associate = Associate()

                    associate.user_id = user.user_id
                    associate.name = user.name.capitalize()
                    associate.level = user.level
                    associate.level_of_completion = user.level_of_completion
                    associate.birth_date = user.birth_date
                    associate.part = user.part.capitalize()
                    associate.programme = user.programme.capitalize()
                    associate.location = user.location.capitalize()
                    associate.hall = user.hall.capitalize()
                    associate.mobile_number = user.mobile_number
                    associate.whatsapp_number = user.whatsapp_number
                    associate.society = user.society.capitalize()
                    associate.circuit = user.circuit.capitalize()
                    associate.diocese = user.diocese.capitalize()
                    associate.created_at = now()

                    associate.save()
                    user.delete()
            self.message_user(request, "Members have been promoted successfully")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class BirthdayResource(resources.ModelResource):
    class Meta:
        model = BirthdaysThisMonth
        fields = ['user__name', 'user__birth_date', 'user__level', 'user__level_of_completion', 'user__part',
                  'user__mobile_number', 'user__location']


@admin.register(BirthdaysThisMonth)
class BirthdaysMonthAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    actions = ['delete_past_birthdays']
    list_display = ['name', 'birth_date', 'level', 'part', 'mobile_number', 'location']
    list_per_page = 25
    list_filter = ['user__level', 'user__birth_date', 'user__location']
    search_fields = ('name__icontains', 'mobile_number__icontains', 'level__icontains',)
    ordering = ['user__birth_date']
    readonly_fields = ('user_id',)
    resource_classes = [BirthdayResource]

    @admin.action(description="Remove Past Birthdays")
    def delete_past_birthdays(self, request, queryset):
        today = now().date()
        old_birthdays = BirthdaysThisMonth.objects.filter(user__birth_date__month__lt=today.month)
        count = old_birthdays.count()
        old_birthdays.delete()

        self.message_user(request, f"{count} past birthdays deleted.")


@admin.register(BirthdaysToday)
class BirthdaysTodayAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    actions = ['delete_past_birthdays']
    list_display = ['user_name', 'user_birth_date', 'user_level', 'user_part', 'user_mobile_number', 'user_location']
    list_per_page = 25
    list_filter = ['user__level', 'user__part', 'user__birth_date', 'user__location']
    search_fields = ('user_name__icontains', 'user_mobile_number__icontains', 'user_level__icontains',)
    ordering = ['user__level', 'user__name']
    readonly_fields = ('user_user_id',)
    resource_classes = [BirthdayResource]

    @admin.action(description="Remove Past Birthdays")
    def delete_past_birthdays(self, request, queryset):
        today = now().date()
        old_birthdays = BirthdaysToday.objects.filter(user__birth_date__lt=today)
        count = old_birthdays.count()
        old_birthdays.delete()

        self.message_user(request, f"{count} past birthdays deleted.")


class RehearsalsUsersInline(admin.TabularInline):
    model = RehearsalAttendance.present_user.through
    extra = 0
    can_delete = False
    fields = ('member', 'member_part')
    readonly_fields = ('member_part',)
    list_filter = ('member_part',)
    sortable_by = ('member_part',)
    autocomplete_fields = ('member',)

    def member_part(self, obj):
        return obj.member.part


@admin.register(RehearsalAttendance)
class RehearsalAttendanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('present_user',)
    list_display = ['present_user_name', 'member_part', 'date']
    list_per_page = 25
    ordering = ['-date']
    inlines = [RehearsalsUsersInline]
    list_filter = ('present_user__part', 'date')
    def present_user_name(self, obj):
        return "  |  ".join(member.name for member in obj.present_user.all())

    @admin.display(ordering=['member_part'])
    def member_part(self, obj):
        return ", ".join(member.part for member in obj.present_user.all())


class SundayServiceUsersInline(admin.TabularInline):
    model = SundayServiceAttendance.present_user.through
    extra = 0
    can_delete = False
    fields = ('member', 'member_part')
    readonly_fields = ('member_part',)
    list_filter = ('member_part',)
    autocomplete_fields = ('member',)

    def member_part(self, obj):
        return obj.member.part


@admin.register(SundayServiceAttendance)
class SundayServiceAttendanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('present_user',)
    list_display = ['present_user_name', 'member_part', 'date']
    list_per_page = 25
    ordering = ['-date']
    inlines = [SundayServiceUsersInline]
    list_filter = ('present_user__part', 'date')
    def present_user_name(self, obj):
        return "  |  ".join(member.name for member in obj.present_user.all())

    @admin.display(ordering=['member_part'])
    def member_part(self, obj):
        return ", ".join(member.part for member in obj.present_user.all())


class MondayPrayerMeetingUsersInline(admin.TabularInline):
    model = MondayPrayerMeetingAttendance.present_user.through
    extra = 0
    can_delete = False
    fields = ('member', 'member_part')
    readonly_fields = ('member_part',)
    list_filter = ('member_part',)
    autocomplete_fields = ('member',)

    def member_part(self, obj):
        return obj.member.part


@admin.register(MondayPrayerMeetingAttendance)
class MondayPrayerMeetingAttendanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('present_user',)
    list_display = ['present_user_name', 'member_part', 'date']
    list_per_page = 25
    ordering = ['-date']
    inlines = [MondayPrayerMeetingUsersInline]
    list_filter = ('present_user__part', 'date')
    def present_user_name(self, obj):
        return "  |  ".join(member.name for member in obj.present_user.all())

    @admin.display(ordering=['member_part'])
    def member_part(self, obj):
        return ", ".join(member.part for member in obj.present_user.all())


class OtherAttendanceInline(admin.TabularInline):
    model = OtherAttendance.present_user.through
    extra = 0
    can_delete = False
    fields = ('member', 'member_part')
    readonly_fields = ('member_part',)
    list_filter = ('member_part',)
    autocomplete_fields = ('member',)

    def member_part(self, obj):
        return obj.member.part


@admin.register(OtherAttendance)
class OtherAttendanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ('present_user',)
    list_display = ['present_user_name', 'member_part', 'date']
    list_per_page = 25
    ordering = ['date']
    inlines = [OtherAttendanceInline]
    list_filter = ('present_user__part', 'date')

    def present_user_name(self, obj):
        return "  |  ".join(member.name for member in obj.present_user.all())

    @admin.display(ordering=['member_part'])
    def member_part(self, obj):
        return ", ".join(member.part for member in obj.present_user.all())


class AssociateResource(resources.ModelResource):
    class Meta:
        model = Associate
        fields = ['name', 'birth_date', 'level', 'level_of_completion', 'part',
                  'mobile_number', 'location']


@admin.register(Associate)
class AssociateAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'birth_date', 'level', 'part', 'mobile_number', 'location']
    list_per_page = 25
    list_filter = ['part', 'birth_date', 'location']
    search_fields = ('name__icontains', 'mobile_number__icontains', 'location__icontains',)
    ordering = ['name']
    readonly_fields = ('user_id',)
    resource_classes = [AssociateResource]












