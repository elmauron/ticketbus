import base64
import json
import re
import time
from datetime import datetime

import socketio
from PIL import Image
from crum import get_current_request
from django.db import models
from django.forms import model_to_dict

from config import settings
from core.cooperative.choices import *
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=13, verbose_name='Ruc')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=10, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=9, verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, verbose_name='Email')
    website = models.CharField(max_length=250, verbose_name='Página web')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logitpo de la empresa')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='IVA')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_iva(self):
        return float(self.iva)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toJsonDumps(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['iva'] = float(self.iva)
        return json.dumps(item)

    def get_base64_encoded_image(self):
        try:
            image = base64.b64encode(open(self.image.path, 'rb').read()).decode('utf-8')
            type_image = Image.open(self.image.path).format.lower()
            return f"data:image/{type_image};base64,{image}"
        except:
            pass
        return None

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Empresa'),
        )


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'


class Exemplar(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='Marca')

    def __str__(self):
        return f'{self.brand.name} / {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        item['brand'] = self.brand.toJSON()
        return item

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    dni = models.CharField(max_length=13, unique=True, verbose_name='Número de documento')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate_format()
        return item

    def delete(self, using=None, keep_parents=False):
        super(Client, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Member(models.Model):
    names = models.CharField(max_length=200, verbose_name='Nombres')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Número de documento')
    image = models.ImageField(upload_to='member/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo electrónico')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    date_joined = models.DateField(default=datetime.now)
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    contribution = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Aporte mensual')

    def __str__(self):
        return self.names

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['contribution'] = float(self.contribution)
        return item

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'


class Chauffeur(models.Model):
    names = models.CharField(max_length=200, verbose_name='Nombres')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Número de documento')
    image = models.ImageField(upload_to='chauffeur/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo electrónico')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono celular')
    date_joined = models.DateField(default=datetime.now)
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    license = models.CharField(max_length=2, choices=TYPE_LICENSE, verbose_name='Tipo de licencia')

    def __str__(self):
        return self.names

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['license'] = {'id': self.license, 'name': self.get_license_display()}
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Chofer'
        verbose_name_plural = 'Choferes'


class Bus(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    exemplar = models.ForeignKey(Exemplar, on_delete=models.PROTECT, verbose_name='Marca/Modelo')
    member = models.ForeignKey(Member, on_delete=models.PROTECT, verbose_name='Socio')
    year = models.IntegerField(default=0, verbose_name='Año')
    plaque = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    car_seats = models.IntegerField(default=0, verbose_name='Número de Asientos')
    car_disk = models.IntegerField(default=0, verbose_name='Número de Anden')
    image = models.ImageField(upload_to='bus/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    ticket_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Precio pasaje')

    def __str__(self):
        return f'Nombre: {self.name} Placa: {self.plaque} / Socio: {self.member.names}'

    def get_short_name(self):
        return f'{self.name} ({self.plaque})'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['exemplar'] = self.exemplar.toJSON()
        item['member'] = self.member.toJSON()
        item['image'] = self.get_image()
        item['ticket_price'] = float(self.ticket_price)
        return item

    class Meta:
        verbose_name = 'Bus'
        verbose_name_plural = 'Buses'


class Place(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'


class Route(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, verbose_name='Bus')
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.PROTECT, verbose_name='Chofer')
    departure_time = models.TimeField(default=datetime.now, verbose_name='Hora de salida')
    place = models.ForeignKey(Place, on_delete=models.PROTECT, verbose_name='Destino')
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Precio')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return f"Bus: {self.bus.name} ({self.bus.plaque}) / Destino: {self.place.name} / Hora de salida: {self.departure_time_format()} / Anden:{self.bus.car_disk} Precio: ${f'{self.price:.2f}'}"

    def departure_time_format(self):
        return self.departure_time.strftime('%H:%M %p')

    def search_seats(self):
        date_now = datetime.now().date()
        seats = list(self.saledetail_set.filter(date_joined=date_now).values_list('seat', flat=True))
        return seats

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.__str__()
        item['bus'] = self.bus.toJSON()
        item['departure_time'] = self.departure_time_format()
        item['chauffeur'] = self.chauffeur.toJSON()
        item['place'] = self.place.toJSON()
        item['price'] = float(self.price)
        return item

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        default_permissions = ()
        permissions = (
            ('view_route', 'Can view Ruta'),
            ('view_client_route', 'Can view Ruta | Cliente'),
            ('add_route', 'Can add Ruta'),
            ('change_route', 'Can change Ruta'),
            ('delete_route', 'Can delete Ruta'),
        )


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Cliente')
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
    payment_condition = models.CharField(choices=PAYMENT_CONDITION, max_length=50, default=PAYMENT_CONDITION[0][0], verbose_name='Condición de pago')
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=50, default=PAYMENT_METHOD[0][0], verbose_name='Método de pago')
    type_voucher = models.CharField(choices=VOUCHER, max_length=50, default=VOUCHER[0][0], verbose_name='Comprobante')
    hour_joined = models.TimeField(default=datetime.now, verbose_name='Hora de registro')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Subtotal')
    iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Iva')
    total_iva = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total iva')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Total')
    cash = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Efectivo')
    change = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Cambio')
    card_number = models.CharField(max_length=19, null=True, blank=True, verbose_name='Número de tarjeta')
    card_titular = models.CharField(max_length=30, null=True, blank=True, verbose_name='Titular')
    card_amount_debited = models.DecimalField(max_digits=9, decimal_places=2, default=0.00, verbose_name='Monto a debitar')
    card_type = models.CharField(max_length=250, choices=CARD_TYPE, default=CARD_TYPE[0][0], verbose_name='Tipo de tarjeta')
    card_year = models.CharField(max_length=5, verbose_name='Año')
    card_code_verification = models.CharField(max_length=3, verbose_name='Código de verificación')

    def __str__(self):
        return self.client.get_full_name()

    def get_number(self):
        return f'{self.id:06d}'

    def get_client(self):
        if self.client:
            return self.client.toJSON()
        return {}

    def card_number_format(self):
        if self.card_number:
            cardnumber = self.card_number.split(' ')
            convert = re.sub('[0-9]', 'X', ' '.join(cardnumber[1:]))
            return f'{cardnumber[0]} {convert}'
        return self.card_number

    def toJSON(self):
        item = model_to_dict(self)
        item['cant_tikets'] = self.saledetail_set.all().count()
        item['number'] = self.get_number()
        item['card_number'] = self.card_number_format()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['hour_joined'] = self.hour_joined.strftime('%H:%M')
        item['employee'] = self.employee.toJSON()
        item['client'] = self.client.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['payment_method'] = {'id': self.payment_method, 'name': self.get_payment_method_display()}
        item['type_voucher'] = {'id': self.type_voucher, 'name': self.get_type_voucher_display()}
        item['subtotal'] = float(self.subtotal)
        item['iva'] = float(self.iva)
        item['total_iva'] = float(self.total_iva)
        item['total'] = float(self.total)
        item['cash'] = float(self.cash)
        item['change'] = float(self.change)
        item['card_amount_debited'] = float(self.card_amount_debited)
        item['card_type'] = {'id': self.card_type, 'name': self.get_card_type_display()}
        return item

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.saledetail_set.all():
            i.subtotal = float(i.price) * int(i.cant)
            i.save()
            subtotal += i.subtotal
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total = float(self.subtotal) + float(self.total_iva)
        self.save()

    def send_data_with_socket(self):
        try:
            request = get_current_request()
            URL = request.build_absolute_uri('/').strip('/').split(':')
            detail = [i.toJSON() for i in self.saledetail_set.all()]
            info = {'tickets': detail}
            if settings.SOCKET_CONNECTION is None:
                sio = socketio.Client()
                sio.connect(url=f'{URL[0]}:{URL[1]}:{settings.SOCKET_PORT}', namespaces=['/'])
            else:
                sio = settings.SOCKET_CONNECTION
            sio.emit('message', info)
            time.sleep(2)
            sio.disconnect()
            print('Message sent successfully')
        except Exception as e:
            print(f'Error: {str(e)}')

    def delete(self, using=None, keep_parents=False):
        try:
            self.saledetail_set.all().delete()
        except:
            pass
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Venta | Admin'),
            ('add_sale', 'Can add Venta | Admin'),
            ('delete_sale', 'Can delete Venta | Admin'),
            ('view_client_sale', 'Can view Venta | Cliente'),
            ('add_client_sale', 'Can add Venta | Cliente'),
        )


class SaleDetail(models.Model):
    date_joined = models.DateField(default=datetime.now)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    seat = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return self.route.bus.plaque

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale', 'date_joined'])
        item['route'] = self.route.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
