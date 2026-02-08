from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .validators import validate_cpf
from django.utils import timezone

# Função / Cargo
class Funcao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Função")
    salario_mensal = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Salário por função (R$)"
    )
    def __str__(self):
        return f"{self.nome} - R$ {self.salario_mensal:.2f}"
    
# Funcionário
class Funcionario(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", validators=[validate_cpf])
    endereco = models.CharField(max_length=250, verbose_name="Endereço", blank=True)
    cep = models.CharField(max_length=9, verbose_name="CEP", blank=True)
    email = models.EmailField(verbose_name="E-mail", blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True)
    funcao = models.ForeignKey(Funcao, on_delete=models.PROTECT, related_name='funcionarios')
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.nome} ({self.funcao.nome})"
    
    @property
    def salario_total(self):
        from django.db.models import Sum
        bonus = BonusPayment.objects.filter(funcionario=self).aggregate(
            total=Sum("valor")
        )["total"] or 0

        return self.salario_base + bonus

# Tipo Caixa / Tipo Produto
class TipoCaixa(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Tipo da Caixa")
    tamanho = models.CharField(max_length=20, verbose_name="Tamanho")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.tamanho}"

class TipoProduto(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Tipo de Produto")
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

# Financeiro
class Financeiro(models.Model):
    data = models.DateField(default=timezone.now)

    ano = models.PositiveIntegerField(editable=False)
    mes = models.PositiveIntegerField(editable=False)

    salario_total_funcionarios = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    frete = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refeicao_cafe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refeicao_almoco = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    contabilidade = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    inss = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['-data']

    def calcular_total(self):
        valores = [
            self.salario_total_funcionarios,
            self.frete,
            self.refeicao_cafe,
            self.refeicao_almoco,
            self.contabilidade,
            self.inss,
        ]
        return sum((v or Decimal("0.00")) for v in valores)

    def save(self, *args, **kwargs):
        # Preenche ano e mês automaticamente
        if self.data:
            self.ano = self.data.year
            self.mes = self.data.month

        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y')} - R$ {self.total}"
    
# Lavagem / Lavadores
class LavagemCarreta(models.Model):
    data = models.DateField(verbose_name="Data da Lavagem")
    carreta_ident = models.CharField(max_length=100, verbose_name="Carreta (Nome Motorista)", blank=True)
    cliente = models.ForeignKey(
        "Cliente",
        on_delete=models.PROTECT,
        related_name="lavagens_carreta",
        null=True, blank=True
    )
    TIPO_CHOICES = [
        ("sujo", "Sujo"),
        ("carga", "Por Carga"),
    ]
    tipo_lavagem = models.CharField(max_length=10, choices=TIPO_CHOICES, default="sujo")

    def __str__(self):
        return f"Carreta {self.carreta_ident} - {self.data}"
    tipo_caixa = models.ForeignKey(TipoCaixa, on_delete=models.PROTECT)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.PROTECT)
    quantidade_caixas = models.PositiveIntegerField(default=0)
    valor_por_caixa = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def valor_total(self):
        return self.quantidade_caixas * self.valor_por_caixa

class LavadorSujoEntry(models.Model):
    lavador = models.CharField(max_length=50, default="Lavador 1", editable=False)
    data = models.DateField()
    cliente = models.ForeignKey(
        "Cliente",
        on_delete=models.CASCADE,
        related_name="lavagens_sujo",
        null=True, blank=True
    )
    TIPO_CHOICES = [
        ("sujo", "Sujo"),
        ("carga", "Por Carga"),
    ]
    tipo_lavagem = models.CharField(max_length=10, choices=TIPO_CHOICES, default="sujo")

    def __str__(self):
        return f"Sujo - {self.data}"
    quantidade_caixas = models.PositiveIntegerField()
    tamanho_caixa = models.CharField(max_length=10)
    tipo_produto = models.ForeignKey(TipoProduto, on_delete=models.PROTECT)
    valor_por_caixa = models.DecimalField(max_digits=8, decimal_places=2)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def valor_total(self):
        return self.quantidade_caixas * self.valor_por_caixa

    def __str__(self):
        return f"{self.lavador} - {self.data} - {self.quantidade_caixas} caixas"

class LavadorCargaEntry(models.Model):
    lavador = models.CharField(max_length=50, default="Lavador 2", editable=False)
    data = models.DateField()
    cliente = models.ForeignKey(
        "Cliente",
        on_delete=models.CASCADE,
        related_name="lavagens_carga",
        null=True, blank=True
    )
    TIPO_CHOICES = [
        ("sujo", "Sujo"),
        ("carga", "Por Carga"),
    ]
    tipo_lavagem = models.CharField(max_length=10, choices=TIPO_CHOICES, default="carga")

    def __str__(self):
        return f"Carga - {self.data}"
    quantidade_caixas = models.PositiveIntegerField()
    q_3A = models.PositiveIntegerField(default=0)
    q_2A = models.PositiveIntegerField(default=0)
    q_1A = models.PositiveIntegerField(default=0)
    q_G = models.PositiveIntegerField(default=0)
    valor_rendido = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor que rendeu da carreta")
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def total_caixas_por_categoria(self):
        return self.q_3A + self.q_2A + self.q_1A + self.q_G

    def __str__(self):
        return f"{self.lavador} - {self.data} - {self.quantidade_caixas} caixas"

# Profile para aprovação de usuário
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Aprovado' if self.is_approved else 'Pendente'}"
    

@property
def valor_unitario(self):
    if hasattr(self, "valor_por_caixa") and self.valor_por_caixa:
        return self.valor_por_caixa
    if hasattr(self, "valor_rendido") and self.valor_rendido:
        return self.valor_rendido
    return 0

# Signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Cliente (para vincular lavagens e gerar relatórios por cliente)
class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nome


# Atualize as lavagens para incluir o cliente (adicione este campo em cada modelo de lavagem)
# Em LavagemCarreta, LavadorSujoEntry e LavadorCargaEntry:
# cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)

# Exemplo:
# cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT)


# Controle de presença dos funcionários
class Presenca(models.Model):
    STATUS_CHOICES = [
        ('P', 'Presente'),
        ('F', 'Falta'),
        ('O', 'Folga'),
    ]

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    class Meta:
        unique_together = ('funcionario', 'data')

    def __str__(self):
        return f"{self.funcionario.nome} - {self.data} - {self.get_status_display()}"


# Registro de bônus (semanal) e cesta básica (mensal)
class BonusPayment(models.Model):
    TIPOS = (
        ('semanal', 'Bônus Semanal (R$ 120,00)'),
        ('cesta', 'Cesta Básica (mensal)'),
    )

    funcionario = models.ForeignKey('Funcionario', on_delete=models.CASCADE, related_name='bonuses')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data = models.DateField(auto_now_add=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.funcionario.nome} - {self.get_tipo_display()} - R$ {self.valor}"
