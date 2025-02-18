# Generated by Django 5.0.6 on 2024-07-09 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_listings_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryName',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imageUrl',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=60),
        ),
    ]
