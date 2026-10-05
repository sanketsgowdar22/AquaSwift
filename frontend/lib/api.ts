/**
 * AquaSwift — API Client
 *
 * Type-safe fetch wrapper for the FastAPI backend.
 * Automatically attaches JWT, handles errors, and refreshes tokens.
 */

import Cookies from "js-cookie";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  code: string;
  status: number;
  details?: Record<string, unknown>;

  constructor(status: number, code: string, message: string, details?: Record<string, unknown>) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

interface RequestOptions extends Omit<RequestInit, "body"> {
  body?: unknown;
  skipAuth?: boolean;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { body, skipAuth, ...fetchOptions } = options;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(fetchOptions.headers as Record<string, string>),
  };

  // Attach JWT if available
  if (!skipAuth) {
    const token = Cookies.get("access_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...fetchOptions,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  // Handle 401 — try to refresh token
  if (response.status === 401 && !skipAuth) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      // Retry the request with new token
      const newToken = Cookies.get("access_token");
      if (newToken) headers["Authorization"] = `Bearer ${newToken}`;
      const retryResponse = await fetch(`${API_BASE}${endpoint}`, {
        ...fetchOptions,
        headers,
        body: body ? JSON.stringify(body) : undefined,
      });
      if (retryResponse.ok) return retryResponse.json();
    }
    // Clear auth state and redirect to login
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new ApiError(401, "UNAUTHORIZED", "Session expired. Please log in again.");
  }

  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      throw new ApiError(response.status, "UNKNOWN", response.statusText);
    }
    throw new ApiError(
      response.status,
      errorData.code || "UNKNOWN",
      errorData.message || "An error occurred",
      errorData.details
    );
  }

  // Handle 204 No Content
  if (response.status === 204) return {} as T;

  return response.json();
}

async function tryRefreshToken(): Promise<boolean> {
  const refreshToken = Cookies.get("refresh_token");
  if (!refreshToken) return false;

  try {
    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (response.ok) {
      const data = await response.json();
      Cookies.set("access_token", data.access_token, { expires: 1 });
      Cookies.set("refresh_token", data.refresh_token, { expires: 30 });
      return true;
    }
  } catch {
    // Refresh failed
  }
  return false;
}

// ---- Convenience Methods ----

export const api = {
  get: <T>(url: string, opts?: RequestOptions) => request<T>(url, { method: "GET", ...opts }),
  post: <T>(url: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(url, { method: "POST", body, ...opts }),
  patch: <T>(url: string, body?: unknown, opts?: RequestOptions) =>
    request<T>(url, { method: "PATCH", body, ...opts }),
  delete: <T>(url: string, opts?: RequestOptions) => request<T>(url, { method: "DELETE", ...opts }),
};

// ---- Auth API ----

export interface LoginRequest {
  email?: string;
  password?: string;
  phone?: string;
  otp?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    phone: string | null;
    email: string | null;
    full_name: string;
    is_active: boolean;
    roles: string[];
    created_at: string;
  };
}

export const authApi = {
  login: (data: LoginRequest) => api.post<AuthResponse>("/auth/login", data, { skipAuth: true }),
  requestOtp: (phone: string) => api.post<{ message: string }>("/auth/otp/request", { phone }, { skipAuth: true }),
  verifyOtp: (phone: string, otp: string) => api.post<AuthResponse>("/auth/otp/verify", { phone, otp }, { skipAuth: true }),
  refresh: (refreshToken: string) => api.post<AuthResponse>("/auth/refresh", { refresh_token: refreshToken }, { skipAuth: true }),
  logout: () => api.post<{ message: string }>("/auth/logout"),
};

// ---- Admin API ----

export const adminApi = {
  dashboard: () => api.get<{
    active_orders: number;
    today_orders: number;
    pending_deliveries: number;
    available_drivers: number;
    low_inventory_alerts: number;
    total_users: number;
  }>("/admin/dashboard"),

  // Orders
  orders: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return api.get<{ items: Order[]; total: number }>(`/admin/orders${qs}`);
  },

  // Users
  users: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return api.get<{ items: User[] }>(`/admin/users${qs}`);
  },

  // Catalog
  purposes: () => api.get<Purpose[]>("/catalog/purposes"),
  createPurpose: (data: Partial<Purpose>) => api.post<Purpose>("/admin/catalog/purposes", data),
  updatePurpose: (id: string, data: Partial<Purpose>) => api.patch<Purpose>(`/admin/catalog/purposes/${id}`, data),
  qualities: () => api.get<Quality[]>("/catalog/qualities"),
  createQuality: (data: Partial<Quality>) => api.post<Quality>("/admin/catalog/qualities", data),
  methods: () => api.get<DeliveryMethod[]>("/catalog/methods"),
  createMethod: (data: Partial<DeliveryMethod>) => api.post<DeliveryMethod>("/admin/catalog/methods", data),
  variants: (purposeId?: string) => {
    const qs = purposeId ? `?purpose_id=${purposeId}` : "";
    return api.get<Variant[]>(`/catalog/variants${qs}`);
  },
  createVariant: (data: Partial<Variant>) => api.post<Variant>("/admin/catalog/variants", data),

  // Inventory
  inventoryBalances: () => api.get<InventoryBalance[]>("/admin/inventory/balances"),
  inventoryLedger: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return api.get<InventoryTransaction[]>(`/admin/inventory/ledger${qs}`);
  },
  inventoryReceive: (data: { source_id: string; quantity_litres: number; notes?: string }) =>
    api.post<InventoryBalance>("/admin/inventory/receive", data),

  // Sources
  sources: () => api.get<Source[]>("/admin/sources"),
  createSource: (data: Partial<Source>) => api.post<Source>("/admin/sources", data),

  // Pricing
  pricingRules: () => api.get<PricingRule[]>("/admin/pricing/rules"),
  createPricingRule: (data: Partial<PricingRule>) => api.post<PricingRule>("/admin/pricing/rules", data),

  // Coupons
  coupons: () => api.get<Coupon[]>("/admin/coupons"),
  createCoupon: (data: Partial<Coupon>) => api.post<Coupon>("/admin/coupons", data),

  // Vehicles
  vehicles: () => api.get<Vehicle[]>("/admin/vehicles"),
  createVehicle: (data: Partial<Vehicle>) => api.post<Vehicle>("/admin/vehicles", data),

  // Deliveries
  deliveries: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return api.get<{ items: Delivery[]; total: number }>(`/admin/deliveries${qs}`);
  },

  // Payments
  payments: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return api.get<Payment[]>(`/admin/payments${qs}`);
  },

  // Reports
  salesReport: (days = 30) => api.get<{ period_days: number; total_orders: number; total_litres: number }>(`/admin/reports/sales?days=${days}`),
  deliveryReport: (days = 30) => api.get<{ period_days: number; completed_deliveries: number }>(`/admin/reports/deliveries?days=${days}`),

  // Audit
  auditLogs: (params?: Record<string, string>) => {
    const qs = params ? "?" + new URLSearchParams(params).toString() : "";
    return api.get<{ items: AuditLog[] }>(`/admin/audit-logs${qs}`);
  },

  // Businesses
  businesses: () => api.get<Business[]>("/admin/businesses"),

  // Roles
  roles: () => api.get<Role[]>("/admin/roles"),
};

// ---- Type Definitions ----

export interface User {
  id: string;
  phone: string | null;
  email: string | null;
  full_name: string;
  is_active: boolean;
  roles: string[];
  created_at: string;
}

export interface Purpose { id: string; name: string; description: string | null; icon_url: string | null; display_order: number; is_active: boolean; }
export interface Quality { id: string; name: string; description: string | null; is_active: boolean; }
export interface DeliveryMethod { id: string; name: string; is_active: boolean; }
export interface Variant { id: string; purpose_id: string; quality_id: string; delivery_method_id: string; min_quantity_litres: number; max_quantity_litres: number; is_active: boolean; purpose_name?: string; quality_name?: string; delivery_method_name?: string; }
export interface Source { id: string; name: string; type: string; gps_lat: number | null; gps_lng: number | null; capacity_litres: number; status: string; created_at: string; }
export interface InventoryBalance { source_id: string; source_name: string | null; available_litres: number; reserved_litres: number; allocated_litres: number; total_litres: number; }
export interface InventoryTransaction { id: string; source_id: string; type: string; quantity_litres: number; reference_type: string | null; notes: string | null; created_by: string; created_at: string; }
export interface PricingRule { id: string; version: number; purpose_id: string | null; quality_id: string | null; customer_type: string | null; pricing_model: string; base_price: string; tiers: unknown[] | null; active_from: string; active_to: string | null; is_active: boolean; }
export interface Coupon { id: string; code: string; discount_type: string; discount_value: string; min_order_amount: string | null; max_discount_amount: string | null; valid_from: string; valid_to: string; total_usage_limit: number | null; per_customer_limit: number; current_usage_count: number; is_active: boolean; }
export interface Vehicle { id: string; registration_number: string; type: string; capacity_litres: number; status: string; current_driver_id: string | null; created_at: string; }
export interface Order { id: string; order_number: string; customer_id: string; status: string; order_type: string; total_quantity_litres: number; items: OrderItem[]; notes: string | null; created_at: string; }
export interface OrderItem { id: string; variant_id: string; purpose_name: string; quality_name: string; delivery_method_name: string; quantity_litres: number; unit_price: string; water_total: string; delivery_charge: string; discount_total: string; tax_total: string; final_total: string; }
export interface Delivery { id: string; order_id: string; source_id: string | null; driver_id: string | null; vehicle_id: string | null; status: string; quantity_litres: number; delivered_quantity_litres: number | null; otp_code: string | null; scheduled_at: string | null; completed_at: string | null; created_at: string; }
export interface Payment { id: string; order_id: string; amount: string; currency: string; status: string; gateway: string; gateway_order_id: string | null; gateway_payment_id: string | null; created_at: string; }
export interface AuditLog { id: string; actor_id: string | null; action: string; entity_type: string; entity_id: string; before_state: unknown; after_state: unknown; created_at: string; }
export interface Business { id: string; name: string; registration_number: string | null; contact_email: string | null; contact_phone: string | null; is_active: boolean; }
export interface Role { id: string; name: string; description: string | null; permissions: string[]; }
