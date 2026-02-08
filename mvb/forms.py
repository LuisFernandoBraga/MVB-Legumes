from django import forms
from .models import Funcionario, Funcao, Financeiro, LavagemCarreta, LavadorSujoEntry, LavadorCargaEntry, TipoCaixa, TipoProduto, Cliente
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import validate_cpf

class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao
        fields = ['nome', 'salario_mensal']

class FuncionarioForm(forms.ModelForm):
    cpf = forms.CharField(validators=[validate_cpf], max_length=14)
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'endereco', 'cep', 'email', 'telefone', 'funcao', 'ativo']

class FinanceiroForm(forms.ModelForm):
    class Meta:
        model = Financeiro
        fields = [
            'data', 'salario_total_funcionarios', 'frete',
            'refeicao_cafe', 'refeicao_almoco', 'contabilidade', 'inss'
        ]
        labels = {
            'data': 'Data do lançamento',
            'ano': 'Ano',
            'mes': 'Mês (1-12)',
            'salario_total_funcionarios': 'Salário total dos funcionários',
            'frete': 'Frete',
            'refeicao_cafe': 'Refeição - Café da manhã',
            'refeicao_almoco': 'Refeição - Almoço',
            'contabilidade': 'Contabilidade',
            'inss': 'INSS',
        }

class LavagemCarretaForm(forms.ModelForm):
    class Meta:
        model = LavagemCarreta
        fields = ['data','carreta_ident','tipo_caixa',
                  'tipo_produto','quantidade_caixas','valor_por_caixa', 
                  'cliente', 'tipo_lavagem'
        ]
    #Código para filtrar itens excluidos para que não apareçam na seleção    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_produto'].queryset = TipoProduto.objects.filter(ativo=True)
        self.fields['tipo_caixa'].queryset = TipoCaixa.objects.filter(ativo=True)

class LavadorSujoForm(forms.ModelForm):
    class Meta:
        model = LavadorSujoEntry
        fields = ['data','quantidade_caixas','tamanho_caixa',
                  'tipo_produto','valor_por_caixa', 'cliente', 'tipo_lavagem'
        ]

class LavadorCargaForm(forms.ModelForm):
    class Meta:
        model = LavadorCargaEntry
        fields = ['data','quantidade_caixas','q_3A','q_2A','q_1A','q_G',
                  'valor_rendido', 'cliente', 'tipo_lavagem'
        ]

class TipoCaixaForm(forms.ModelForm):
    class Meta:
        model = TipoCaixa
        fields = ['nome','tamanho']

class TipoProdutoForm(forms.ModelForm):
    class Meta:
        model = TipoProduto
        fields = ['nome']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "cnpj", "telefone", "email"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
# Registro de usuário
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nome (para boas-vindas)", required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")