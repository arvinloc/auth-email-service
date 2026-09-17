const statusText = document.getElementById("status-text");

function finish(message) {
  statusText.textContent = message;
}

(async () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  if (!token) {
    finish("В этой ссылке отсутствует токен");
    return;
  }

  try {
    const data = await authRequest("/auth/magic-link/verify", {
      method: "POST",
      body: { token },
    });

    localStorage.setItem("access_token", data.token);
    statusText.textContent = "Вход выполнен - перенаправление...";
    setTimeout(() => {
      window.location.href = "dashboard.html";
    }, 500);
  } catch (err) {
    finish(err.message || "Эта ссылка недействительна или время ее действия истекло");
  }
})();