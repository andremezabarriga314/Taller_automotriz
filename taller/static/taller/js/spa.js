(() => {
    "use strict";

    const getParts = (html) => {
        const doc = new DOMParser().parseFromString(html, "text/html");

        return {
            doc,
            sidebar: doc.querySelector(".sidebar"),
            main: doc.querySelector(".main-content")
        };
    };

    async function navigate(url, options = {}) {
        const method = options.method || "GET";
        const body = options.body || null;
        const push = options.push !== false;

        try {
            const response = await fetch(url, {
                method,
                body,
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const html = await response.text();
            const parts = getParts(html);

            // Si la respuesta no contiene el panel, navegar normalmente.
            if (!parts.sidebar || !parts.main) {
                window.location.href = response.url || url;
                return;
            }

            const currentSidebar = document.querySelector(".sidebar");
            const currentMain = document.querySelector(".main-content");

            if (!currentSidebar || !currentMain) {
                window.location.href = response.url || url;
                return;
            }

            currentSidebar.replaceWith(parts.sidebar);
            currentMain.replaceWith(parts.main);

            document.title = parts.doc.title || "MotorTech Service";

            if (push) {
                history.pushState({}, "", response.url || url);
            }

            window.scrollTo(0, 0);

        } catch (error) {
            console.error("Error de navegación:", error);
            window.location.href = url;
        }
    }

    // Navegación de enlaces.
    document.addEventListener("click", (event) => {
        const link = event.target.closest("a[href]");

        if (!link || event.defaultPrevented) return;
        if (event.button !== 0) return;
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        if (link.target === "_blank" || link.hasAttribute("download")) return;

        const url = new URL(link.href, window.location.href);

        if (url.origin !== window.location.origin) return;
        if (url.pathname.startsWith("/admin/")) return;
        if (url.pathname.startsWith("/static/")) return;
        if (url.pathname.startsWith("/media/")) return;
        if (url.hash && url.pathname === window.location.pathname) return;

        event.preventDefault();
        navigate(url.href);
    });

    // Envío de formularios sin recargar el panel.
    document.addEventListener("submit", (event) => {
        const form = event.target;

        if (!(form instanceof HTMLFormElement)) return;
        if (form.target === "_blank") return;

        const method = (form.method || "GET").toUpperCase();
        const url = new URL(form.action || window.location.href);

        if (url.origin !== window.location.origin) return;

        event.preventDefault();

        if (method === "GET") {
            const data = new FormData(form);
            const params = new URLSearchParams();

            for (const [key, value] of data.entries()) {
                if (typeof value === "string" && value !== "") {
                    params.append(key, value);
                }
            }

            url.search = params.toString();
            navigate(url.href);
            return;
        }

        navigate(url.href, {
            method,
            body: new FormData(form)
        });
    });

    // Botones atrás y adelante del navegador.
    window.addEventListener("popstate", () => {
        navigate(window.location.href, { push: false });
    });

})();
