from atexit import register
from django.contrib import admin
from url.encurtador.models import UrlLog, UrlRedirect

# Register your models here.


@admin.register(UrlRedirect)
class UrlRedirectAdmin(admin.ModelAdmin):
    list_display = ('slug', 'destino', 'criado_em', 'atualizado_em')


@admin.register(UrlLog)
class UrlLogAdmin(admin.ModelAdmin):
    list_display = ('criado_em', 'origem', 'user_agent',
                    'host', 'ip', 'url_redirect')

    def has_change_permission(self, request, obj=...) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj = ...) -> bool:
        return False