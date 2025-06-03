document.querySelectorAll("#languageSelect li").forEach(item => {
    item.addEventListener("click", () => {
        document.querySelectorAll("#languageSelect li").forEach(li => li.classList.remove("selected"));
        item.classList.add("selected");
        document.getElementById("redirectBtn").setAttribute("data-lang", item.getAttribute("data-lang"));
    });
});

document.getElementById("redirectBtn").addEventListener("click", () => {
    let lang = document.getElementById("redirectBtn").getAttribute("data-lang") || "en";
    window.location.href = lang + "/index.html";
});
