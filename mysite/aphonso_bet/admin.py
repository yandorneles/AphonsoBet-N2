from django.contrib import admin

from .models import Aposta, Campeonato, CampeonatoTime, Carteira, Esporte, Jogo, Moeda, MovimentacoesFinanceiras, Time

class ApostaAdmin(admin.ModelAdmin):
    model = Aposta
    list_display = (
        'usuario',
        'jogo',
        'valor_aposta',
        'total_premio',
        'resultadoCasa',
        'resultadoFora',
        'quitado',
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class CampeonatoAdmin(admin.ModelAdmin):
    model = Campeonato
    list_display = (
        'descricao',
        'regiao',
        'ano',
        'esporte',
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class CampeonatoTimeAdmin(admin.ModelAdmin):
    model = CampeonatoTime
    list_display = (
        'campeonato',
        'time',
    )

class CarteiraAdmin(admin.ModelAdmin):
    model = Carteira
    list_display = (
        'usuario',
        'saldo',
        'moeda',
        'banco',
        'agencia',
        'conta',
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class EsporteAdmin(admin.ModelAdmin):
    model = Esporte
    list_display = (
        "descricao",
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class JogoAdmin(admin.ModelAdmin):
    model = Jogo
    list_display = (
        'campeonato',
        'timeCasa',
        'fatorCasa',
        'timeFora',
        'fatorFora',
        'dataEHora',
        'local',
        'resultadoCasa',
        'resultadoFora',
        'finalizado',
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class MoedaAdmin(admin.ModelAdmin):
    model = Moeda
    list_display = (
        'nome',
        'acronimo',
        'simbolo',
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class MovimentacoesFinanceirasAdmin(admin.ModelAdmin):
    model = MovimentacoesFinanceiras
    list_display = (
        'tipo',
        'valor',
        'moeda',
        'remetente',
        'destinatario',
        "criado_por",
        "criado_em",
        "alterado_em"
    )

class TimeAdmin(admin.ModelAdmin):
    model = Time
    list_display = (
        'nome',
        'bandeira',
        'acronimo',
        'pais',
        'esporte',
        "criado_por",
        "criado_em",
        "alterado_em"
    )


admin.site.register(Aposta, ApostaAdmin)
admin.site.register(Campeonato, CampeonatoAdmin)
admin.site.register(CampeonatoTime, CampeonatoTimeAdmin)
admin.site.register(Carteira, CarteiraAdmin)
admin.site.register(Esporte, EsporteAdmin)
admin.site.register(Jogo, JogoAdmin)
admin.site.register(Moeda, MoedaAdmin)
admin.site.register(MovimentacoesFinanceiras, MovimentacoesFinanceirasAdmin)
admin.site.register(Time, TimeAdmin)
