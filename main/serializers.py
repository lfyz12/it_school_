from rest_framework import serializers
from .models import CustomUser, regist, curs, lessons, lessons_text, buy_curs

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['uuid', 'img1', 'curss', 'username', 'email']  

class RegistSerializer(serializers.ModelSerializer):
    class Meta:
        model = regist
        fields = ['username', 'name', 'email', 'password1', 'password2']

class CursSerializer(serializers.ModelSerializer):
    class Meta:
        model = curs
        fields = ['name', 'info', 'dop_info', 'img', 'price']

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = lessons
        fields = ['curs', 'name', 'video', 'text']

class LessonsTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = lessons_text
        fields = ['lesson', 'title', 'text', 'img', 'code']

class BuyCursSerializer(serializers.ModelSerializer):
    class Meta:
        model = buy_curs
        fields = ['name', 'curs', 'price']
