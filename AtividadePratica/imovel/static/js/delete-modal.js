(function () {
    "use strict";

    const modal = document.getElementById("delete-modal");
    const itemName = document.getElementById("delete-item-name");
    const confirmButton = document.getElementById("delete-confirm-button");

    if (!modal || !itemName || !confirmButton) return;

    let lastFocusedElement = null;

    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        if (lastFocusedElement) lastFocusedElement.focus();
    }

    document.querySelectorAll(".delete-trigger").forEach(function (trigger) {
        trigger.addEventListener("click", function (event) {
            event.preventDefault();
            lastFocusedElement = trigger;
            itemName.textContent = trigger.dataset.itemName || "este registro";
            confirmButton.href = trigger.href;
            modal.hidden = false;
            document.body.style.overflow = "hidden";
            confirmButton.focus();
        });
    });

    modal.querySelectorAll("[data-modal-close]").forEach(function (button) {
        button.addEventListener("click", closeModal);
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) closeModal();
    });

    document.addEventListener("keydown", function (event) {
        if (!modal.hidden && event.key === "Escape") closeModal();
    });
}());
