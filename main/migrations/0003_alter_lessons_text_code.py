# Generated by Django 4.1.1 on 2022-11-03 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_lessons_text_options_lessons_text_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons_text',
            name='code',
            field=models.CharField(choices=[(True, True), (False, False)], max_length=10, verbose_name='Код?'),
        ),
    ]
