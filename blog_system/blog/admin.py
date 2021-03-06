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
    prepopulated_fields = {'slug':('title',)}
    form = BlogAdminForm
    list_display = ('slug', 'status', 'position', 'comentar','time')
    list_filter = ['time']


class ComentariosAdmin(admin.ModelAdmin):
    list_display = ('Blog', 'nombre', 'cuerpo')
    list_filter = ['fecha_pub']


class RatingAdmin(admin.ModelAdmin):
    list_display = ('Blog', 'calificacion')


admin.site.register(Categorias)
admin.site.register(Blog, BlogAdmin, )
admin.site.register(comentarios, ComentariosAdmin)
admin.site.register(rating, RatingAdmin)
