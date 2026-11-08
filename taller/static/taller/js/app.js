document.addEventListener("click", function(event) {
    const sidebar = document.getElementById("sidebar");
    if (!sidebar || !sidebar.classList.contains("open")) return;
    if (!sidebar.contains(event.target) && !event.target.closest(".menu-toggle")) {
        sidebar.classList.remove("open");
    }
});
