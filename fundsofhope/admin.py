from django.contrib import admin

from fundsofhope.models import User, Ngo, Project, ProjectPicture, NgoPicture


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phoneNo')


class NgoAdmin(admin.ModelAdmin):
    list_display = ('ngoId', 'name', 'email', 'phoneNo', 'address')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cost', 'startDate', 'endDate')


class ProjectPictureAdmin(admin.ModelAdmin):
    list_display = ['picture']


class NgoPictureAdmin(admin.ModelAdmin):
    list_display = ['head', 'profile']


admin.site.register(User, UserAdmin)
admin.site.register(Ngo, NgoAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectPicture, ProjectPictureAdmin)
admin.site.register(NgoPicture, NgoPictureAdmin)
