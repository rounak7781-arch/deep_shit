const feedback = document.getElementById("feedback");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultBox = document.getElementById("resultBox");
const resultsBody = document.getElementById("resultsBody");

function badge(sentiment) {
    return `<span class="badge ${sentiment.toLowerCase()}">${sentiment}</span>`;
}

function updateCounts(results) {
    const counts = {Positive:0, Negative:0, Neutral:0};
    results.forEach(r => counts[r.sentiment]++);
    document.getElementById("positiveCount").textContent = counts.Positive;
    document.getElementById("negativeCount").textContent = counts.Negative;
    document.getElementById("neutralCount").textContent = counts.Neutral;
    document.getElementById("totalCount").textContent = results.length;
}

function renderResults(results) {
    resultsBody.innerHTML = results.map(r =>
        `<tr><td>${escapeHtml(r.feedback)}</td><td>${badge(r.sentiment)}</td></tr>`
    ).join("");
    updateCounts(results);
}

function escapeHtml(text) {
    return text.replace(/[&<>"']/g, c => ({
        "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
    }[c]));
}

async function loadInitial() {
    const response = await fetch("/");
    // Initial table is injected from a tiny JSON-like block below via a second request is unnecessary.
    // Use sample data so the dashboard is immediately present.
    const sample = [
        {feedback:"The system is very easy and helpful",sentiment:"Positive"},
        {feedback:"The teacher is poor",sentiment:"Negative"},
        {feedback:"The classroom is okay",sentiment:"Neutral"}
    ];
    renderResults(sample);
}
loadInitial();

analyzeBtn.addEventListener("click", async () => {
    const text = feedback.value.trim();
    if (!text) return;
    analyzeBtn.disabled = true;
    const response = await fetch("/analyze", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({feedback:text})
    });
    const data = await response.json();
    analyzeBtn.disabled = false;
    resultBox.classList.remove("hidden");
    if (data.error) {
        resultBox.textContent = data.error;
        return;
    }
    resultBox.innerHTML = `<strong>${badge(data.sentiment)}</strong><p>${escapeHtml(data.feedback)}</p>`;
});

document.getElementById("uploadBtn").addEventListener("click", async () => {
    const file = document.getElementById("csvFile").files[0];
    const msg = document.getElementById("uploadMsg");
    if (!file) { msg.textContent = "Choose a CSV file first."; return; }

    const form = new FormData();
    form.append("file", file);
    msg.textContent = "Analyzing dataset...";
    const response = await fetch("/upload", {method:"POST", body:form});
    const data = await response.json();

    if (data.error) {
        msg.textContent = data.error;
        return;
    }
    renderResults(data.results);
    msg.textContent = `${data.results.length} feedback records analyzed successfully.`;
});
