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
