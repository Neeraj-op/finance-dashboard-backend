"""
Create demo data for production demonstration.
Run with: python create_demo_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from finance.models import FinancialRecord
from decimal import Decimal
from datetime import date, timedelta
import random

def create_demo_data():
    print("Creating demo data...")
    
    if FinancialRecord.objects.exists():
        print("Demo data already exists. Skipping...")
        return
    # Create demo users if they don't exist
    admin, created = User.objects.get_or_create(
        username='demo_admin',
        defaults={
            'email': 'admin@demo.com',
            'role': User.Role.ADMIN,
            'is_active': True
        }
    )
    if created:
        admin.set_password('DemoAdmin123!')
        admin.save()
        print("✓ Created demo admin user")
    
    analyst, created = User.objects.get_or_create(
        username='demo_analyst',
        defaults={
            'email': 'analyst@demo.com',
            'role': User.Role.ANALYST,
            'is_active': True
        }
    )
    if created:
        analyst.set_password('DemoAnalyst123!')
        analyst.save()
        print("✓ Created demo analyst user")
    
    viewer, created = User.objects.get_or_create(
        username='demo_viewer',
        defaults={
            'email': 'viewer@demo.com',
            'role': User.Role.VIEWER,
            'is_active': True
        }
    )
    if created:
        viewer.set_password('DemoViewer123!')
        viewer.save()
        print("✓ Created demo viewer user")
    
    # Sample data for admin user
    sample_records = [
        # Income records
        {'amount': 75000, 'type': 'INCOME', 'category': 'SALARY', 'date': date(2024, 1, 31), 'desc': 'January salary'},
        {'amount': 75000, 'type': 'INCOME', 'category': 'SALARY', 'date': date(2024, 2, 29), 'desc': 'February salary'},
        {'amount': 75000, 'type': 'INCOME', 'category': 'SALARY', 'date': date(2024, 3, 31), 'desc': 'March salary'},
        {'amount': 35000, 'type': 'INCOME', 'category': 'BUSINESS', 'date': date(2024, 1, 15), 'desc': 'Freelance project'},
        {'amount': 50000, 'type': 'INCOME', 'category': 'BUSINESS', 'date': date(2024, 2, 20), 'desc': 'Consulting work'},
        
        # Expense records
        {'amount': 25000, 'type': 'EXPENSE', 'category': 'RENT', 'date': date(2024, 1, 1), 'desc': 'January rent'},
        {'amount': 25000, 'type': 'EXPENSE', 'category': 'RENT', 'date': date(2024, 2, 1), 'desc': 'February rent'},
        {'amount': 25000, 'type': 'EXPENSE', 'category': 'RENT', 'date': date(2024, 3, 1), 'desc': 'March rent'},
        {'amount': 15000, 'type': 'EXPENSE', 'category': 'FOOD', 'date': date(2024, 1, 15), 'desc': 'Groceries'},
        {'amount': 12000, 'type': 'EXPENSE', 'category': 'FOOD', 'date': date(2024, 2, 15), 'desc': 'Groceries'},
        {'amount': 8000, 'type': 'EXPENSE', 'category': 'TRANSPORT', 'date': date(2024, 1, 10), 'desc': 'Fuel & public transport'},
        {'amount': 7500, 'type': 'EXPENSE', 'category': 'TRANSPORT', 'date': date(2024, 2, 10), 'desc': 'Fuel & public transport'},
        {'amount': 5000, 'type': 'EXPENSE', 'category': 'UTILITIES', 'date': date(2024, 1, 5), 'desc': 'Electricity & water'},
        {'amount': 4500, 'type': 'EXPENSE', 'category': 'UTILITIES', 'date': date(2024, 2, 5), 'desc': 'Electricity & water'},
        {'amount': 6000, 'type': 'EXPENSE', 'category': 'ENTERTAINMENT', 'date': date(2024, 1, 20), 'desc': 'Movies & dining out'},
        {'amount': 3500, 'type': 'EXPENSE', 'category': 'ENTERTAINMENT', 'date': date(2024, 2, 20), 'desc': 'Movies & dining out'},
        {'amount': 8000, 'type': 'EXPENSE', 'category': 'HEALTHCARE', 'date': date(2024, 1, 12), 'desc': 'Medical checkup'},
        {'amount': 10000, 'type': 'EXPENSE', 'category': 'SHOPPING', 'date': date(2024, 2, 14), 'desc': 'Clothing & accessories'},
    ]
    
    created_count = 0
    for record in sample_records:
        _, created = FinancialRecord.objects.get_or_create(
            user=admin,
            amount=Decimal(str(record['amount'])),
            type=record['type'],
            category=record['category'],
            date=record['date'],
            defaults={'description': record['desc']}
        )
        if created:
            created_count += 1
    
    print(f"✓ Created {created_count} financial records")
    
    # Create a few records for viewer
    viewer_records = [
        {'amount': 60000, 'type': 'INCOME', 'category': 'SALARY', 'date': date(2024, 1, 31), 'desc': 'January salary'},
        {'amount': 20000, 'type': 'EXPENSE', 'category': 'RENT', 'date': date(2024, 1, 1), 'desc': 'January rent'},
        {'amount': 8000, 'type': 'EXPENSE', 'category': 'FOOD', 'date': date(2024, 1, 15), 'desc': 'Groceries'},
    ]
    
    for record in viewer_records:
        FinancialRecord.objects.get_or_create(
            user=viewer,
            amount=Decimal(str(record['amount'])),
            type=record['type'],
            category=record['category'],
            date=record['date'],
            defaults={'description': record['desc']}
        )
    
    print("\n=== Demo Data Summary ===")
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Records: {FinancialRecord.objects.filter(is_deleted=False).count()}")
    print(f"Income Records: {FinancialRecord.objects.filter(type='INCOME', is_deleted=False).count()}")
    print(f"Expense Records: {FinancialRecord.objects.filter(type='EXPENSE', is_deleted=False).count()}")
    
    print("\n=== Demo Login Credentials ===")
    print("Admin:   username='demo_admin',   password='DemoAdmin123!'")
    print("Analyst: username='demo_analyst', password='DemoAnalyst123!'")
    print("Viewer:  username='demo_viewer',  password='DemoViewer123!'")
    print("\nDemo data created successfully! ✓")

if __name__ == '__main__':
    create_demo_data()