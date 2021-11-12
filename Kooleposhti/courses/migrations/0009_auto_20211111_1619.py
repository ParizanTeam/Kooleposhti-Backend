# Generated by Django 3.2.8 on 2021-11-11 12:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_image'),
        ('courses', '0008_auto_20211111_1202'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='Session',
        ),
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('course', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='prerequisites', to='courses.course')),
            ],
        ),
    ]