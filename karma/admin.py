from django.contrib import admin
from karma.models import Task, Person, KarmaLog, Committee
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'karma')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'committee', 'getKarma')


class KarmaLogAdmin(admin.ModelAdmin):
    list_display = ('person', 'task', 'time')

admin.site.register(Task, TaskAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(KarmaLog, KarmaLogAdmin)
admin.site.register(Committee)