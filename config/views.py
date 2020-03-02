from django.shortcuts import redirect
from django.urls import reverse

def redirect_view(request):
    response = redirect(reverse('trabajo_final_grado:index'))
    return response