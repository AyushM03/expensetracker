import { useState, useEffect } from "react";
import { api } from "@/utils/api";

export function useExpenses(params = {}) {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchExpenses = async () => {
    try {
      setLoading(true);
      const data = await api.getExpenses(params);
      setExpenses(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchExpenses(); }, []);

  const addExpense = async (data) => {
    const newExp = await api.createExpense(data);
    setExpenses((prev) => [newExp, ...prev]);
    return newExp;
  };

  const removeExpense = async (id) => {
    await api.deleteExpense(id);
    setExpenses((prev) => prev.filter((e) => e.id !== id));
  };

  return { expenses, loading, error, addExpense, removeExpense, refetch: fetchExpenses };
}
