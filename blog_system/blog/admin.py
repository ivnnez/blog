from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from .models import Blog, comentarios, rating, Categorias

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='full_ckeditor'))
    perex = forms.CharField(widget=CKEditorWidget(config_name='basic_ckeditor'))

    class Meta:
        model = Blog


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

admin.site.register(Categorias)
admin.site.register(Blog, BlogAdmin)
admin.site.register(comentarios)
admin.site.register(rating)
