# Generated by Django 4.1 on 2023-05-03 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pub_date', models.DateField()),
                ('content', models.TextField(default='')),
                ('number_view', models.CharField(default='0', max_length=100)),
                ('number_comment', models.CharField(default='0', max_length=100)),
                ('up_vote', models.CharField(default='0', max_length=100)),
                ('down_vote', models.CharField(default='0', max_length=100)),
                ('tag', models.TextField(default='')),
                ('types_blog', models.CharField(choices=[('trả lời', 'hỏi'), ('bình luận', 'đăng bài viết')], default='trả lời', max_length=20)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], default='MALE', max_length=20)),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('address', models.CharField(default='', max_length=100)),
                ('company', models.CharField(default='', max_length=100)),
                ('friends_list', models.TextField(blank=True, default='', null=True)),
                ('blogs_list', models.TextField(blank=True, default='', null=True)),
                ('question_list', models.TextField(blank=True, default='', null=True)),
                ('organization', models.TextField(blank=True, default='', null=True)),
                ('reporter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commented',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.reporter')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.reporter'),
        ),
    ]
