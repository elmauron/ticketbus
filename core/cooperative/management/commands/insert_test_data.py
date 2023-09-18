import os
import random
import string
from datetime import date, timedelta
from os.path import basename

import django
from django.core.files import File
from django.core.management import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group
from core.cooperative.models import *


class Command(BaseCommand):
    help = "It allows me to insert test data into the software"

    def handle(self, *args, **options):
        numbers = list(string.digits)
        letters = list(string.ascii_letters)

        company = Company.objects.create(
            name='BUSIKET S.A.',
            ruc=''.join(random.choices(numbers, k=13)),
            email='williamjair94@hotmail.com',
            phone=''.join(random.choices(numbers, k=7)),
            mobile=''.join(random.choices(numbers, k=10)),
            description='Contamos con más de 68 años de experiencia en servicio, seguridad y comodidad. Nuestras 54 unidades doble piso son modernas y equipadas con la mejor tecnología en servicio de viajes terrestres.',
            website='https://algorisoft.com',
            address='Cdla. Dager, Calle Rio Zamora entre Av.Tumbes y Av. Tarqui',
            iva=12.00
        )
        image_path = f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/logo.png'
        company.image.save(basename(image_path), content=File(open(image_path, 'rb')), save=False)
        company.save()

        for name in ['INTERPROVINCIALES', 'INTRAREGIONAL', 'INTRAPROVINCIAL', 'TROLEBÚS']:
            Category.objects.create(name=name)

        for name in ['TOYOTA', 'CHEVROLET', 'HYNDAI']:
            Brand.objects.create(name=name)

        for brand in Brand.objects.all():
            for year in range(2018, 2022):
                Exemplar.objects.create(brand=brand, name=str(year))

        with open(f'{settings.BASE_DIR}/deploy/json/customers.json', 'r') as json_file:
            data = json.load(json_file)

            for item in data[0:10]:
                Member.objects.create(
                    names=f"{item['first']} {item['last']}",
                    dni=f"0{''.join(random.choices(numbers, k=9))}",
                    mobile=f"0{''.join(random.choices(numbers, k=9))}",
                    address=item['country'],
                    email=item['email'],
                    contribution=random.randint(50, 100)
                )

            for item in data[11:20]:
                Chauffeur.objects.create(
                    names=f"{item['first']} {item['last']}",
                    dni=f"0{''.join(random.choices(numbers, k=9))}",
                    mobile=f"0{''.join(random.choices(numbers, k=9))}",
                    address=item['country'],
                    email=item['email'],
                    license=TYPE_LICENSE[random.randint(1, 11)][0]
                )

            user = User.objects.create(
                names='Consumidor Final',
                email='davilawilliam94@gmail.com',
                username='9999999999999',
            )
            user.set_password(user.username)
            user.save()
            user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))

            Client.objects.create(
                user=user,
                dni='9999999999999',
                birthdate=date(1994, 10, 19),
                mobile='9999999999',
                address='Milagro, cdla. Paquisha'
            )

            for item in data[21:30]:
                user = User.objects.create(
                    names=f"{item['first']} {item['last']}",
                    username=f"0{''.join(random.choices(numbers, k=9))}",
                    email=item['email']
                )
                user.set_password(user.username)
                user.save()
                user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
                Client.objects.create(
                    user=user,
                    dni=user.username,
                    mobile=f"0{''.join(random.choices(numbers, k=9))}",
                    address=item['country']
                )

        names = ['MARISCAL SUCRE', 'FLOTA PELILEO', 'RUTA MILAGREÑA', 'EJECUTIVO EXPRESS', 'TUM', 'MARISCAL SUCRE', 'EXPRESO MILAGRO', 'CITIM', 'TRONCALEÑA', 'ESMERALDAS']
        car_disk = 1

        exemplar_id = list(Exemplar.objects.values_list('id', flat=True))
        category_id = list(Category.objects.values_list('id', flat=True))
        for member in Member.objects.all():
            for _ in range(0, random.randint(1, 3)):
                Bus.objects.create(
                    year=random.randint(2012, 2022),
                    name=random.choice(names),
                    category_id=random.choice(category_id),
                    plaque=f"{''.join(random.choices(letters, k=3)).upper()}-{''.join(random.choices(numbers, k=3))}",
                    exemplar_id=random.choice(exemplar_id),
                    member=member,
                    car_seats=random.randint(50, 60),
                    car_disk=car_disk,
                    ticket_price=random.uniform(1.30, 2.50)
                )
                car_disk += 1

        for place_name in ['MILAGRO-MARISCAL SUCRE', 'MILAGRO-PELILEO', 'MILAGRO-GUAYAQUIL', 'MILAGRO-TRIUNFO', 'MILAGRO-SANTA ELENA', 'MILAGRO-TRONCAL', 'MILAGRO-ESMERALDAS']:
            Place.objects.create(name=place_name)

        current_date = datetime.now()
        place_id = list(Place.objects.values_list('id', flat=True))
        chauffeur_id = list(Chauffeur.objects.values_list('id', flat=True))
        bus_id = list(Bus.objects.values_list('id', flat=True))
        hours = [8, 12, 16, 20, 23]

        for bus in Bus.objects.all():
            for hour in hours:
                departure_time = current_date.replace(hour=hour, minute=0) + timedelta(days=random.randint(0, 7))
                Route.objects.create(
                    departure_time=departure_time.time(),
                    chauffeur_id=random.choice(chauffeur_id),
                    place_id=random.choice(place_id),
                    bus_id=random.choice(bus_id),
                    price=bus.ticket_price
                )
