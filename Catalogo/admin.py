from django.contrib import admin

# Register your models here.
from Catalogo.models import  Cerveza, Categoria, GraduacionAlcoholica, Servicio, Bar, Usuario, TipoServicio, Barril, Pedido, DetallePedido, Chopera
admin.site.register(Cerveza)
admin.site.register(Categoria)
admin.site.register(GraduacionAlcoholica)
admin.site.register(Servicio)
admin.site.register(Bar)
admin.site.register(Usuario)
admin.site.register(Barril)
admin.site.register(TipoServicio)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Chopera)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'servicio', 'total')  # 👈 Aquí agregás 'fecha'
    readonly_fields = ('fecha',)  # 👈 Opcional, para que se vea como solo lectura