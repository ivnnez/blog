from django.db import models
from taggit_autosuggest.managers import TaggableManager
from taggit.models import TaggedItemBase, TagBase, GenericTaggedItemBase

POSITION_CHOICES = (
    (u'1', (u'Up')),
    (u'2', (u'Middle')),
    (u'3', (u'Down')),
)

STATUS_CHOICES = (
    (u'D', (u'Draft')),
    (u'P', (u'Public')),
    (u'H', (u'Hidden')),
)


class Categorias(TagBase):
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


class TaggedCategory(GenericTaggedItemBase):
    tag = models.ForeignKey(Categorias,
                            related_name="%(app_label)s_%(class)s_items")


class TaggedTag(TaggedItemBase):
    content_object = models.ForeignKey('Blog')


class Blog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    perex = models.TextField(unique=True)
    content = models.TextField()
    imagen = models.ImageField(upload_to='photos')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)
    categoria = TaggableManager(through=TaggedCategory, verbose_name="Categoria")
    categoria.rel.related_name = '+'
    comentar = models.BooleanField(default=False)
    tags = TaggableManager(through=TaggedTag)
    tags.rel.related_neme = "-"

    @models.permalink
    def get_absolute_url(self):
        return ('blog', (self.slug))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-time']


class comentarios(models.Model):
    Blog = models.ForeignKey(Blog)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    cuerpo = models.TextField(verbose_name="Comentario", max_length=80)
    fecha_pub = models.DateTimeField(auto_now_add=True, editable=False)


class rating(models.Model):
    Blog = models.ForeignKey(Blog)
    calificacion = models.IntegerField(default=0)
