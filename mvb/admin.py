from django.contrib import admin
from .models import Funcao, Funcionario, Financeiro, LavagemCarreta, LavadorSujoEntry, LavadorCargaEntry, TipoCaixa, TipoProduto, Profile
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

@admin.action(description="Aprovar usuários selecionados (cria profile.is_approved=True)")
def aprovar_usuarios(modeladmin, request, queryset):
    count = 0
    for user in queryset:
        profile = getattr(user, 'profile', None)
        if profile and not profile.is_approved:
            profile.is_approved = True
            profile.save()
            count += 1
    messages.success(request, f'{count} usuário(s) aprovados.')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    actions = [aprovar_usuarios]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Funcao)
admin.site.register(Funcionario)
admin.site.register(Financeiro)
admin.site.register(LavagemCarreta)
admin.site.register(LavadorSujoEntry)
admin.site.register(LavadorCargaEntry)
admin.site.register(TipoCaixa)
admin.site.register(TipoProduto)
admin.site.register(Profile)