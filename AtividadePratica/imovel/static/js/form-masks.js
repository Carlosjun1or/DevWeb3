(function () {
    "use strict";

    function onlyDigits(value) {
        return value.replace(/\D/g, "");
    }

    function formatPhone(value) {
        const digits = onlyDigits(value).slice(0, 11);
        if (digits.length <= 2) return digits.length ? `(${digits}` : "";
        if (digits.length <= 7) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
        if (digits.length <= 10) {
            return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
        }
        return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
    }

    function formatCurrency(value) {
        let raw = value.replace(/^R\$\s*/, "").replace(/\s/g, "");
        const hasComma = raw.includes(",");
        const decimalFromServer = /^\d+\.\d{2}$/.test(raw);

        if (decimalFromServer) {
            raw = raw.replace(".", ",");
        }

        const parts = raw.split(",");
        const integer = onlyDigits(parts[0]);
        if (!integer) return "";

        const formattedInteger = Number(integer).toLocaleString("pt-BR");
        if (!hasComma && !decimalFromServer) return formattedInteger;

        const decimals = onlyDigits(parts[1] || "").slice(0, 2);
        return `${formattedInteger},${decimals}`;
    }

    document.querySelectorAll("[data-mask='phone']").forEach(function (field) {
        field.addEventListener("input", function () {
            field.value = formatPhone(field.value);
        });
        field.value = formatPhone(field.value);
    });

    document.querySelectorAll("[data-mask='currency']").forEach(function (field) {
        field.addEventListener("input", function () {
            field.value = formatCurrency(field.value);
        });
        field.value = formatCurrency(field.value);
    });

    document.querySelectorAll("form").forEach(function (form) {
        form.addEventListener("submit", function () {
            form.querySelectorAll("[data-mask='currency']").forEach(function (field) {
                field.value = field.value.replace(/\./g, "").replace(",", ".");
            });
        });
    });
}());
