const API = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
export type User = { id: number; email: string; role: string };
export type NodeType = "trigger" | "transform" | "condition" | "ai_summary" | "http_request" | "approval" | "output";
export type NodeDef = { id: string; type: NodeType; label: string; config: Record<string, unknown> };
export type Definition = { nodes: NodeDef[]; edges: { source: string; target: string }[] };
export type Workflow = { id: number; name: string; description: string; definition: Definition; created_at: string; updated_at: string };
export type Run = { id: number; status: string; steps: { node_id: string; label: string; type: string; status: string; output: unknown }[]; result_data: unknown; error_message?: string | null; started_at: string };
export function getToken() { return localStorage.getItem("flowforge_token"); }
export function setToken(token: string | null) { if (token) localStorage.setItem("flowforge_token", token); else localStorage.removeItem("flowforge_token"); }
export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body) headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  let response: Response;
  try { response = await fetch(`${API}${path}`, { ...options, headers }); }
  catch { throw new Error("Cannot reach API. Check backend status, API URL, and CORS configuration."); }
  const body = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) throw new Error(body?.detail || `Request failed (${response.status})`);
  return body as T;
}
