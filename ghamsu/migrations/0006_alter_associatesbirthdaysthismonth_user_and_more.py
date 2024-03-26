# Generated by Django 4.1.9 on 2024-03-26 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ghamsu", "0005_historicalassociatesbirthdaystoday_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="associatesbirthdaysthismonth",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="associate_birthdays_monthly",
                to="ghamsu.associate",
            ),
        ),
        migrations.AlterField(
            model_name="associatesbirthdaystoday",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="associate_birthdays_today",
                to="ghamsu.associate",
            ),
        ),
        migrations.AlterField(
            model_name="historicalassociatesbirthdaysthismonth",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="ghamsu.associate",
            ),
        ),
        migrations.AlterField(
            model_name="historicalassociatesbirthdaystoday",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="ghamsu.associate",
            ),
        ),
    ]