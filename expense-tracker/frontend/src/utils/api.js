const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, options = {}) {
  const token = getToken();
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Something went wrong");
  }
  return res.json();
}

export const api = {
  register: (data) => request("/auth/register", { method: "POST", body: JSON.stringify(data) }),
  login: (data) => request("/auth/login", { method: "POST", body: JSON.stringify(data) }),
  getExpenses: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/expenses/?${q}`);
  },
  createExpense: (data) => request("/expenses/", { method: "POST", body: JSON.stringify(data) }),
  updateExpense: (id, data) => request(`/expenses/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteExpense: (id) => request(`/expenses/${id}`, { method: "DELETE" }),
  getMonthlySummary: (month) => request(`/expenses/summary/${month}`),
  getAiAdvice: (month, question) => {
    const q = question ? `?question=${encodeURIComponent(question)}` : "";
    return request(`/expenses/ai-advice/${month}${q}`);
  },
};
