from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.principal, name='principal'),

    # CRUD Setor
    path('setores/', views.SetorListView.as_view(), name='setor_list'),
    path('setores/novo/', views.SetorCreateView.as_view(), name='setor_create'),
    path('setores/<int:pk>/editar/', views.SetorUpdateView.as_view(), name='setor_update'),
    path('setores/<int:pk>/excluir/', views.SetorDeleteView.as_view(), name='setor_delete'),

    # CRUD Sala
    path('salas/', views.SalaListView.as_view(), name='sala_list'),
    path('salas/nova/', views.SalaCreateView.as_view(), name='sala_create'),
    path('salas/<int:pk>/editar/', views.SalaUpdateView.as_view(), name='sala_update'),
    path('salas/<int:pk>/excluir/', views.SalaDeleteView.as_view(), name='sala_delete'),

    # CRUD Inventário
    path('inventarios/', views.InventarioListView.as_view(), name='inventario_list'),
    path('inventarios/novo/', views.InventarioCreateView.as_view(), name='inventario_create'),
    path('inventarios/<int:pk>/editar/', views.InventarioUpdateView.as_view(), name='inventario_update'),
    path('inventarios/<int:pk>/excluir/', views.InventarioDeleteView.as_view(), name='inventario_delete'),
    path('relatorio/pdf/', views.relatorio_inventario_pdf, name='relatorio_pdf'),
    path('relatorio/csv/', views.relatorio_inventario_csv, name='relatorio_csv'),

    # CRUD Conferência
    path('conferencias/', views.ConferenciaListView.as_view(), name='conferencia_list'),
    path('conferencias/nova/', views.ConferenciaCreateView.as_view(), name='conferencia_create'),
    path('conferencias/<int:pk>/editar/', views.ConferenciaUpdateView.as_view(), name='conferencia_update'),
    path('conferencias/<int:pk>/excluir/', views.ConferenciaDeleteView.as_view(), name='conferencia_delete'),

    # Realizar Conferência
    path('conferencias/iniciar/', views.iniciar_conferencia, name='iniciar_conferencia'),
    path('conferencias/<int:pk>/realizar/', views.realizar_conferencia, name='realizar_conferencia'),
    path('conferencias/<int:conferencia_pk>/confirmar/<int:inventario_pk>/', views.confirmar_item,
         name='confirmar_item'),
]
