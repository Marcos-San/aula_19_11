// ============================================
// SISTEMA DE INVENTÁRIO IFB
// script.js - Arquivo de Scripts Principal
// ============================================

'use strict';

// ========== INICIALIZAÇÃO ==========
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Sistema de Inventário IFB - Inicializado');

    // Executar funções de inicialização
    inicializarSistema();
    configurarMenuMobile();
    configurarScannerCodigoBarras();
    configurarConfirmacoes();
    configurarMensagens();
    configurarPreviewImagens();
    configurarContadorCaracteres();
    configurarValidacaoFormularios();
    configurarLoadingState();
    configurarAtalhosTeclado();
    configurarTabelasResponsivas();
    animarEstatisticas();

    console.log('✅ Todas as funcionalidades carregadas');
    console.log('💡 Atalhos disponíveis: Alt+N (Novo) | Alt+S (Salvar) | Esc (Cancelar)');
});

// ========== INICIALIZAÇÃO DO SISTEMA ==========
function inicializarSistema() {
    // Auto-focus em campos de busca
    const campoBusca = document.querySelector('input[name="codigo_patrimonio"]');
    if (campoBusca) {
        campoBusca.focus();
        campoBusca.select();
    }

    // Timestamp de carregamento
    const tempoCarregamento = performance.now();
    console.log(`⚡ Tempo de carregamento: ${tempoCarregamento.toFixed(2)}ms`);
}

// ========== MENU MOBILE ==========
function configurarMenuMobile() {
    const nav = document.querySelector('nav');

    if (!nav) return;

    // Criar botão toggle apenas em mobile
    if (window.innerWidth <= 768) {
        criarBotaoMenuMobile(nav);
    }

    // Reconfigurar ao redimensionar janela
    window.addEventListener('resize', debounce(function() {
        const btnExistente = document.querySelector('.menu-toggle');

        if (window.innerWidth <= 768 && !btnExistente) {
            criarBotaoMenuMobile(nav);
        } else if (window.innerWidth > 768 && btnExistente) {
            btnExistente.remove();
            const menu = nav.querySelector('ul');
            if (menu) menu.style.display = 'flex';
        }
    }, 250));
}

function criarBotaoMenuMobile(nav) {
    const menu = nav.querySelector('ul');
    if (!menu) return;

    const btnMenu = document.createElement('button');
    btnMenu.className = 'menu-toggle';
    btnMenu.innerHTML = '☰ Menu';
    btnMenu.setAttribute('aria-label', 'Abrir menu de navegação');
    btnMenu.setAttribute('aria-expanded', 'false');

    menu.style.display = 'none';
    nav.insertBefore(btnMenu, menu);

    btnMenu.addEventListener('click', function() {
        const isOpen = menu.style.display !== 'none';

        if (isOpen) {
            menu.style.display = 'none';
            btnMenu.innerHTML = '☰ Menu';
            btnMenu.setAttribute('aria-expanded', 'false');
        } else {
            menu.style.display = 'flex';
            btnMenu.innerHTML = '✕ Fechar';
            btnMenu.setAttribute('aria-expanded', 'true');
        }
    });
}

// ========== SCANNER DE CÓDIGO DE BARRAS ==========
function configurarScannerCodigoBarras() {
    const campoBusca = document.querySelector('input[name="codigo_patrimonio"]');

    if (!campoBusca) return;

    let buffer = '';
    let ultimaTecla = Date.now();

    // Detectar entrada de scanner (rápida) vs digitação (lenta)
    campoBusca.addEventListener('keypress', function(e) {
        const agora = Date.now();
        const deltaTime = agora - ultimaTecla;

        // Se passou mais de 100ms, reinicia o buffer (provavelmente digitação manual)
        if (deltaTime > 100) {
            buffer = '';
        }

        ultimaTecla = agora;

        // Adiciona caractere ao buffer
        if (e.key !== 'Enter') {
            buffer += e.key;
        }

        // Enter = submeter
        if (e.key === 'Enter') {
            e.preventDefault();

            // Se buffer tem mais de 3 caracteres, assume que foi scan
            if (buffer.length > 3) {
                this.value = buffer;
                console.log('📱 Scanner detectado:', buffer);
            }

            // Valida antes de submeter
            if (this.value.trim()) {
                this.form.submit();
            } else {
                mostrarNotificacao('Por favor, digite ou escaneie um código', 'warning');
                this.focus();
            }

            buffer = '';
        }
    });

    // Validação no submit
    const form = campoBusca.form;
    if (form) {
        form.addEventListener('submit', function(e) {
            const valor = campoBusca.value.trim();

            if (!valor) {
                e.preventDefault();
                mostrarNotificacao('Por favor, digite ou escaneie um código de patrimônio', 'error');
                campoBusca.focus();
            }
        });
    }

    // Focus automático após carregar
    setTimeout(() => {
        campoBusca.focus();
    }, 100);
}

// ========== CONFIRMAÇÕES ==========
function configurarConfirmacoes() {
    // Links de exclusão
    const linksExcluir = document.querySelectorAll('a[href*="excluir"], a[href*="delete"]');

    linksExcluir.forEach(link => {
        link.addEventListener('click', function(e) {
            const confirmacao = confirm('⚠️ Tem certeza que deseja excluir este item?\n\nEsta ação não pode ser desfeita.');

            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });

    // Botão de finalizar conferência
    const btnFinalizar = document.querySelector('button[name="finalizar"]');

    if (btnFinalizar) {
        btnFinalizar.addEventListener('click', function(e) {
            const confirmacao = confirm('🏁 Deseja realmente finalizar esta conferência?\n\nApós finalizar, não será possível adicionar mais itens.');

            if (!confirmacao) {
                e.preventDefault();
            }
        });
    }
}

// ========== SISTEMA DE MENSAGENS ==========
function configurarMensagens() {
    const mensagens = document.querySelectorAll('.alert');

    mensagens.forEach(mensagem => {
        // Auto-hide após 5 segundos
        const timeoutId = setTimeout(() => {
            fecharMensagem(mensagem);
        }, 5000);

        // Permite fechar clicando
        mensagem.style.cursor = 'pointer';
        mensagem.title = 'Clique para fechar';

        mensagem.addEventListener('click', function() {
            clearTimeout(timeoutId);
            fecharMensagem(this);
        });
    });
}

function fecharMensagem(mensagem) {
    mensagem.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    mensagem.style.opacity = '0';
    mensagem.style.transform = 'translateX(20px)';

    setTimeout(() => {
        mensagem.remove();
    }, 500);
}

function mostrarNotificacao(texto, tipo = 'info') {
    const messagesContainer = document.querySelector('.messages') || criarContainerMensagens();

    const tiposClasse = {
        'success': 'alert-success',
        'error': 'alert-error',
        'warning': 'alert-warning',
        'info': 'alert-info'
    };

    const alert = document.createElement('div');
    alert.className = `alert ${tiposClasse[tipo] || 'alert-info'}`;
    alert.textContent = texto;
    alert.style.cursor = 'pointer';

    messagesContainer.appendChild(alert);

    // Auto-hide
    setTimeout(() => fecharMensagem(alert), 5000);

    // Fechar ao clicar
    alert.addEventListener('click', () => fecharMensagem(alert));
}

function criarContainerMensagens() {
    const container = document.createElement('div');
    container.className = 'messages';

    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(container, main.firstChild);
    }

    return container;
}

// ========== PREVIEW DE IMAGENS ==========
function configurarPreviewImagens() {
    const inputsImagem = document.querySelectorAll('input[type="file"]');

    inputsImagem.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (!file) return;

            // Validar tipo de arquivo
            if (!file.type.startsWith('image/')) {
                mostrarNotificacao('Por favor, selecione apenas arquivos de imagem', 'warning');
                this.value = '';
                return;
            }

            // Validar tamanho (máx 5MB)
            if (file.size > 5 * 1024 * 1024) {
                mostrarNotificacao('Imagem muito grande. Tamanho máximo: 5MB', 'error');
                this.value = '';
                return;
            }

            // Remove preview anterior
            const previewAntigo = this.parentElement.querySelector('.image-preview');
            if (previewAntigo) previewAntigo.remove();

            // Cria preview
            const reader = new FileReader();

            reader.onload = function(e) {
                const preview = document.createElement('div');
                preview.className = 'image-preview';
                preview.style.cssText = 'margin-top: 1rem; text-align: center;';

                preview.innerHTML = `
                    <img src="${e.target.result}"
                         alt="Preview da imagem"
                         style="max-width: 100%; max-height: 400px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <p style="margin-top: 0.75rem; color: #27ae60; font-weight: 600;">
                        ✓ Imagem carregada: ${file.name} (${formatarTamanho(file.size)})
                    </p>
                `;

                input.parentElement.appendChild(preview);
            };

            reader.readAsDataURL(file);
        });
    });
}

function formatarTamanho(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const tamanhos = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + tamanhos[i];
}

// ========== CONTADOR DE CARACTERES ==========
function configurarContadorCaracteres() {
    const textareas = document.querySelectorAll('textarea');

    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');

        if (!maxLength) return;

        // Cria contador
        const contador = document.createElement('div');
        contador.className = 'char-counter';
        contador.style.cssText = 'text-align: right; font-size: 0.85rem; color: #7f8c8d; margin-top: 0.5rem; font-weight: 500;';

        // Função de atualização
        const atualizarContador = () => {
            const atual = textarea.value.length;
            const restante = maxLength - atual;
            const percentual = (atual / maxLength) * 100;

            contador.textContent = `${atual} / ${maxLength} caracteres`;

            // Mudar cor conforme limite
            if (percentual >= 95) {
                contador.style.color = '#e74c3c';
                contador.style.fontWeight = '700';
            } else if (percentual >= 80) {
                contador.style.color = '#f39c12';
                contador.style.fontWeight = '600';
            } else {
                contador.style.color = '#7f8c8d';
                contador.style.fontWeight = '500';
            }
        };

        textarea.parentElement.appendChild(contador);
        textarea.addEventListener('input', atualizarContador);

        // Inicializar
        atualizarContador();
    });
}

// ========== VALIDAÇÃO DE FORMULÁRIOS ==========
function configurarValidacaoFormularios() {
    const formularios = document.querySelectorAll('form');

    formularios.forEach(form => {
        form.addEventListener('submit', function(e) {
            const camposObrigatorios = form.querySelectorAll('[required]');
            let valido = true;
            let primeiroInvalido = null;

            camposObrigatorios.forEach(campo => {
                if (!campo.value.trim()) {
                    valido = false;

                    // Adiciona classe de erro
                    campo.style.borderColor = '#e74c3c';
                    campo.style.backgroundColor = '#fee';

                    if (!primeiroInvalido) {
                        primeiroInvalido = campo;
                    }

                    // Remove destaque após 3 segundos
                    setTimeout(() => {
                        campo.style.borderColor = '';
                        campo.style.backgroundColor = '';
                    }, 3000);
                }
            });

            if (!valido) {
                e.preventDefault();
                mostrarNotificacao('Por favor, preencha todos os campos obrigatórios', 'error');

                if (primeiroInvalido) {
                    primeiroInvalido.focus();
                    primeiroInvalido.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });

        // Remover validação ao digitar
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                this.style.borderColor = '';
                this.style.backgroundColor = '';
            });
        });
    });
}

// ========== LOADING STATE EM BOTÕES ==========
function configurarLoadingState() {
    const formularios = document.querySelectorAll('form');

    formularios.forEach(form => {
        form.addEventListener('submit', function() {
            const botao = form.querySelector('button[type="submit"], input[type="submit"]');

            if (!botao) return;

            const textoOriginal = botao.textContent || botao.value;

            botao.disabled = true;
            botao.style.opacity = '0.7';
            botao.style.cursor = 'wait';

            if (botao.tagName === 'BUTTON') {
                botao.innerHTML = '⏳ Processando...';
            } else {
                botao.value = '⏳ Processando...';
            }

            // Fallback - restaura após 10 segundos
            setTimeout(() => {
                botao.disabled = false;
                botao.style.opacity = '';
                botao.style.cursor = '';

                if (botao.tagName === 'BUTTON') {
                    botao.textContent = textoOriginal;
                } else {
                    botao.value = textoOriginal;
                }
            }, 10000);
        });
    });
}

// ========== ATALHOS DE TECLADO ==========
function configurarAtalhosTeclado() {
    document.addEventListener('keydown', function(e) {
        // Alt + N = Novo registro
        if (e.altKey && e.key.toLowerCase() === 'n') {
            e.preventDefault();
            const btnNovo = document.querySelector('a[href*="nova"], a[href*="novo"], .add-button');

            if (btnNovo) {
                btnNovo.click();
                console.log('⌨️ Atalho: Novo registro');
            }
        }

        // Alt + S = Salvar formulário
        if (e.altKey && e.key.toLowerCase() === 's') {
            e.preventDefault();
            const form = document.querySelector('form');

            if (form) {
                form.requestSubmit();
                console.log('⌨️ Atalho: Salvar formulário');
            }
        }

        // Esc = Cancelar/Voltar
        if (e.key === 'Escape') {
            const btnCancelar = document.querySelector('form a, .btn-secondary');

            if (btnCancelar) {
                btnCancelar.click();
                console.log('⌨️ Atalho: Cancelar');
            }
        }

        // Ctrl + K = Focar em busca (se existir)
        if (e.ctrlKey && e.key.toLowerCase() === 'k') {
            e.preventDefault();
            const campoBusca = document.querySelector('input[type="search"], input[name="codigo_patrimonio"]');

            if (campoBusca) {
                campoBusca.focus();
                campoBusca.select();
                console.log('⌨️ Atalho: Busca focada');
            }
        }
    });
}

// ========== TABELAS RESPONSIVAS ==========
function configurarTabelasResponsivas() {
    const tabelas = document.querySelectorAll('table');

    tabelas.forEach(tabela => {
        // Verifica se já não está em container
        if (tabela.parentElement.classList.contains('table-container')) return;

        // Cria wrapper para scroll horizontal
        const wrapper = document.createElement('div');
        wrapper.className = 'table-container';

        tabela.parentNode.insertBefore(wrapper, tabela);
        wrapper.appendChild(tabela);
    });
}

// ========== ANIMAÇÃO DE ESTATÍSTICAS ==========
function animarEstatisticas() {
    const cards = document.querySelectorAll('.card p');

    cards.forEach(card => {
        const valorFinal = parseInt(card.textContent);

        if (isNaN(valorFinal)) return;

        let valorAtual = 0;
        const duracao = 1500; // 1.5 segundos
        const incrementos = 60;
        const incremento = valorFinal / incrementos;
        const intervaloTempo = duracao / incrementos;

        card.textContent = '0';

        const intervalo = setInterval(() => {
            valorAtual += incremento;

            if (valorAtual >= valorFinal) {
                card.textContent = valorFinal;
                clearInterval(intervalo);
            } else {
                card.textContent = Math.floor(valorAtual);
            }
        }, intervaloTempo);
    });
}

// ========== UTILITÁRIOS ==========

// Debounce - evita execução excessiva de funções
function debounce(func, wait) {
    let timeout;

    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };

        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle - limita execução de funções
function throttle(func, limit) {
    let inThrottle;

    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Scroll suave para elemento
function scrollSuave(elemento) {
    if (elemento) {
        elemento.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// ========== BUSCA EM TEMPO REAL (OPCIONAL) ==========
function configurarBuscaTabela() {
    const inputBusca = document.querySelector('input[type="search"].table-search');

    if (!inputBusca) return;

    const tabela = inputBusca.closest('.table-container')?.querySelector('table');
    if (!tabela) return;

    inputBusca.addEventListener('input', debounce(function() {
        const termo = this.value.toLowerCase();
        const linhas = tabela.querySelectorAll('tbody tr');

        linhas.forEach(linha => {
            const texto = linha.textContent.toLowerCase();
            linha.style.display = texto.includes(termo) ? '' : 'none';
        });
    }, 300));
}

// ========== TOOLTIP SIMPLES ==========
function configurarTooltips() {
    const elementosComTitulo = document.querySelectorAll('[title]');

    elementosComTitulo.forEach(elemento => {
        let tooltip = null;

        elemento.addEventListener('mouseenter', function() {
            const titulo = this.getAttribute('title');

            if (!titulo) return;

            tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = titulo;
            tooltip.style.cssText = `
                position: fixed;
                background: #2c3e50;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                font-size: 0.875rem;
                z-index: 10000;
                pointer-events: none;
                white-space: nowrap;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            `;

            document.body.appendChild(tooltip);

            this.removeAttribute('title');
            this.dataset.originalTitle = titulo;
        });

        elemento.addEventListener('mousemove', function(e) {
            if (tooltip) {
                tooltip.style.left = (e.pageX + 10) + 'px';
                tooltip.style.top = (e.pageY + 10) + 'px';
            }
        });

        elemento.addEventListener('mouseleave', function() {
            if (tooltip) {
                tooltip.remove();
                tooltip = null;
            }

            if (this.dataset.originalTitle) {
                this.setAttribute('title', this.dataset.originalTitle);
            }
        });
    });
}

// ========== LOG DE DEBUG ==========
console.log('%c🎯 Sistema de Inventário IFB ', 'background: #1d8348; color: white; font-size: 14px; padding: 5px 10px; border-radius: 3px;');
console.log('%cVersão: 1.0.0', 'color: #7f8c8d;');
console.log('%cDesenvolvido com Django + JavaScript', 'color: #7f8c8d;');
console.log('');
console.log('📋 Atalhos disponíveis:');
console.log('  Alt + N → Novo registro');
console.log('  Alt + S → Salvar formulário');
console.log('  Esc → Cancelar/Voltar');
console.log('  Ctrl + K → Focar em busca');

// ========== FIM DO ARQUIVO ==========