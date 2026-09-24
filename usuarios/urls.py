from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Ruta raíz
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('empleado/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleado/editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
]