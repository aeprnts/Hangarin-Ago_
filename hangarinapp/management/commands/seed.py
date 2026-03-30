from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from hangarinapp.models import Task, Note, SubTask, Priority, Category
import random

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with fake Tasks, SubTasks, Notes, Categories, and Priorities"

    def handle(self, *args, **kwargs):
        
        if Category.objects.count() == 0:
            for name in ["Work", "Personal", "School", "Health", "Finance"]:
                Category.objects.create(name=name)

        if Priority.objects.count() == 0:
            for name in ["Low", "Medium", "High"]:
                Priority.objects.create(name=name)

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=random.choice(["Pending", "In Progress", "Completed"]),
                category=Category.objects.order_by('?').first(),
                priority=Priority.objects.order_by('?').first(),
            )
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=4),
                status=random.choice(["Pending", "In Progress", "Completed"])
            )

        self.stdout.write(self.style.SUCCESS("Fake data seeded successfully!"))
