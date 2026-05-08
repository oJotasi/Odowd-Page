from django import forms
from Catalogo.models import Cerveza, TipoServicio, Chopera, Barril, Servicio
from django.utils import timezone
from datetime import timedelta

class CervezaForm(forms.ModelForm):
    class Meta:
        model = Cerveza
        fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu']

PROVINCIAS = [
    ('Salta', 'Salta'),
]


class VentaForm(forms.Form):
    barril = forms.ModelChoiceField(queryset=Barril.objects.none(), label="Formato (Litros)")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")
    fecha_alquiler = forms.DateField(
        label="Fecha de alquiler",
        widget=forms.DateInput(attrs={'type': 'date'}),  # cambiamos a DateInput para usar min y max
        initial=timezone.now().date()
    )
    provincia = forms.ChoiceField(choices=PROVINCIAS, label="Provincia")
    localidad = forms.CharField(max_length=50, label="Localidad")
    direccion = forms.CharField(widget=forms.Textarea, label="Dirección exacta")

    def __init__(self, cerveza, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['barril'].queryset = Barril.objects.filter(cerveza=cerveza, stock__gt=0)

        today = timezone.now().date()
        max_day = today + timedelta(days=60)

        # Limitamos el input para que solo permita fechas dentro del rango
        self.fields['fecha_alquiler'].widget.attrs['min'] = today.isoformat()
        self.fields['fecha_alquiler'].widget.attrs['max'] = max_day.isoformat()

    def clean_fecha_alquiler(self):
        fecha = self.cleaned_data['fecha_alquiler']
        hoy = timezone.now().date()
        limite = hoy + timedelta(days=60)
        if fecha < hoy:
            raise forms.ValidationError("No podés seleccionar una fecha anterior a hoy.")
        if fecha > limite:
            raise forms.ValidationError("No podés seleccionar una fecha con más de 60 días de anticipación.")
        return fecha
    def clean(self):
        cleaned_data = super().clean()
        provincia = cleaned_data.get("provincia")
        localidad = cleaned_data.get("localidad")
        direccion = cleaned_data.get("direccion")

        ubicacion = f"{direccion}, {localidad}, {provincia}"
        cleaned_data["ubicacion_entrega"] = ubicacion  # esta será pasada a la vista

        return cleaned_data
    
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'tipo', 'precio', 'foto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

class BarrilForm(forms.ModelForm):
    class Meta:
        model = Barril
        fields = ['litros', 'stock']  

class ChoperaForm(forms.ModelForm):
    class Meta:
        model = Chopera
        fields = ['numero', 'disponible']
