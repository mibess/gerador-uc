(function () {
    const VARIANTS = {
        success: {
            surface: ['border-emerald-200', 'bg-emerald-50/95'],
            icon: `
                <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>
                </svg>
            `,
            iconClass: ['text-emerald-600'],
            fallbackTitle: 'Tudo certo!'
        },
        error: {
            surface: ['border-rose-200', 'bg-rose-50/95'],
            icon: `
                <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a1 1 0 00.86 1.5h18.63a1 1 0 00.86-1.5L13.7 3.86a1 1 0 00-1.72 0z"/>
                </svg>
            `,
            iconClass: ['text-rose-600'],
            fallbackTitle: 'Algo deu errado'
        },
        neutral: {
            surface: ['border-slate-200', 'bg-white/95'],
            icon: `
                <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
            `,
            iconClass: ['text-slate-500'],
            fallbackTitle: 'Aviso'
        }
    };

    const container = document.getElementById('alert-container');
    const template = document.getElementById('alert-template');

    if (!container || !template) {
        window.AlertBanner = { show: () => {} };
        return;
    }

    const show = ({ title = '', message = '', variant = 'neutral', duration = 4000 } = {}) => {
        const variantConfig = VARIANTS[variant] || VARIANTS.neutral;
        const fragment = template.content.cloneNode(true);
        const wrapper = fragment.querySelector('[data-alert-wrapper]');
        const surface = fragment.querySelector('[data-alert-surface]');
        const iconSpot = fragment.querySelector('[data-alert-icon]');
        const titleEl = fragment.querySelector('[data-alert-title]');
        const messageEl = fragment.querySelector('[data-alert-message]');
        const closeBtn = fragment.querySelector('[data-alert-close]');

        variantConfig.surface.forEach(cls => surface.classList.add(cls));
        iconSpot.classList.add(...variantConfig.iconClass);
        iconSpot.innerHTML = variantConfig.icon;
        titleEl.textContent = title || variantConfig.fallbackTitle;
        messageEl.textContent = message;
        messageEl.classList.toggle('hidden', !message);

        let dismissed = false;
        const dismiss = () => {
            if (dismissed) return;
            dismissed = true;
            wrapper.classList.add('-translate-y-2', 'opacity-0');
            setTimeout(() => wrapper.remove(), 200);
        };

        closeBtn.addEventListener('click', dismiss);

        container.appendChild(wrapper);
        requestAnimationFrame(() => {
            wrapper.classList.remove('translate-y-4', 'opacity-0');
        });

        if (duration > 0) {
            setTimeout(dismiss, duration);
        }

        return dismiss;
    };

    window.AlertBanner = { show };
})();

function copiarUC() {
    const text = document.getElementById('uc-gerada')?.innerText;
    if (!text) return;

    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('copyButton');
        btn.innerText = "Copiado!";
        btn.style.backgroundColor = "#2ECC71";

        setTimeout(() => {
            btn.innerText = "Copiar";
            btn.style.backgroundColor = "var(--aneel-blue-light)";
        }, 2000);
    });
}

(function () {
    const form = document.getElementById('geradorForm');
    const distribuidoraInput = document.getElementById('distribuidoraInput');
    const resultWrapper = document.getElementById('result-wrapper');
    const resultContainer = document.getElementById('result-container');
    const ucSpan = document.getElementById('uc-gerada');
    const triggerButton = document.getElementById('distribuidoraButton');

    if (!form || !window.fetch || !distribuidoraInput || !resultWrapper || !resultContainer || !ucSpan) {
        return;
    }

    const submitButton = form.querySelector('button[type="submit"]');
    if (!submitButton) return;

    const defaultButtonText = submitButton.innerText.trim();

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        if (!distribuidoraInput.value) {
            triggerButton?.focus();
            triggerButton?.classList.add('ring-2', 'ring-[var(--aneel-blue-light)]');
            setTimeout(function () {
                triggerButton?.classList.remove('ring-2', 'ring-[var(--aneel-blue-light)]');
            }, 400);
            return;
        }

        // o processo é muito rápido, então apenas um leve feedback visual
        //submitButton.disabled = true;
        //submitButton.innerText = 'Gerando...';
        submitButton.classList.add('opacity-70', 'cursor-not-allowed');

        try {
            const response = await fetch('/api/gerar-uc', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ distribuidora: distribuidoraInput.value })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Não foi possível gerar o código.');
            }

            ucSpan.innerText = data.numero_uc;
            resultWrapper.classList.remove('hidden');
            resultContainer.classList.remove('opacity-100', 'translate-y-0');
            resultContainer.classList.add('opacity-0', 'translate-y-2');
            resultContainer.getBoundingClientRect();
            resultContainer.classList.remove('opacity-0', 'translate-y-2');
            resultContainer.classList.add('opacity-100', 'translate-y-0');
            resultWrapper.scrollIntoView({ behavior: 'smooth', block: 'center' });
            if (window.AlertBanner && typeof window.AlertBanner.show === 'function') {
                window.AlertBanner.show({
                    title: 'Código UC gerado',
                    message: 'Seu novo identificador está disponível logo abaixo. Copie e compartilhe quando precisar.',
                    variant: 'success'
                });
            }
        } catch (error) {
            console.error(error);
            const fallbackMessage = error.message || 'Erro ao gerar o código. Tente novamente.';
            if (window.AlertBanner && typeof window.AlertBanner.show === 'function') {
                window.AlertBanner.show({
                    title: 'Erro ao gerar o código',
                    message: fallbackMessage,
                    variant: 'error'
                });
            } else {
                alert(fallbackMessage);
            }
        } finally {
            submitButton.disabled = false;
            submitButton.innerText = defaultButtonText;
            submitButton.classList.remove('opacity-70', 'cursor-not-allowed');
        }
    });
})();

(function () {
    const dropdown    = document.getElementById('distribuidoraDropdown');
    const button      = document.getElementById('distribuidoraButton');
    const menu        = document.getElementById('distribuidoraMenu');
    const input       = document.getElementById('distribuidoraInput');
    const labelSpan   = document.getElementById('distribuidoraLabel');
    const searchInput = document.getElementById('distribuidoraSearch');

    if (!dropdown || !button || !menu || !input || !labelSpan) return;

    const optionButtons = Array.from(menu.querySelectorAll('button[data-value]'));

    const normalizar = (texto = '') =>
        texto.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

    const filtrarDistribuidoras = (termo = '') => {
        const filtro = normalizar(termo);
        optionButtons.forEach((btn) => {
            const alvo = normalizar(btn.dataset.search || btn.innerText);
            const corresponde = !filtro || alvo.includes(filtro);
            btn.classList.toggle('hidden', !corresponde);
        });
    };

    const resetFiltro = () => {
        if (searchInput) {
            searchInput.value = '';
            filtrarDistribuidoras('');
        }
    };

    const selecionarBotao = (botao) => {
        const value = botao.getAttribute('data-value');

        input.value = value;
        // Copia exatamente o layout interno do botão selecionado
        labelSpan.innerHTML = botao.innerHTML;

        optionButtons.forEach((btn) => {
            btn.classList.remove('bg-[var(--aneel-blue)]', 'text-white');
            btn.classList.add('text-slate-700', 'hover:bg-[var(--aneel-blue)]', 'hover:text-white');
        });

        botao.classList.add('bg-[var(--aneel-blue)]', 'text-white');
        botao.classList.remove('text-slate-700', 'hover:bg-[var(--aneel-blue)]', 'hover:text-white');

        menu.classList.add('hidden');
        resetFiltro();
    };

    button.addEventListener('click', function (e) {
        e.stopPropagation();
        const estavaFechado = menu.classList.contains('hidden');
        menu.classList.toggle('hidden');

        if (estavaFechado && !menu.classList.contains('hidden')) {
            resetFiltro();
            searchInput?.focus();
        }
    });

    optionButtons.forEach((item) => {
        item.addEventListener('click', function () {
            selecionarBotao(this);
        });
    });

    searchInput?.addEventListener('input', function () {
        filtrarDistribuidoras(this.value);
    });

    searchInput?.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const primeira = optionButtons.find((btn) => !btn.classList.contains('hidden'));
            primeira?.click();
        }
    });

    document.addEventListener('click', function (e) {
        if (!dropdown.contains(e.target)) {
            menu.classList.add('hidden');
            resetFiltro();
        }
    });
})();
