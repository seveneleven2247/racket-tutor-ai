const state = {
  lessons: [],
  languages: [],
  user: null,
  authMode: "register",
  profileLoaded: false,
  target: localStorage.getItem("racketTutor.targetLanguage") || "racket",
  knownLanguages: readKnownLanguages(),
  baseLanguage: localStorage.getItem("racketTutor.baseLanguage") || readKnownLanguages()[0] || "",
  languageExperienceChosen: localStorage.getItem("racketTutor.languageExperienceChosen") === "true"
    || localStorage.getItem("racketTutor.baseLanguage") !== null
    || localStorage.getItem("racketTutor.knownLanguages") !== null
    || localStorage.getItem("racketTutor.cppStatus") !== null,
  activeDay: Number(localStorage.getItem("racketTutor.activeDay") || 1),
  query: "",
  unlockedSampleCode: null,
  submittedLessons: new Set(),
  aiReviewEnabled: false,
};

function accessHeaders() {
  const code = localStorage.getItem("racketTutor.accessCode");
  return code ? { "X-Access-Code": code } : {};
}

const els = {
  dayList: document.querySelector("#dayList"),
  authPanel: document.querySelector("#authPanel"),
  authForm: document.querySelector("#authForm"),
  authName: document.querySelector("#authName"),
  authPassword: document.querySelector("#authPassword"),
  authSubmit: document.querySelector("#authSubmit"),
  authMessage: document.querySelector("#authMessage"),
  showRegister: document.querySelector("#showRegister"),
  showLogin: document.querySelector("#showLogin"),
  userPanel: document.querySelector("#userPanel"),
  userNameLabel: document.querySelector("#userNameLabel"),
  logoutButton: document.querySelector("#logoutButton"),
  onboardingPanel: document.querySelector("#onboardingPanel"),
  continueFromExperience: document.querySelector("#continueFromExperience"),
  languageExperienceInputs: document.querySelectorAll("[data-language-experience]"),
  noneExperience: document.querySelector("#noneExperience"),
  experienceMessage: document.querySelector("#experienceMessage"),
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
  unlockNotice: document.querySelector("#unlockNotice"),
  cppBridge: document.querySelector("#cppBridge"),
  bridgeEyebrow: document.querySelector("#bridgeEyebrow"),
  bridgeConcept: document.querySelector("#bridgeConcept"),
  bridgeAngle: document.querySelector("#bridgeAngle"),
  baseSyntaxLabel: document.querySelector("#baseSyntaxLabel"),
  cppSyntaxBlock: document.querySelector("#cppSyntaxBlock"),
  targetSyntaxLabel: document.querySelector("#targetSyntaxLabel"),
  targetSyntaxBlock: document.querySelector("#targetSyntaxBlock"),
  translationSteps: document.querySelector("#translationSteps"),
  pitfallList: document.querySelector("#pitfallList"),
  bridgeDrill: document.querySelector("#bridgeDrill"),
  docsList: document.querySelector("#docsList"),
  explanation: document.querySelector("#explanation"),
  focusList: document.querySelector("#focusList"),
  codePanel: document.querySelector("#codePanel"),
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
  aiReviewStatus: document.querySelector("#aiReviewStatus"),
  submissionForm: document.querySelector("#submissionForm"),
  submitButton: document.querySelector("#submitButton"),
  feedbackBox: document.querySelector("#feedbackBox"),
  refreshSubmissions: document.querySelector("#refreshSubmissions"),
  submissionList: document.querySelector("#submissionList"),
  feedbackButton: document.querySelector("#feedbackButton"),
  feedbackModal: document.querySelector("#feedbackModal"),
  closeFeedback: document.querySelector("#closeFeedback"),
  siteFeedbackForm: document.querySelector("#siteFeedbackForm"),
  feedbackCategory: document.querySelector("#feedbackCategory"),
  feedbackMessage: document.querySelector("#feedbackMessage"),
  sendFeedback: document.querySelector("#sendFeedback"),
  siteFeedbackStatus: document.querySelector("#siteFeedbackStatus"),
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
  const unique = [...new Set(values.filter((value) => value !== "none"))].slice(0, 1);
  state.knownLanguages = unique;
  state.baseLanguage = unique[0] || "";
  state.languageExperienceChosen = true;
  localStorage.setItem("racketTutor.knownLanguages", JSON.stringify(unique));
  localStorage.setItem("racketTutor.baseLanguage", state.baseLanguage);
  localStorage.setItem("racketTutor.languageExperienceChosen", "true");
  localStorage.setItem("racketTutor.cppStatus", state.baseLanguage ? "knows_cpp" : "needs_cpp");
}

function profilePayload() {
  return {
    knownLanguages: state.knownLanguages,
    baseLanguage: state.baseLanguage,
    languageExperienceChosen: state.languageExperienceChosen,
    targetLanguage: state.target,
    activeDay: state.activeDay,
    checklists: collectChecklistState(),
  };
}

function emptyProfilePayload() {
  return {
    knownLanguages: [],
    baseLanguage: "",
    languageExperienceChosen: false,
    targetLanguage: "racket",
    activeDay: 1,
    checklists: {},
  };
}

function collectChecklistState() {
  const checklists = {};
  for (let index = 0; index < localStorage.length; index += 1) {
    const key = localStorage.key(index);
    const prefix = "racketTutor.checklist.";
    if (!key || !key.startsWith(prefix)) continue;
    checklists[key.slice(prefix.length)] = JSON.parse(localStorage.getItem(key) || "[]");
  }
  return checklists;
}

let profileSaveTimer = null;

function scheduleProfileSave() {
  if (!state.user || !state.profileLoaded) return;
  clearTimeout(profileSaveTimer);
  profileSaveTimer = setTimeout(saveProfile, 350);
}

async function saveProfile() {
  if (!state.user) return;
  await fetch("/api/profile", {
    method: "POST",
    headers: { ...accessHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(profilePayload()),
  });
}

function applyProfile(profile) {
  if (!profile) return;
  const base = profile.baseLanguage || (profile.knownLanguages || [])[0] || "";
  if (profile.languageExperienceChosen) {
    writeKnownLanguages(base ? [base] : []);
  } else {
    state.knownLanguages = [];
    state.baseLanguage = "";
    state.languageExperienceChosen = false;
    localStorage.removeItem("racketTutor.knownLanguages");
    localStorage.removeItem("racketTutor.baseLanguage");
    localStorage.removeItem("racketTutor.languageExperienceChosen");
    localStorage.removeItem("racketTutor.cppStatus");
  }
  state.target = profile.targetLanguage || state.target;
  if (state.baseLanguage && state.target === state.baseLanguage) {
    state.target = chooseDefaultTarget();
  }
  state.activeDay = Number(profile.activeDay || 1);
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  localStorage.setItem("racketTutor.activeDay", String(state.activeDay));
  for (const [key, value] of Object.entries(profile.checklists || {})) {
    localStorage.setItem(`racketTutor.checklist.${key}`, JSON.stringify(value));
  }
  state.profileLoaded = true;
}

function padDay(day) {
  return String(day).padStart(2, "0");
}

function checklistKey(day) {
  return `racketTutor.checklist.${state.target}.${day}`;
}

function submissionKey(target, day) {
  return `${target}:${day}`;
}

function hasSubmitted(day, target = state.target) {
  return state.submittedLessons.has(submissionKey(target, day));
}

function isLessonUnlocked(day) {
  return day >= 1;
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
  scheduleProfileSave();
}

function checkedCount(day) {
  return readChecklist(day).filter(Boolean).length;
}

function activeLesson() {
  return state.lessons.find((lesson) => lesson.day === state.activeDay) || state.lessons[0];
}

function isCppFoundationMode() {
  return !state.baseLanguage;
}

function hasExperienceProfile() {
  return state.languageExperienceChosen
    || localStorage.getItem("racketTutor.languageExperienceChosen") === "true"
    || localStorage.getItem("racketTutor.baseLanguage") !== null
    || localStorage.getItem("racketTutor.knownLanguages") !== null
    || localStorage.getItem("racketTutor.cppStatus") !== null;
}

function isAuthenticated() {
  return Boolean(state.user);
}

function setMainContentHidden(hidden) {
  document.querySelector(".topbar").hidden = hidden;
  document.querySelector(".lesson-layout").hidden = hidden;
}

function renderOnboarding() {
  const needsAuth = !isAuthenticated();
  const needsChoice = !hasExperienceProfile();
  if (els.authPanel) {
    els.authPanel.hidden = !needsAuth;
  }
  for (const input of els.languageExperienceInputs || []) {
    input.checked = state.baseLanguage === input.value;
  }
  if (els.noneExperience) {
    els.noneExperience.checked = !state.baseLanguage && hasExperienceProfile();
  }
  if (els.onboardingPanel) {
    els.onboardingPanel.hidden = needsAuth || !needsChoice;
  }
  setMainContentHidden(needsAuth || needsChoice);
  for (const item of [els.progressBlock, els.searchBox, els.dayList, els.userPanel]) {
    if (item) item.hidden = needsAuth || needsChoice;
  }
  if (els.languagePicker) {
    els.languagePicker.hidden = needsAuth || needsChoice || isCppFoundationMode();
  }
  if (els.cppTrackNotice) {
    els.cppTrackNotice.hidden = needsAuth || needsChoice || !isCppFoundationMode();
  }
  if (els.userNameLabel && state.user) {
    els.userNameLabel.textContent = state.user.name;
  }
}

function setCppStatus(status) {
  writeKnownLanguages(status === "knows_cpp" ? ["cpp"] : []);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");

  if (!state.baseLanguage) {
    state.target = "cpp";
  } else if (state.target === "cpp") {
    state.target = "racket";
  }
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  renderOnboarding();
  scheduleProfileSave();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
}

function resetPrerequisiteChoice() {
  state.knownLanguages = [];
  state.baseLanguage = "";
  state.languageExperienceChosen = false;
  localStorage.removeItem("racketTutor.knownLanguages");
  localStorage.removeItem("racketTutor.baseLanguage");
  localStorage.removeItem("racketTutor.languageExperienceChosen");
  localStorage.removeItem("racketTutor.cppStatus");
  renderOnboarding();
  scheduleProfileSave();
}

function chooseDefaultTarget() {
  const candidates = ["cpp", "python", "java", "c", "racket"];
  return candidates.find((id) => id !== state.baseLanguage) || "cpp";
}

function continueFromLanguageExperience() {
  const checkedLanguage = [...els.languageExperienceInputs].find((input) => input.checked);
  if (!els.noneExperience?.checked && !checkedLanguage) {
    if (els.experienceMessage) els.experienceMessage.textContent = "Choose one language or None before continuing.";
    return;
  }
  if (els.experienceMessage) els.experienceMessage.textContent = "";
  const selected = els.noneExperience?.checked ? "" : (checkedLanguage?.value || "");
  writeKnownLanguages(selected ? [selected] : []);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");
  state.target = state.baseLanguage ? (state.target === state.baseLanguage ? chooseDefaultTarget() : state.target) : "cpp";
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  renderOnboarding();
  scheduleProfileSave();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
}

function setAuthMode(mode) {
  state.authMode = mode;
  const register = mode === "register";
  els.showRegister.classList.toggle("active", register);
  els.showLogin.classList.toggle("active", !register);
  els.authSubmit.textContent = register ? "Create Account" : "Log In";
  els.authPassword.autocomplete = register ? "new-password" : "current-password";
  els.authMessage.textContent = "";
}

function renderAiReviewStatus(enabled = state.aiReviewEnabled) {
  if (!els.aiReviewStatus) return;
  if (!enabled) {
    els.aiReviewStatus.hidden = true;
    els.aiReviewStatus.innerHTML = "";
    return;
  }
  els.aiReviewStatus.hidden = false;
  els.aiReviewStatus.classList.toggle("enabled", enabled);
  els.aiReviewStatus.innerHTML = `<strong>AI Review Connected</strong><span>Submissions receive deeper paragraph-level review and line-by-line improvement suggestions, even for short code.</span>`;
}

async function loadSession() {
  const response = await fetch("/api/me", { headers: accessHeaders() });
  if (!response.ok) {
    renderAiReviewStatus(false);
    renderOnboarding();
    return;
  }
  const data = await response.json();
  state.aiReviewEnabled = Boolean(data.openaiFeedbackEnabled);
  renderAiReviewStatus();
  state.user = data.user;
  if (state.user) {
    applyProfile(data.profile);
  }
  renderOnboarding();
  if (state.user && hasExperienceProfile()) {
    await loadCourse();
  }
  await loadSubmissions();
}

async function submitAuth(event) {
  event.preventDefault();
  els.authSubmit.disabled = true;
  els.authMessage.textContent = state.authMode === "register" ? "Creating account..." : "Logging in...";
  try {
    const response = await fetch(`/api/${state.authMode}`, {
      method: "POST",
      headers: { ...accessHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({
        name: els.authName.value,
        password: els.authPassword.value,
        profile: state.authMode === "register" ? emptyProfilePayload() : profilePayload(),
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Account request failed");
    state.user = data.user;
    applyProfile(data.profile);
    els.authForm.reset();
    els.authMessage.textContent = "";
    renderOnboarding();
    if (hasExperienceProfile()) {
      await loadCourse();
    }
    await loadSubmissions();
  } catch (error) {
    els.authMessage.textContent = error.message;
  } finally {
    els.authSubmit.disabled = false;
  }
}

async function logout() {
  await fetch("/api/logout", { method: "POST", headers: accessHeaders() });
  state.user = null;
  state.profileLoaded = false;
  state.lessons = [];
  state.submittedLessons = new Set();
  state.unlockedSampleCode = null;
  state.knownLanguages = [];
  state.baseLanguage = "";
  state.languageExperienceChosen = false;
  state.target = "racket";
  state.activeDay = 1;
  localStorage.removeItem("racketTutor.knownLanguages");
  localStorage.removeItem("racketTutor.baseLanguage");
  localStorage.removeItem("racketTutor.languageExperienceChosen");
  localStorage.removeItem("racketTutor.cppStatus");
  localStorage.removeItem("racketTutor.targetLanguage");
  localStorage.removeItem("racketTutor.activeDay");
  for (const key of Object.keys(localStorage)) {
    if (key.startsWith("racketTutor.checklist.")) {
      localStorage.removeItem(key);
    }
  }
  if (els.submissionList) els.submissionList.innerHTML = "";
  if (els.feedbackBox) {
    els.feedbackBox.hidden = true;
    els.feedbackBox.textContent = "";
    els.feedbackBox.classList.remove("error");
  }
  if (els.authPanel) els.authPanel.hidden = false;
  setAuthMode("login");
  renderOnboarding();
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
    const submitted = hasSubmitted(lesson.day);
    const unlocked = isLessonUnlocked(lesson.day);
    const button = document.createElement("button");
    button.type = "button";
    button.disabled = !unlocked;
    button.title = unlocked ? "" : `Submit Day ${padDay(lesson.day - 1)} homework before opening this lesson.`;
    button.className = `day-card${lesson.day === state.activeDay ? " active" : ""}${!unlocked ? " locked" : ""}`;
    button.innerHTML = `
      <span class="day-number">${padDay(lesson.day)}</span>
      <span>
        <strong>${lesson.title}</strong>
        <span>${lesson.category}${submitted ? " · Submitted" : ""}</span>
      </span>
      <span class="done-dot${done || submitted ? " complete" : ""}" aria-hidden="true"></span>
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
  document.title = "CodeBridge";
  document.querySelector(".brand h1").textContent = "CodeBridge";
  if (els.brandSubtitle) {
    els.brandSubtitle.textContent = isCppFoundationMode()
      ? "C++ Foundations · prerequisite track · 56 days"
      : `${lesson.base_language_name || "Known language"} foundation to ${lesson.target_language_name || "target language"} · 56 days`;
  }
  els.lessonTitle.textContent = lesson.title;
  els.categoryLabel.textContent = lesson.category;
  els.goalTitle.textContent = lesson.title;
  els.goalText.textContent = lesson.goal;
  els.dayMetric.textContent = padDay(lesson.day);
  els.checkMetric.textContent = `${done}/${lesson.checklist.length}`;
  els.weekMetric.textContent = lesson.week;
  if (els.unlockNotice) {
    const submittedToday = hasSubmitted(lesson.day);
    const finalDay = lesson.day === state.lessons.length;
    els.unlockNotice.classList.toggle("complete", submittedToday);
    els.unlockNotice.innerHTML = submittedToday
      ? `<strong>Homework submitted.</strong><span>${finalDay ? "You finished the final lesson for this track." : `You can keep moving through the open course.`}</span>`
      : `<strong>All lessons are unlocked.</strong><span>You can study any day now. Submit HW Q1, HW Q2, and HW Q3 when you want feedback and history.</span>`;
  }
  els.cppBridge.textContent = lesson.cpp_bridge;
  renderSyntaxBridge(lesson);
  els.explanation.textContent = lesson.explanation;
  els.codePanel.hidden = state.unlockedSampleCode?.day !== lesson.day || state.unlockedSampleCode?.target !== state.target;
  els.codeBlock.textContent = els.codePanel.hidden ? "" : state.unlockedSampleCode.code;
  renderLineNotes(lesson);
  els.assignmentText.textContent = lesson.assignment;

  els.prevDay.disabled = lesson.day === 1;
  els.nextDay.disabled = lesson.day === state.lessons.length;
  els.nextDay.title = "";

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
  const baseName = lesson.base_language_name || bridge.base_label || "Known Language";

  els.bridgeEyebrow.textContent = `${baseName} Syntax → ${targetName} Syntax`;
  els.bridgeConcept.textContent = bridge.concept;
  els.bridgeAngle.textContent = bridge.today_angle;
  els.baseSyntaxLabel.textContent = `${baseName} Syntax`;
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
          <div><dt>${lesson.base_language_name || "Known Language"} Comparison</dt><dd></dd></div>
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
  const nextDay = Math.max(1, Math.min(day, state.lessons.length));
  if (!isLessonUnlocked(nextDay)) {
    els.feedbackBox.hidden = false;
    els.feedbackBox.classList.add("error");
    els.feedbackBox.textContent = `Day ${padDay(nextDay)} is locked. Submit Day ${padDay(nextDay - 1)} homework before moving on.`;
    renderDayList();
    return;
  }
  state.activeDay = nextDay;
  state.unlockedSampleCode = null;
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
  } else if (state.target === state.baseLanguage) {
    state.target = chooseDefaultTarget();
    localStorage.setItem("racketTutor.targetLanguage", state.target);
  }
  const response = await fetch(`/api/course?target=${encodeURIComponent(state.target)}&base=${encodeURIComponent(state.baseLanguage || "cpp")}`, { headers: accessHeaders() });
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
  while (state.activeDay > 1 && !isLessonUnlocked(state.activeDay)) {
    state.activeDay -= 1;
  }
  renderLesson();
}

function renderLanguageOptions() {
  if (!els.languageSelect || !state.languages.length) return;
  els.languageSelect.innerHTML = "";
  for (const language of state.languages) {
    if (language.id === state.baseLanguage) continue;
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
  state.submittedLessons = new Set(
    data.submissions.map((item) => submissionKey(item.target || "racket", item.day)),
  );
  els.submissionList.innerHTML = "";
  if (state.lessons.length) {
    renderDayList();
    renderProgress();
  }

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
        <summary>View submitted program and review</summary>
        <div class="submission-detail">
          <h4>Submitted Program</h4>
          <pre data-submission-content></pre>
          <h4>What to Fix / Review Feedback</h4>
          <pre data-submission-feedback></pre>
        </div>
      </details>
    `;
    div.querySelector("[data-submission-content]").textContent =
      item.content || item.contentPreview || "No submitted program text was saved for this older record.";
    div.querySelector("[data-submission-feedback]").textContent = item.feedback;
    els.submissionList.appendChild(div);
  });
}

async function submitAssignment(event) {
  event.preventDefault();
  const lesson = activeLesson();
  const formData = new FormData(els.submissionForm);
  formData.set("day", lesson.day);
  formData.set("target", state.target);
  formData.set("base", state.baseLanguage || "cpp");

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
    if (data.sampleCode) {
      state.unlockedSampleCode = {
        day: data.submission.day,
        target: data.submission.target,
        code: data.sampleCode,
      };
      state.submittedLessons.add(submissionKey(data.submission.target, data.submission.day));
      renderLesson();
    }
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

function openFeedbackModal() {
  if (!els.feedbackModal) return;
  els.feedbackModal.hidden = false;
  if (els.siteFeedbackStatus) els.siteFeedbackStatus.textContent = "";
  requestAnimationFrame(() => els.feedbackMessage?.focus());
}

function closeFeedbackModal() {
  if (!els.feedbackModal) return;
  els.feedbackModal.hidden = true;
}

async function submitSiteFeedback(event) {
  event.preventDefault();
  const lesson = activeLesson();
  els.sendFeedback.disabled = true;
  els.siteFeedbackStatus.textContent = "Sending feedback...";
  try {
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: { ...accessHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({
        category: els.feedbackCategory.value,
        message: els.feedbackMessage.value,
        page: window.location.href,
        day: lesson?.day || null,
        target: state.target,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Feedback failed to send");
    els.siteFeedbackForm.reset();
    els.siteFeedbackStatus.textContent = "Feedback sent. Thank you.";
    setTimeout(closeFeedbackModal, 900);
  } catch (error) {
    els.siteFeedbackStatus.textContent = error.message;
  } finally {
    els.sendFeedback.disabled = false;
  }
}

els.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderDayList();
});

els.languageSelect.addEventListener("change", (event) => {
  state.target = event.target.value;
  state.unlockedSampleCode = null;
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");
  scheduleProfileSave();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
});

els.authForm.addEventListener("submit", submitAuth);
els.showRegister.addEventListener("click", () => setAuthMode("register"));
els.showLogin.addEventListener("click", () => setAuthMode("login"));
els.logoutButton.addEventListener("click", logout);

els.noneExperience.addEventListener("change", () => {
  if (els.noneExperience.checked) writeKnownLanguages([]);
});

for (const input of els.languageExperienceInputs) {
  input.addEventListener("change", () => {
    if (input.checked) writeKnownLanguages([input.value]);
  });
}

els.continueFromExperience.addEventListener("click", continueFromLanguageExperience);
els.resetPrerequisite.addEventListener("click", resetPrerequisiteChoice);
els.markCppKnown.addEventListener("click", () => setCppStatus("knows_cpp"));

els.prevDay.addEventListener("click", () => selectDay(state.activeDay - 1));
els.nextDay.addEventListener("click", () => selectDay(state.activeDay + 1));

els.copyCode.addEventListener("click", async () => {
  if (els.codePanel.hidden || !state.unlockedSampleCode) return;
  await navigator.clipboard.writeText(state.unlockedSampleCode.code);
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
els.feedbackButton?.addEventListener("click", openFeedbackModal);
els.closeFeedback?.addEventListener("click", closeFeedbackModal);
els.feedbackModal?.addEventListener("click", (event) => {
  if (event.target === els.feedbackModal) closeFeedbackModal();
});
els.siteFeedbackForm?.addEventListener("submit", submitSiteFeedback);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !els.feedbackModal?.hidden) {
    closeFeedbackModal();
  }
});

renderOnboarding();
setAuthMode("register");
loadSession().catch((error) => {
  els.authMessage.textContent = error.message;
});
