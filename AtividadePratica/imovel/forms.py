from django import forms
from decimal import Decimal, InvalidOperation

from .models import Corretor, Imovel, TipoImovel


class FormImovel(forms.ModelForm):
    preco = forms.CharField(
        label="Preço",
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Ex.: R$ 450.000,00",
            "inputmode": "decimal",
            "autocomplete": "off",
            "data-mask": "currency",
        }),
    )
    tipo = forms.ChoiceField(
        label="Tipo do imóvel",
        choices=[
            ("", "Selecione o tipo do imóvel"),
            *TipoImovel.choices,
        ],
    )
    finalidade = forms.ChoiceField(
        label="Finalidade",
        choices=[
            ("", "Selecione a finalidade"),
            ("Venda", "Venda"),
            ("Aluguel", "Aluguel"),
        ],
    )
    corretor = forms.ModelChoiceField(
        label="Corretor responsável",
        queryset=Corretor.objects.all(),
        empty_label="Selecione o corretor responsável",
    )

    class Meta:
        model = Imovel
        fields = [
            'titulo', 'descricao', 'tipo', 'finalidade', 'preco', 'endereco',
            'cidade', 'quantidade_quartos', 'imagem', 'corretor',
        ]
        labels = {
            'titulo': 'Título do imóvel',
            'descricao': 'Descrição',
            'tipo': 'Tipo do imóvel',
            'preco': 'Preço',
            'endereco': 'Endereço',
            'cidade': 'Cidade',
            'quantidade_quartos': 'Quantidade de quartos',
            'imagem': 'Imagem do imóvel',
            'corretor': 'Corretor responsável',
        }
        help_texts = {
            'descricao': 'Informe os principais detalhes do imóvel.',
            'preco': 'Digite o valor em reais.',
            'quantidade_quartos': 'Informe 0 para terrenos ou imóveis sem quartos.',
            'imagem': 'Formatos recomendados: JPG ou PNG.',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ex.: Casa com piscina no Gonzaga',
                'autocomplete': 'off',
            }),
            'descricao': forms.Textarea(attrs={
                'placeholder': 'Descreva os cômodos, diferenciais e localização...',
                'rows': 5,
            }),
            'endereco': forms.TextInput(attrs={
                'placeholder': 'Ex.: Rua das Flores, 123',
                'autocomplete': 'street-address',
            }),
            'cidade': forms.TextInput(attrs={
                'placeholder': 'Ex.: Santos',
                'autocomplete': 'address-level2',
            }),
            'quantidade_quartos': forms.NumberInput(attrs={
                'placeholder': 'Ex.: 3',
                'min': '0',
                'step': '1',
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }

    def clean_preco(self):
        valor = self.cleaned_data["preco"].strip()
        valor = valor.replace("R$", "").replace(" ", "")
        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")

        try:
            preco = Decimal(valor)
        except InvalidOperation as error:
            raise forms.ValidationError("Informe um preço válido.") from error

        if preco < 0:
            raise forms.ValidationError("O preço não pode ser negativo.")
        return preco


class FormCorretor(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['nome', 'email', 'telefone']
        labels = {
            'nome': 'Nome completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }
        help_texts = {
            'email': 'Usaremos este e-mail para contato profissional.',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex.: Ana Beatriz Souza',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ex.: ana@imobiliaria.com',
                'autocomplete': 'email',
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': 'Ex.: (13) 99999-9999',
                'autocomplete': 'tel',
                'inputmode': 'tel',
                'data-mask': 'phone',
            }),
        }