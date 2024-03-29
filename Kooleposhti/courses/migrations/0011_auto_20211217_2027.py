# Generated by Django 3.2.8 on 2021-12-17 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_publicprofile_bio'),
        ('courses', '0010_auto_20211211_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='grade',
            field=models.CharField(choices=[('عالی', 'A'), ('خیلی خوب', 'B'), ('خوب', 'C'), ('نیاز به تلاش بیشتر', 'D')], max_length=18),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateTimeField()),
                ('title', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('used_no', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_codes', to='accounts.instructor')),
            ],
        ),
    ]
