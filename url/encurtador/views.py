from django.forms import DateField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from url.encurtador.models import UrlLog, UrlRedirect
from collections import Counter
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import datetime, timedelta

# Create your views here.


def redirecionar(request, slug):
    try:
        Url_obj = UrlRedirect.objects.get(slug=slug)
    except UrlRedirect.DoesNotExist:
        return HttpResponse(f'O slug {slug.upper()} não foi encontrado')

    UrlLog.objects.create(
        origem=request.META.get('HTTP_REFERER'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
        host=request.META.get('HTTP_HOST'),
        ip=request.META.get('REMOTE_ADDR'),
        url_redirect=Url_obj

    )
    return redirect(Url_obj.destino)


def relatorios(request, slug):
    try:
        Url_obj = UrlRedirect.objects.get(slug=slug)
    except UrlRedirect.DoesNotExist:
        return HttpResponse(f'O slug {slug.upper()} não foi encontrado')
    else:
        reduzido = request.build_absolute_uri(f'/{slug}')
        data_inicial = datetime.today() - timedelta(days=7)
        # Renzo
        redirecionamentos_por_data = list(UrlRedirect.objects.filter(
            slug=slug
            ).annotate(
                data = TruncDate('logs__criado_em')
            ).filter(
                data__gt = data_inicial
            ).annotate(
                cliques = Count('data')
            ).order_by('data')
        )
        
        total_cliques = sum(r.cliques for r in redirecionamentos_por_data)

        # hgf
        """
        legenda = []
        data_inicial = datetime.today() - timedelta(days=6)

        lista = UrlLog.objects.filter(
            url_redirect=Url_obj, criado_em__gt=data_inicial)
        lista = [x.criado_em.day for x in lista]
        lista = list(dict(Counter(lista)).values())

        for _ in range(7):
            legenda.append(data_inicial.day)
            data_inicial += timedelta(days=1)
        """

        contexto = {'original': Url_obj.destino,
                    'reduzido': reduzido,
                    'redirecionamentos': redirecionamentos_por_data,
                    'total_cliques': total_cliques
                    }
        return render(request, 'encurtador/relatorio.html', context=contexto)
