/**
 * Web-OOP Learning Platform Frontend Controller (Week 1 & Week 2: Quiz-only grading, Practice as ungraded trainer)
 */

const ACTIVE_WEEK = (document.body && document.body.dataset.activeWeek) ? document.body.dataset.activeWeek : "1";
const STORAGE_PREFIX = `weboop_w${ACTIVE_WEEK}_draft_`;
const quizSelections = {};

/**
 * Switch active sub-tab: 'home' | 'theory' | 'practice' | 'quiz' | 'results'
 */
function switchSubTab(tabId) {
    const validTabs = ["home", "theory", "practice", "quiz", "results"];
    const target = validTabs.includes(tabId) ? tabId : "home";

    document.querySelectorAll(".subtab-btn").forEach((btn) => {
        const isCurrent = btn.dataset.tab === target;
        if (isCurrent) {
            btn.classList.add("subtab-active", "text-sky-400", "font-bold");
            btn.classList.remove("text-slate-400", "border-transparent");
        } else {
            btn.classList.remove("subtab-active", "text-sky-400", "font-bold");
            btn.classList.add("text-slate-400", "border-transparent");
        }
    });

    document.querySelectorAll(".subtab-panel").forEach((panel) => {
        if (panel.id === `panel-${target}`) {
            panel.classList.remove("hidden");
        } else {
            panel.classList.add("hidden");
        }
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
}

/**
 * Switch active practice task step
 */
function switchPracticeTask(taskId) {
    document.querySelectorAll(".practice-step-btn").forEach((btn) => {
        const isCurrent = btn.dataset.task === taskId;
        if (isCurrent) {
            btn.classList.add("week-pill-active");
            btn.classList.remove("bg-slate-900/70", "text-slate-400", "border-slate-800");
        } else {
            btn.classList.remove("week-pill-active");
            btn.classList.add("bg-slate-900/70", "text-slate-400", "border-slate-800");
        }
    });

    document.querySelectorAll(".practice-task-card").forEach((card) => {
        if (card.id === `practice-card-${taskId}`) {
            card.classList.remove("hidden");
        } else {
            card.classList.add("hidden");
        }
    });
}

/**
 * Toggle hint box visibility for a practice task
 */
function toggleTaskHint(taskId) {
    const hintBox = document.getElementById(`hint-box-${taskId}`);
    if (hintBox) {
        hintBox.classList.toggle("hidden");
    }
}

/**
 * Insert ready reference solution into editor for beginners
 */
function fillSolutionCode(taskId) {
    const editor = document.getElementById(`editor-${taskId}`);
    if (!editor) return;
    const solution = editor.dataset.solution || "";
    if (solution) {
        editor.value = solution;
        localStorage.setItem(`${STORAGE_PREFIX}${taskId}`, solution);
    }
}

/**
 * Reset code editor to starter template for a practice task
 */
function resetTaskCode(taskId) {
    const editor = document.getElementById(`editor-${taskId}`);
    if (!editor) return;
    const starter = editor.dataset.starter || "";
    editor.value = starter;
    localStorage.removeItem(`${STORAGE_PREFIX}${taskId}`);
}

/**
 * Execute student code for a practice task via RunnerService API (ungraded trainer)
 */
async function runPracticeTask(taskId) {
    const editor = document.getElementById(`editor-${taskId}`);
    const runBtn = document.getElementById(`run-btn-${taskId}`);
    const resultBox = document.getElementById(`result-box-${taskId}`);
    const verdictBadge = document.getElementById(`verdict-badge-${taskId}`);
    const timeLabel = document.getElementById(`time-label-${taskId}`);
    const outputPre = document.getElementById(`output-pre-${taskId}`);

    if (!editor || !runBtn || !resultBox) return;

    const code = editor.value;
    localStorage.setItem(`${STORAGE_PREFIX}${taskId}`, code);

    const originalText = runBtn.innerHTML;
    runBtn.disabled = true;
    runBtn.innerHTML = `<span>⏳ Запуск в песочнице...</span>`;

    try {
        const res = await fetch(`/api/week${ACTIVE_WEEK}/practice/${taskId}/run`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code }),
        });

        const data = await res.json();
        resultBox.classList.remove("hidden");

        if (timeLabel) {
            timeLabel.textContent = `${data.execution_time_ms || 0} мс`;
        }

        if (data.passed) {
            verdictBadge.textContent = `✅ ОТЛИЧНО! КОД РАБОТАЕТ ВЕРНО`;
            verdictBadge.className =
                "px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
        } else {
            verdictBadge.textContent = `❌ ЕСТЬ ОШИБКИ (${data.status}) — ПОПРОБУЙТЕ ПОДСКАЗКУ ИЛИ ГОТОВОЕ РЕШЕНИЕ`;
            verdictBadge.className =
                "px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40";
        }

        if (outputPre) {
            outputPre.textContent = data.output || "Нет вывода";
        }

        if (data.progress) {
            updateProgressUI(data.progress);
        }
    } catch (err) {
        resultBox.classList.remove("hidden");
        if (verdictBadge) {
            verdictBadge.textContent = "⚠️ ОШИБКА СЕТИ";
            verdictBadge.className =
                "px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40";
        }
        if (outputPre) {
            outputPre.textContent = String(err);
        }
    } finally {
        runBtn.disabled = false;
        runBtn.innerHTML = originalText;
    }
}

/**
 * Select an option in the final quiz
 */
function selectQuizOption(questionId, optionIndex) {
    quizSelections[questionId] = optionIndex;

    document.querySelectorAll(`.quiz-opt-${questionId}`).forEach((btn) => {
        const idx = parseInt(btn.dataset.index, 10);
        if (idx === optionIndex) {
            btn.className = `quiz-opt-${questionId} w-full text-left p-3.5 rounded-xl border transition flex items-center gap-3 bg-sky-500/20 border-sky-400 text-white shadow-sm`;
        } else {
            btn.className = `quiz-opt-${questionId} w-full text-left p-3.5 rounded-xl border transition flex items-center gap-3 bg-slate-900/70 border-slate-800 text-slate-300 hover:border-slate-700`;
        }
    });
}

/**
 * Submit final quiz answers to API for the active week
 */
async function submitWeek1Quiz() {
    const submitBtn = document.getElementById("btn-submit-quiz");
    const banner = document.getElementById("quiz-result-banner");
    if (!submitBtn) return;

    const originalHtml = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = "<span>Проверка ответов...</span>";

    try {
        const res = await fetch(`/api/week${ACTIVE_WEEK}/quiz/check`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers: quizSelections }),
        });
        const data = await res.json();

        if (banner) {
            banner.classList.remove("hidden");
            const isGood = data.score >= 12.0;
            banner.className = `p-5 rounded-xl border ${
                isGood
                    ? "bg-emerald-500/15 border-emerald-500/40 text-emerald-200"
                    : "bg-amber-500/15 border-amber-500/40 text-amber-200"
            }`;
            banner.innerHTML = `
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                        <div class="text-base font-bold">
                            Ваш результат за тест: ${data.correct_count} из ${data.total_questions} (${data.score} / ${data.max_score} баллов)
                        </div>
                        <p class="text-xs opacity-90 mt-1">
                            ${
                                isGood
                                    ? `🎉 Поздравляем! Зачет по Неделе ${ACTIVE_WEEK} получен!`
                                    : "Для зачета нужно минимум 12 баллов из 20 (6 правильных ответов из 10). Посмотрите подсказки под вопросами и попробуйте еще раз!"
                            }
                        </p>
                    </div>
                    <button onclick="switchSubTab('results')" class="px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition shrink-0">
                        Перейти в Результаты →
                    </button>
                </div>
            `;
        }

        if (Array.isArray(data.results)) {
            data.results.forEach((item) => {
                const expBox = document.getElementById(`quiz-exp-${item.id}`);
                if (expBox) {
                    expBox.classList.remove("hidden");
                    if (item.is_correct) {
                        expBox.className =
                            "mt-3 p-3.5 rounded-lg text-xs bg-emerald-500/15 border border-emerald-500/40 text-emerald-200";
                        expBox.innerHTML = `<strong>✅ Верно (+2 балла)!</strong> ${item.explanation}`;
                    } else {
                        expBox.className =
                            "mt-3 p-3.5 rounded-lg text-xs bg-rose-500/15 border border-rose-500/40 text-rose-200";
                        expBox.innerHTML = `<strong>❌ Неверно.</strong> ${item.explanation}`;
                    }
                }
            });
        }

        if (data.progress) {
            updateProgressUI(data.progress);
        }
    } catch (err) {
        console.error("Quiz check error:", err);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalHtml;
    }
}

/**
 * Update all score counters and status indicators across tabs
 */
function updateProgressUI(progress) {
    const setTxt = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    };

    setTxt("header-total-score", `${progress.total_score} / ${progress.max_score} б.`);
    setTxt("home-total-score", `${progress.total_score} / ${progress.max_score} б.`);
    setTxt("home-tasks-done", `${progress.tasks_completed} / ${progress.tasks_total}`);
    setTxt("home-quiz-score", `${progress.quiz_score} / ${progress.quiz_max} б.`);

    setTxt("results-total-score", `${progress.total_score} / ${progress.max_score} б.`);
    setTxt("results-quiz-score", `${progress.quiz_score} / ${progress.quiz_max} б.`);
    setTxt("results-percent-label", `${progress.progress_percent}%`);

    const bar = document.getElementById("results-progress-bar");
    if (bar) {
        bar.style.width = `${progress.progress_percent}%`;
    }

    const headerBadge = document.getElementById("header-status-badge");
    if (headerBadge) {
        if (progress.is_completed) {
            headerBadge.textContent = "ЗАЧЕТ ПОЛУЧЕН";
            headerBadge.className =
                "px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
        } else {
            headerBadge.textContent = "В ПРОЦЕССЕ";
            headerBadge.className =
                "px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider bg-sky-500/20 text-sky-300 border border-sky-500/40";
        }
    }

    if (progress.tasks) {
        Object.keys(progress.tasks).forEach((tid) => {
            const tinfo = progress.tasks[tid];
            if (!tinfo) return;
            setTxt(`step-status-${tid}`, tinfo.is_completed ? "✅ Разобрано" : "Тренажер");
            setTxt(`res-status-${tid}`, tinfo.is_completed ? "✅ Пройдено" : "По желанию");
            const dot = document.getElementById(`step-dot-${tid}`);
            if (dot) {
                dot.className = tinfo.is_completed
                    ? "w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]"
                    : "w-2.5 h-2.5 rounded-full bg-slate-600";
            }
        });
    }
}

/**
 * Show notice when clicking locked future weeks
 */
function showLockedWeekToast(weekTitle) {
    const toast = document.getElementById("locked-week-toast");
    const label = document.getElementById("locked-week-toast-text");
    if (!toast || !label) return;
    label.textContent = `${weekTitle} откроется в следующем учебном модуле.`;
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3500);
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".code-editor-textarea").forEach((textarea) => {
        const taskId = textarea.dataset.task;
        const saved = localStorage.getItem(`${STORAGE_PREFIX}${taskId}`);
        if (saved && saved.trim().length > 0) {
            textarea.value = saved;
        }

        textarea.addEventListener("input", () => {
            localStorage.setItem(`${STORAGE_PREFIX}${taskId}`, textarea.value);
        });

        textarea.addEventListener("keydown", (e) => {
            if (e.key === "Tab") {
                e.preventDefault();
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                textarea.value =
                    textarea.value.substring(0, start) + "    " + textarea.value.substring(end);
                textarea.selectionStart = textarea.selectionEnd = start + 4;
                localStorage.setItem(`${STORAGE_PREFIX}${taskId}`, textarea.value);
            }
        });
    });
});
