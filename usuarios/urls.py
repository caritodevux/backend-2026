from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Autenticación y Home
    path('', views.dashboard, name='dashboard'),  # Ruta raíz
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Módulo Administración de Personal (EVA2)
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/empleados/', views.listar_empleados, name='listar_empleados'),
    path('personal/empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('personal/empleados/<int:empleado_id>/', views.detalle_empleado, name='detalle_empleado'),
    path('personal/empleados/<int:empleado_id>/editar/', views.editar_empleado, name='editar_empleado'),
    path('personal/empleados/<int:empleado_id>/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),
]