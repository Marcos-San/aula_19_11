from django.db import models
from django.contrib.auth.models import User


class Setor(models.Model):
    nome = models.TextField()
    sigla = models.TextField(max_length=10)
    campus = models.TextField()

    class Meta:
        verbose_name_plural = "Setores"

    def __str__(self):
        return f"{self.sigla} - {self.nome}"


class Sala(models.Model):
    numero = models.IntegerField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='salas')

    class Meta:
        verbose_name_plural = "Salas"
        ordering = ['numero']

    def __str__(self):
        return f"Sala {self.numero}"


class Inventario(models.Model):
    TIPO_CHOICES = [
        ('mobiliario', 'Mobiliário'),
        ('eletrodomestico', 'Eletrodoméstico'),
        ('informatica', 'Informática'),
        ('escritorio', 'Escritório'),
        ('outros', 'Outros'),
    ]

    STATUS_CHOICES = [
        ('bom', 'Bom'),
        ('danificado', 'Danificado'),
        ('inutilizado', 'Inutilizado'),
    ]

    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código do Patrimônio")
    descricao = models.TextField(max_length=1000)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bom')
    valor_aquisicao = models.FloatField(null=True, blank=True)
    valor_depreciado = models.FloatField(null=True, blank=True)
    numero_serie = models.TextField(blank=True, null=True)
    obs = models.TextField(blank=True, null=True, verbose_name="Observações")
    sala_atual = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventarios')

    class Meta:
        verbose_name_plural = "Inventários"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Conferencia(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='conferencias')
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    ano = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    finalizada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Conferências"
        ordering = ['-data_inicio']

    def __str__(self):
        return f"Conferência {self.sala} - {self.ano} ({self.usuario.username})"


class ItemConferencia(models.Model):
    conferencia = models.ForeignKey(Conferencia, on_delete=models.CASCADE, related_name='itens')
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    status_conferido = models.CharField(max_length=20, choices=Inventario.STATUS_CHOICES)
    observacao = models.TextField(blank=True, null=True)
    imagem_observacao = models.ImageField(upload_to='observacoes/', null=True, blank=True)
    data_conferencia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Itens de Conferência"
        unique_together = ['conferencia', 'inventario']

    def __str__(self):
        return f"{self.inventario.codigo} - {self.conferencia}"

