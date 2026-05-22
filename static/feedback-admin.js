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
  userStats: document.querySelector("#userStats"),
  userList: document.querySelector("#adminUserList"),
  onlineWindow: document.querySelector("#onlineWindow"),
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

function renderStat(label, value, note = "") {
  return `
    <article class="admin-stat-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      ${note ? `<small>${escapeHtml(note)}</small>` : ""}
    </article>
  `;
}

function renderUsers(data) {
  const stats = data.stats || {};
  const users = data.users || [];
  const onlineWindow = stats.onlineWindowMinutes || 15;
  els.onlineWindow.textContent = `Online means active in the last ${onlineWindow} minutes.`;
  els.userStats.innerHTML = [
    renderStat("Registered", stats.totalRegistered ?? 0, "all accounts"),
    renderStat("Online now", stats.onlineUsers ?? 0, "active users"),
    renderStat("Active sessions", stats.activeSessions ?? 0, `${stats.totalSessions ?? 0} total sessions`),
    renderStat("Admins", stats.adminUsers ?? 0, "full permissions"),
  ].join("");

  els.userList.innerHTML = "";
  if (!users.length) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="7">No registered users yet.</td>`;
    els.userList.appendChild(row);
    return;
  }

  for (const user of users) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>
        <strong>${escapeHtml(user.name)}</strong>
        <span>${escapeHtml(user.role || "student")}</span>
      </td>
      <td>
        <span class="online-badge ${user.online ? "online" : "offline"}">${user.online ? "Online" : "Offline"}</span>
      </td>
      <td>${escapeHtml(formatDate(user.createdAt))}</td>
      <td>${escapeHtml(formatDate(user.lastActiveAt))}</td>
      <td>Day ${String(user.activeDay || 1).padStart(2, "0")} · ${escapeHtml(user.baseLanguage || "none")} → ${escapeHtml(user.targetLanguage || "racket")}</td>
      <td>${escapeHtml(user.activeSessionCount || 0)} active / ${escapeHtml(user.sessionCount || 0)} total</td>
      <td>${escapeHtml(user.submissions || 0)}</td>
    `;
    els.userList.appendChild(row);
  }
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
    const [usersResponse, feedbackResponse] = await Promise.all([
      fetch("/api/admin/users", { headers: accessHeaders() }),
      fetch(`/api/admin/feedback${query}`, { headers: accessHeaders() }),
    ]);
    const usersData = await usersResponse.json();
    const feedbackData = await feedbackResponse.json();
    if (!usersResponse.ok) throw new Error(usersData.error || "User monitor failed to load");
    if (!feedbackResponse.ok) throw new Error(feedbackData.error || "Feedback failed to load");
    renderUsers(usersData);
    renderFeedback(feedbackData.feedback || []);
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
setInterval(loadFeedback, 60000);
