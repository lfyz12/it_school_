from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, regist, curs, lessons, lessons_text, buy_curs

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'uuid']
    fieldsets = (
        ('Дополнительная информация', {'fields': ('email', 'img1', 'curss')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}) )

    # add_fieldsets = (
    #     ('New info', {
    #         'classes': ('wide',),
    #         'fields': ('email', 'img1')}),)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(regist)
admin.site.register(curs)

class lessonsAdmin(admin.ModelAdmin):
    model = lessons
    list_display = ['id', 'name', 'curs']

admin.site.register(lessons, lessonsAdmin)

class lessons_textAdmin(admin.ModelAdmin):
    model = lessons_text
    list_display = ['id', 'title', 'lesson']

admin.site.register(lessons_text, lessons_textAdmin)
admin.site.register(buy_curs)