from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

default=datetime.now

'''
% de comisión de la publicidad
'''
COMISION_PUBLICIDAD = 1

ANIOS = (
    (0, '-----'),
    (2017, '2017'),
    (2018, '2018'),
    (2019, '2019'),
    (2020, '2020'),
    (2021, '2021'),
    (2022, '2022'),
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
)
AREA_OPERATIVA = (
    (1, 'Dirección General'),
    (2, 'Finanzas'),
    (3, 'Ventas'),
)
ESQUINA_SI = (
    (0, 'No'),
    (1, 'Si'),
)
ESTADO_CIVIL = (
    (1, 'Soltero'),
    (2, 'Casado'),
    (3, 'Unión libre'),
    (4, 'Divorciado'),
)
ESTADOS = (
    (0, 'Sin Estado'),
    (1, 'Aguascalientes'),(2, 'Baja California'),(3, 'Baja California Sur'),
    (4, 'Campeche'),(5, 'Coahuila'),(6, 'Colima'),(7, 'Chiapas'),(8, 'Chihuahua'),
    (9, 'Ciudad de México'),(10, 'Durango'),(11, 'Guanajuato'),(12, 'Guerrero'),
    (13, 'Hidalgo'),(14, 'Jalisco'),(15, 'México'),(16, 'Michoacán'),(17, 'Morelos'),
    (18, 'Nayarit'),(19, 'Nuevo León'),(20, 'Oaxaca'),(21, 'Puebla'),(22, 'Querétaro'),
    (23, 'Quintana Roo'),(24, 'San Luis Potosí'),(25, 'Sinaloa'),(26, 'Sonora'),
    (27, 'Tabasco'),(28, 'Tamaulipas'),(29, 'Tlaxcala'),(30, 'Veracruz'),(31, 'Yucatán'),
    (32, 'Zacatecas'),
)
FASE = (
    (0, ''),
    (1, '1'),
    (2, '2'),
    (3, '3'),
)
GENERO = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)
GENERO_P = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)
MESES = (
    (0, '-----'),
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
    
)
MODO_PAGO = (
    (1, 'Contado'),
    (2, 'Crédito directo'),
    (4, 'Contado a crédito'),
)
PAGO = (
    ('H', 'Horas'),
    ('D', 'Diario'),
    ('S', 'Semanal'),
    ('Q', 'Quincenal'),
    ('M', 'Mensual'),
)
PERCEPCION_DEDUCCION = (
    (1, 'Percepción'),
    (-1, 'Deducción'),
)
PARENTEZCO = (
    (1, 'Madre'),
    (2, 'Padre'),
    (3, 'Abuela'),
    (4, 'Abuelo'),
    (5, 'Hijo'),
    (6, 'Hija'),
    (7, 'Nieto'),
    (8, 'Nieta'),
    (9, 'Tia'),
    (10, 'Tio'),
    (11, 'Hermano'),
    (12, 'Hermana'),
    (13, 'Otro'),
)
PUESTO = (
    (1, 'Asesor'),
    (2, 'Gerente de ventas'),
    (3, 'Director General'),
    (4, 'Personal de finanzas'),
    (5, 'Director comercial'),
)
REGIMEN = (
    (0, 'Bienes separados'),
    (1, 'Bienes mancomunados'),
)
RESP_SI_NO = (
    (0, 'No'),
    (1, 'Si'),
)
STATUS_APARTADO = (
    (1, 'Socio 1'),
    (2, 'Socio 2'),
    (3, 'Socio 3'),
)
STATUS_BIEN = (
    (1, 'Disponible'),
    (2, 'Apartado'),
    (3, 'Vendido'),
    (4, 'Reservado'),
    (9, 'Eliminado'),
)
STATUS_COMISION = (
    (0, 'Nueva'),
    (1, 'Depósito pendiente'),
    (2, 'Impresión de recibos'),
    (3, 'Terminada'),
)
STATUS_COMPRA = (
    (1, 'Nueva'),
    (2, 'Cerrada'),
    (99, 'Cancelada'),
)
STATUS_COTIZACION = (
    (1, 'Nueva'),
    (2, 'Autorizada'),
    (3, 'Capturada'),
    (4, 'Orden de Compra'),
    (99, 'Cancelada'),
)
STATUS_DEPOSITO = (
    (0, '---------'),
    (1, 'Sin confirmar'),
    (2, 'Confirmado'),
)
STATUS_FOLIO = (
    (1, 'Activo'),
    (9, 'Cancelado'),
)
STATUS_FORMA_PAGO = (
    (0, '---------'),
    (1, 'Cheque'),
    (2, 'Transferencia'),
    (3, 'Efectivo'),
)
STATUS_GESTION = (
    (1, 'Nuevo'),
    (2, 'Autorizado'),
    (3, 'Procesado'),
    (4, 'Cancelado'),
    (5, 'Baja'),
)
STATUS_GESTION_COMISION = (
    (0, 'Nueva'),
    (1, 'Depositada'),
    (2, 'Recibida'),
)
STATUS_NOMINA = (
    (1, 'Nuevo'),
    (2, 'Procesada'),
    (3, 'Cancelada'),
    (4, 'Autorizada'),
    (5, 'Baja'),
)
STATUS_OBRA = (
    (1, 'En progreso'),
    (2, 'Suspendida'),
    (3, 'Cancelada'),
    (99, 'Terminada'),
)
STATUS_ORDEN_COMPRA = (
    (1, 'Nueva'),
    (2, 'Autorizada'),
    (99, 'Cancelada'),
)
STATUS_PAGO = (
    (1, 'Vigente'),
    (2, 'Pagado'),
    (99, 'Cancelado'),
)
STATUS_PAGADO_VENCIDO = (
    (1, 'A tiempo'),
    (2, 'Vencido'),
)
STATUS_RECEPCION = (
    (1, 'Nueva'),
    (2, 'Cerrada'),
    (99, 'Cancelada'),
)
STATUS_SI_NO = (
    (1, 'Activo'),
    (2, 'Baja'),
)
STATUS_SOLICITUD = (
    (1, 'Nueva'),
    (2, 'Apartado de lote'),
    (3, 'Comprometida'),
    (4, 'Pagando a crédito'),
    (5, 'Reasignar'),
    (6, 'Terminada'), 
    (7, 'Terminada'),
    (8, 'Cancelada'),
    (9, 'Terminada'),
    (10, 'Pagando a crédito'),
    (99, 'Cancelada'),
)
STATUS_TIPO_BIEN = (
    (1, 'Lotes'),
    (2, 'Locales comerciales'),
    (3, 'Vivienda horizontal'),
    (4, 'Vivienda vertical'),
    (5, 'Consultorios'),
    (6, 'Locales comerciales y oficinas'),
    (7, 'Estacionamientos')
)
TIPO_APARTADO_MINIMO = (
    (1,'Importe minimo de apartado'),
    (2,'Porcentaje del precio de lista mínimo de apartado'),
)
TIPO_APLICA_DESCUENTO = (
    (1,'Importe de descuento por m²'),
    (2,'% de descuento por m2'),
    (3,'Importe de descuento del precio de lista'),
    (4,'% de descuento de precio de lista'),
)
TIPO_CALCULO = (
    ("C", 'Cantidad'),
    ("P", 'Porcentaje'),
)
TIPO_CLIENTE = (
    (0, 'Persona física'),
    (1, 'Persona moral'),
)
TIPO_CORREO = (
    (1, 'Empresarial'),
    (2, 'Personal'),
)
TIPO_DESCUENTO = (
    (1, 'Porcentaje'),
    (2, 'Monto'),
)
TIPO_DOCUMENTO = (
    (1, 'Credencial de elector frente'),
    (2, 'Credencial de elector reverso'),
    (3, 'Acta de matrimonio'),
    (4, 'Comprobante de domicilio'),
    (5, 'Estado de cuenta banco'),
)
TIPO_EMPLEADO = (
    ('I', 'Interno'),
    ('E', 'Externo'),
)
TIPO_ENGANCHE_MINIMO = (
    (1,'Importe mínimo de enganche'),
    (2,'Porcentaje mínimo de enganche del precio de lista')
)
TIPO_FOLIO = (
    (1, 'Recibo pago bienes'),
    (2, 'Contrato'),
    (3, 'Comisiones'),
    (4, 'Facturas'),
    (5, 'Remisiones'),
    (6, 'Mensualidades'),
)
TIPO_LOTE = (
    (1, "Regular"),
    (0, "Irregular"),
)
TIPO_PLANO = (
    (1, 'Arquitectónico'),
    (2, 'Hidráulico'),
    (3, 'Eléctrico'),
)
TIPO_PROYECTO = (
    (1, 'Lotes'),
    (2, 'Locales comerciales'),
    (3, 'Vivienda horizontal'),
    (4, 'Vivienda vertical'),
    (5, 'Consultorios'),
    (6, 'Locales comerciales y oficinas'),
)
############################################
CURRENCY_CHOICES = (
    ('MXN', 'Pesos Mexicanos'),
    ('EUR', 'Euros'),
    ('USD', 'Dólares americanos'),
)
CURRENCY_DEFAULT = 'MXN'
############################################
class Banco(models.Model, PermissionRequiredMixin):
    banco = models.CharField("Banco",max_length=100)
    abreviacion = models.CharField("Abreviación del banco",max_length=30)
    estatus_banco = models.IntegerField("Activo",choices=STATUS_SI_NO, default=1)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['banco']
        unique_together= (('banco',),)
        db_table = 'Banco'

    def __str__(self):   # para poner los nombre en los renglones
        return '%s' % (self.banco)

class Titulo(models.Model, PermissionRequiredMixin):
    nombre = models.CharField("Razón Social",max_length=80)
    rfc = models.CharField("R.F.C.",max_length=20)
    domicilio1 = models.CharField("Domicilio renglon 1",max_length=80)
    domicilio2 = models.CharField("Domicilio renglon 2",max_length=80, default=" ")
    domicilio3 = models.CharField("Domicilio renglon 3",max_length=80, default=" ")
    telefono = models.CharField("Teléfono",max_length=100, default=" ")
    correo = models.CharField("Correo",max_length=100, null=True, blank=True)
    created = models.DateTimeField("Creado", auto_now_add=True)
    modified = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Título'
        verbose_name_plural = 'Títulos'
        db_table = 'Titulo'

    def __str__(self):   # para poner los nombre en los renglones
        return '%s %s' % (self.id, self.nombre)
