from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment, NewUser


# Register your models here.
# field = list(UserAdmin.fieldsets)
# field[1] = ('Personal Infor',{})
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Infor',
            {
                'fields': (
                    'profile_pic',
                )
            }
        )
    )


admin.site.register(NewUser, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
