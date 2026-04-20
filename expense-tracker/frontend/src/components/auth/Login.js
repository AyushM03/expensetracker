import { useState } from "react";
import { useAuth } from "@/context/AuthContext";

export default function Login() {
  const { login, register } = useAuth();
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      if (isLogin) await login(form.email, form.password);
      else await register(form.name, form.email, form.password);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-sm border w-full max-w-md">
        <h1 className="text-2xl font-semibold text-gray-900 mb-2">ExpenseTracker</h1>
        <p className="text-gray-500 text-sm mb-6">{isLogin ? "Sign in to your account" : "Create your account"}</p>
        {error && <p className="text-red-600 text-sm mb-4 bg-red-50 p-3 rounded-lg">{error}</p>}
        <form onSubmit={handle} className="space-y-4">
          {!isLogin && (
            <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Your name"
              value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          )}
          <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Email"
            type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Password"
            type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <button type="submit" disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50">
            {loading ? "Please wait..." : isLogin ? "Sign in" : "Create account"}
          </button>
        </form>
        <p className="text-center text-sm text-gray-500 mt-4">
          {isLogin ? "No account? " : "Already have one? "}
          <button className="text-blue-600" onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? "Register" : "Sign in"}
          </button>
        </p>
      </div>
    </div>
  );
}
