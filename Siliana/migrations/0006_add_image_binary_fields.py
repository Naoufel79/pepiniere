# Generated manually for PostgreSQL image storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Siliana', '0005_produit_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='image_data',
            field=models.BinaryField(blank=True, editable=False, null=True, verbose_name='بيانات الصورة'),
        ),
        migrations.AddField(
            model_name='produit',
            name='image_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم الصورة'),
        ),
        migrations.AddField(
            model_name='produit',
            name='image_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='نوع الصورة'),
        ),
    ]
