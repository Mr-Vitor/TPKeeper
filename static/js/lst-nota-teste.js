document.addEventListener("DOMContentLoaded", function () {
    // Alternar abas ativas
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            tabs.forEach(t => t.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Adicionar nova nota (futuro)
    document.querySelector(".add-note").addEventListener("click", function () {
        alert("Função de adicionar nota ainda não implementada!");
    });
});
