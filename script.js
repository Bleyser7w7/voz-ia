async function convertirAudio() {

    const texto = document.getElementById("texto").value;
    const voz = document.getElementById("voz").value;

    const estado = document.getElementById("estado");
    const player = document.getElementById("player");
    const descargar = document.getElementById("descargar");

    if(texto.trim() === ""){
        estado.innerText = "Escribe un texto.";
        return;
    }

    estado.innerText = "Generando audio IA...";

    const respuesta = await fetch("/convertir", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            texto: texto,
            voz: voz
        })
    });

    if(!respuesta.ok){
        estado.innerText = "Error generando audio.";
        return;
    }

    const blob = await respuesta.blob();

    const url = window.URL.createObjectURL(blob);

    player.src = url;

    descargar.href = url;

    estado.innerText = "Audio generado.";
}