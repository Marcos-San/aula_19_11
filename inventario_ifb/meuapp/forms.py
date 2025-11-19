from django import forms
from .models import Sala, Inventario, Conferencia, ItemConferencia, Setor

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome', 'sigla', 'campus']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control'}),
            'campus': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['numero', 'setor']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'setor': forms.Select(attrs={'class': 'form-control'}),
        }


class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['codigo', 'descricao', 'tipo', 'status', 'valor_aquisicao',
                  'valor_depreciado', 'numero_serie', 'obs', 'sala_atual']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'valor_aquisicao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_depreciado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sala_atual': forms.Select(attrs={'class': 'form-control'}),
        }


class ConferenciaForm(forms.ModelForm):
    class Meta:
        model = Conferencia
        fields = ['sala', 'ano']
        widgets = {
            'sala': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class IniciarConferenciaForm(forms.Form):
    sala = forms.ModelChoiceField(
        queryset=Sala.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Selecione a Sala"
    )
    ano = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Ano da Conferência"
    )


class BuscarPatrimonioForm(forms.Form):
    codigo_patrimonio = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite ou escaneie o código do patrimônio',
            'autofocus': True,
            'autocomplete': 'off'
        }),
        label="Código do Patrimônio"
    )


class ConfirmarItemForm(forms.ModelForm):
    class Meta:
        model = ItemConferencia
        fields = ['status_conferido', 'observacao', 'imagem_observacao']
        widgets = {
            'status_conferido': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem_observacao': forms.FileInput(attrs={'class': 'form-control'}),
        }

