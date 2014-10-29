from django.db import models
from taggit_autosuggest.managers import TaggableManager

class categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __unicode__(self):
        return self.nombre


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


class Blog(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    perex = models.TextField()
    content = models.TextField()
    imagen = models.ImageField(upload_to='photos')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)
    categoria = models.ManyToManyField(categoria, null=True, blank=True)
    comentar = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('blog', [self.slug])

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-time']


class comentarios(models.Model):
    nombre = models.CharField(max_length=200)
    cuerpo = models.TextField()
    fecha_pub = models.DateTimeField(auto_now_add=True)
    Blog = models.ForeignKey(Blog)

    def __unicode__(self):
        return "%s --> Lo hizo %s --> Hora:  %s" % ( self.Blog, self.nombre, self.fecha_pub)


