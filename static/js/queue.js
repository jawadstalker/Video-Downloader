async function refreshDownloads() {
    const response = await fetch("/api/downloads");
    const jobs = await response.json();
    const container = document.getElementById("downloads");
    if (!container) return;
    container.innerHTML = jobs.length ? jobs.map(job => `
        <article class="download-item">
            <div class="download-top">
                <strong>${job.title}</strong>
                <span class="status ${job.status}">${job.status}</span>
            </div>
            <div class="progress"><span style="width:${job.progress}%"></span></div>
            <div class="download-meta">
                <span>${job.progress}%</span>
                <span>${job.speed || ""}</span>
                <span>ETA ${job.eta || "--"}</span>
            </div>
            <div class="download-actions">
                ${job.status === "downloading" ? `<button onclick="jobAction('${job.id}','pause')">Pause</button>` : ""}
                ${job.status === "paused" ? `<button onclick="jobAction('${job.id}','resume')">Resume</button>` : ""}
                ${["queued","downloading","paused","retrying"].includes(job.status) ? `<button onclick="jobAction('${job.id}','cancel')">Cancel</button>` : ""}
                ${job.status === "failed" ? `<button onclick="jobAction('${job.id}','retry')">Retry</button>` : ""}
            </div>
            ${job.error ? `<small class="job-error">${job.error}</small>` : ""}
        </article>`).join("") : "<p class='muted'>No downloads yet.</p>";
}
async function jobAction(id, action) {
    await fetch(`/api/downloads/${id}/${action}`, {method:"POST"});
    refreshDownloads();
}
setInterval(refreshDownloads, 1000);
document.addEventListener("DOMContentLoaded", refreshDownloads);
