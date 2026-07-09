document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.querySelector(".notification_dropdown");
    if (dropdown) {
        dropdown.addEventListener("toggle", function () {
            if (this.open) {
                fetch("/notifications/read", {
                    method: "POST"
                })
                    .then(() => {
                        const counter = document.querySelector(".notification_count");
                        if (counter) counter.remove();
                    });
            }
        });
    }
});

setTimeout(() => {
    document.querySelectorAll('.flash_message').forEach(msg => msg.remove());
}, 3000);

document.addEventListener("DOMContentLoaded", () => {
    const filters = document.querySelectorAll(".category_filter");
    filters.forEach(button => {
        button.addEventListener("click", () => {
            const category = button.dataset.category;
            const rows = document.querySelectorAll("tbody tr");
            rows.forEach(row => {
                const rowCategory = row.dataset.category;
                if (category === "All" || rowCategory === category) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    });
});
