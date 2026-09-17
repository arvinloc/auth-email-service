const emailEl = document.getElementById("dash-email");
const logoutBtn = document.getElementById("logout-btn");
const form = document.getElementById("sentiment-form");
const textInput = document.getElementById("sentiment-text");
const resultBox = document.getElementById("result");
const resultLabel = document.getElementById("result-label");
const resultConfidence = document.getElementById("result-confidence");
const errorBox = document.getElementById("sentiment-error");

logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("access_token");
  window.location.href = "index.html";
});

function requireAuthOrRedirect() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "index.html";
    return null;
  }
  return token;
}


async function loadUser() {
  try {
    const data = await authRequest("/protected", { auth: true });
    emailEl.textContent = data.data?.email ?? "—";
  } catch (err) {
    localStorage.removeItem("access_token");
    window.location.href = "index.html";
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = textInput.value.trim();

  const btn = form.querySelector("button");

  errorBox.className = "status";
  resultBox.className = "result";

  if (!text) return;

  btn.disabled = true;
  btn.textContent = "Анализ...";

  try {
    const data = await mlRequest("/predict", {
      method: "POST",
      auth: true,

      body: { text },
    });

    resultLabel.textContent = data.label;
    resultLabel.className = `result-label ${data.label}`;
    resultConfidence.textContent = `Уверенность: ${(data.proba * 100).toFixed(1)}%`;
    resultBox.className = "result show";
  } catch (err) {

    errorBox.textContent = err.message;
    errorBox.className = "status show error";
  } finally {
    btn.disabled = false;
    btn.textContent = "Анализировать тональность";
  }
});

if (requireAuthOrRedirect()) {
  loadUser();
  
}
