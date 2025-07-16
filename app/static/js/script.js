function updateDateTime() {
    const dateTime = new Date();
    const dateTimeStr = dateTime.toLocaleString();
    document.getElementById("datetime").textContent = dateTimeStr;
}

setInterval(updateDateTime, 1000);

const botaoOcultar = document.getElementById("botao-ocultar");
const minhaDiv = document.getElementById("hide");

botaoOcultar.addEventListener("click", function() {
    minhaDiv.style.display = "none";
});

// Handler para confirmação de exclusão de livro
function confirmDeleteHandler(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const bookId = button.getAttribute('data-book-id');
    const bookStatus = button.getAttribute('data-book-status');
    if (confirm(`Are you sure you want to delete book ID ${bookId}?`)) {
        // Redireciona para rota de exclusão (ajuste a URL conforme sua rota Flask)
        window.location.href = `/delete_book/${bookId}`;
    }
}

// Handler para abrir popup de empréstimo de livro
function openLoanPopupHandler(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const bookId = button.getAttribute('data-book-id');
    // Exemplo: abrir modal ou redirecionar para página de empréstimo
    window.location.href = `/loan_book/${bookId}`;
}
