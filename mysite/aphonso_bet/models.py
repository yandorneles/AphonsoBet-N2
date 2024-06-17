from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import os
from uuid import uuid4

# função para alterar o nome do arquivo
# ref: https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload
def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper



class ModelAbstrato(models.Model):
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True



class Esporte(ModelAbstrato):
    descricao = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.id} {self.descricao}'

class Campeonato(ModelAbstrato):
    descricao = models.CharField(max_length=50)
    regiao = models.CharField(max_length=50)
    ano = models.IntegerField()
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.id} {self.descricao} {self.ano}'

class Time(ModelAbstrato):
    nome = models.CharField(max_length=50)
    bandeira = models.ImageField(upload_to=path_and_rename('aphonso_bet\\static\\upload'))
    acronimo = models.CharField(max_length=3)
    pais = models.CharField(max_length=50, default='BRASIL')
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.id} {self.nome}'

class CampeonatoTime(ModelAbstrato):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    
class Jogo(ModelAbstrato):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    timeCasa = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='casa')
    fatorCasa = models.FloatField(default=1)
    timeFora = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='fora')
    fatorFora = models.FloatField(default=1)
    dataEHora = models.DateTimeField()
    local = models.CharField(max_length=100)
    resultadoCasa = models.IntegerField(default = 0)
    resultadoFora = models.IntegerField(default = 0)
    finalizado = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.id} {self.campeonato} {self.timeCasa} x {self.timeFora}'

class Moeda(ModelAbstrato):
    nome = models.CharField(max_length=50)
    acronimo = models.CharField(max_length=3)
    simbolo = models.CharField(max_length=2)

    def __str__(self) -> str:
        return f'{self.id} {self.acronimo}'

class Carteira(ModelAbstrato):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proprietario')
    saldo = models.FloatField(default=50.00)
    moeda = models.ForeignKey(Moeda, on_delete=models.CASCADE)
    banco = models.CharField(max_length=50, null=True)
    agencia = models.IntegerField(null=True)
    conta =  models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return f"{self.id} {self.usuario.username}"

class MovimentacoesFinanceiras(ModelAbstrato):
    ENTRADA = 'EN'
    SAIDA = 'SA'
    TRANSFERENCIA = 'TR'
    TIPOS_MOVIMENTACOES = {
        ENTRADA: 'Entradas',
        SAIDA: 'Saídas',
        TRANSFERENCIA: 'Transferências'
    }
    tipo = models.CharField(max_length=2, choices=TIPOS_MOVIMENTACOES, default=ENTRADA)
    valor = models.FloatField()
    moeda = models.ForeignKey(Moeda, on_delete=models.CASCADE)
    remetente = models.ForeignKey(Carteira, on_delete=models.CASCADE, related_name='remetente')
    destinatario = models.ForeignKey(Carteira, on_delete=models.CASCADE, related_name='destinatario')
    
class Aposta(ModelAbstrato):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apostador')
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    valor_aposta = models.FloatField()
    total_premio = models.FloatField()
    resultadoCasa = models.IntegerField(default = 0)
    resultadoFora = models.IntegerField(default = 0)
    quitado = models.BooleanField(default=False)