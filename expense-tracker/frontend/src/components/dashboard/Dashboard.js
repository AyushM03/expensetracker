import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { useExpenses } from "@/hooks/useExpenses";
import { api } from "@/utils/api";

const CATEGORIES = ["food","travel","shopping","rent","utilities","entertainment","health","education","other"];

export default function Dashboard() {
  const { logout } = useAuth();
  const { expenses, loading, addExpense, removeExpense } = useExpenses();
  const [form, setForm] = useState({ title: "", amount: "", category: "food", note: "" });
  const [advice, setAdvice] = useState("");
  const [advLoading, setAdvLoading] = useState(false);

  const handleAdd = async (e) => {
    e.preventDefault();
    await addExpense({ ...form, amount: parseFloat(form.amount) });
    setForm({ title: "", amount: "", category: "food", note: "" });
  };

  const getAdvice = async () => {
    setAdvLoading(true);
    const month = new Date().toISOString().slice(0, 7);
    const res = await api.getAiAdvice(month);
    setAdvice(res.advice);
    setAdvLoading(false);
  };

  const total = expenses.reduce((s, e) => s + e.amount, 0);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">ExpenseTracker</h1>
            <p className="text-gray-500 text-sm">Total this month: ₹{total.toLocaleString("en-IN")}</p>
          </div>
          <button onClick={logout} className="text-sm text-gray-500 hover:text-gray-800">Logout</button>
        </div>

        {/* Add expense form */}
        <form onSubmit={handleAdd} className="bg-white border rounded-xl p-5 mb-6 grid grid-cols-2 gap-3">
          <input className="border rounded-lg px-3 py-2 text-sm" placeholder="Title"
            value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <input className="border rounded-lg px-3 py-2 text-sm" placeholder="Amount (₹)" type="number"
            value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} required />
          <select className="border rounded-lg px-3 py-2 text-sm"
            value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <input className="border rounded-lg px-3 py-2 text-sm" placeholder="Note (optional)"
            value={form.note} onChange={(e) => setForm({ ...form, note: e.target.value })} />
          <button type="submit" className="col-span-2 bg-blue-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-700">
            Add Expense
          </button>
        </form>

        {/* AI Advice */}
        <div className="bg-white border rounded-xl p-5 mb-6">
          <div className="flex justify-between items-center mb-3">
            <h2 className="font-medium text-gray-900">AI Financial Advisor</h2>
            <button onClick={getAdvice} disabled={advLoading}
              className="text-sm bg-purple-600 text-white px-4 py-1.5 rounded-lg hover:bg-purple-700 disabled:opacity-50">
              {advLoading ? "Analyzing..." : "Get advice"}
            </button>
          </div>
          {advice && <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{advice}</p>}
        </div>

        {/* Expense list */}
        <div className="bg-white border rounded-xl overflow-hidden">
          {loading ? (
            <p className="p-6 text-center text-gray-400 text-sm">Loading expenses...</p>
          ) : expenses.length === 0 ? (
            <p className="p-6 text-center text-gray-400 text-sm">No expenses yet. Add your first one above.</p>
          ) : (
            expenses.map((e) => (
              <div key={e.id} className="flex items-center justify-between px-5 py-3 border-b last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-900">{e.title}</p>
                  <p className="text-xs text-gray-400">{e.category} · {new Date(e.date).toLocaleDateString("en-IN")}</p>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-medium text-gray-900">₹{e.amount.toLocaleString("en-IN")}</span>
                  <button onClick={() => removeExpense(e.id)} className="text-red-400 hover:text-red-600 text-xs">delete</button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
