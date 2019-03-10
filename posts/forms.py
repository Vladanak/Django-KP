from django import forms


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите ФИО работника'
    }), max_length=100, min_length=3)
    specialty = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите специальность',
    }), max_length=30, min_length=1)
    plan = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите план',
    }), max_value=999999, min_value=1)
    plan_rez = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите фактической результат',
    }), max_value=999999, min_value=0)
    plan_clock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите план времени',
    }), max_value=99999, min_value=0)
    plan_clock_rez = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите фактическое отработанное время',
    }), max_value=99999, min_value=0)
    plan_defect = forms.IntegerField(widget=forms.NumberInput(attrs={
        'size': 30,
        'class': 'form-control',
        'placeholder': 'Введите количество брака',
    }), max_value=99999, min_value=0)


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'size': 30,
        'class': 'form-control search-query',
    }))
