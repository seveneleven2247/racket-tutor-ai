function accessHeaders() {
  const code = localStorage.getItem("racketTutor.accessCode");
  return code ? { "X-Access-Code": code } : {};
}

const els = {
  adminGate: document.querySelector("#adminGate"),
  adminGateMessage: document.querySelector("#adminGateMessage"),
  adminContent: document.querySelector("#adminContent"),
  adminRefresh: document.querySelector("#adminRefresh"),
  statusFilter: document.querySelector("#feedbackStatusFilter"),
  feedbackCount: document.querySelector("#feedbackCount"),
  feedbackList: document.querySelector("#adminFeedbackList"),
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function statusBadge(status) {
  const safeStatus = ["open", "reviewing", "fixed", "closed"].includes(status) ? status : "open";
  return `<span class="status-badge status-${safeStatus}">${safeStatus}</span>`;
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString() : "Unknown time";
}

function renderFeedback(records) {
  els.feedbackList.innerHTML = "";
  els.feedbackCount.textContent = `${records.length} feedback item${records.length === 1 ? "" : "s"}`;

  if (!records.length) {
    const empty = document.createElement("article");
    empty.className = "panel";
    empty.textContent = "No feedback matches this filter.";
    els.feedbackList.appendChild(empty);
    return;
  }

  for (const item of records) {
    const article = document.createElement("article");
    article.className = "feedback-admin-card";
    article.innerHTML = `
      <div class="feedback-admin-head">
        <div>
          <div class="feedback-meta">
            ${statusBadge(item.status)}
            <span>${escapeHtml(item.category || "other")}</span>
            <span>${escapeHtml(item.userName || "Anonymous")}</span>
            <span>${escapeHtml(formatDate(item.createdAt))}</span>
          </div>
          <h2>${item.day ? `Day ${String(item.day).padStart(2, "0")} · ` : ""}${escapeHtml(item.target || "course")} feedback</h2>
        </div>
      </div>
      <p class="feedback-message"></p>
      <dl class="feedback-details">
        <div><dt>Page</dt><dd></dd></div>
        <div><dt>Updated</dt><dd>${escapeHtml(formatDate(item.updatedAt))}</dd></div>
      </dl>
      <form class="feedback-admin-form" data-feedback-id="${item.id}">
        <label>
          <span>Status</span>
          <select name="status">
            <option value="open">Open</option>
            <option value="reviewing">Reviewing</option>
            <option value="fixed">Fixed</option>
            <option value="closed">Closed</option>
          </select>
        </label>
        <label>
          <span>Admin note</span>
          <textarea name="adminNote" rows="3" placeholder="What changed, or what still needs checking?"></textarea>
        </label>
        <button class="secondary-button" type="submit">Update</button>
        <span class="inline-status" aria-live="polite"></span>
      </form>
    `;
    article.querySelector(".feedback-message").textContent = item.message;
    article.querySelector("dd").textContent = item.page || "No page recorded";
    article.querySelector('select[name="status"]').value = item.status || "open";
    article.querySelector('textarea[name="adminNote"]').value = item.adminNote || "";
    article.querySelector("form").addEventListener("submit", updateFeedback);
    els.feedbackList.appendChild(article);
  }
}

async function loadMe() {
  const response = await fetch("/api/me", { headers: accessHeaders() });
  if (!response.ok) throw new Error("Please log in before opening the feedback tracker.");
  const data = await response.json();
  if (!data.user?.isAdmin) throw new Error("This page requires the Elven administrator account.");
  return data.user;
}

async function loadFeedback() {
  els.adminRefresh.disabled = true;
  const query = els.statusFilter.value ? `?status=${encodeURIComponent(els.statusFilter.value)}` : "";
  try {
    await loadMe();
    els.adminGate.hidden = true;
    els.adminContent.hidden = false;
    const response = await fetch(`/api/admin/feedback${query}`, { headers: accessHeaders() });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Feedback failed to load");
    renderFeedback(data.feedback || []);
  } catch (error) {
    els.adminContent.hidden = true;
    els.adminGate.hidden = false;
    els.adminGateMessage.textContent = error.message;
  } finally {
    els.adminRefresh.disabled = false;
  }
}

async function updateFeedback(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const status = form.querySelector(".inline-status");
  const feedbackId = form.dataset.feedbackId;
  const statusSelect = form.querySelector('select[name="status"]');
  const noteInput = form.querySelector('textarea[name="adminNote"]');
  const body = {
    status: statusSelect.value,
    adminNote: noteInput.value,
  };
  status.textContent = "Saving...";
  try {
    const response = await fetch(`/api/admin/feedback/${feedbackId}`, {
      method: "PATCH",
      headers: { ...accessHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Update failed");
    status.textContent = "Saved";
    await loadFeedback();
  } catch (error) {
    status.textContent = error.message;
  }
}

els.adminRefresh.addEventListener("click", loadFeedback);
els.statusFilter.addEventListener("change", loadFeedback);

loadFeedback();
