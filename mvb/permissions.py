from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Acesso negado: apenas administradores.")
            return redirect('mvb_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped

def entry_allowed(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):

        # 1) Usuário não logado → bloqueia
        if not request.user.is_authenticated:
            return redirect("login")

        # 2) Admin tem acesso total
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)

        # 3) Usuário comum → precisa estar aprovado
        profile = getattr(request.user, "profile", None)
        if not profile or not profile.is_approved:
            messages.error(request, "Sua conta ainda não foi aprovada pelo administrador.")
            return redirect("mvb_dashboard")

        # 4) Se for POST → apenas criação é permitida
        if request.method == "POST":
            if "pk" in kwargs:
                messages.error(request, "Você não tem permissão para editar registros.")
                return redirect("mvb_dashboard")

        # 5) Permissão concedida
        return view_func(request, *args, **kwargs)

    return _wrapped