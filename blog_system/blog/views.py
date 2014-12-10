# Create your views here.
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from .models import Blog, comentarios, rating  # poner tag si se necesita, en el blog tag=blog.tag.all(), 'tag':tag
from django.shortcuts import render_to_response
from forms import ComentarioForm, ContactForm, ratingForm, LoginForm
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models import Sum, Count
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def base(request):
    Descripcion = settings.SITE_DESCRIPTION
    Locale = settings.SITE_LOCALE
    Type = settings.SITE_TYPE
    Title = settings.SITE_TITLE
    Url = settings.SITE_URL
    Image = settings.SITE_IMAGE
    return TemplateResponse(request, "base.html")


def home(request):
    cate = Blog.categoria.all()
    # filtramos los blogs para no enviar todo a la pagina ordenamos 'time' para enviar los mas recientes
    
    try:
        a= Blog.objects.filter(position=1,status='P')[1].pk
        b=Blog.objects.get(id=a)
        b.position='3'
        b.save()
    except:
        pass
    blogsP1 = Blog.objects.filter(status='P', position='1').order_by('-time')[:1]
    blogsP2 = Blog.objects.filter(status='P', position='2').order_by('-time')[:4]
    blogsP3 = Blog.objects.filter(status='P', position='3').order_by('-time')[:3]
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]
    return TemplateResponse(request, "home.html", {'blogsP1': blogsP1, 'blogsP2': blogsP2, 'blogsP3': blogsP3,
                                                   'blogsRecientes': blogsRecientes, 'cate': cate})
def blogs(request, pagina):
    cate = Blog.categoria.all()
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]

    Lista= Blog.objects.filter(status='P').order_by('-time')
    paginator = Paginator(Lista,3)
    try:
        page = int(pagina)
    except:
        page = 1
    try:
        blogspaginados= paginator.page(page)
    except(EmptyPage, InvalidPage):
        blogspaginados = paginator.page(paginator.num_pages)

    return TemplateResponse(request, "blogs.html", {'blogspaginados':blogspaginados, 'blogsRecientes': blogsRecientes, 'cate': cate})



def blog(request, id_blog):
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]
    blog = get_object_or_404(Blog, id=id_blog)
    cate = Blog.categoria.all()
    numCalifblog = rating.objects.filter(Blog=id_blog).aggregate(Count('Blog')).values()[0]

    sumCalifblog = rating.objects.filter(Blog=blog.id).aggregate(Sum('calificacion')).values()[0]

    if sumCalifblog > 0:
        numStarsblog = (sumCalifblog)/numCalifblog
        Star = [i + 1 for i in range(numStarsblog)]
    else:
        Star = [i + 1 for i in range(0)]

    if blog.comentar:
        comenta = comentarios.objects.filter(Blog=blog.id).order_by('fecha_pub').reverse()[:5]
        if request.method == "POST":
            form = ComentarioForm(request.POST)
            formR = ratingForm(request.POST)
            if formR.is_valid():
                calificacion= formR.cleaned_data['calificacion']
                ctR = rating()
                ctR.Blog = Blog.objects.get(id=id_blog)
                ctR.calificacion = calificacion
                ctR.save()
            # info = 'inicializando'
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                cuerpo = form.cleaned_data['cuerpo']
                ct = comentarios()
                ct.nombre = nombre
                ct.Blog = Blog.objects.get(id=id_blog)
                ct.cuerpo = cuerpo
                ct.save()
                # info = 'se guardo satisfactoriamente'
                return TemplateResponse(request, "blog.html", {'form':ComentarioForm(),'ct': ct, 'id_blog': id_blog, 'blog': blog, 'cate': cate,
                                                               'blogsRecientes': blogsRecientes, 'comentarios': comenta, 'Star': Star})
            # else:
            # info = ' informacion con datos incorrectos'
            form = ComentarioForm()
            ctx = {'form': form, 'id_blog': id_blog, 'blog': blog, 'cate': cate, 'blogsRecientes': blogsRecientes,
                   'comentarios': comenta, 'Star': Star}
            return render_to_response('blog.html', ctx, context_instance=RequestContext(request))
        else:
            form = ComentarioForm()
            ctx = {'form': form, 'id_blog': id_blog, 'blog': blog, 'cate': cate, 'blogsRecientes': blogsRecientes,
                   'comentarios': comenta, 'Star': Star}
        return render_to_response('blog.html', ctx, context_instance=RequestContext(request))
    else:
        comenta = ''
    return TemplateResponse(request, "blog.html",
                            {'blog': blog, 'cate': cate, 'blogsRecientes': blogsRecientes, 'comentarios': comenta, 'Star': Star})


def categorias(request, id_categoria):
    blogsCategoria = Blog.objects.filter(status='P', categoria=id_categoria).order_by('-time')
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]
    cate = Blog.categoria.all()
    return TemplateResponse(request, "categorias.html",
                            {'cate': cate, 'blogsCategoria': blogsCategoria,'blogsRecientes': blogsRecientes})


def demo(request):
    cate = Blog.categoria.all()
    return TemplateResponse(request, "demo.html", {'blogs': Blog.objects.all(), 'cate': cate})


def contacto_view(request):
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]
    cate = Blog.categoria.all()
    info_enviado = False  # definir si se envio la informacion
    email = ""
    titulo = ""
    texto = ""

    if request.method == "POST":
        formulario = ContactForm(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['Email']
            titulo = formulario.cleaned_data['Titulo']
            texto = formulario.cleaned_data['Texto']

            # enviando gmail
            to_admin = 'pruebashordeipi@gmail.com'
            html_content = "Informacion recibida <br><br><br>***Mensaje**<br><br>%s" % (texto)
            msg = EmailMultiAlternatives('correo de contacto', html_content, 'from@server.com', [to_admin])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    else:
        formulario = ContactForm()
    ctx = {'form': formulario, 'email': email, 'titulo': titulo, 'texto': texto, 'info_enviado': info_enviado,
           'blogsRecientes': blogsRecientes, 'cate': cate}
    return render_to_response('contacto.html', ctx, context_instance=RequestContext(request))


def busqueda(request):
    cate = Blog.categoria.all()
    blogsRecientes = Blog.objects.filter(status='P').order_by('-time')[:4]
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(title__icontains=query)|
            Q(perex__icontains=query)|
            Q(content__icontains=query)
        )
        results = Blog.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("busqueda.html", {"results": results, "query": query, 'cate':cate, 'blogsRecientes':blogsRecientes})


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        usuario = form.cleaned_data['username']
        password = form.cleaned_data['password']
        usuario = authenticate(username=usuario, password=password)
        if usuario is not None and usuario.is_active:
            login(self.request, usuario)
        return super(LoginView, self).form_valid(form)


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')