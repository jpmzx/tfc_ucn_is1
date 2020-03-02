from django.urls import path, include
from trabajo_final_grado.views import (trabajos,)

app_name = 'trabajo_final_grado'

urlpatterns = [
    path('', trabajos.IndexView.as_view(), name='index'),
    path('crear/', trabajos.CreateView.as_view(), name='create'),
    path('<int:id>/gestionar_tareas/', trabajos.ManageTasksView.as_view(), name='manage_tasks'),
    path('<int:id>/eliminar/', trabajos.DeleteTrabajoView.as_view(), name='delete'),
]