from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # auth
    path('login/', auth_views.LoginView.as_view(template_name='mvb/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='mvb/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='mvb/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='mvb/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='mvb/password_reset_complete.html'), name='password_reset_complete'),

    # registro / aprovação
    path('register/', views.register_request, name='register'),
    path('pedidos_pendentes/', views.lista_pedidos_pendentes, name='lista_pedidos_pendentes'),
    path('aprovar_usuario/<int:user_id>/', views.aprovar_usuario, name='aprovar_usuario'),

    # dashboard
    path('', views.mvb_dashboard, name='mvb_dashboard'),

    # export
    path('export/excel/<str:periodo>/', views.export_relatorio_excel, name='export_excel'),
    path('export/pdf/<str:periodo>/', views.export_relatorio_pdf, name='export_pdf'),

    # Funções / Funcionários
    path('funcoes/', views.lista_funcoes, name='lista_funcoes'),
    path('funcoes/nova/', views.nova_funcao, name='nova_funcao'),
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('funcionarios/novo/', views.novo_funcionario, name='novo_funcionario'),
    path('funcionarios/editar/<int:pk>/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/deletar/<int:pk>/', views.deletar_funcionario, name='deletar_funcionario'),

    #Produtos/Caixas
    path('tipos-caixa/', views.lista_tipos_caixa, name='lista_tipos_caixa'),
    path('tipos-caixa/novo/', views.criar_tipo_caixa, name='criar_tipo_caixa'),
    path('tipos-caixa/excluir/<int:pk>/', views.excluir_tipo_caixa, name='excluir_tipo_caixa'),

    path('tipos-produto/', views.lista_tipos_produto, name='lista_tipos_produto'),
    path('tipos-produto/novo/', views.criar_tipo_produto, name='criar_tipo_produto'),
    path('tipos-produto/excluir/<int:pk>/', views.excluir_tipo_produto, name='excluir_tipo_produto'),

    # Lavagens
    path('lavagens/', views.lista_lavagens, name='lista_lavagens'),
    path('lavagens/nova/', views.nova_lavagem, name='nova_lavagem'),
    path('lavador/sujo/', views.lista_lavador_sujo, name='lista_lavador_sujo'),
    path('lavador/sujo/novo/', views.novo_lavador_sujo, name='novo_lavador_sujo'),
    path('lavador/carga/', views.lista_lavador_carga, name='lista_lavador_carga'),
    path('lavador/carga/novo/', views.novo_lavador_carga, name='novo_lavador_carga'),
    path("lavagens/exportar/excel/", views.exportar_lavagens_excel, name="exportar_lavagens_excel"),
    path("lavagens/exportar/pdf/", views.exportar_lavagens_pdf, name="exportar_lavagens_pdf"),
    path('lavagens/<int:pk>/editar/', views.editar_lavagem, name='editar_lavagem'),
    path('lavagens/<int:pk>/excluir/', views.excluir_lavagem, name='excluir_lavagem'),

    # Financeiro
    path('financeiro/', views.lista_financeiro, name='lista_financeiro'),
    path('financeiro/adicionar/', views.adicionar_financeiro, name='adicionar_financeiro'),
    path('financeiro/novo/', views.novo_financeiro, name='novo_financeiro'),
    path('financeiro/grafico.png', views.financeiro_grafico_png, name='financeiro_grafico_png'),
    path('financeiro/exportar/pdf', views.exportar_financeiro_pdf, name='exportar_financeiro_pdf'),
    path('financeiro/exportar/excel', views.exportar_financeiro_excel, name='exportar_financeiro_excel'),
    path("financeiro/<int:pk>/editar/", views.editar_financeiro, name="editar_financeiro"),
    path("financeiro/<int:pk>/excluir/", views.excluir_financeiro, name="excluir_financeiro"),
    #path('financeiro/relatorio_finan', views.relatorio_finan, name='relatorio_finan'),

    # Relatório
    path('relatorio/<str:periodo>/', views.relatorio_periodo, name='relatorio_periodo'),

    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path("clientes/<int:pk>/editar/", views.editar_cliente, name="editar_cliente"),
    path("clientes/<int:pk>/excluir/", views.excluir_cliente, name="excluir_cliente"),

    # Presenças e bônus
    path("presencas/registrar/", views.registrar_presencas, name="registrar_presencas"),
    path('bonus/grant/', views.verificar_eligiveis_e_conceder, name='verificar_eligiveis_e_conceder'),
    path("presencas/lista/", views.lista_presencas, name="lista_presencas"),
    path("presencas/editar/<int:pk>/", views.editar_presenca, name="editar_presenca"),
    path("presencas/excluir/<int:pk>/", views.excluir_presenca, name="excluir_presenca"),
    
    # Relatório individual por cliente
    path('relatorio/cliente/<int:cliente_id>/', views.relatorio_por_cliente, name='relatorio_por_cliente'),

    # Relatório filtrado
    path("relatorios/exportar-excel/", views.exportar_excel_filtrado, name="exportar_excel_filtrado"),
    path("relatorios/exportar-pdf/", views.exportar_pdf_filtrado, 
    name="exportar_pdf_filtrado"),

    path("relatorios/", views.relatorios, name="relatorios"),
    path("relatorios/resultado/", views.resultado_relatorio, name="resultado_relatorio"),
]
