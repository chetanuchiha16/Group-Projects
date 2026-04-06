import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminLogin() {
  const [secret, setSecret] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!secret) return alert("Enter admin secret");
    localStorage.setItem("admin_secret", "supersecretkey");
    navigate("/admin/panel");
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="p-6 rounded-2xl shadow-xl w-80 bg-white/80 dark:bg-white/5 backdrop-blur-lg border border-gray-200 dark:border-white/10">
        <h1 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Admin Login</h1>
        <input
          type="password"
          placeholder="Enter secret"
          value={secret}
          onChange={(e) => setSecret(e.target.value)}
          className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-zinc-800 border-gray-300 dark:border-zinc-600 text-gray-800 dark:text-gray-200 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white py-2 rounded-xl hover:bg-blue-700 transition"
        >
          Login
        </button>
      </div>
    </div>
  );
}
