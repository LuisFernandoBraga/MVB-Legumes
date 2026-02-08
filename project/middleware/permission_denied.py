from django.shortcuts import redirect
from django.contrib import messages

class PermissionDeniedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            if "PermissionDenied" in str(type(e)):
                messages.error(request, "Você não tem permissão para acessar este recurso.")
                return redirect("mvb_dashboard")
            raise e