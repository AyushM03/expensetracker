import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/router";
import { useEffect } from "react";
import Dashboard from "@/components/dashboard/Dashboard";
import Login from "@/components/auth/Login";

export default function Home() {
  const { user, loading } = useAuth();
  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>;
  return user ? <Dashboard /> : <Login />;
}
