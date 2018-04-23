from django.shortcuts import render
from django.http import HttpResponse
from .models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.template.loader import get_template
from django.template import Context

def mainPage(request):
    group = Pages.objects.all()
    list = ''
    for item in group:
        list = list + item.name + '<br>'
    if request.user.is_authenticated():
        message = "Logueado como " + str(request.user) + ". " + "<a href=http://localhost:8000/logout/>Logout</a><br><br>"
    else:
        message = "Usuario no logueado. " + "<a href=http://localhost:8000/authenticate/>Login</a><br><br>"
    return HttpResponse(message +
    "La lista de recursos disponibles es la siguiente:<br><br>" +
    list + '<br>'
    "Un ejemplo de cómo pedir un recurso es: "
    "http://localhost:8000/pepito<br><br>"
    "Si pides un recurso que no existe, la página te lo indicará")

@csrf_exempt
def getPage(request, text):
    if request.user.is_authenticated():
        message = "Logueado como " + str(request.user) + ". " + "<a href=http://localhost:8000/logout/>Logout</a><br><br>"
    else:
        message = "Usuario no logueado. " + "<a href=http://localhost:8000/authenticate/>Login</a><br><br>"
    if request.method == "GET":
        try:
            object = Pages.objects.get(name = text)
            return HttpResponse(message + object.page)
        except Pages.DoesNotExist:
            return HttpResponse(message + "No hay una página para " + text)
    else:
        if request.user.is_authenticated():
            try:
                object = Pages.objects.get(name = text)
                object.page = request.body.decode("utf-8")
                object.save()
                return HttpResponse(message + "Página actualizada")
            except Pages.DoesNotExist:
                page = Pages(name = text, page = request.body.decode("utf-8"))
                page.save()
                return HttpResponse(message + "Nueva página creada")
        else:
            return HttpResponse(message + "Para crear una página primero debes loguearte.")

def getPageTemplate(request, text):
    template = get_template('template.html')
    if request.user.is_authenticated():
        message = "Logueado como " + str(request.user) + "."
        link = "<a href=http://localhost:8000/logout/>Logout</a>"
    else:
        message = "Usuario no logueado."
        link = "<a href=http://localhost:8000/authenticate/>Login</a>"
    if request.method == "GET":
        try:
            object = Pages.objects.get(name = text)
            return HttpResponse(template.render(Context({'message': message, 'link': link, 'page': object.page})))
        except Pages.DoesNotExist:
            return HttpResponse(template.render(Context({'message': message, 'link': link, 'page': "No hay una página para " + text})))

def loginPage(request):
    return HttpResponse("""<form action='/login/' method='post'>
    Usuario:<br>
    <input type='text' name='Usuario' value=''>
    <br>
    Contraseña:<br>
    <input type='password' name='Contraseña' value=''>
    <br><br>
    <input type='submit' value='Login'>
    </form>""")

@csrf_exempt
def loginView(request):
    username = request.POST['Usuario']
    password = request.POST['Contraseña']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("<meta http-equiv='refresh' content='3;url=http://localhost:8000/'>"
        "Login realizado correctamente, redirigiéndote a la página principal...")
    else:
        return HttpResponse("<meta http-equiv='refresh' content='3;url=http://localhost:8000/authenticate/'>"
        "Login erróneo, redirigiéndote a la página de login...")

def logoutView(request):
    logout(request)
    return HttpResponse("<meta http-equiv='refresh' content='3;url=http://localhost:8000/'>"
    "Logout realizado correctamente, redirigiéndote a la página principal...")
