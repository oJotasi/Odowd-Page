from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Categoria(models.Model):

    nombre = models.CharField(max_length=30)
    descripcion =  models.TextField()   
    fermentacion = models.CharField(max_length=20)
    sabor = models.CharField(max_length=30)

    # el metodo se usa para mostrar su nombre cuando se muestre el objeto en el panel de administracion
    def __str__(self):
        return self.nombre
    
class GraduacionAlcoholica(models.Model):

    porcentaje = models.FloatField()

    # metodo para mostrar el porcentaje de alcohol
    def __str__(self):
        return f"{self.porcentaje}%"


#class Envasado(models.Model):
#    tipo = models.CharField(max_length=30)          # barril, lata, botella
#    volumen_ml = models.CharField(max_length=30)     # 500, 1000, 30000, 50000

#    def __str__(self):
#        return self.volumen_ml
    
class Cerveza(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    estilo = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    porcentaje_alcohol = models.ForeignKey(GraduacionAlcoholica, on_delete=models.SET_NULL, null=True)
    ibu = models.IntegerField()
    foto = models.ImageField(upload_to='catalogo/upload/img/', null=True)
    precio_litro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('cervezaInfo', args=[str(self.id)])

    def __str__(self):
        return self.nombre

class Barril(models.Model):
    cerveza = models.ForeignKey(Cerveza, on_delete=models.CASCADE, related_name='barriles')
    litros = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.litros}L - {self.cerveza.nombre}"
    
    def calcular_precio(self):
        return self.litros * self.cerveza.precio_litro
    

class TipoServicio(models.Model):  # Ej: chopera, barriles para bares
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    tipo = models.ForeignKey(TipoServicio, on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    #barril = models.ForeignKey(Barril, on_delete=models.SET_NULL, null=True)
    foto = models.ImageField(upload_to='catalogo/upload/img/', null=True)

    def __str__(self):
        return self.nombre
    
class Chopera(models.Model):
    numero = models.IntegerField(unique=True)  # Chopera 1, 2, 3
    disponible = models.BooleanField(default=True)      

    def __str__(self):
        return f"Chopera #{self.numero} - {'Disponible' if self.disponible else 'Ocupada'}"


class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_alquiler = models.DateField(default=timezone.now)  # Fecha de uso
    servicio = models.ForeignKey('Servicio', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ubicacion_entrega = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.servicio.tipo.nombre if self.servicio else 'Sin servicio'}"
    
    def actualizar_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalle.all())
        self.save()

class ReservaServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.servicio.nombre} reservado en {self.fecha}"
    

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalle')
    #cerveza = models.ForeignKey(Cerveza, on_delete=models.CASCADE)
    barril = models.ForeignKey(Barril, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


    def save(self, *args, **kwargs):
        if self.cantidad > self.barril.stock:
            raise ValueError("No hay stock suficiente.")
        self.subtotal = self.barril.litros * self.barril.cerveza.precio_litro * self.cantidad
        super().save(*args, **kwargs)
        self.barril.stock -= self.cantidad
        self.barril.save()


    def __str__(self):
        return f"{self.cantidad}x {self.barril.litros}L de {self.barril.cerveza.nombre}"



class Bar(models.Model): 
    nombre = models.CharField(max_length=30)
    lugar = models.TextField()
    hora_habre = models.TimeField()
    hora_cierra = models.TimeField()


class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=30)


