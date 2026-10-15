/**
 * Week 1 Client Interaction Script: Tabs, LocalStorage, Quiz Validation, and Runner Integration.
 * Zero-Build Pure Vanilla JS.
 */

document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------
    // 1. Tab Switching Logic
    // -------------------------------------------------------------
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabPanes = document.querySelectorAll(".tab-pane");

    function switchTab(targetId) {
        tabButtons.forEach(btn => {
            if (btn.dataset.target === targetId) {
                btn.classList.add("active", "border-indigo-600", "text-indigo-600");
                btn.classList.remove("border-transparent", "text-slate-500");
            } else {
                btn.classList.remove("active", "border-indigo-600", "text-indigo-600");
                btn.classList.add("border-transparent", "text-slate-500");
            }
        });

        tabPanes.forEach(pane => {
            if (pane.id === targetId) {
                pane.classList.remove("hidden");
                pane.classList.add("block");
            } else {
                pane.classList.add("hidden");
                pane.classList.remove("block");
            }
        });

        if (targetId === "tab-lecture" && window.mermaid) {
            try {
                window.mermaid.run();
            } catch (e) {
                console.debug("Mermaid run caught:", e);
            }
        }
    }

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => switchTab(btn.dataset.target));
    });

    const btnNextToQuiz = document.getElementById("btn-next-to-quiz");
    if (btnNextToQuiz) {
        btnNextToQuiz.addEventListener("click", () => switchTab("tab-quiz"));
    }

    // -------------------------------------------------------------
    // 2. Global Progress State Updater
    // -------------------------------------------------------------
    function updateProgressBadges(data) {
        const headerScore = document.getElementById("header-score-badge");
        const headerStatus = document.getElementById("header-status-badge");

        if (headerScore && data.total_week_score !== undefined) {
            headerScore.textContent = `${data.total_week_score} / 20.0 б.`;
        } else if (headerScore && data.score !== undefined && data.max_score === 20.0) {
            headerScore.textContent = `${data.score} / 20.0 б.`;
        }

        if (headerStatus && data.is_completed !== undefined) {
            if (data.is_completed) {
                headerStatus.textContent = "Сдано (Зачет)";
                headerStatus.className = "px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider shadow-sm transition bg-emerald-500 text-white";
            } else {
                headerStatus.textContent = "В процессе";
                headerStatus.className = "px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider shadow-sm transition bg-amber-500 text-white";
            }
        }

        if (data.quiz_score !== undefined) {
            const bQuiz = document.getElementById("badge-quiz-score");
            const dQuiz = document.getElementById("quiz-score-display");
            if (bQuiz) bQuiz.textContent = `${data.quiz_score} / 3 б.`;
            if (dQuiz) dQuiz.textContent = `${data.quiz_score} / 3.0 б.`;
        }
        if (data.practice_score !== undefined) {
            const bPrac = document.getElementById("badge-practice-score");
            const dPrac = document.getElementById("practice-score-display");
            if (bPrac) bPrac.textContent = `${data.practice_score} / 7 б.`;
            if (dPrac) dPrac.textContent = `${data.practice_score} / 7.0 б.`;
        }
        if (data.lab_score !== undefined) {
            const bLab = document.getElementById("badge-lab-score");
            const dLab = document.getElementById("lab-score-display");
            if (bLab) bLab.textContent = `${data.lab_score} / 10 б.`;
            if (dLab) dLab.textContent = `${data.lab_score} / 10.0 б.`;
        }
    }

    async function fetchInitialProgress() {
        try {
            const res = await fetch("/api/week1/progress");
            if (res.ok) {
                const data = await res.json();
                updateProgressBadges(data);
            }
        } catch (err) {
            console.error("Failed to load initial progress:", err);
        }
    }
    fetchInitialProgress();

    // -------------------------------------------------------------
    // 3. LocalStorage Persistence for Code Editors
    // -------------------------------------------------------------
    const PRACTICE_STORAGE_KEY = "web_oop_w1_practice_code";
    const LAB_STORAGE_KEY = "web_oop_w1_lab_code";

    const practiceEditor = document.getElementById("practice-code-editor");
    const practiceSaveStatus = document.getElementById("practice-auto-save-status");
    const labEditor = document.getElementById("lab-code-editor");
    const labSaveStatus = document.getElementById("lab-auto-save-status");

    // Restore from LocalStorage if present
    if (practiceEditor) {
        const savedPractice = localStorage.getItem(PRACTICE_STORAGE_KEY);
        if (savedPractice && savedPractice.trim().length > 0) {
            practiceEditor.value = savedPractice;
        }
        let timeout = null;
        practiceEditor.addEventListener("input", () => {
            if (practiceSaveStatus) practiceSaveStatus.textContent = "Сохранение...";
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                localStorage.setItem(PRACTICE_STORAGE_KEY, practiceEditor.value);
                if (practiceSaveStatus) practiceSaveStatus.textContent = "Черновик сохранен в LocalStorage";
            }, 300);
        });
    }

    if (labEditor) {
        const savedLab = localStorage.getItem(LAB_STORAGE_KEY);
        if (savedLab && savedLab.trim().length > 0) {
            labEditor.value = savedLab;
        }
        let timeout = null;
        labEditor.addEventListener("input", () => {
            if (labSaveStatus) labSaveStatus.textContent = "Сохранение...";
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                localStorage.setItem(LAB_STORAGE_KEY, labEditor.value);
                if (labSaveStatus) labSaveStatus.textContent = "Черновик сохранен в LocalStorage";
            }, 300);
        });
    }

    // Reset Buttons
    const btnPracticeReset = document.getElementById("btn-practice-reset");
    if (btnPracticeReset && practiceEditor) {
        btnPracticeReset.addEventListener("click", () => {
            if (confirm("Сбросить код практикума к исходному шаблону? Несохраненные изменения будут потеряны.")) {
                if (window.WEEK1_TEMPLATES && window.WEEK1_TEMPLATES.practiceStarter) {
                    practiceEditor.value = window.WEEK1_TEMPLATES.practiceStarter;
                    localStorage.setItem(PRACTICE_STORAGE_KEY, practiceEditor.value);
                    if (practiceSaveStatus) practiceSaveStatus.textContent = "Шаблон восстановлен";
                }
            }
        });
    }

    const btnLabReset = document.getElementById("btn-lab-reset");
    if (btnLabReset && labEditor) {
        btnLabReset.addEventListener("click", () => {
            if (confirm("Сбросить код лабораторной работы к исходному шаблону? Несохраненные изменения будут потеряны.")) {
                if (window.WEEK1_TEMPLATES && window.WEEK1_TEMPLATES.labStarter) {
                    labEditor.value = window.WEEK1_TEMPLATES.labStarter;
                    localStorage.setItem(LAB_STORAGE_KEY, labEditor.value);
                    if (labSaveStatus) labSaveStatus.textContent = "Шаблон восстановлен";
                }
            }
        });
    }

    // -------------------------------------------------------------
    // 4. Quiz Validation
    // -------------------------------------------------------------
    const quizForm = document.getElementById("quiz-form");
    const quizStatusMsg = document.getElementById("quiz-status-msg");

    if (quizForm) {
        quizForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(quizForm);
            const answers = {};

            for (const [key, value] of formData.entries()) {
                answers[key] = parseInt(value, 10);
            }

            if (Object.keys(answers).length === 0) {
                if (quizStatusMsg) quizStatusMsg.textContent = "Пожалуйста, выберите хотя бы один вариант ответа!";
                return;
            }

            const btnSubmit = document.getElementById("btn-submit-quiz");
            if (btnSubmit) {
                btnSubmit.disabled = true;
                btnSubmit.innerHTML = `
                    <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                    </svg>
                    <span>Проверка ответов...</span>
                `;
            }

            try {
                const res = await fetch("/api/week1/quiz/check", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ answers }),
                });

                if (!res.ok) throw new Error(`HTTP error ${res.status}`);
                const data = await res.json();

                // Update feedback boxes
                for (const [qid, detail] of Object.entries(data.details)) {
                    const fbContainer = document.getElementById(`feedback-${qid}`);
                    if (!fbContainer) continue;
                    const fbBody = fbContainer.querySelector(".feedback-body");

                    fbContainer.classList.remove("hidden");
                    if (detail.is_correct) {
                        fbBody.className = "p-3.5 rounded-lg text-xs leading-relaxed font-sans border bg-emerald-50 text-emerald-900 border-emerald-200";
                        fbBody.innerHTML = `<strong>Верно! (+${(data.score / data.total_questions).toFixed(1)} б.)</strong> ${detail.explanation}`;
                    } else {
                        fbBody.className = "p-3.5 rounded-lg text-xs leading-relaxed font-sans border bg-rose-50 text-rose-900 border-rose-200";
                        fbBody.innerHTML = `<strong>Неверно.</strong> ${detail.explanation} <div class="mt-1 pt-1 border-t border-rose-200 text-slate-700"><strong>Правильный ответ:</strong> ${detail.correct_explanation}</div>`;
                    }
                }

                if (quizStatusMsg) {
                    quizStatusMsg.textContent = `Квиз проверен! Правильно: ${data.correct_count} из ${data.total_questions}. Начислено: ${data.score} из ${data.max_score} б.`;
                }

                updateProgressBadges(data);
                const dQuiz = document.getElementById("quiz-score-display");
                const bQuiz = document.getElementById("badge-quiz-score");
                if (dQuiz) dQuiz.textContent = `${data.score} / ${data.max_score} б.`;
                if (bQuiz) bQuiz.textContent = `${data.score} / 3 б.`;

            } catch (err) {
                console.error("Quiz submission error:", err);
                if (quizStatusMsg) quizStatusMsg.textContent = "Ошибка при проверке квиза. Повторите попытку.";
            } finally {
                if (btnSubmit) {
                    btnSubmit.disabled = false;
                    btnSubmit.innerHTML = `
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                        </svg>
                        <span>Проверить ответы и сохранить балл</span>
                    `;
                }
            }
        });
    }

    // -------------------------------------------------------------
    // 5. Practice Runner Integration
    // -------------------------------------------------------------
    const btnRunPractice = document.getElementById("btn-run-practice");
    const practiceResultBox = document.getElementById("practice-result-box");
    const practiceStatusBadge = document.getElementById("practice-status-badge");
    const practiceTestsBadge = document.getElementById("practice-tests-badge");
    const practiceExecutionTime = document.getElementById("practice-execution-time");
    const practiceLogOutput = document.getElementById("practice-log-output");

    if (btnRunPractice && practiceEditor) {
        btnRunPractice.addEventListener("click", async () => {
            btnRunPractice.disabled = true;
            btnRunPractice.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span>Выполнение в песочнице...</span>
            `;

            try {
                const res = await fetch("/api/week1/practice/run", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ code: practiceEditor.value }),
                });

                if (!res.ok) throw new Error(`HTTP error ${res.status}`);
                const data = await res.json();

                if (practiceResultBox) practiceResultBox.classList.remove("hidden");
                if (practiceExecutionTime) practiceExecutionTime.textContent = `${data.execution_time_ms} ms`;
                if (practiceLogOutput) practiceLogOutput.textContent = data.output || "Вывод пуст";

                if (practiceStatusBadge) {
                    if (data.status === "PASSED") {
                        practiceStatusBadge.textContent = "PASSED";
                        practiceStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300";
                    } else if (data.status === "SECURITY_VIOLATION") {
                        practiceStatusBadge.textContent = "SECURITY VIOLATION";
                        practiceStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300";
                    } else if (data.status === "TIMEOUT") {
                        practiceStatusBadge.textContent = "TIMEOUT (5s)";
                        practiceStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300";
                    } else {
                        practiceStatusBadge.textContent = data.status || "FAILED";
                        practiceStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300";
                    }
                }

                if (practiceTestsBadge) {
                    practiceTestsBadge.textContent = `${data.passed_tests} / ${data.total_tests} тестов (+${data.score} б.)`;
                    if (data.passed_tests === data.total_tests) {
                        practiceTestsBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800";
                    } else {
                        practiceTestsBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800";
                    }
                }

                updateProgressBadges(data);
                const dPrac = document.getElementById("practice-score-display");
                const bPrac = document.getElementById("badge-practice-score");
                if (dPrac) dPrac.textContent = `${data.score} / 7.0 б.`;
                if (bPrac) bPrac.textContent = `${data.score} / 7 б.`;

            } catch (err) {
                console.error("Practice run error:", err);
                if (practiceResultBox) practiceResultBox.classList.remove("hidden");
                if (practiceLogOutput) practiceLogOutput.textContent = `Ошибка выполнения запроса: ${err.message}`;
            } finally {
                btnRunPractice.disabled = false;
                btnRunPractice.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>Запустить 7 автотестов RunnerService</span>
                `;
            }
        });
    }

    // -------------------------------------------------------------
    // 6. Lab Runner Integration
    // -------------------------------------------------------------
    const btnRunLab = document.getElementById("btn-run-lab");
    const labResultBox = document.getElementById("lab-result-box");
    const labStatusBadge = document.getElementById("lab-status-badge");
    const labTestsBadge = document.getElementById("lab-tests-badge");
    const labExecutionTime = document.getElementById("lab-execution-time");
    const labLogOutput = document.getElementById("lab-log-output");

    if (btnRunLab && labEditor) {
        btnRunLab.addEventListener("click", async () => {
            btnRunLab.disabled = true;
            btnRunLab.innerHTML = `
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span>Выполнение в песочнице...</span>
            `;

            try {
                const res = await fetch("/api/week1/lab/run", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ code: labEditor.value }),
                });

                if (!res.ok) throw new Error(`HTTP error ${res.status}`);
                const data = await res.json();

                if (labResultBox) labResultBox.classList.remove("hidden");
                if (labExecutionTime) labExecutionTime.textContent = `${data.execution_time_ms} ms`;
                if (labLogOutput) labLogOutput.textContent = data.output || "Вывод пуст";

                if (labStatusBadge) {
                    if (data.status === "PASSED") {
                        labStatusBadge.textContent = "PASSED";
                        labStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300";
                    } else if (data.status === "SECURITY_VIOLATION") {
                        labStatusBadge.textContent = "SECURITY VIOLATION";
                        labStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300";
                    } else if (data.status === "TIMEOUT") {
                        labStatusBadge.textContent = "TIMEOUT (5s)";
                        labStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300";
                    } else {
                        labStatusBadge.textContent = data.status || "FAILED";
                        labStatusBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300";
                    }
                }

                if (labTestsBadge) {
                    labTestsBadge.textContent = `${data.passed_tests} / ${data.total_tests} тестов (+${data.score} б.)`;
                    if (data.passed_tests === data.total_tests) {
                        labTestsBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800";
                    } else {
                        labTestsBadge.className = "px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800";
                    }
                }

                updateProgressBadges(data);
                const dLab = document.getElementById("lab-score-display");
                const bLab = document.getElementById("badge-lab-score");
                if (dLab) dLab.textContent = `${data.score} / 10.0 б.`;
                if (bLab) bLab.textContent = `${data.score} / 10 б.`;

            } catch (err) {
                console.error("Lab run error:", err);
                if (labResultBox) labResultBox.classList.remove("hidden");
                if (labLogOutput) labLogOutput.textContent = `Ошибка выполнения запроса: ${err.message}`;
            } finally {
                btnRunLab.disabled = false;
                btnRunLab.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span>Запустить 10 автотестов RunnerService</span>
                `;
            }
        });
    }
});
