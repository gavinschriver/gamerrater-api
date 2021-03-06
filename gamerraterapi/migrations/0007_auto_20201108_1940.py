# Generated by Django 3.1.3 on 2020-11-08 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamerraterapi', '0006_auto_20201107_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pics',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pictures', to='gamerraterapi.game'),
        ),
        migrations.AlterField(
            model_name='pics',
            name='image',
            field=models.ImageField(null=True, upload_to='gamepics'),
        ),
    ]
