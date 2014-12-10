from django import forms
from models import comentarios, rating


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = comentarios
        fields = ('nombre', 'cuerpo')


class ContactForm(forms.Form):
    Email = forms.EmailField(widget=forms.TextInput())
    Titulo = forms.CharField(widget=forms.TextInput())
    Texto = forms.CharField(widget=forms.Textarea())


class ratingForm(forms.ModelForm):
    class Meta:
        model = rating
        fields = ('calificacion',)


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))