from blog_system.settings import (
    SITE_DESCRIPTION,
    SITE_LOCALE,
    SITE_TYPE,
    SITE_TITLE,
    SITE_URL,
    SITE_IMAGE,
)
from blog.models import Categorias


def blog_context_processor(request):
    context = {
        "Locale": SITE_LOCALE,
        "Type": SITE_TYPE,
        "Title": SITE_TITLE,
        "Descripcion": SITE_DESCRIPTION,
        "Url": SITE_URL,
        "Image": SITE_IMAGE,
        "categorias": Categorias.objects.all(),
    }
    return context
