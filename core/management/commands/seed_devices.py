from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Category, Tag, Device

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with initial device data'

    def handle(self, *args, **options):
        # Create categories
        serial_cat, _ = Category.objects.get_or_create(
            name='Serial Devices',
            defaults={'description': 'Devices that communicate serially', 'slug': 'serial-devices'}
        )
        parallel_cat, _ = Category.objects.get_or_create(
            name='Parallel Devices',
            defaults={'description': 'Devices that communicate in parallel', 'slug': 'parallel-devices'}
        )

        # Create tags
        usb_tag, _ = Tag.objects.get_or_create(name='USB', defaults={'slug': 'usb'})
        wireless_tag, _ = Tag.objects.get_or_create(name='Wireless', defaults={'slug': 'wireless'})

        # Get or create a default user
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'role': 'admin', 'password': 'user98765', 'id': 1}
        )

        # Create devices
        devices_data = [
            {
                'name': 'Arduino Uno',
                'type': 'serial',
                'description': 'Popular microcontroller board',
                'specs': {'voltage': '5V', 'clock': '16MHz'},
                'category': serial_cat,
                'tags': [usb_tag],
            },
            {
                'name': 'Raspberry Pi 4',
                'type': 'parallel',
                'description': 'Single-board computer',
                'specs': {'ram': '8GB', 'cpu': '1.5GHz'},
                'category': parallel_cat,
                'tags': [wireless_tag],
            },
        ]

        for device_data in devices_data:
            tags = device_data.pop('tags')
            device, created = Device.objects.get_or_create(
                name=device_data['name'],
                defaults=device_data
            )
            device.created_by = user
            device.tags.set(tags)
            device.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created device: {device.name}'))
            else:
                self.stdout.write(f'Device {device.name} already exists')