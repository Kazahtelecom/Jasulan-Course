/**
 * Web-OOP Frontend Application Logic (Vanilla JS, Zero-Build).
 */

document.addEventListener("DOMContentLoaded", () => {
    initHealthMonitoring();
    initSmokeTest();
});

async function checkHealth() {
    const backendText = document.getElementById("status-backend-text");
    const backendIndicator = document.getElementById("status-backend-indicator");
    const dbText = document.getElementById("status-db-text");
    const dbIndicator = document.getElementById("status-db-indicator");
    const runnerText = document.getElementById("status-runner-text");
    const runnerIndicator = document.getElementById("status-runner-indicator");
    const overallBadge = document.getElementById("overall-status-badge");

    try {
        const response = await fetch("/api/health");
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }
        const data = await response.json();

        // Update Backend
        if (data.status === "ok") {
            backendText.textContent = "Активен (HTTP 200)";
            backendText.className = "text-base font-bold text-emerald-600 mt-1";
            backendIndicator.className = "w-4 h-4 rounded-full status-active";
        } else {
            backendText.textContent = "Ошибка";
            backendText.className = "text-base font-bold text-rose-600 mt-1";
            backendIndicator.className = "w-4 h-4 rounded-full status-error";
        }

        // Update SQLite
        if (data.db === "connected") {
            dbText.textContent = "Подключена (SQLite)";
            dbText.className = "text-base font-bold text-emerald-600 mt-1";
            dbIndicator.className = "w-4 h-4 rounded-full status-active";
        } else {
            dbText.textContent = "Ошибка соединения";
            dbText.className = "text-base font-bold text-rose-600 mt-1";
            dbIndicator.className = "w-4 h-4 rounded-full status-error";
        }

        // Update Runner
        if (data.runner === "ready") {
            runnerText.textContent = "Готов к работе";
            runnerText.className = "text-base font-bold text-emerald-600 mt-1";
            runnerIndicator.className = "w-4 h-4 rounded-full status-active";
        } else {
            runnerText.textContent = "Не готов";
            runnerText.className = "text-base font-bold text-rose-600 mt-1";
            runnerIndicator.className = "w-4 h-4 rounded-full status-error";
        }

        // Overall status
        if (data.status === "ok" && data.db === "connected" && data.runner === "ready") {
            overallBadge.textContent = "Все системы активны";
            overallBadge.className = "px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800";
        } else {
            overallBadge.textContent = "Внимание: есть неполадки";
            overallBadge.className = "px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800";
        }
    } catch (err) {
        backendText.textContent = "Недоступен";
        backendIndicator.className = "w-4 h-4 rounded-full status-error";
        dbText.textContent = "Неизвестно";
        dbIndicator.className = "w-4 h-4 rounded-full status-error";
        runnerText.textContent = "Недоступен";
        runnerIndicator.className = "w-4 h-4 rounded-full status-error";
        overallBadge.textContent = "Сервер недоступен";
        overallBadge.className = "px-3 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800";
    }
}

function initHealthMonitoring() {
    checkHealth();
    setInterval(checkHealth, 10000);
}

function initSmokeTest() {
    const btn = document.getElementById("btn-run-smoke");
    const container = document.getElementById("smoke-result-container");
    const badge = document.getElementById("smoke-badge");
    const timeEl = document.getElementById("smoke-time");
    const outputEl = document.getElementById("smoke-output");

    if (!btn) return;

    btn.addEventListener("click", async () => {
        btn.disabled = true;
        btn.classList.add("opacity-60", "cursor-not-allowed");
        btn.querySelector("span").textContent = "Исполнение в песочнице...";

        container.classList.remove("hidden");
        badge.textContent = "Выполняется...";
        badge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800";
        timeEl.textContent = "...";
        outputEl.textContent = "Инициализация sandbox, AST-анализ и запуск pytest...";

        try {
            const resp = await fetch("/api/runner/smoke", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            if (!resp.ok) {
                throw new Error(`HTTP error ${resp.status}`);
            }

            const data = await resp.json();
            timeEl.textContent = `${data.execution_time_ms} ms`;
            outputEl.textContent = data.output || "(Вывод пуст)";

            if (data.passed) {
                badge.textContent = `УСПЕХ (${data.status})`;
                badge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800";
            } else {
                badge.textContent = `ОШИБКА (${data.status})`;
                badge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800";
            }
        } catch (err) {
            badge.textContent = "СБОЙ СЕТИ";
            badge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800";
            outputEl.textContent = `Ошибка выполнения запроса: ${err.message}`;
        } finally {
            btn.disabled = false;
            btn.classList.remove("opacity-60", "cursor-not-allowed");
            btn.querySelector("span").textContent = "Smoke-тест раннера";
        }
    });
}
