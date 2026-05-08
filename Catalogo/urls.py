from django.urls import path
from Catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cervezas/', views.CervezaListView.as_view(), name='cervezas'),
    path('cerveza/<pk>', views.CervezaDetailView.as_view(), name='cerveza'),
    path('cerveza/<int:pk>/editar/', views.CervezaUpdateView.as_view(), name='cerveza_update'),
    path('cerveza/<int:pk>/eliminar/', views.borrar_cerveza, name='cerveza_delete'),
    path('cerveza/new/', views.CervezaCreateView.as_view(), name='cerveza_new'),
    path('servicios/<cerveza_id>', views.ServicioListView.as_view(), name='servicios'),
    path('servicio/<int:pk>/', views.ServicioDetailView.as_view(), name='servicio'),
    path('venta/<int:cerveza_id>/servicio/<int:servicio_id>/', views.realizar_venta, name='venta'),
    path('NuestrosServicios/', views.ServicioEstaticoListView.as_view(), name='servicioEstatico_List'),
    path('NuestrosServicios/nuevo/', views.ServicioCreateView.as_view(), name='servicio_crear'),
    path('NuestrosServicios/<int:pk>/editar/', views.ServicioUpdateView.as_view(), name='servicio_editar'),
    path('NuestrosServicios/<int:pk>/eliminar/', views.ServicioDeleteView.as_view(), name='servicio_eliminar'),
    path('cerveza/<int:cerveza_id>/barriles/', views.editar_stock_barriles, name='editar_stock_barriles'),
    path('barril/<int:barril_id>/editar/', views.editar_barril, name='editar_stock_barril'),
    path('barril/<int:barril_id>/eliminar/', views.eliminar_barril, name='eliminar_barril'),
    path('choperas/', views.editar_stock_choperas, name='editar_stock_choperas'),
    path('chopera/<int:chopera_id>/editar/', views.editar_chopera, name='editar_chopera'),
    path('chopera/<int:chopera_id>/eliminar/', views.eliminar_chopera, name='eliminar_chopera'),
    path('estadisticas/ventas/', views.grafico_ventas_cervezas, name='grafico_ventas'),
    
    path('findUs/', views.generic.TemplateView.as_view(template_name='findUs.html'), name='findUs'),
    path('contacto/', views.generic.TemplateView.as_view(template_name='contacto.html'), name='contacto'),
]
