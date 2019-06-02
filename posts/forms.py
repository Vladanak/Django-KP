from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите Ф.И.О. сотрудника без цифр и символов'
    }), max_length=100, min_length=3, validators=[RegexValidator(
            regex='^[A-zА-яЁё]*$',
            message=_('Username must be Alphanumeric'),
            code='invalid_username'
        )])
    specialty = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите специальность без цифр и символов',
    }), max_length=30, min_length=1, validators=[RegexValidator(
            regex='^[A-zА-яЁё]*$',
            message='Username must be Alphanumeric',
            code='invalid_username'
        )])
    plan = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите план',
    }), max_value=999999, min_value=1)
    plan_rez = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите фактической результат',
    }), max_value=999999, min_value=1)
    plan_clock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите план времени',
    }), max_value=99999, min_value=1)
    plan_clock_rez = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите фактическое отработанное время',
    }), max_value=99999, min_value=1)
    plan_defect = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите количество недочётов',
    }), max_value=99999, min_value=0)


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control search-query',
    }), validators=[RegexValidator(
            regex='^[A-zА-яЁё]*$',
            message=_('fIELD must be Alphanumeric'),
            code='invalid_username'
        )])
