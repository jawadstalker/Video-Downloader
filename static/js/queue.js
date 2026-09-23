function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, function(char) {
        return {"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"}[char];
    });
}

async function refreshDownloads() {
    const response = await fetch("/api/downloads");
    if (!response.ok) return;

    const jobs = await response.json();
    const container = document.getElementById("downloads");
    if (!container) return;

    container.innerHTML = jobs.length ? jobs.map(function(job) {
        const progress = Math.max(0, Math.min(100, Number(job.progress) || 0));
        let actions = "";

        if (job.status === "downloading") {
            actions += '<button onclick="jobAction(\'' + escapeHtml(job.id) + '\',\'pause\')">Pause</button>';
        }
        if (job.status === "paused") {
            actions += '<button onclick="jobAction(\'' + escapeHtml(job.id) + '\',\'resume\')">Resume</button>';
        }
        if (["queued", "downloading", "paused", "retrying"].includes(job.status)) {
            actions += '<button onclick="jobAction(\'' + escapeHtml(job.id) + '\',\'cancel\')">Cancel</button>';
        }
        if (job.status === "failed") {
            actions += '<button onclick="jobAction(\'' + escapeHtml(job.id) + '\',\'retry\')">Retry</button>';
        }

        return '<article class="download-item">' +
            '<div class="download-top"><strong>' + escapeHtml(job.title) + '</strong>' +
            '<span class="status ' + escapeHtml(job.status) + '">' + escapeHtml(job.status) + '</span></div>' +
            '<div class="progress"><span style="width:' + progress + '%"></span></div>' +
            '<div class="download-meta"><span>' + progress + '%</span>' +
            '<span>' + escapeHtml(job.speed || "") + '</span><span>ETA ' + escapeHtml(job.eta || "--") + '</span></div>' +
            '<div class="download-actions">' + actions + '</div>' +
            (job.error ? '<small class="job-error">' + escapeHtml(job.error) + '</small>' : '') +
            '</article>';
    }).join("") : "<p class='muted'>No downloads yet.</p>";
}

async function jobAction(id, action) {
    const response = await fetch("/api/downloads/" + encodeURIComponent(id) + "/" + encodeURIComponent(action), {method: "POST"});
    if (!response.ok) {
        const data = await response.json().catch(function() { return {}; });
        alert(data.error || "Unable to update the download.");
    }
    refreshDownloads();
}

document.addEventListener("DOMContentLoaded", refreshDownloads);
setInterval(refreshDownloads, 1000);
