from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .models import Sala, Inventario, Conferencia, ItemConferencia, Setor
from .forms import (SalaForm, InventarioForm, ConferenciaForm,
                    IniciarConferenciaForm, BuscarPatrimonioForm,
                    ConfirmarItemForm, SetorForm)
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from .models import Inventario
import csv
import openpyxl

# ========== VIEWS DE AUTENTICAÇÃO ==========
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('principal')
    else:
        form = AuthenticationForm()
    return render(request, 'meuapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ========== DASHBOARD ==========
@login_required
def principal(request):
    total_salas = Sala.objects.count()
    total_inventarios = Inventario.objects.count()
    total_conferencias = Conferencia.objects.count()
    conferencias_abertas = Conferencia.objects.filter(finalizada=False).count()

    context = {
        'total_salas': total_salas,
        'total_inventarios': total_inventarios,
        'total_conferencias': total_conferencias,
        'conferencias_abertas': conferencias_abertas,
    }
    return render(request, 'meuapp/principal.html', context)


# ========== CRUD SETOR ==========
class SetorListView(LoginRequiredMixin, ListView):
    model = Setor
    template_name = 'meuapp/setor_list.html'
    context_object_name = 'setores'


class SetorCreateView(LoginRequiredMixin, CreateView):
    model = Setor
    form_class = SetorForm
    template_name = 'meuapp/setor_form.html'
    success_url = reverse_lazy('setor_list')


class SetorUpdateView(LoginRequiredMixin, UpdateView):
    model = Setor
    form_class = SetorForm
    template_name = 'meuapp/setor_form.html'
    success_url = reverse_lazy('setor_list')


class SetorDeleteView(LoginRequiredMixin, DeleteView):
    model = Setor
    template_name = 'meuapp/setor_confirm_delete.html'
    success_url = reverse_lazy('setor_list')


# ========== CRUD SALA ==========
class SalaListView(LoginRequiredMixin, ListView):
    model = Sala
    template_name = 'meuapp/sala_list.html'
    context_object_name = 'salas'


class SalaCreateView(LoginRequiredMixin, CreateView):
    model = Sala
    form_class = SalaForm
    template_name = 'meuapp/sala_form.html'
    success_url = reverse_lazy('sala_list')


class SalaUpdateView(LoginRequiredMixin, UpdateView):
    model = Sala
    form_class = SalaForm
    template_name = 'meuapp/sala_form.html'
    success_url = reverse_lazy('sala_list')


class SalaDeleteView(LoginRequiredMixin, DeleteView):
    model = Sala
    template_name = 'meuapp/sala_confirm_delete.html'
    success_url = reverse_lazy('sala_list')


# ========== CRUD INVENTÁRIO ==========
class InventarioListView(LoginRequiredMixin, ListView):
    model = Inventario
    template_name = 'meuapp/inventario_list.html'
    context_object_name = 'inventarios'
    paginate_by = 50


class InventarioCreateView(LoginRequiredMixin, CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'meuapp/inventario_form.html'
    success_url = reverse_lazy('inventario_list')


class InventarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'meuapp/inventario_form.html'
    success_url = reverse_lazy('inventario_list')


class InventarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Inventario
    template_name = 'meuapp/inventario_confirm_delete.html'
    success_url = reverse_lazy('inventario_list')


# ========== CRUD CONFERÊNCIA ==========
class ConferenciaListView(LoginRequiredMixin, ListView):
    model = Conferencia
    template_name = 'meuapp/conferencia_list.html'
    context_object_name = 'conferencias'


class ConferenciaCreateView(LoginRequiredMixin, CreateView):
    model = Conferencia
    form_class = ConferenciaForm
    template_name = 'meuapp/conferencia_form.html'
    success_url = reverse_lazy('conferencia_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ConferenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Conferencia
    form_class = ConferenciaForm
    template_name = 'meuapp/conferencia_form.html'
    success_url = reverse_lazy('conferencia_list')


class ConferenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Conferencia
    template_name = 'meuapp/conferencia_confirm_delete.html'
    success_url = reverse_lazy('conferencia_list')


# ========== REALIZAR CONFERÊNCIA ==========
@login_required
def iniciar_conferencia(request):
    if request.method == 'POST':
        form = IniciarConferenciaForm(request.POST)
        if form.is_valid():
            sala = form.cleaned_data['sala']
            ano = form.cleaned_data['ano']

            # Criar nova conferência
            conferencia = Conferencia.objects.create(
                sala=sala,
                ano=ano,
                usuario=request.user
            )

            return redirect('realizar_conferencia', pk=conferencia.pk)
    else:
        form = IniciarConferenciaForm()

    return render(request, 'meuapp/iniciar_conferencia.html', {'form': form})


@login_required
def realizar_conferencia(request, pk):
    conferencia = get_object_or_404(Conferencia, pk=pk)

    if conferencia.finalizada:
        messages.warning(request, 'Esta conferência já foi finalizada.')
        return redirect('conferencia_list')

    if request.method == 'POST':
        if 'finalizar' in request.POST:
            conferencia.finalizada = True
            conferencia.data_fim = timezone.now()
            conferencia.save()
            messages.success(request, 'Conferência finalizada com sucesso!')
            return redirect('conferencia_list')

        form = BuscarPatrimonioForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo_patrimonio']
            try:
                inventario = Inventario.objects.get(codigo=codigo)
                return redirect('confirmar_item', conferencia_pk=conferencia.pk, inventario_pk=inventario.pk)
            except Inventario.DoesNotExist:
                messages.error(request, f'Patrimônio com código "{codigo}" não encontrado.')
    else:
        form = BuscarPatrimonioForm()

    itens_conferidos = conferencia.itens.all()

    context = {
        'conferencia': conferencia,
        'form': form,
        'itens_conferidos': itens_conferidos,
    }
    return render(request, 'meuapp/realizar_conferencia.html', context)

def relatorio_inventario_pdf(request):
    # Configura a resposta HTTP para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_inventario.pdf"'

    # Cria o PDF
    p = canvas.Canvas(response, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, altura - 50, "Relatório de Inventário")

    # Lista de itens
    p.setFont("Helvetica", 12)
    y = altura - 80
    for inventario in Inventario.objects.all():
        linha = f"{inventario.codigo} - Descrição: {inventario.descricao} - Tipo: {inventario.tipo} - Status: {inventario.status} - Sala atual: {inventario.sala_atual}"
        p.drawString(50, y, linha)
        y -= 20
        if y < 50:  # Nova página se necessário
            p.showPage()
            p.setFont("Helvetica", 12)
            y = altura - 50

    p.showPage()
    p.save()
    return response

def relatorio_inventario_csv(request):
    # Configura a resposta HTTP para CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_inventario.csv"'

    # Cria o writer CSV
    writer = csv.writer(response)

    # Cabeçalhos
    writer.writerow([
        "Codigo",
        "Descricao",
        "Tipo",
        "Status",
        "Sala Atual"
    ])

    # Linhas do relatório
    for inventario in Inventario.objects.all():
        writer.writerow([
            inventario.codigo,
            inventario.descricao,
            inventario.tipo,
            inventario.status,
            inventario.sala_atual
        ])

    return response

@login_required
def confirmar_item(request, conferencia_pk, inventario_pk):
    conferencia = get_object_or_404(Conferencia, pk=conferencia_pk)
    inventario = get_object_or_404(Inventario, pk=inventario_pk)

    # Verificar se já foi conferido
    item_existente = ItemConferencia.objects.filter(
        conferencia=conferencia,
        inventario=inventario
    ).first()

    if request.method == 'POST':
        form = ConfirmarItemForm(request.POST, request.FILES, instance=item_existente)
        if form.is_valid():
            item = form.save(commit=False)
            item.conferencia = conferencia
            item.inventario = inventario
            item.save()

            # Atualizar sala atual do inventário
            inventario.sala_atual = conferencia.sala
            inventario.save()

            messages.success(request, f'Item {inventario.codigo} conferido com sucesso!')
            return redirect('realizar_conferencia', pk=conferencia.pk)
    else:
        initial = {'status_conferido': inventario.status}
        form = ConfirmarItemForm(instance=item_existente, initial=initial)

    context = {
        'conferencia': conferencia,
        'inventario': inventario,
        'form': form,
        'ja_conferido': item_existente is not None,
    }
    return render(request, 'meuapp/confirmar_item.html', context)



