"use client";

import { createContext, useContext, useEffect, useState, useCallback, type ReactNode } from "react";
import Cookies from "js-cookie";
import { authApi, type AuthResponse, type User } from "@/lib/api";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithOtp: (phone: string, otp: string) => Promise<void>;
  logout: () => void;
  hasRole: (role: string) => boolean;
  hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Hydrate from cookie on mount
    const token = Cookies.get("access_token");
    const userData = Cookies.get("user_data");
    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch {
        Cookies.remove("user_data");
      }
    }
    setIsLoading(false);
  }, []);

  const handleAuthResponse = useCallback((data: AuthResponse) => {
    Cookies.set("access_token", data.access_token, { expires: 1 }); // 1 day
    Cookies.set("refresh_token", data.refresh_token, { expires: 30 }); // 30 days
    Cookies.set("user_data", JSON.stringify(data.user), { expires: 1 });
    setUser(data.user);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const data = await authApi.login({ email, password });
    handleAuthResponse(data);
  }, [handleAuthResponse]);

  const loginWithOtp = useCallback(async (phone: string, otp: string) => {
    const data = await authApi.verifyOtp(phone, otp);
    handleAuthResponse(data);
  }, [handleAuthResponse]);

  const logout = useCallback(() => {
    authApi.logout().catch(() => {}); // Best effort
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    Cookies.remove("user_data");
    setUser(null);
  }, []);

  const hasRole = useCallback((role: string) => {
    return user?.roles?.includes(role) ?? false;
  }, [user]);

  const hasPermission = useCallback((_permission: string) => {
    // In V1, role-based; permission check is server-side
    // This is a client hint — actual enforcement is in the backend
    if (hasRole("SUPER_ADMIN")) return true;
    return false;
  }, [hasRole]);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        loginWithOtp,
        logout,
        hasRole,
        hasPermission,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
