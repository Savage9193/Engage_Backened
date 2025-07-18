# Generated by Django 3.1.12 on 2025-07-14 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year', models.IntegerField()),
                ('issue_date', models.CharField(max_length=100)),
                ('final_date', models.IntegerField()),
                ('employment_length', models.FloatField()),
                ('home_ownership', models.CharField(max_length=100)),
                ('income_category', models.CharField(max_length=100)),
                ('annual_income', models.IntegerField()),
                ('loan_amount', models.IntegerField()),
                ('term', models.CharField(max_length=100)),
                ('application_type', models.CharField(max_length=100)),
                ('purpose', models.CharField(max_length=100)),
                ('interest_payments', models.CharField(max_length=100)),
                ('loan_condition', models.CharField(max_length=100)),
                ('interest_rate', models.FloatField()),
                ('grade', models.CharField(max_length=10)),
                ('debt_to_income_ratio', models.FloatField()),
                ('total_payment', models.FloatField()),
                ('total_principle_to_recover', models.FloatField()),
                ('total_recoveries', models.FloatField()),
                ('installment', models.FloatField()),
                ('region', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
