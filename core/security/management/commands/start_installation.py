import os
from os.path import basename

import django
from django.core.files import File
from django.core.management import BaseCommand

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.cooperative.models import *
from core.security.models import *
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = "Allows to initiate the base software installation"

    def handle(self, *args, **options):
        dashboard = Dashboard.objects.create(
            name='BUSIKET WEB',
            author='William Jair Dávila Vargas',
            icon='fas fa-shopping-cart',
            layout=1,
            navbar='navbar-dark navbar-navy',
            sidebar='sidebar-dark-navy'
        )
        image_path = f'{settings.BASE_DIR}{settings.STATIC_URL}img/default/logo.png'
        dashboard.image.save(basename(image_path), content=File(open(image_path, 'rb')), save=False)
        dashboard.save()

        moduletype = ModuleType.objects.create(name='Seguridad', icon='fas fa-lock')
        print(f'insertado {moduletype.name}')

        modules_data = [
            {
                'name': 'Tipos de Módulos',
                'url': '/security/module/type/',
                'icon': 'fas fa-door-open',
                'description': 'Permite administrar los tipos de módulos del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Módulos',
                'url': '/security/module/',
                'icon': 'fas fa-th-large',
                'description': 'Permite administrar los módulos del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Grupos',
                'url': '/security/group/',
                'icon': 'fas fa-users',
                'description': 'Permite administrar los grupos de usuarios del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Respaldos',
                'url': '/security/database/backups/',
                'icon': 'fas fa-database',
                'description': 'Permite administrar los respaldos de base de datos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Conf. Dashboard',
                'url': '/security/dashboard/update/',
                'icon': 'fas fa-tools',
                'description': 'Permite configurar los datos de la plantilla',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Dashboard._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Accesos',
                'url': '/security/user/access/',
                'icon': 'fas fa-user-secret',
                'description': 'Permite administrar los accesos de los usuarios',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=UserAccess._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Usuarios',
                'url': '/user/',
                'icon': 'fas fa-user',
                'description': 'Permite administrar a los administradores del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Cambiar password',
                'url': '/user/update/password/',
                'icon': 'fas fa-key',
                'description': 'Permite cambiar tu password de tu cuenta',
                'moduletype': None,
                'permissions': None
            },
            {
                'name': 'Editar perfil',
                'url': '/user/update/profile/',
                'icon': 'fas fa-user',
                'description': 'Permite cambiar la información de tu cuenta',
                'moduletype': None,
                'permissions': None
            }
        ]

        moduletype = ModuleType.objects.create(name='Cooperativa', icon='fas fa-city')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Compañia',
                'url': '/cooperative/company/update/',
                'icon': 'fas fa-building',
                'description': 'Permite gestionar la información de la compañía',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Company._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Socios',
                'url': '/cooperative/member/',
                'icon': 'fas fa-user-cog',
                'description': 'Permite administrar a los socios del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Member._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Choferes',
                'url': '/cooperative/chauffeur/',
                'icon': 'fas fa-user-astronaut',
                'description': 'Permite administrar a los choferes del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Chauffeur._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Destinos',
                'url': '/cooperative/place/',
                'icon': 'fas fa-street-view',
                'description': 'Permite administrar los lugares de las rutas',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Place._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Rutas',
                'url': '/cooperative/route/',
                'icon': 'fas fa-tasks',
                'description': 'Permite administrar las rutas del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Route._meta.label.split('.')[1].lower()).exclude(codename='view_client_route'))
            },
        ])

        moduletype = ModuleType.objects.create(name='Vehículos', icon='fas fa-car')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Buses',
                'url': '/cooperative/bus/',
                'icon': 'fas fa-bus',
                'description': 'Permite administrar a los buses del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Bus._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Marcas',
                'url': '/cooperative/brand/',
                'icon': 'fas fa-ring',
                'description': 'Permite administrar las marcas de los vehículos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Brand._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Modelos',
                'url': '/cooperative/exemplar/',
                'icon': 'fas fa-box-open',
                'description': 'Permite administrar los modelos de los vehículos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Exemplar._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Categorías',
                'url': '/cooperative/category/',
                'icon': 'fas fa-truck-loading',
                'description': 'Permite administrar las categorías de los productos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()))
            }
        ])

        moduletype = ModuleType.objects.create(name='Facturación', icon='fas fa-shopping-cart')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Clientes',
                'url': '/cooperative/client/',
                'icon': 'fas fa-user-friends',
                'description': 'Permite administrar a los clientes del sistema',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()))
            },
            {
                'name': 'Ventas',
                'url': '/cooperative/sale/',
                'icon': 'fas fa-shopping-cart',
                'description': 'Permite administrar las ventas de los boletos',
                'moduletype': moduletype,
                'permissions': list(Permission.objects.filter(content_type__model=Sale._meta.label.split('.')[1].lower()).exclude(codename__in=['view_client_sale', 'add_client_sale']))
            },
            {
                'name': 'Boletería',
                'url': '/cooperative/sale/client/',
                'icon': 'fas fa-shopping-cart',
                'description': 'Permite administrar las ventas de los boletos',
                'moduletype': None,
                'permissions': list(Permission.objects.filter(codename__in=['view_client_sale', 'add_client_sale']))
            },
            {
                'name': 'Editar perfil',
                'url': '/cooperative/client/update/profile/',
                'icon': 'fas fa-user',
                'description': 'Permite cambiar la información de tu cuenta',
                'moduletype': None,
                'permissions': None
            },
            {
                'name': 'Destinos',
                'url': '/cooperative/route/client/',
                'icon': 'fas fa-street-view',
                'description': 'Permite administrar los destinos de las rutas',
                'moduletype': None,
                'permissions': [Permission.objects.get(codename='view_client_route')]
            },
        ])

        moduletype = ModuleType.objects.create(name='Reportes', icon='fas fa-chart-pie')
        print(f'insertado {moduletype.name}')

        modules_data.extend([
            {
                'name': 'Buses',
                'url': '/reports/bus/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de los buses',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Rutas',
                'url': '/reports/route/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de las rutas',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Ventas',
                'url': '/reports/sale/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de las ventas',
                'moduletype': moduletype,
                'permissions': None
            },
            {
                'name': 'Clientes',
                'url': '/reports/client/',
                'icon': 'fas fa-chart-bar',
                'description': 'Permite ver los reportes de los clientes',
                'moduletype': moduletype,
                'permissions': None
            }
        ])

        for module_data in modules_data:
            module = Module.objects.create(
                module_type=module_data['moduletype'],
                name=module_data['name'],
                url=module_data['url'],
                icon=module_data['icon'],
                description=module_data['description']
            )
            if module_data['permissions']:
                for permission in module_data['permissions']:
                    module.permissions.add(permission)
            print(f'insertado {module.name}')

        group = Group.objects.create(name='Administrador')
        print(f'insertado {group.name}')

        CLIENT_URLS = ['/cooperative/client/update/profile/', '/cooperative/sale/client/', '/cooperative/route/client/']

        for module in Module.objects.filter().exclude(url__in=CLIENT_URLS):
            GroupModule.objects.create(module=module, group=group)
            for permission in module.permissions.all():
                group.permissions.add(permission)

        user = User.objects.create(
            names='William Jair Dávila Vargas',
            username='admin',
            email='davilawilliam93@gmail.com',
            is_active=True,
            is_superuser=True,
            is_staff=True
        )
        user.set_password('hacker94')
        user.save()
        user.groups.add(group)
        print(f'Bienvenido {user.names}')

        group = Group.objects.create(name='Cliente')
        print(f'insertado {group.name}')

        for module in Module.objects.filter(url__in=CLIENT_URLS + ['/user/update/password/']):
            GroupModule.objects.create(module=module, group=group)
            for permission in module.permissions.all():
                group.permissions.add(permission)
