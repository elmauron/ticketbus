from django.urls import path

from core.cooperative.views.brand.views import *
from core.cooperative.views.place.views import *
from core.cooperative.views.category.views import *
from core.cooperative.views.client.views import *
from core.cooperative.views.company.views import CompanyUpdateView
from core.cooperative.views.exemplar.views import *
from core.cooperative.views.member.views import *
from core.cooperative.views.chauffeur.views import *
from core.cooperative.views.bus.views import *
from core.cooperative.views.route.views import *
from core.cooperative.views.sale.views import *

urlpatterns = [
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # place
    path('place/', PlaceListView.as_view(), name='place_list'),
    path('place/add/', PlaceCreateView.as_view(), name='place_create'),
    path('place/update/<int:pk>/', PlaceUpdateView.as_view(), name='place_update'),
    path('place/delete/<int:pk>/', PlaceDeleteView.as_view(), name='place_delete'),
    # brand
    path('brand/', BrandListView.as_view(), name='brand_list'),
    path('brand/add/', BrandCreateView.as_view(), name='brand_create'),
    path('brand/update/<int:pk>/', BrandUpdateView.as_view(), name='brand_update'),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
    # exemplar
    path('exemplar/', ExemplarListView.as_view(), name='exemplar_list'),
    path('exemplar/add/', ExemplarCreateView.as_view(), name='exemplar_create'),
    path('exemplar/update/<int:pk>/', ExemplarUpdateView.as_view(), name='exemplar_update'),
    path('exemplar/delete/<int:pk>/', ExemplarDeleteView.as_view(), name='exemplar_delete'),
    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # member
    path('member/', MemberListView.as_view(), name='member_list'),
    path('member/add/', MemberCreateView.as_view(), name='member_create'),
    path('member/update/<int:pk>/', MemberUpdateView.as_view(), name='member_update'),
    path('member/delete/<int:pk>/', MemberDeleteView.as_view(), name='member_delete'),
    # chauffeur
    path('chauffeur/', ChauffeurListView.as_view(), name='chauffeur_list'),
    path('chauffeur/add/', ChauffeurCreateView.as_view(), name='chauffeur_create'),
    path('chauffeur/update/<int:pk>/', ChauffeurUpdateView.as_view(), name='chauffeur_update'),
    path('chauffeur/delete/<int:pk>/', ChauffeurDeleteView.as_view(), name='chauffeur_delete'),
    # bus
    path('bus/', BusListView.as_view(), name='bus_list'),
    path('bus/add/', BusCreateView.as_view(), name='bus_create'),
    path('bus/update/<int:pk>/', BusUpdateView.as_view(), name='bus_update'),
    path('bus/delete/<int:pk>/', BusDeleteView.as_view(), name='bus_delete'),
    # ruts
    path('route/', RouteListView.as_view(), name='route_list'),
    path('route/client/', RouteClientListView.as_view(), name='route_client'),
    path('route/add/', RouteCreateView.as_view(), name='route_create'),
    path('route/update/<int:pk>/', RouteUpdateView.as_view(), name='route_update'),
    path('route/delete/<int:pk>/', RouteDeleteView.as_view(), name='route_delete'),
    # sale
    path('sale/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_print_invoice'),
    path('sale/client/print/invoice/<int:pk>/', SalePrintInvoiceView.as_view(), name='sale_client_print_invoice'),
    path('sale/client/', SaleClientListView.as_view(), name='sale_client_list'),
    path('sale/client/add/', SaleClientCreateView.as_view(), name='sale_client_create'),
]
