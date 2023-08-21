from django.contrib import admin
from .models import CustomUser, TeamMember, Team, Task, TaskAssignment
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Task)
admin.site.register(TaskAssignment)

