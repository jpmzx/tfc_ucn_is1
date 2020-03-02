from django.shortcuts import render
from django.views.generic import View
from trabajo_final_grado import forms
from django.contrib import messages
from django.http import  HttpResponseRedirect
from django.urls import reverse
from trabajo_final_grado import models

class IndexView(View):

    def get(self, request):
        trabajos = models.TrabajoFinalGrado.objects.all()
        return render(request, 'trabajo_final_grado/trabajos/index.html', {
            'trabajos': trabajos
        })


class CreateView(View):

    template_name = 'trabajo_final_grado/trabajos/create.html'

    def get(self, request, *args, **kwargs):
        form = forms.TrabajoFinalGradoCreateForm()
        return render(request, self.template_name, {'form' : form})

    def post(self, request, *args, **kwargs):
        form = forms.TrabajoFinalGradoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trabajo final de grado creado correctamente')
            return HttpResponseRedirect(reverse('trabajo_final_grado:index'))
        else:
            messages.error(request, 'Algo salió mal')
            return render(request, self.template_name, {'form' : form })


class ManageTasksView(View):

    template_name = 'trabajo_final_grado/trabajos/manage_taks.html'

    def get(self, request, id, *args, **kwargs):
        try:
            trabajo = models.TrabajoFinalGrado.objects.get(id=id)
        except models.TrabajoFinalGrado.DoesNotExist:
            messages.error(request, 'Trabajo final no encontrado')
            return HttpResponseRedirect(reverse('trabajo_final_grado:index'))
        
        form = forms.GestionarTareaform(instance=trabajo)
        return render(request, self.template_name, {
            'form' : form,
            'trabajo': trabajo})

    def post(self, request, id, *args, **kwargs):
        try:
            trabajo = models.TrabajoFinalGrado.objects.get(id=id)
        except models.TrabajoFinalGrado.DoesNotExist:
            messages.error(request, 'Trabajo final no encontrado')
            return HttpResponseRedirect(reverse('trabajo_final_grado:index'))
        form = forms.GestionarTareaform(instance=trabajo, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea gestionada correctamente')
            return HttpResponseRedirect(reverse('trabajo_final_grado:index'))
        else:
            messages.error(request, 'Algo salió mal')
            return render(request, self.template_name, {
            'form' : form,
            'trabajo': trabajo})
        
class DeleteTrabajoView(View):

    template_name = 'trabajo_final_grado/trabajos/manage_taks.html'

    def get(self, request, id, *args, **kwargs):
        try:
            trabajo = models.TrabajoFinalGrado.objects.get(id=id)
        except models.TrabajoFinalGrado.DoesNotExist:
            messages.error(request, 'Trabajo final no encontrado')
        else:
            trabajo.delete()
            messages.success(request, 'Trabajo final de grado creado correctamente')
        return HttpResponseRedirect(reverse('trabajo_final_grado:index'))
