# Generated by Django 4.2.3 on 2023-09-06 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("results", "0003_alter_course_grade_alter_course_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="grade",
            field=models.CharField(
                choices=[
                    ("A", "A"),
                    ("B", "B"),
                    ("C", "C"),
                    ("D", "D"),
                    ("E", "E"),
                    ("F", "F"),
                ],
                max_length=10,
            ),
        ),
    ]