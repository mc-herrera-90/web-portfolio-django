console.log("🔥 CONTACT.JS CARGADO");
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const button = document.getElementById("submitButton");
    const text = document.getElementById("buttonText");
    const spinner = document.getElementById("buttonSpinner");

    if (!form || !button || !text || !spinner) {
        console.log("No se encontraron los elementos del formulario.");
        return;
    }

    form.addEventListener("submit", function () {
        button.disabled = true;
        text.textContent = "Enviando...";
        spinner.classList.remove("d-none");
    });
});
