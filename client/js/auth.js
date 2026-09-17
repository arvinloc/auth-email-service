const tabLogin = document.getElementById("tab-login");
const tabSignup = document.getElementById("tab-signup");
const formLogin = document.getElementById("form-login");
const formSignup = document.getElementById("form-signup");
const statusBox = document.getElementById("status");

function setTab(tab) {
  const isLogin = tab === "login";
  tabLogin.classList.toggle("active", isLogin);
  tabSignup.classList.toggle("active", !isLogin);
  formLogin.style.display = isLogin ? "block" : "none";
  formSignup.style.display = isLogin ? "none" : "block";
  hideStatus();
}

function showStatus(message, kind = "error") {
  statusBox.textContent = message;
  statusBox.className = `status show ${kind}`;
}

function hideStatus() {
  statusBox.className = "status";
}

tabLogin.addEventListener("click", () => setTab("login"));
tabSignup.addEventListener("click", () => setTab("signup"));

formLogin.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;
  const btn = formLogin.querySelector("button");

  btn.disabled = true;
  hideStatus();

  try {
    const data = await authRequest("/auth/login", {
      method: "POST",
      body: { email, password },
    });
    localStorage.setItem("access_token", data.token);
    window.location.href = "dashboard.html";
  } catch (err) {
    showStatus(err.message, "error");
  } finally {
    btn.disabled = false;
  }
});

formSignup.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("signup-email").value.trim();
  const password = document.getElementById("signup-password").value;
  const btn = formSignup.querySelector("button");

  btn.disabled = true;
  hideStatus();

  try {
    const data = await authRequest("/auth/signup", {
      method: "POST",
      body: { email, password },
    });
    showStatus(data.message || "Проверьте свою почту, чтобы подтвердить регистрацию", "success");
    formSignup.reset();
  } catch (err) {
    showStatus(err.message, "error");
  } finally {
    btn.disabled = false;
  }
});
