const state = {
  lessons: [],
  languages: [],
  target: localStorage.getItem("racketTutor.targetLanguage") || "racket",
  knownLanguages: readKnownLanguages(),
  activeDay: Number(localStorage.getItem("racketTutor.activeDay") || 1),
  query: "",
};

function accessHeaders() {
  const code = localStorage.getItem("racketTutor.accessCode");
  return code ? { "X-Access-Code": code } : {};
}

const els = {
  dayList: document.querySelector("#dayList"),
  onboardingPanel: document.querySelector("#onboardingPanel"),
  continueFromExperience: document.querySelector("#continueFromExperience"),
  languageExperienceInputs: document.querySelectorAll("[data-language-experience]"),
  brandSubtitle: document.querySelector("#brandSubtitle"),
  languagePicker: document.querySelector(".language-picker"),
  languageSelect: document.querySelector("#languageSelect"),
  resetPrerequisite: document.querySelector("#resetPrerequisite"),
  cppTrackNotice: document.querySelector("#cppTrackNotice"),
  markCppKnown: document.querySelector("#markCppKnown"),
  progressBlock: document.querySelector(".progress-block"),
  searchBox: document.querySelector(".search-box"),
  searchInput: document.querySelector("#searchInput"),
  progressText: document.querySelector("#progressText"),
  progressFill: document.querySelector("#progressFill"),
  weekLabel: document.querySelector("#weekLabel"),
  lessonTitle: document.querySelector("#lessonTitle"),
  prevDay: document.querySelector("#prevDay"),
  nextDay: document.querySelector("#nextDay"),
  categoryLabel: document.querySelector("#categoryLabel"),
  goalTitle: document.querySelector("#goalTitle"),
  goalText: document.querySelector("#goalText"),
  dayMetric: document.querySelector("#dayMetric"),
  checkMetric: document.querySelector("#checkMetric"),
  weekMetric: document.querySelector("#weekMetric"),
  cppBridge: document.querySelector("#cppBridge"),
  bridgeEyebrow: document.querySelector("#bridgeEyebrow"),
  bridgeConcept: document.querySelector("#bridgeConcept"),
  bridgeAngle: document.querySelector("#bridgeAngle"),
  cppSyntaxBlock: document.querySelector("#cppSyntaxBlock"),
  targetSyntaxLabel: document.querySelector("#targetSyntaxLabel"),
  targetSyntaxBlock: document.querySelector("#targetSyntaxBlock"),
  translationSteps: document.querySelector("#translationSteps"),
  pitfallList: document.querySelector("#pitfallList"),
  bridgeDrill: document.querySelector("#bridgeDrill"),
  docsList: document.querySelector("#docsList"),
  explanation: document.querySelector("#explanation"),
  focusList: document.querySelector("#focusList"),
  codeBlock: document.querySelector("#codeBlock"),
  lineNotesEyebrow: document.querySelector("#lineNotesEyebrow"),
  lineNotesPanel: document.querySelector("#lineNotesPanel"),
  lineNotesList: document.querySelector("#lineNotesList"),
  copyCode: document.querySelector("#copyCode"),
  practiceList: document.querySelector("#practiceList"),
  checklist: document.querySelector("#checklist"),
  resetChecklist: document.querySelector("#resetChecklist"),
  assignmentText: document.querySelector("#assignmentText"),
  rubricList: document.querySelector("#rubricList"),
  submissionForm: document.querySelector("#submissionForm"),
  submitButton: document.querySelector("#submitButton"),
  feedbackBox: document.querySelector("#feedbackBox"),
  refreshSubmissions: document.querySelector("#refreshSubmissions"),
  submissionList: document.querySelector("#submissionList"),
};

function readKnownLanguages() {
  const raw = localStorage.getItem("racketTutor.knownLanguages");
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }
  const legacyStatus = localStorage.getItem("racketTutor.cppStatus");
  if (legacyStatus === "knows_cpp") return ["cpp"];
  if (legacyStatus === "needs_cpp") return [];
  return [];
}

function writeKnownLanguages(values) {
  const unique = [...new Set(values)];
  state.knownLanguages = unique;
  localStorage.setItem("racketTutor.knownLanguages", JSON.stringify(unique));
  localStorage.setItem("racketTutor.cppStatus", unique.includes("cpp") ? "knows_cpp" : "needs_cpp");
}

function padDay(day) {
  return String(day).padStart(2, "0");
}

function checklistKey(day) {
  return `racketTutor.checklist.${state.target}.${day}`;
}

function readChecklist(day) {
  const raw = localStorage.getItem(checklistKey(day));
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function writeChecklist(day, values) {
  localStorage.setItem(checklistKey(day), JSON.stringify(values));
}

function checkedCount(day) {
  return readChecklist(day).filter(Boolean).length;
}

function activeLesson() {
  return state.lessons.find((lesson) => lesson.day === state.activeDay) || state.lessons[0];
}

function isCppFoundationMode() {
  return state.knownLanguages.length > 0 && !state.knownLanguages.includes("cpp");
}

function hasExperienceProfile() {
  return localStorage.getItem("racketTutor.knownLanguages") !== null || localStorage.getItem("racketTutor.cppStatus") !== null;
}

function setMainContentHidden(hidden) {
  document.querySelector(".topbar").hidden = hidden;
  document.querySelector(".lesson-layout").hidden = hidden;
}

function renderOnboarding() {
  const needsChoice = !hasExperienceProfile();
  for (const input of els.languageExperienceInputs || []) {
    input.checked = state.knownLanguages.includes(input.value);
  }
  if (els.onboardingPanel) {
    els.onboardingPanel.hidden = !needsChoice;
  }
  setMainContentHidden(needsChoice);
  for (const item of [els.progressBlock, els.searchBox, els.dayList]) {
    if (item) item.hidden = needsChoice;
  }
  if (els.languagePicker) {
    els.languagePicker.hidden = needsChoice || isCppFoundationMode();
  }
  if (els.cppTrackNotice) {
    els.cppTrackNotice.hidden = needsChoice || !isCppFoundationMode();
  }
}

function setCppStatus(status) {
  const current = new Set(state.knownLanguages);
  if (status === "knows_cpp") {
    current.add("cpp");
  } else {
    current.delete("cpp");
  }
  writeKnownLanguages([...current]);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");

  if (!state.knownLanguages.includes("cpp")) {
    state.target = "cpp";
  } else if (state.target === "cpp") {
    state.target = "racket";
  }
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  renderOnboarding();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
}

function resetPrerequisiteChoice() {
  state.knownLanguages = [];
  localStorage.removeItem("racketTutor.knownLanguages");
  localStorage.removeItem("racketTutor.cppStatus");
  renderOnboarding();
}

function chooseDefaultTarget() {
  const known = new Set(state.knownLanguages);
  const candidates = ["racket", "python", "java", "c"];
  return candidates.find((id) => !known.has(id)) || "racket";
}

function continueFromLanguageExperience() {
  const selected = [...els.languageExperienceInputs].filter((input) => input.checked).map((input) => input.value);
  writeKnownLanguages(selected);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");
  state.target = selected.includes("cpp") ? chooseDefaultTarget() : "cpp";
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  renderOnboarding();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
}

function renderDayList() {
  const query = state.query.trim().toLowerCase();
  const lessons = state.lessons.filter((lesson) => {
    if (!query) return true;
    return [
      lesson.day,
      lesson.category,
      lesson.title,
      lesson.goal,
      lesson.syntax_bridge?.concept || "",
      lesson.syntax_bridge?.today_angle || "",
      lesson.syntax_bridge?.docs?.map((doc) => doc.title).join(" ") || "",
      lesson.racket_focus.join(" "),
      lesson.target_language_name || "",
    ]
      .join(" ")
      .toLowerCase()
      .includes(query);
  });

  els.dayList.innerHTML = "";
  for (const lesson of lessons) {
    const done = checkedCount(lesson.day) === lesson.checklist.length;
    const button = document.createElement("button");
    button.type = "button";
    button.className = `day-card${lesson.day === state.activeDay ? " active" : ""}`;
    button.innerHTML = `
      <span class="day-number">${padDay(lesson.day)}</span>
      <span>
        <strong>${lesson.title}</strong>
        <span>${lesson.category}</span>
      </span>
      <span class="done-dot${done ? " complete" : ""}" aria-hidden="true"></span>
    `;
    button.addEventListener("click", () => selectDay(lesson.day));
    els.dayList.appendChild(button);
  }
}

function renderProgress() {
  const total = state.lessons.reduce((sum, lesson) => sum + lesson.checklist.length, 0);
  const done = state.lessons.reduce((sum, lesson) => sum + checkedCount(lesson.day), 0);
  els.progressText.textContent = `${done} / ${total}`;
  els.progressFill.style.width = total ? `${Math.round((done / total) * 100)}%` : "0%";
}

function renderLesson() {
  const lesson = activeLesson();
  if (!lesson) return;

  const checks = readChecklist(lesson.day);
  const done = checks.filter(Boolean).length;

  localStorage.setItem("racketTutor.activeDay", String(lesson.day));
  els.weekLabel.textContent = `Week ${lesson.week}`;
  document.title = `${lesson.target_language_name || "Racket"} Tutor AI`;
  document.querySelector(".brand h1").textContent = `${lesson.target_language_name || "Code"} Tutor AI`;
  if (els.brandSubtitle) {
    els.brandSubtitle.textContent = isCppFoundationMode()
      ? "C++ Foundations · prerequisite track · 56 days"
      : `C++ foundation to ${lesson.target_language_name || "target language"} · 56 days`;
  }
  els.lessonTitle.textContent = lesson.title;
  els.categoryLabel.textContent = lesson.category;
  els.goalTitle.textContent = lesson.title;
  els.goalText.textContent = lesson.goal;
  els.dayMetric.textContent = padDay(lesson.day);
  els.checkMetric.textContent = `${done}/${lesson.checklist.length}`;
  els.weekMetric.textContent = lesson.week;
  els.cppBridge.textContent = lesson.cpp_bridge;
  renderSyntaxBridge(lesson);
  els.explanation.textContent = lesson.explanation;
  els.codeBlock.textContent = lesson.code;
  renderLineNotes(lesson);
  els.assignmentText.textContent = lesson.assignment;

  els.prevDay.disabled = lesson.day === 1;
  els.nextDay.disabled = lesson.day === state.lessons.length;

  els.focusList.innerHTML = "";
  for (const focus of lesson.racket_focus) {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = focus;
    els.focusList.appendChild(tag);
  }

  els.practiceList.innerHTML = "";
  for (const item of lesson.practice) {
    const li = document.createElement("li");
    li.textContent = item;
    els.practiceList.appendChild(li);
  }

  els.rubricList.innerHTML = "";
  for (const item of lesson.grading_rubric) {
    const li = document.createElement("li");
    li.textContent = item;
    els.rubricList.appendChild(li);
  }

  renderChecklist(lesson);
  renderDayList();
  renderProgress();
}

function renderSyntaxBridge(lesson) {
  const bridge = lesson.syntax_bridge;
  if (!bridge) return;
  const targetName = lesson.target_language_name || bridge.target_label || "Target";

  els.bridgeEyebrow.textContent = `C++ Syntax → ${targetName} Syntax`;
  els.bridgeConcept.textContent = bridge.concept;
  els.bridgeAngle.textContent = bridge.today_angle;
  els.cppSyntaxBlock.textContent = bridge.cpp;
  els.targetSyntaxLabel.textContent = `${targetName} Syntax`;
  els.targetSyntaxBlock.textContent = bridge.target || bridge.racket;
  els.bridgeDrill.textContent = bridge.drill;

  els.translationSteps.innerHTML = "";
  for (const step of bridge.translation_steps) {
    const li = document.createElement("li");
    li.textContent = step;
    els.translationSteps.appendChild(li);
  }

  els.pitfallList.innerHTML = "";
  for (const pitfall of bridge.pitfalls) {
    const li = document.createElement("li");
    li.textContent = pitfall;
    els.pitfallList.appendChild(li);
  }

  els.docsList.innerHTML = "";
  for (const doc of bridge.docs || lesson.official_docs || []) {
    const link = document.createElement("a");
    link.href = doc.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = doc.title;
    els.docsList.appendChild(link);
  }
}

function renderLineNotes(lesson) {
  const notes = lesson.line_notes || [];
  const show = notes.length > 0;
  els.lineNotesPanel.hidden = !show;
  els.lineNotesList.innerHTML = "";
  if (!show) return;
  els.lineNotesEyebrow.textContent = `${lesson.target_language_name || "Code"} Line-by-Line Syntax`;

  notes.forEach((note, index) => {
    const row = document.createElement("article");
    row.className = "line-note";
    const codeText = note.line || "Blank line";
    row.innerHTML = `
      <div class="line-note-index">L${index + 1}</div>
      <div class="line-note-body">
        <pre><code></code></pre>
        <p></p>
        <dl>
          <div><dt>Syntax</dt><dd></dd></div>
          <div><dt>C++ Comparison</dt><dd></dd></div>
        </dl>
      </div>
    `;
    row.querySelector("code").textContent = codeText;
    row.querySelector("p").textContent = note.plain;
    const descriptions = row.querySelectorAll("dd");
    descriptions[0].textContent = note.syntax;
    descriptions[1].textContent = note.cpp;
    els.lineNotesList.appendChild(row);
  });
}

function renderChecklist(lesson) {
  const values = readChecklist(lesson.day);
  els.checklist.innerHTML = "";

  lesson.checklist.forEach((item, index) => {
    const id = `day-${lesson.day}-check-${index}`;
    const label = document.createElement("label");
    label.className = `check-item${values[index] ? " done" : ""}`;
    label.htmlFor = id;

    const input = document.createElement("input");
    input.id = id;
    input.type = "checkbox";
    input.checked = Boolean(values[index]);
    input.addEventListener("change", () => {
      const next = readChecklist(lesson.day);
      next[index] = input.checked;
      writeChecklist(lesson.day, next);
      renderLesson();
    });

    const span = document.createElement("span");
    span.textContent = item;

    label.append(input, span);
    els.checklist.appendChild(label);
  });
}

function selectDay(day) {
  state.activeDay = Math.max(1, Math.min(day, state.lessons.length));
  renderLesson();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function loadCourse() {
  if (!hasExperienceProfile()) {
    renderOnboarding();
    return;
  }
  if (isCppFoundationMode()) {
    state.target = "cpp";
    localStorage.setItem("racketTutor.targetLanguage", state.target);
  }
  const response = await fetch(`/api/course?target=${encodeURIComponent(state.target)}`, { headers: accessHeaders() });
  if (response.status === 401) {
    window.location.href = "/";
    return;
  }
  if (!response.ok) throw new Error("Course data failed to load");
  const data = await response.json();
  state.languages = data.languages || state.languages;
  state.target = data.target || state.target;
  state.lessons = data.lessons;
  renderOnboarding();
  renderLanguageOptions();
  if (!state.lessons.some((lesson) => lesson.day === state.activeDay)) {
    state.activeDay = 1;
  }
  renderLesson();
}

function renderLanguageOptions() {
  if (!els.languageSelect || !state.languages.length) return;
  els.languageSelect.innerHTML = "";
  for (const language of state.languages) {
    if (language.id === "cpp") continue;
    const option = document.createElement("option");
    option.value = language.id;
    option.textContent = language.name;
    option.selected = language.id === state.target;
    els.languageSelect.appendChild(option);
  }
}

async function loadSubmissions() {
  const response = await fetch("/api/submissions", { headers: accessHeaders() });
  if (!response.ok) return;
  const data = await response.json();
  els.submissionList.innerHTML = "";

  if (!data.submissions.length) {
    const empty = document.createElement("p");
    empty.className = "body-text";
    empty.textContent = "No submissions yet.";
    els.submissionList.appendChild(empty);
    return;
  }

  data.submissions.slice(0, 12).forEach((item) => {
    const created = new Date(item.createdAt).toLocaleString();
    const div = document.createElement("div");
    div.className = "submission-item";
    div.innerHTML = `
      <strong>${item.targetLanguage || "Racket"} · Day ${padDay(item.day)} · ${item.title}</strong>
      <span>${item.studentName} · ${created}${item.filename ? ` · ${item.filename}` : ""}</span>
      <details>
        <summary>View feedback</summary>
        <pre></pre>
      </details>
    `;
    div.querySelector("pre").textContent = item.feedback;
    els.submissionList.appendChild(div);
  });
}

async function submitAssignment(event) {
  event.preventDefault();
  const lesson = activeLesson();
  const formData = new FormData(els.submissionForm);
  formData.set("day", lesson.day);
  formData.set("target", state.target);

  els.submitButton.disabled = true;
  els.submitButton.textContent = "Reviewing";
  els.feedbackBox.hidden = false;
  els.feedbackBox.classList.remove("error");
  els.feedbackBox.textContent = "Reading the assignment and generating feedback...";

  try {
    const response = await fetch("/api/submit", {
      method: "POST",
      headers: accessHeaders(),
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Submission failed");
    }
    els.feedbackBox.textContent = data.submission.feedback;
    els.submissionForm.reset();
    await loadSubmissions();
  } catch (error) {
    els.feedbackBox.classList.add("error");
    els.feedbackBox.textContent = error.message;
  } finally {
    els.submitButton.disabled = false;
    els.submitButton.textContent = "Submit and Review";
  }
}

els.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderDayList();
});

els.languageSelect.addEventListener("change", (event) => {
  state.target = event.target.value;
  if (!state.knownLanguages.includes("cpp")) {
    writeKnownLanguages([...state.knownLanguages, "cpp"]);
  }
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  state.activeDay = 1;
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
});

els.continueFromExperience.addEventListener("click", continueFromLanguageExperience);
els.resetPrerequisite.addEventListener("click", resetPrerequisiteChoice);
els.markCppKnown.addEventListener("click", () => setCppStatus("knows_cpp"));

els.prevDay.addEventListener("click", () => selectDay(state.activeDay - 1));
els.nextDay.addEventListener("click", () => selectDay(state.activeDay + 1));

els.copyCode.addEventListener("click", async () => {
  await navigator.clipboard.writeText(activeLesson().code);
  els.copyCode.textContent = "Copied";
  setTimeout(() => {
    els.copyCode.textContent = "Copy Code";
  }, 1200);
});

els.resetChecklist.addEventListener("click", () => {
  writeChecklist(state.activeDay, []);
  renderLesson();
});

els.submissionForm.addEventListener("submit", submitAssignment);
els.refreshSubmissions.addEventListener("click", loadSubmissions);

renderOnboarding();
if (hasExperienceProfile()) {
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
}
loadSubmissions();
