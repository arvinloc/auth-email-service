// точка входа в порты микросервисов
const AUTH_API_BASE = "http://localhost:8000";
const ML_API_BASE = "http://localhost:8001";

async function request(base, path, { method = "GET", body, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };

  if (auth) {
    const token = localStorage.getItem("access_token");
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${base}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    
  }

  if (!res.ok) {
    const message = data?.detail || `Request failed (${res.status})`;
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }

  return data;
}

// auth-service (signup, login, magic-link)
function authRequest(path, options) {
  return request(AUTH_API_BASE, path, options);
}

// ml-service (predict)
function mlRequest(path, options) {
  return request(ML_API_BASE, path, options);
}
