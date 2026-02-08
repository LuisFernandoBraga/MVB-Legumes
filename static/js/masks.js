document.addEventListener('DOMContentLoaded', () => {

    // Funções de máscara reutilizáveis
    const masks = {
        cpf(value) {
            value = value.replace(/\D/g, '');
            return value
                .replace(/(\d{3})(\d)/, '$1.$2')
                .replace(/(\d{3})(\d)/, '$1.$2')
                .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        },
        cnpj(value) {
            value = value.replace(/\D/g, '');
            return value
                .replace(/^(\d{2})(\d)/, '$1.$2')
                .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
                .replace(/\.(\d{3})(\d)/, '.$1/$2')
                .replace(/(\d{4})(\d)/, '$1-$2');
        },
        cep(value) {
            value = value.replace(/\D/g, '');
            return value.replace(/(\d{5})(\d)/, '$1-$2');
        },
        telefone(value) {
            value = value.replace(/\D/g, '');
            if (value.length <= 10) {
                return value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
            }
            return value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
        },
        cartao(value) {
            value = value.replace(/\D/g, '');
            return value.replace(/(\d{4})(?=\d)/g, '$1 ');
        }
    };

    // Aplica a máscara dinamicamente
    document.querySelectorAll('[data-mask]').forEach(input => {
        const type = input.dataset.mask;

        if (masks[type]) {
            input.addEventListener('input', e => {
                const cursor = e.target.selectionStart;
                const oldLength = e.target.value.length;

                e.target.value = masks[type](e.target.value);

                // Mantém posição do cursor após aplicar a máscara
                const newLength = e.target.value.length;
                e.target.selectionEnd = cursor + (newLength - oldLength);
            });
        }
    });
});