/**
 * Web-OOP Learning Platform Frontend Controller
 * Modular architecture: UI Navigation, Student State, Practice Runner, Quiz Evaluation, Progress Sync.
 */

/* ========================================================================= */
/* MODULE 1: STATE & CONFIGURATION                                           */
/* ========================================================================= */

const ACTIVE_WEEK = (document.body && document.body.dataset.activeWeek) ? document.body.dataset.activeWeek : "1";

function getActiveStudent() {
    const selector = document.getElementById("student-selector");
    if (selector && selector.value) {
        return selector.value;
    }
    return localStorage.getItem("weboop_current_student") || "zhasulan";
}

const STORAGE_PREFIX = `weboop_w${ACTIVE_WEEK}_draft_`;
const quizSelections = {};

/* ========================================================================= */
/* MODULE 2: UI NAVIGATION                                                   */
/* ========================================================================= */

/**
 * Switch active sub-tab: 'home' | 'theory' | 'practice' | 'quiz' | 'results'
 */
function switchSubTab(tabId) {
    // Cleanly exit any active fullscreens before switching main tab
    exitAllPracticeFullscreen();
    if (typeof closeUmlFullscreen === "function") {
        closeUmlFullscreen();
    }

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
    // Check if any practice card is currently in fullscreen Zen mode
    const isFullscreenActive = document.querySelector(".practice-task-card.practice-fullscreen-active") !== null;

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
        const isTarget = card.id === `practice-card-${taskId}`;
        if (isTarget) {
            card.classList.remove("hidden");
            if (isFullscreenActive) {
                card.classList.add("practice-fullscreen-active");
                card.scrollTop = 0;
                const btnLabel = document.getElementById(`fullscreen-btn-label-${taskId}`);
                if (btnLabel) btnLabel.textContent = "✕ Обычный вид";
            } else {
                card.classList.remove("practice-fullscreen-active");
            }
        } else {
            card.classList.add("hidden");
            card.classList.remove("practice-fullscreen-active");
            const otherId = card.id.replace("practice-card-", "");
            const btnLabel = document.getElementById(`fullscreen-btn-label-${otherId}`);
            if (btnLabel) btnLabel.textContent = "⛶ На весь экран";
        }
    });

    // Body overflow must be hidden ONLY if fullscreen is actively engaged
    if (isFullscreenActive) {
        document.body.classList.add("overflow-hidden");
    } else {
        document.body.classList.remove("overflow-hidden");
    }

    // Refresh line numbers gutter
    if (typeof updateLineNumbers === "function") {
        updateLineNumbers(taskId);
    }
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

/**
 * Apply header collapse state and persist to localStorage
 */
function applyHeaderCollapseState(isCollapsed) {
    const header = document.getElementById("main-site-header");
    const label = document.getElementById("header-collapse-label");
    if (!header) return;

    if (isCollapsed) {
        header.classList.add("header-collapsed");
        if (label) label.textContent = "▼ Развернуть меню";
    } else {
        header.classList.remove("header-collapsed");
        if (label) label.textContent = "▲ Свернуть меню";
    }
}

/**
 * Toggle collapsible top navigation header
 */
function toggleHeaderCollapse() {
    const header = document.getElementById("main-site-header");
    if (!header) return;
    const willCollapse = !header.classList.contains("header-collapsed");
    applyHeaderCollapseState(willCollapse);
    localStorage.setItem("weboop_header_collapsed", willCollapse ? "1" : "0");
}

/* ========================================================================= */
/* MODULE 3: STUDENT PROFILE SWITCHER                                        */
/* ========================================================================= */

/**
 * Handle student profile selection switch
 */
function onStudentChange(newStudentUsername) {
    localStorage.setItem("weboop_current_student", newStudentUsername);
    const url = new URL(window.location.href);
    url.searchParams.set("student", newStudentUsername);
    window.location.href = url.toString();
}

/* ========================================================================= */
/* MODULE 4: CODE TRAINER, IDE CONTROLS & RUNNER TRANSPORT                   */
/* ========================================================================= */

let currentEditorFontSize = parseInt(localStorage.getItem("weboop_editor_font_size") || "14", 10);
if (Number.isNaN(currentEditorFontSize) || currentEditorFontSize < 12 || currentEditorFontSize > 20) {
    currentEditorFontSize = 14;
}

/**
 * Recalculate and render line numbers (1..N) and live line counter for a task editor
 */
function updateLineNumbers(taskId) {
    const editor = document.getElementById(`editor-${taskId}`);
    const gutter = document.getElementById(`line-numbers-${taskId}`);
    const countLabel = document.getElementById(`line-count-label-${taskId}`);
    if (!editor) return;

    const linesCount = Math.max(1, editor.value.split("\n").length);
    if (gutter) {
        const numbers = [];
        for (let i = 1; i <= linesCount; i += 1) {
            numbers.push(i);
        }
        gutter.textContent = numbers.join("\n");
        gutter.scrollTop = editor.scrollTop;
    }
    if (countLabel) {
        countLabel.textContent = `Строк: ${linesCount}`;
    }
}

/**
 * Apply font size (12px..20px) to all code editors and line number gutters
 */
function applyEditorFontSize(sizePx) {
    const clamped = Math.min(20, Math.max(12, sizePx));
    currentEditorFontSize = clamped;
    localStorage.setItem("weboop_editor_font_size", String(clamped));

    document.querySelectorAll(".code-editor-textarea, .line-numbers-gutter").forEach((el) => {
        el.style.fontSize = `${clamped}px`;
    });

    document.querySelectorAll(".editor-fontsize-label").forEach((lbl) => {
        lbl.textContent = `${clamped}px`;
    });
}

/**
 * Increase or decrease code editor font size by delta (-1 or +1)
 */
function changeEditorFontSize(delta) {
    applyEditorFontSize(currentEditorFontSize + delta);
}

/**
 * Set split width ratio (25%..65%) between task description pane and code editor pane
 */
function setPracticeSplitRatio(taskId, ratioPercent) {
    const clamped = Math.min(65, Math.max(25, Math.round(ratioPercent)));
    localStorage.setItem("weboop_split_width", String(clamped));

    document.querySelectorAll(".practice-task-pane").forEach((pane) => {
        if (window.innerWidth >= 1024) {
            pane.style.width = `${clamped}%`;
        } else {
            pane.style.width = "";
        }
    });
}

/**
 * Toggle fullscreen Zen mode (100vw x 100vh) for a practice task card
 */
function togglePracticeFullscreen(taskId) {
    const card = document.getElementById(`practice-card-${taskId}`);
    const btnLabel = document.getElementById(`fullscreen-btn-label-${taskId}`);
    if (!card) return;

    const isEntering = !card.classList.contains("practice-fullscreen-active");

    document.querySelectorAll(".practice-task-card").forEach((otherCard) => {
        otherCard.classList.remove("practice-fullscreen-active");
    });
    document.querySelectorAll("[id^='fullscreen-btn-label-']").forEach((lbl) => {
        lbl.textContent = "⛶ На весь экран";
    });

    if (isEntering) {
        card.classList.add("practice-fullscreen-active");
        if (btnLabel) btnLabel.textContent = "✕ Обычный вид";
        document.body.classList.add("overflow-hidden");
    } else {
        card.classList.remove("practice-fullscreen-active");
        if (btnLabel) btnLabel.textContent = "⛶ На весь экран";
        document.body.classList.remove("overflow-hidden");
    }
}

/**
 * Exit fullscreen mode for any active practice card
 */
function exitAllPracticeFullscreen() {
    document.querySelectorAll(".practice-task-card").forEach((card) => {
        card.classList.remove("practice-fullscreen-active");
    });
    document.querySelectorAll("[id^='fullscreen-btn-label-']").forEach((lbl) => {
        lbl.textContent = "⛶ На весь экран";
    });
    document.body.classList.remove("overflow-hidden");
}

/**
 * Toggle terminal execution output box height (compact 150px vs spacious 360px)
 */
function toggleTerminalSize(taskId) {
    const pre = document.getElementById(`output-pre-${taskId}`);
    if (!pre) return;
    if (pre.style.height === "360px") {
        pre.style.height = "150px";
    } else {
        pre.style.height = "360px";
    }
}

/**
 * Initialize interactive drag-splitter between task description and code editor
 */
function initPracticeSplitResizers() {
    let activeResizer = null;
    let activeLayout = null;
    let activeTaskId = null;

    document.querySelectorAll(".practice-split-resizer").forEach((resizer) => {
        resizer.addEventListener("mousedown", (e) => {
            if (window.innerWidth < 1024) return;
            e.preventDefault();
            activeResizer = resizer;
            activeTaskId = resizer.dataset.task;
            activeLayout = document.getElementById(`split-layout-${activeTaskId}`);
            resizer.classList.add("resizer-dragging");
            document.body.style.userSelect = "none";
            document.body.style.cursor = "col-resize";
        });
    });

    window.addEventListener("mousemove", (e) => {
        if (!activeResizer || !activeLayout || !activeTaskId) return;
        const rect = activeLayout.getBoundingClientRect();
        if (rect.width <= 0) return;
        const relativeX = e.clientX - rect.left;
        const ratio = (relativeX / rect.width) * 100;
        setPracticeSplitRatio(activeTaskId, ratio);
    });

    window.addEventListener("mouseup", () => {
        if (!activeResizer) return;
        activeResizer.classList.remove("resizer-dragging");
        activeResizer = null;
        activeLayout = null;
        activeTaskId = null;
        document.body.style.userSelect = "";
        document.body.style.cursor = "";
    });

    window.addEventListener("resize", () => {
        const savedSplit = parseInt(localStorage.getItem("weboop_split_width") || "42", 10);
        document.querySelectorAll(".practice-task-pane").forEach((pane) => {
            if (window.innerWidth >= 1024) {
                pane.style.width = `${Math.min(65, Math.max(25, savedSplit))}%`;
            } else {
                pane.style.width = "";
            }
        });
    });
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
        updateLineNumbers(taskId);
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
    updateLineNumbers(taskId);
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

    const activeStudent = getActiveStudent();

    try {
        const res = await fetch(`/api/week${ACTIVE_WEEK}/practice/${taskId}/run`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Student-Id": activeStudent,
            },
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

/* ========================================================================= */
/* MODULE 5: QUIZ STATE & EVALUATION                                         */
/* ========================================================================= */

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

    const activeStudent = getActiveStudent();

    try {
        const res = await fetch(`/api/week${ACTIVE_WEEK}/quiz/check`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Student-Id": activeStudent,
            },
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

/* ========================================================================= */
/* MODULE 6: THEORY COMPLETION TRANSPORT                                     */
/* ========================================================================= */

/**
 * Mark lecture theory as completed for the active week
 */
async function completeTheory(weekNum) {
    const btn = document.getElementById("btn-complete-theory");
    if (!btn) return;

    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = "<span>⏳ Сохранение...</span>";

    const activeStudent = getActiveStudent();

    try {
        const res = await fetch(`/api/week${weekNum}/theory/complete`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Student-Id": activeStudent,
            },
        });
        const data = await res.json();
        if (data.status === "COMPLETED") {
            btn.className =
                "px-5 py-2.5 rounded-xl text-xs font-bold transition bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
            btn.innerHTML = "✅ Теория прочитана";
        }
        if (data.progress) {
            updateProgressUI(data.progress);
        }
    } catch (err) {
        console.error("Error completing theory:", err);
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

/* ========================================================================= */
/* MODULE 7: LIVE UI PROGRESS SYNC                                           */
/* ========================================================================= */

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

/* ========================================================================= */
/* MODULE 8: INITIALIZATION                                                  */
/* ========================================================================= */

document.addEventListener("DOMContentLoaded", () => {
    // Sync student selector with current URL or localStorage
    const currentStudent = getActiveStudent();
    const selector = document.getElementById("student-selector");
    if (selector && currentStudent) {
        selector.value = currentStudent;
    }

    // Restore saved collapsible header state
    const savedHeaderCollapsed = localStorage.getItem("weboop_header_collapsed") === "1";
    applyHeaderCollapseState(savedHeaderCollapsed);

    // Restore saved editor font size
    applyEditorFontSize(currentEditorFontSize);

    // Restore saved split width ratio and initialize resizers
    const savedSplitRatio = parseInt(localStorage.getItem("weboop_split_width") || "42", 10);
    if (!Number.isNaN(savedSplitRatio)) {
        setPracticeSplitRatio("", savedSplitRatio);
    }
    initPracticeSplitResizers();

    // Initialize code editor textareas & line number gutters
    document.querySelectorAll(".code-editor-textarea").forEach((textarea) => {
        const taskId = textarea.dataset.task;
        const saved = localStorage.getItem(`${STORAGE_PREFIX}${taskId}`);
        if (saved && saved.trim().length > 0) {
            textarea.value = saved;
        }

        updateLineNumbers(taskId);

        textarea.addEventListener("input", () => {
            localStorage.setItem(`${STORAGE_PREFIX}${taskId}`, textarea.value);
            updateLineNumbers(taskId);
        });

        textarea.addEventListener("scroll", () => {
            const gutter = document.getElementById(`line-numbers-${taskId}`);
            if (gutter) {
                gutter.scrollTop = textarea.scrollTop;
            }
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
                updateLineNumbers(taskId);
            }
        });
    });

    // Global Escape listener to exit practice fullscreen mode
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            exitAllPracticeFullscreen();
        }
    });

    // Initialize UML Viewer & Magnifier Lens listeners
    initUmlViewer();
});

/* ========================================================================= */
/* MODULE 9: UML DIAGRAM VIEWER & MAGNIFIER LENS (ЛУПА)                      */
/* ========================================================================= */

let umlLensActive = false;
let currentUmlTab = ACTIVE_WEEK === "3" ? "week3" : (ACTIVE_WEEK === "2" ? "week2" : "week1");
let modalZoomScale = 1.0;
let modalPanX = 0;
let modalPanY = 0;
let isModalPanning = false;
let panStartX = 0;
let panStartY = 0;

/**
 * Quick jump from any tab/header to the UML diagram section in Theory
 */
function openUmlDiagramSection() {
    switchSubTab("theory");
    setTimeout(() => {
        const sec = document.getElementById("uml-diagram-section");
        if (sec) {
            sec.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }, 150);
}

/**
 * Switch between Week Domain, Platform Architecture, and DB ERD diagrams
 */
function switchUmlDiagramTab(tabKey) {
    currentUmlTab = tabKey;

    document.querySelectorAll(".uml-tab-btn").forEach((btn) => {
        const isCurrent = btn.dataset.diagramTab === tabKey;
        if (isCurrent) {
            btn.className =
                "uml-tab-btn px-4 py-2 rounded-xl font-bold transition shrink-0 bg-sky-500/20 text-sky-300 border border-sky-500/50 shadow-[0_0_12px_rgba(56,189,248,0.2)]";
        } else {
            btn.className =
                "uml-tab-btn px-4 py-2 rounded-xl font-medium transition shrink-0 bg-slate-900 text-slate-400 border border-slate-800 hover:text-slate-200";
        }
    });

    // Hide all panes
    document.querySelectorAll(".uml-diagram-pane").forEach((pane) => pane.classList.add("hidden"));

    // Show selected pane
    if (tabKey === "week1") {
        const pane = document.getElementById("uml-diagram-week1");
        if (pane) pane.classList.remove("hidden");
    } else if (tabKey === "week2") {
        const pane = document.getElementById("uml-diagram-week2");
        if (pane) pane.classList.remove("hidden");
    } else if (tabKey === "week3") {
        const pane = document.getElementById("uml-diagram-week3");
        if (pane) pane.classList.remove("hidden");
    } else if (tabKey === "week") {
        const activeWeekId = ACTIVE_WEEK === "3" ? "uml-diagram-week3" : (ACTIVE_WEEK === "2" ? "uml-diagram-week2" : "uml-diagram-week1");
        const pane = document.getElementById(activeWeekId);
        if (pane) pane.classList.remove("hidden");
    } else if (tabKey === "arch") {
        const pane = document.getElementById("uml-diagram-arch");
        if (pane) pane.classList.remove("hidden");
    } else if (tabKey === "db") {
        const pane = document.getElementById("uml-diagram-db");
        if (pane) pane.classList.remove("hidden");
    }

    // Refresh lens content if lens is active
    if (umlLensActive) {
        syncUmlLensContent();
    }
}

/**
 * Toggle the interactive hovering magnifier lens
 */
function toggleUmlLens() {
    umlLensActive = !umlLensActive;
    const btn = document.getElementById("btn-toggle-lens");
    const btnText = document.getElementById("btn-toggle-lens-text");
    const hint = document.getElementById("uml-mode-hint");
    const lens = document.getElementById("uml-lens");
    const viewport = document.getElementById("uml-viewport");

    if (umlLensActive) {
        if (btn) {
            btn.className =
                "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-cyan-500/20 text-cyan-300 border border-cyan-400 shadow-[0_0_20px_rgba(0,240,255,0.4)]";
        }
        if (btnText) btnText.textContent = "Выключить лупу";
        if (hint) hint.textContent = "🔍 Лупа активна: ведите курсор по диаграмме для увеличения 2.5×.";
        if (viewport) viewport.classList.add("lens-active");
        syncUmlLensContent();
    } else {
        if (btn) {
            btn.className =
                "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-slate-900 hover:bg-slate-800 text-sky-300 border border-sky-500/40 shadow-[0_0_15px_rgba(56,189,248,0.15)]";
        }
        if (btnText) btnText.textContent = "Включить лупу";
        if (hint) hint.textContent = "Нажмите «Включить лупу» или дважды кликните по диаграмме для зума.";
        if (lens) lens.classList.add("hidden");
        if (viewport) viewport.classList.remove("lens-active");
    }
}

/**
 * Clone active SVG into the circular lens container
 */
function syncUmlLensContent() {
    const lensContent = document.getElementById("uml-lens-content");
    const viewport = document.getElementById("uml-viewport");
    if (!lensContent || !viewport) return;

    // Find currently visible SVG
    const visiblePane = document.querySelector(".uml-diagram-pane:not(.hidden)");
    if (!visiblePane) return;
    const svg = visiblePane.querySelector("svg");
    if (!svg) return;

    lensContent.innerHTML = "";
    const clonedSvg = svg.cloneNode(true);
    clonedSvg.removeAttribute("id");
    clonedSvg.style.width = `${viewport.clientWidth}px`;
    clonedSvg.style.height = `${viewport.clientHeight}px`;
    clonedSvg.style.maxWidth = "none";
    clonedSvg.style.maxHeight = "none";
    lensContent.appendChild(clonedSvg);
}

/**
 * Initialize hovering magnifier lens tracking on the viewport
 */
function initUmlViewer() {
    const viewport = document.getElementById("uml-viewport");
    const lens = document.getElementById("uml-lens");
    const lensContent = document.getElementById("uml-lens-content");
    if (!viewport || !lens || !lensContent) return;

    const handlePointerMove = (e) => {
        if (!umlLensActive) return;

        const rect = viewport.getBoundingClientRect();
        const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
        const clientY = e.clientY || (e.touches && e.touches[0] ? e.touches[0].clientY : 0);

        const x = clientX - rect.left;
        const y = clientY - rect.top;

        // Check if pointer is within bounds
        if (x < 0 || x > rect.width || y < 0 || y > rect.height) {
            lens.classList.add("hidden");
            return;
        }

        lens.classList.remove("hidden");
        lens.style.left = `${x}px`;
        lens.style.top = `${y}px`;

        // Lens radius is 96px (192px / 2). Magnification factor = 2.5
        const zoom = 2.5;
        const lensRadius = 96;
        const tx = -(x * zoom - lensRadius);
        const ty = -(y * zoom - lensRadius);

        lensContent.style.transform = `translate(${tx}px, ${ty}px) scale(${zoom})`;
    };

    viewport.addEventListener("mousemove", handlePointerMove);
    viewport.addEventListener("touchmove", handlePointerMove, { passive: true });

    viewport.addEventListener("mouseleave", () => {
        if (umlLensActive) lens.classList.add("hidden");
    });

    viewport.addEventListener("touchend", () => {
        if (umlLensActive) lens.classList.add("hidden");
    });

    window.addEventListener("resize", () => {
        if (umlLensActive) syncUmlLensContent();
    });

    // Close modal on Escape
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeUmlFullscreen();
        }
    });

    // Setup modal drag listeners on window for smooth panning
    window.addEventListener("mousemove", (e) => {
        if (!isModalPanning) return;
        modalPanX = e.clientX - panStartX;
        modalPanY = e.clientY - panStartY;
        applyUmlModalTransform();
    });

    window.addEventListener("mouseup", () => {
        if (isModalPanning) {
            isModalPanning = false;
            const wrapper = document.getElementById("uml-modal-canvas-wrapper");
            if (wrapper) {
                wrapper.classList.remove("cursor-grabbing");
                wrapper.classList.add("cursor-grab");
            }
        }
    });
}

/**
 * Open Fullscreen Modal with Zoom & Pan Controls
 */
function openUmlFullscreen() {
    const modal = document.getElementById("uml-fullscreen-modal");
    const modalContent = document.getElementById("uml-modal-content");
    const modalTitle = document.getElementById("uml-modal-title");
    if (!modal || !modalContent) return;

    // Determine title
    let title = "UML-диаграмма классов: Неделя 1 (Инкапсуляция SmartCard)";
    if (currentUmlTab === "week3" || (currentUmlTab === "week" && ACTIVE_WEEK === "3")) {
        title = "UML-диаграмма классов: Неделя 3 (Паттерны GoF и Clean Architecture)";
    } else if (currentUmlTab === "week2" || (currentUmlTab === "week" && ACTIVE_WEEK === "2")) {
        title = "UML-диаграмма классов: Неделя 2 (SOLID & Dependency Injection)";
    } else if (currentUmlTab === "arch") {
        title = "Архитектура платформы Web-OOP (WeekModule & Services)";
    } else if (currentUmlTab === "db") {
        title = "ER-диаграмма базы данных (SQLite: Student, Progress, Submissions)";
    }
    if (modalTitle) modalTitle.textContent = title;

    // Find visible SVG and clone into modal
    const visiblePane = document.querySelector(".uml-diagram-pane:not(.hidden)");
    if (visiblePane) {
        const svg = visiblePane.querySelector("svg");
        if (svg) {
            modalContent.innerHTML = "";
            const cloned = svg.cloneNode(true);
            cloned.removeAttribute("id");
            cloned.style.width = "90vw";
            cloned.style.height = "75vh";
            cloned.style.maxWidth = "none";
            cloned.style.maxHeight = "none";
            modalContent.appendChild(cloned);
        }
    }

    // Reset zoom and pan
    modalZoomScale = 1.0;
    modalPanX = 0;
    modalPanY = 0;
    applyUmlModalTransform();

    modal.classList.remove("hidden");
    document.body.classList.add("overflow-hidden");
}

/**
 * Close Fullscreen Modal
 */
function closeUmlFullscreen() {
    const modal = document.getElementById("uml-fullscreen-modal");
    if (modal) {
        modal.classList.add("hidden");
        document.body.classList.remove("overflow-hidden");
    }
}

/**
 * Change modal zoom scale
 */
function zoomUmlModal(delta) {
    modalZoomScale = Math.min(Math.max(0.5, modalZoomScale + delta), 3.5);
    applyUmlModalTransform();
}

/**
 * Reset modal zoom to 100% and center pan
 */
function resetUmlModalZoom() {
    modalZoomScale = 1.0;
    modalPanX = 0;
    modalPanY = 0;
    applyUmlModalTransform();
}

/**
 * Mouse wheel zoom inside modal
 */
function onUmlWheel(e) {
    e.preventDefault();
    const delta = e.deltaY < 0 ? 0.15 : -0.15;
    zoomUmlModal(delta);
}

/**
 * Start mouse drag pan in modal
 */
function startUmlPan(e) {
    if (e.target.closest("button")) return;
    isModalPanning = true;
    panStartX = e.clientX - modalPanX;
    panStartY = e.clientY - modalPanY;

    const wrapper = document.getElementById("uml-modal-canvas-wrapper");
    if (wrapper) {
        wrapper.classList.remove("cursor-grab");
        wrapper.classList.add("cursor-grabbing");
    }
}

/**
 * Apply transform to modal content
 */
function applyUmlModalTransform() {
    const content = document.getElementById("uml-modal-content");
    const label = document.getElementById("uml-modal-zoom-label");
    const ind = document.getElementById("uml-scale-indicator");

    const percent = Math.round(modalZoomScale * 100);
    if (label) label.textContent = `${percent}%`;
    if (ind) ind.textContent = `${percent}%`;

    if (content) {
        content.style.transform = `translate(${modalPanX}px, ${modalPanY}px) scale(${modalZoomScale})`;
    }
}

