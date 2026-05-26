document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector("#resume");
    if (!fileInput) return;

    fileInput.addEventListener("change", function (event) {
        const fileName = event.target.files[0]?.name || "Choose a resume file";
        const label = document.querySelector("label[for='resume']");
        if (label) label.textContent = fileName;
    });
});
