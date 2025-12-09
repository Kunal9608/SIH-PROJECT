function showToast(text, color) {
    let box = document.createElement("div");
    box.className = "toast-alert";
    box.style.background = color;
    box.innerText = text;
    document.body.appendChild(box);
    setTimeout(() => box.remove(), 2500);
}