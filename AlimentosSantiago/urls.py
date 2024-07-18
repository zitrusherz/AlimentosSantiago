# AlimentosSantiago/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_pedidos.urls')),  # Asegúrate de que esta línea esté correcta
    path('accounts/', include('accounts.urls')),
]
