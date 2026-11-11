(() => {
  const placeholders = {
    username: 'Seu nome de usuário',
    email: 'voce@exemplo.com',
    password: 'Sua senha',
    password1: 'Crie uma senha',
    password2: 'Repita sua senha',
    old_password: 'Sua senha atual',
    new_password1: 'Crie uma nova senha',
    new_password2: 'Repita a nova senha',
    first_name: 'Seu nome',
    last_name: 'Seu sobrenome',
    nome: 'Nome completo',
    telefone: '(11) 99999-9999',
    mensagem: 'Como podemos ajudar?',
    biografia: 'Conte um pouco sobre o integrante',
    cargo: 'Ex.: Designer',
    foto_url: 'https://exemplo.com/foto.jpg',
    busca: 'Nome do serviço',
    q: 'Nome do produto ou serviço',
    quantidade: '1',
  };

  function formatPhone(value) {
    let digits = value.replace(/\D/g, '');
    if (digits.startsWith('55') && (digits.length === 12 || digits.length === 13)) {
      digits = digits.slice(2);
    }
    digits = digits.slice(0, 11);

    if (digits.length === 0) return '';
    if (digits.length <= 2) return `(${digits}`;
    if (digits.length <= 10) {
      return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`.replace(/-$/, '');
    }
    return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
  }

  function formatCurrency(value) {
    const digits = value.replace(/\D/g, '').slice(0, 10);
    if (!digits) return '';

    const amount = Number(digits) / 100;
    return `R$ ${new Intl.NumberFormat('pt-BR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount)}`;
  }

  function maskInput(input, formatter) {
    const selectionStart = input.selectionStart;
    const digitsBeforeCursor = input.value.slice(0, selectionStart).replace(/\D/g, '').length;
    const maskedValue = formatter(input.value);

    input.value = maskedValue;
    if (selectionStart === null) return;

    let cursor = 0;
    let digitsAtCursor = 0;
    while (cursor < maskedValue.length && digitsAtCursor < digitsBeforeCursor) {
      if (/\d/.test(maskedValue[cursor])) digitsAtCursor += 1;
      cursor += 1;
    }
    if (digitsBeforeCursor === 0 && maskedValue.startsWith('(')) cursor = 1;
    input.setSelectionRange(cursor, cursor);
  }

  document.querySelectorAll('input, textarea').forEach((input) => {
    if (!input.placeholder && placeholders[input.name]) {
      input.placeholder = placeholders[input.name];
    }

    const formatter = input.dataset.mask === 'phone'
      ? formatPhone
      : input.dataset.mask === 'currency'
        ? formatCurrency
        : null;
    if (!formatter) return;

    input.addEventListener('input', () => maskInput(input, formatter));
    if (input.value) maskInput(input, formatter);
  });
})();
