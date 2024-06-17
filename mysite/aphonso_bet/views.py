import os
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Jogo, Carteira, Aposta, MovimentacoesFinanceiras

def obterCarteira(user):
    carteira = None
    if user.is_authenticated:
        carteira = Carteira.objects.filter(usuario = user.id).first()
    return carteira

# Página inicial na rota raiz
def pagina_inicial(request):
    jogos = Jogo.objects.filter(finalizado = False)
    resultados = Jogo.objects.filter(finalizado = True)
    carteira = obterCarteira(request.user)
    return render(request, 'index.html', {"jogos":jogos, "resultados": resultados, "carteira":carteira})

# Página de login /login
def pagina_login(request):
    if request.user.is_authenticated:
        return redirect("pagina_inicio")

    if request.method == 'POST':
        username = request.POST["usuario"]
        password = request.POST["senha"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html', {"msg":"Usuário ou senha inválidos!"})
    else:
        return render(request, 'login.html', {"msg":""})

# Página de logout /logout
def pagina_logout(request):
    logout(request)
    return redirect("pagina_inicio")

# Página de Cadastro /cadastro
def pagina_cadastro(request):
    return render(request, 'cadastro.html', {})

# Página de apostas /apostas
def pagina_apostas(request):
    if not request.user.is_authenticated:
        return redirect("pagina_inicio")
    
    carteira = obterCarteira(request.user)
    apostas = Aposta.objects.filter(usuario = request.user.id)
    return render(request, 'apostas.html', {"carteira":carteira, "apostas":apostas})

# Página de apostar /apostar/{jogo_id}
def pagina_apostar(request, jogo_id):
    if not request.user.is_authenticated:
        return redirect("pagina_inicio")

    carteira = obterCarteira(request.user)

    if request.method == 'POST':
        jogoId = request.POST["inputJogoId"]
        timeCasaId = request.POST["inputTimeCasaId"]
        timeCasaPontos = request.POST["inputTimeCasaPontos"]
        timeForaId = request.POST["inputTimeForaId"]
        timeForaPontos = request.POST["inputTimeForaPontos"]
        valor = request.POST["inputValor"]

        usuario = User.objects.get(id = request.user.id)
        jogo = Jogo.objects.get(id = jogoId)

        total_premio = float(valor)
        if int(timeCasaPontos) > int(timeForaPontos):
            total_premio *= jogo.fatorCasa
        elif int(timeCasaPontos) < int(timeForaPontos):
            total_premio *= jogo.fatorFora    

        aposta = Aposta(
            usuario = usuario,
            jogo = jogo,
            valor_aposta = valor,
            total_premio = total_premio,
            resultadoCasa = timeCasaPontos,
            resultadoFora = timeForaPontos,
            criado_por_id = usuario.id
        )
        try:
            aposta.save()

            carteira.saldo = carteira.saldo - float(valor)
            carteira.save()

            carteira_admin = Carteira.objects.get(usuario = 1)

            movimento = MovimentacoesFinanceiras()
            movimento.valor = valor
            movimento.moeda = carteira.moeda
            movimento.remetente = carteira
            movimento.destinatario = carteira_admin
            movimento.criado_por = usuario
            movimento.save()

            return redirect('pagina_apostas')
        except Exception as e:
            print(e)
            return render(request, 'apostar.html', {"carteira":carteira, "jogo":jogo, "msg":"Não foi possível fazer a aposta!"})

    else:
        jogo = Jogo.objects.get(id=jogo_id)
        if not request.user.is_authenticated:
            return redirect("pagina_login")
        return render(request, 'apostar.html', {"carteira":carteira, "jogo":jogo, "msg":""})


def obter_upload(request, filename):
    app_folder = os.path.dirname(__file__)
    filepath = os.path.join(app_folder,'static','upload', filename)
    if not os.path.isfile(filepath):
        response = HttpResponse()
        response.status_code = 404
        return response
    ext = filename.split('.')[1]
    with open(filepath, 'rb') as file:
        return HttpResponse(file, content_type=f'image/{ext}')