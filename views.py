from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from mensajes.models import Mensaje
from django.contrib.auth.forms import UserCreationForm

# Vista para registro de usuarios
class RegistroUsuario(CreateView):
    template_name = 'registration/registro.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

# Vista para la página principal
def home_view(request):
    return render(request, 'home.html')

# Vista para crear mensajes
class CrearMensaje(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mensaje
    fields = ['destinatario', 'contenido']
    template_name = 'enviar_mensaje.html'
    success_url = reverse_lazy('mensajes_recibidos')
    permission_required = 'mensajes.crear_perm'  # Permiso para crear mensajes

    def form_valid(self, form):
        # Asignar el remitente al usuario autenticado
        form.instance.remitente = self.request.user
        return super().form_valid(form)

# Vista para listar mensajes recibidos
class MensajesRecibidos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mensaje
    template_name = 'mensajes_recibidos.html'
    permission_required = 'mensajes.ver_perm'  # Permiso para ver mensajes

    def get_queryset(self):
        # Filtrar mensajes para mostrar solo los recibidos por el usuario autenticado
        return Mensaje.objects.filter(destinatario=self.request.user)

# Vista para eliminar mensajes
class EliminarMensaje(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mensaje
    template_name = 'confirmar_eliminacion.html'
    success_url = reverse_lazy('mensajes_recibidos')
    permission_required = 'mensajes.borrar_perm'  # Permiso para eliminar mensajes

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.kwargs.get('tipo')

        # Filtrar mensajes según el tipo (recibido o enviado)
        if tipo == 'recibido':
            return queryset.filter(destinatario=self.request.user)
        elif tipo == 'enviado':
            return queryset.filter(remitente=self.request.user)
        else:
            return Mensaje.objects.none()

    def get_success_url(self):
        # Redirigir según el tipo de mensaje
        tipo = self.kwargs.get('tipo')
        if tipo == 'recibido':
            return reverse_lazy('mensajes_recibidos')
        elif tipo == 'enviado':
            return reverse_lazy('mensajes_enviados')
        else:
            return reverse_lazy('home')
