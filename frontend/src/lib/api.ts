/**
 * API client for METHEAN backend.
 * All calls go through this module for consistent error handling.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

function getCookie(name: string): string | undefined {
  if (typeof document === "undefined") return undefined;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : undefined;
}

const RETRYABLE_STATUSES = new Set([502, 503, 504]);
const MAX_RETRIES = 3;
const BACKOFF_MS = [1000, 2000, 4000];

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function request<T>(
  path: string,
  options: RequestInit & { retry?: boolean } = {},
): Promise<T> {
  const url = `${API_BASE}${path}`;
  const method = (options.method || "GET").toUpperCase();
  const { retry: retryOpt, ...fetchOptions } = options;

  // Retry GET requests by default. Non-GET only when caller opts in.
  const shouldRetry = retryOpt ?? method === "GET";

  // Attach CSRF token header for state-changing requests
  const csrfHeaders: Record<string, string> = {};
  if (["POST", "PUT", "PATCH", "DELETE"].includes(method)) {
    const csrfToken = getCookie("csrf_token");
    if (csrfToken) {
      csrfHeaders["X-CSRF-Token"] = csrfToken;
    }
  }

  const init: RequestInit = {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...csrfHeaders,
      ...fetchOptions.headers,
    },
    ...fetchOptions,
  };

  let lastError: unknown;
  const attempts = shouldRetry ? MAX_RETRIES + 1 : 1;

  for (let attempt = 0; attempt < attempts; attempt++) {
    try {
      const res = await fetch(url, init);

      if (res.ok) {
        if (res.status === 204) return undefined as T;
        return res.json();
      }

      // Don't retry client errors (4xx) — they are not transient
      if (!RETRYABLE_STATUSES.has(res.status) || !shouldRetry || attempt === attempts - 1) {
        const body = await res.json().catch(() => ({ detail: res.statusText }));
        throw new ApiError(res.status, body.detail || res.statusText);
      }

      lastError = new ApiError(res.status, res.statusText);
    } catch (err) {
      // Retry on network errors (TypeError from fetch) if retrying is enabled
      if (err instanceof TypeError && shouldRetry && attempt < attempts - 1) {
        lastError = err;
      } else {
        throw err;
      }
    }

    // Exponential backoff before next attempt
    if (attempt < attempts - 1) {
      await sleep(BACKOFF_MS[attempt] || BACKOFF_MS[BACKOFF_MS.length - 1]);
    }
  }

  throw lastError;
}

// Auth
export const auth = {
  login: (email: string, password: string) =>
    request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  register: (data: { email: string; password: string; display_name: string; household_name: string }) =>
    request<{ user: User; access_token: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  me: () => request<User>("/auth/me"),
  logout: () => request("/auth/logout", { method: "POST" }),
};

// Children
export const children = {
  list: () => request<ChildListItem[]>("/children"),
  create: (data: { first_name: string; last_name?: string; grade_level?: string; date_of_birth?: string }) =>
    request<{ id: string; first_name: string }>("/children", { method: "POST", body: JSON.stringify(data) }),
  state: (childId: string) => request<ChildState>(`/children/${childId}/state`),
  mapState: (childId: string, mapId: string) =>
    request<MapState>(`/children/${childId}/map-state/${mapId}`),
  allMapState: (childId: string) =>
    request<MapState[]>(`/children/${childId}/map-state`),
  retentionSummary: (childId: string) =>
    request<RetentionSummary>(`/children/${childId}/retention-summary`),
  nodeHistory: (childId: string, nodeId: string) =>
    request<StateEvent[]>(`/children/${childId}/nodes/${nodeId}/history`),
  today: (childId: string) => request<any[]>(`/children/${childId}/today`),
  dashboard: (childId: string) => request<ChildDashboardResponse>(`/children/${childId}/dashboard`),
  alerts: (childId: string, limit = 5) => request<any>(`/children/${childId}/alerts?limit=${limit}`),
  theme: (childId: string) => request<any>(`/children/${childId}/theme`),
  updateTheme: (childId: string, data: object) =>
    request<any>(`/children/${childId}/theme`, { method: "PUT", body: JSON.stringify(data) }),
  updatePreferences: (childId: string, data: object) =>
    request<any>(`/children/${childId}/preferences`, { method: "PUT", body: JSON.stringify(data) }),
};

// Snapshots
export interface SnapshotItem {
  id: string; week_start: string; week_end: string;
  total_minutes: number; activities_completed: number;
  nodes_mastered: number; nodes_progressed: number;
  reviews_completed: number; summary: object | null;
}
export const snapshots = {
  list: (childId: string, limit = 20) =>
    request<{ items: SnapshotItem[] }>(`/children/${childId}/snapshots?limit=${limit}`),
};

// Plans
export const plans = {
  generate: (childId: string, data: { week_start: string; daily_minutes?: number }) =>
    request<Plan>(`/children/${childId}/plans/generate`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  list: (childId: string) => request<Plan[]>(`/children/${childId}/plans`),
  detail: (planId: string) => request<PlanDetail>(`/plans/${planId}`),
  approveActivity: (planId: string, activityId: string) =>
    request(`/plans/${planId}/activities/${activityId}/approve`, { method: "PUT" }),
  rejectActivity: (planId: string, activityId: string, reason: string) =>
    request(`/plans/${planId}/activities/${activityId}/reject`, {
      method: "PUT",
      body: JSON.stringify({ reason }),
    }),
  lock: (planId: string) => request(`/plans/${planId}/lock`, { method: "PUT" }),
  unlock: (planId: string) => request(`/plans/${planId}/unlock`, { method: "PUT" }),
  decisionTrace: (planId: string) => request<DecisionTrace>(`/plans/${planId}/decision-trace`),
  rescheduleActivity: (activityId: string, newDate: string) =>
    request<{ activity_id: string; scheduled_date: string }>(`/activities/${activityId}/reschedule`, {
      method: "PUT", body: JSON.stringify({ new_date: newDate }),
    }),
};

// Curriculum
export const curriculum = {
  listMaps: () => request<LearningMap[]>("/learning-maps"),
  getMap: (mapId: string) => request<MapDetail>(`/learning-maps/${mapId}`),
  templates: () => request<Template[]>("/learning-maps/templates"),
  copyTemplate: (templateId: string) =>
    request<{ learning_map_id: string }>(`/learning-maps/from-template/${templateId}`, {
      method: "POST",
    }),
  createNode: (mapId: string, data: object) =>
    request(`/learning-maps/${mapId}/nodes`, { method: "POST", body: JSON.stringify(data) }),
  createEdge: (mapId: string, data: object) =>
    request(`/learning-maps/${mapId}/edges`, { method: "POST", body: JSON.stringify(data) }),
  enroll: (childId: string, mapId: string) =>
    request(`/children/${childId}/enrollments`, {
      method: "POST",
      body: JSON.stringify({ learning_map_id: mapId }),
    }),
  override: (childId: string, nodeId: string, reason: string) =>
    request(`/children/${childId}/nodes/${nodeId}/override`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    }),
  subjects: () => request<Subject[]>("/subjects"),
  createSubject: (data: object) =>
    request("/subjects", { method: "POST", body: JSON.stringify(data) }),
  batchSave: (mapId: string, data: { nodes: object[]; edges: object[] }) =>
    request<any>(`/learning-maps/${mapId}/batch`, { method: "PUT", body: JSON.stringify(data) }),
  enrichMap: (mapId: string) =>
    request<any>(`/learning-maps/${mapId}/enrich`, { method: "POST" }),
  mapExisting: (childId: string, data: object) =>
    request<any>(`/children/${childId}/curriculum/map-existing`, { method: "POST", body: JSON.stringify(data) }),
};

// Tutor
export const tutor = {
  message: (activityId: string, childId: string, message: string, conversationHistory?: Array<{ role: string; text: string }>) =>
    request<TutorResponse>(`/tutor/${activityId}/message`, {
      method: "POST",
      body: JSON.stringify({ message, conversation_history: conversationHistory }),
    }),
};

export async function streamTutorMessage(
  activityId: string,
  childId: string,
  message: string,
  conversationHistory: Array<{ role: string; text: string }>,
  onToken: (text: string) => void,
  onDone: (hints: string[], aiRunId: string) => void,
  onError: (message: string) => void,
): Promise<void> {
  const url = `${API_BASE}/tutor/${activityId}/stream`;
  const csrfToken = getCookie("csrf_token");

  const response = await fetch(url, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(csrfToken ? { "X-CSRF-Token": csrfToken } : {}),
    },
    body: JSON.stringify({ child_id: childId, message, conversation_history: conversationHistory }),
  });

  if (!response.ok) {
    onError("I had trouble connecting. Try again in a moment.");
    return;
  }

  const reader = response.body?.getReader();
  if (!reader) { onError("Streaming not supported."); return; }

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      try {
        const event = JSON.parse(line.slice(6));
        if (event.type === "token") onToken(event.text);
        else if (event.type === "done") onDone(event.hints || [], event.ai_run_id || "");
        else if (event.type === "error") onError(event.message || "Something went wrong.");
      } catch { /* ignore malformed SSE */ }
    }
  }
}

// Attempts
export const attempts = {
  start: (activityId: string, childId: string) =>
    request<Attempt>(`/activities/${activityId}/attempts`, {
      method: "POST",
      body: JSON.stringify({ child_id: childId }),
    }),
  submit: (attemptId: string, data: {
    confidence: number;
    duration_minutes?: number;
    score?: number;
    feedback?: {
      responses?: Array<{ prompt: string; response: string }>;
      self_reflection?: string;
    };
  }) =>
    request<AttemptSubmitResult>(`/attempts/${attemptId}/submit`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  get: (attemptId: string) => request<Attempt>(`/attempts/${attemptId}`),
};

// ── Learning Context ──
export const learn = {
  context: (activityId: string, childId?: string) =>
    request<LearningContext>(`/activities/${activityId}/learn${childId ? `?child_id=${childId}` : ""}`),
};

export interface LearningContext {
  activity: {
    id: string; title: string; description: string;
    activity_type: string; estimated_minutes: number; instructions: object;
  };
  lesson: {
    introduction: string; objectives: string[];
    steps: Array<{ title: string; content: string; type: string }>;
    key_questions: string[]; practice_prompts: string[];
    resources_needed: string[]; real_world_connection: string;
    estimated_time: { introduction: number; guided_work: number; independent_practice: number };
  };
  assessment: { prompts: string[]; mastery_criteria: string; methods: string[] };
  tutor_available: boolean;
  previous_attempts: Array<{ date: string; status: string; duration_minutes: number; score: number | null }>;
  grade_level: string | null;
}

// Governance
export const governance = {
  rules: () => request<GovernanceRule[]>("/governance-rules"),
  createRule: (data: object) =>
    request<GovernanceRule>("/governance-rules", { method: "POST", body: JSON.stringify(data) }),
  updateRule: (id: string, data: object) =>
    request<GovernanceRule>(`/governance-rules/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteRule: (id: string) =>
    request<{ deleted: boolean }>(`/governance-rules/${id}`, { method: "DELETE" }),
  initDefaults: () => request<GovernanceRule[]>("/governance-rules/defaults", { method: "POST" }),
  events: (limit?: number) => request<GovernanceEvent[]>(`/governance-events?limit=${limit || 50}`),
  queue: (limit = 100) =>
    request<{ items: any[]; total: number }>(`/governance/queue?limit=${limit}`),
  approve: (planId: string, activityId: string, reason?: string) =>
    request(`/plans/${planId}/activities/${activityId}/approve`, {
      method: "PUT",
      body: reason ? JSON.stringify({ reason }) : undefined,
    }),
  reject: (planId: string, activityId: string, reason: string) =>
    request(`/plans/${planId}/activities/${activityId}/reject`, {
      method: "PUT",
      body: JSON.stringify({ reason }),
    }),
  modify: (planId: string, activityId: string, data: { reason: string; difficulty?: number; estimated_minutes?: number; notes?: string }) =>
    request(`/plans/${planId}/activities/${activityId}/approve`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  report: (data: { period_start: string; period_end: string }) =>
    request<any>("/governance/report", { method: "POST", body: JSON.stringify(data) }),
  attestReport: (reportId: string, text: string) =>
    request<any>(`/governance/report/attest`, { method: "POST", body: JSON.stringify({ report_id: reportId, attestation_text: text }) }),
  governanceIntelligence: () => request<any>("/household/governance-intelligence"),
};

// Household
export const household = {
  get: () => request<any>("/household/settings"),
  update: (data: object) => request<any>("/household/settings", { method: "PUT", body: JSON.stringify(data) }),
  getPhilosophy: () => request<any>("/household/philosophy"),
  updatePhilosophy: (data: object) => request<any>("/household/philosophy", { method: "PUT", body: JSON.stringify(data) }),
};

// AI
export const ai = {
  runs: (params?: { role?: string }) =>
    request<AIRun[]>(`/ai-runs${params?.role ? `?role=${params.role}` : ""}`),
  run: (runId: string) => request<AIRun>(`/ai-runs/${runId}`),
  contextDetail: (runId: string) => request<ContextDetailResponse>(`/ai-runs/${runId}/context-detail`),
  advisorReports: (childId: string) =>
    request<AdvisorReport[]>(`/children/${childId}/advisor-reports`),
  generateReport: (childId: string) =>
    request<AdvisorReport>(`/children/${childId}/advisor-reports/generate`, { method: "POST" }),
  calibrate: (childId: string, data: object) =>
    request(`/children/${childId}/cartographer/calibrate`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
};

// Types
// ── Compliance ──
export const compliance = {
  states: () => request<{ code: string; name: string; strictness: string }[]>("/compliance/states"),
  stateDetail: (code: string) => request<object>(`/compliance/states/${code}`),
  check: (childId: string, state: string) =>
    request<object>(`/children/${childId}/compliance/check?state=${state}`),
  attendance: (childId: string, start: string, end: string) =>
    request<object>(`/children/${childId}/attendance?start=${start}&end=${end}`),
  hours: (childId: string) => request<object>(`/children/${childId}/hours`),
};

// ── Notifications ──
export const notifications = {
  list: (unread = false, limit = 20) =>
    request<any[]>(`/notifications?unread=${unread}&limit=${limit}`),
  markRead: (id: string) =>
    request(`/notifications/${id}/read`, { method: "PUT" }),
  markAllRead: () =>
    request(`/notifications/read-all`, { method: "PUT" }),
};

// ── Documents ──
export const documents = {
  ihip: (childId: string, academicYear: string, state = "NY") =>
    `/api/v1/children/${childId}/documents/ihip?academic_year=${academicYear}&state=${state}`,
  quarterlyReport: (childId: string, quarter: number, academicYear: string) =>
    `/api/v1/children/${childId}/documents/quarterly-report?quarter=${quarter}&academic_year=${academicYear}`,
  attendance: (childId: string, start: string, end: string) =>
    `/api/v1/children/${childId}/documents/attendance?start=${start}&end=${end}`,
  transcript: (childId: string) =>
    `/api/v1/children/${childId}/documents/transcript`,
};

// ── Data Export ──
export const dataExport = {
  download: () => `/api/v1/household/export`,
};

// ── Subjects & Levels ──
export const subjects = {
  catalog: () => request<any>("/subjects/catalog"),
  addCustom: (data: { name: string; category?: string; description?: string }) =>
    request<any>("/subjects/custom", { method: "POST", body: JSON.stringify(data) }),
};

// ── Academic Calendar ──
export const academicCalendar = {
  get: () => request<any>("/household/academic-calendar"),
  update: (data: object) => request<any>("/household/academic-calendar", { method: "PUT", body: JSON.stringify(data) }),
};

// ── Manual Activities + Time Log ──
export const activities = {
  create: (data: { child_id: string; title: string; activity_type?: string; scheduled_date: string; estimated_minutes?: number; description?: string; subject_area?: string }) =>
    request<any>("/activities", { method: "POST", body: JSON.stringify(data) }),
};

export const timeLog = {
  create: (childId: string, data: { date: string; minutes: number; subject_area: string; description?: string }) =>
    request<any>(`/children/${childId}/time-log`, { method: "POST", body: JSON.stringify(data) }),
};

// ── Achievements ──
export const achievements = {
  list: (childId: string) => request<{ earned: any[]; definitions: any[] }>(`/children/${childId}/achievements`),
  streak: (childId: string) => request<{ current_streak: number; longest_streak: number; last_activity_date: string | null }>(`/children/${childId}/streak`),
};

// ── Learner Intelligence ──
export const intelligence = {
  get: (childId: string) => request<any>(`/children/${childId}/intelligence`),
  addObservation: (childId: string, observation: string) =>
    request<any>(`/children/${childId}/intelligence/observations`, { method: "PUT", body: JSON.stringify({ observation }) }),
  removeObservation: (childId: string, index: number) =>
    request<any>(`/children/${childId}/intelligence/observations/${index}`, { method: "DELETE" }),
  override: (childId: string, field: string, value: any) =>
    request<any>(`/children/${childId}/intelligence/override`, { method: "PUT", body: JSON.stringify({ field, value }) }),
};

export const account = {
  changePassword: (currentPassword: string, newPassword: string) =>
    request<{ success: boolean }>("/auth/password", { method: "PUT", body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }) }),
  getNotificationPreferences: () =>
    request<Record<string, boolean>>("/auth/me/notification-preferences"),
  updateNotificationPreferences: (prefs: Record<string, boolean>) =>
    request<Record<string, boolean>>("/auth/me/notification-preferences", { method: "PUT", body: JSON.stringify(prefs) }),
  forgotPassword: (email: string) =>
    request<{ message: string }>("/auth/forgot-password", { method: "POST", body: JSON.stringify({ email }) }),
  resetPassword: (token: string, newPassword: string) =>
    request<{ success: boolean }>("/auth/reset-password", { method: "POST", body: JSON.stringify({ token, new_password: newPassword }) }),
  resendVerification: () =>
    request<{ sent: boolean }>("/auth/resend-verification", { method: "POST" }),
};

export const billing = {
  subscribe: () => request<{ checkout_url: string }>("/billing/subscribe", { method: "POST" }),
  status: () => request<any>("/billing/status"),
  cancel: () => request<{ canceled: boolean }>("/billing/cancel", { method: "POST" }),
  portal: () => request<{ portal_url: string }>("/billing/portal", { method: "POST" }),
};

export const usage = {
  current: () => request<any>("/usage/current"),
  breakdown: () => request<any>("/usage/breakdown"),
};

// ── Evaluator Calibration ──
export const calibration = {
  profile: (childId: string) => request<CalibrationResponse>(`/children/${childId}/calibration`),
  predictions: (childId: string, params?: { reconciled_only?: boolean; min_drift?: number; skip?: number; limit?: number }) => {
    const qs = new URLSearchParams();
    if (params?.reconciled_only) qs.set("reconciled_only", "true");
    if (params?.min_drift !== undefined) qs.set("min_drift", String(params.min_drift));
    if (params?.skip !== undefined) qs.set("skip", String(params.skip));
    if (params?.limit !== undefined) qs.set("limit", String(params.limit));
    const q = qs.toString();
    return request<{ items: PredictionItem[]; total: number }>(`/children/${childId}/calibration/predictions${q ? `?${q}` : ""}`);
  },
  updateOffset: (childId: string, data: { offset_active?: boolean; parent_override_offset?: number | null }) =>
    request<{ status: string; changes: object }>(`/children/${childId}/calibration/offset`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  driftHistory: (childId: string, weeks = 12) =>
    request<{ series: DriftPoint[]; weeks_requested: number }>(`/children/${childId}/calibration/drift-history?weeks=${weeks}`),
  temporalDrift: (childId: string) =>
    request<TemporalDriftResponse>(`/children/${childId}/calibration/temporal-drift`),
  confidenceDistribution: (childId: string) =>
    request<ConfidenceDistributionResponse>(`/children/${childId}/calibration/confidence-distribution`),
  subjectDetail: (childId: string) =>
    request<{ subjects: SubjectCalibrationItem[] }>(`/children/${childId}/calibration/subject-detail`),
  exportData: (childId: string) =>
    request<object>(`/children/${childId}/calibration/export`),
};

export interface CalibrationResponse {
  profile: CalibrationProfileData | null;
  reconciled_predictions?: number;
  threshold: number;
  message?: string;
}

export interface CalibrationProfileData {
  id: string;
  child_id: string;
  total_predictions: number;
  reconciled_predictions: number;
  mean_drift: number;
  directional_bias: number;
  confidence_band_accuracy: Record<string, { total: number; hit_rate: number }>;
  subject_drift_map: Record<string, { mean_drift: number; count: number; bias: number }>;
  recalibration_offset: number;
  offset_active: boolean;
  parent_override_offset: number | null;
  last_computed_at: string | null;
}

export interface PredictionItem {
  id: string;
  node_id: string;
  attempt_id: string;
  predicted_confidence: number;
  predicted_fsrs_rating: number;
  actual_outcome: number | null;
  drift_score: number | null;
  calibration_offset_applied: number;
  created_at: string;
  outcome_recorded_at: string | null;
}

export interface DriftPoint {
  week: string;
  mean_drift: number;
  count: number;
}

export interface TemporalDriftResponse {
  weekly_buckets: Array<{ week: string; mean_drift: number; count: number; bias: number }>;
  trend: "improving" | "stable" | "worsening" | "insufficient_data";
  trend_slope: number;
}

export interface ConfidenceDistributionResponse {
  histogram: Array<{ band: string; count: number }>;
  mean: number;
  std_dev: number;
  skew: number;
  compression_warning: boolean;
  total: number;
}

export interface SubjectCalibrationItem {
  subject: string;
  mean_drift: number;
  directional_bias: number;
  reconciled_count: number;
  action: "well_calibrated" | "offset_active" | "review_recommended" | "insufficient_data";
  recommendation: string;
}

// ── Learner Style Vector ──
export const styleVector = {
  get: (childId: string) => request<StyleVectorResponse>(`/children/${childId}/style-vector`),
  setOverride: (childId: string, data: { dimension: string; value: number | string; locked: boolean }) =>
    request<{ status: string; dimension: string; overrides: Record<string, object> }>(`/children/${childId}/style-vector/overrides`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  setBounds: (childId: string, data: { dimension: string; min: number | null; max: number | null }) =>
    request<{ status: string; dimension: string; bounds: Record<string, object> }>(`/children/${childId}/style-vector/bounds`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  history: (childId: string) =>
    request<{ entries: StyleVectorData[]; total: number }>(`/children/${childId}/style-vector/history`),
};

export interface StyleVectorResponse {
  vector: StyleVectorData | null;
  observation_count?: number;
  threshold?: number;
  message?: string;
}

export interface StyleVectorData {
  id: string;
  child_id: string;
  optimal_session_minutes: number | null;
  socratic_responsiveness: number | null;
  frustration_threshold: number | null;
  recovery_rate: number | null;
  time_of_day_peak: number | null;
  subject_affinity_map: Record<string, number>;
  modality_preference: string | null;
  pacing_preference: number | null;
  independence_level: number | null;
  attention_pattern: string | null;
  data_points_count: number;
  dimensions_active: number;
  parent_overrides: Record<string, { value: number | string; locked: boolean }>;
  parent_bounds: Record<string, { min?: number; max?: number }>;
  last_computed_at: string | null;
}

// ── Family Intelligence ──
export const familyInsights = {
  list: (params?: { status?: string; pattern_type?: string; child_id?: string; page?: number; per_page?: number }) => {
    const qs = new URLSearchParams();
    if (params?.status) qs.set("status", params.status);
    if (params?.pattern_type) qs.set("pattern_type", params.pattern_type);
    if (params?.child_id) qs.set("child_id", params.child_id);
    if (params?.page) qs.set("page", String(params.page));
    if (params?.per_page) qs.set("per_page", String(params.per_page));
    const q = qs.toString();
    return request<{ items: FamilyInsightItem[]; total: number; page: number; per_page: number }>(
      `/household/family-insights${q ? `?${q}` : ""}`
    );
  },
  get: (id: string) => request<FamilyInsightDetail>(`/household/family-insights/${id}`),
  updateStatus: (id: string, data: { status: string; parent_response?: string }) =>
    request<{ status: string; insight_id: string }>(`/household/family-insights/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  config: () => request<FamilyInsightConfigData>(`/household/family-insights/config`),
  updateConfig: (data: { enabled?: boolean; pattern_settings?: Record<string, object> }) =>
    request<{ status: string; changes: object }>(`/household/family-insights/config`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  summary: () => request<FamilyInsightSummary>(`/household/family-insights/summary`),
};

export interface FamilyInsightItem {
  id: string;
  pattern_type: string;
  affected_children: Array<{ id: string; name: string }>;
  affected_nodes: Array<{ id: string; title: string }>;
  affected_subjects: string[];
  confidence: number;
  recommendation: string;
  status: string;
  is_predictive: boolean;
  predictive_child: { id: string; name: string } | null;
  parent_response: string | null;
  false_positive: boolean | null;
  created_at: string;
}

export interface FamilyInsightDetail extends FamilyInsightItem {
  evidence_json: object;
}

export interface FamilyInsightConfigData {
  enabled: boolean;
  pattern_settings: Record<string, Record<string, any>>;
  is_default?: boolean;
}

export interface FamilyInsightSummary {
  total_active: number;
  by_pattern_type: Record<string, number>;
  by_status: Record<string, number>;
  predictive_count: number;
}

// ── Wellbeing (PARENT-ONLY) ──
export const wellbeing = {
  anomalies: (childId: string, params?: { status?: string; anomaly_type?: string; page?: number }) => {
    const qs = new URLSearchParams();
    if (params?.status) qs.set("status", params.status);
    if (params?.anomaly_type) qs.set("anomaly_type", params.anomaly_type);
    if (params?.page) qs.set("page", String(params.page));
    const q = qs.toString();
    return request<{ items: WellbeingAnomalyItem[]; total: number }>(`/children/${childId}/wellbeing/anomalies${q ? `?${q}` : ""}`);
  },
  anomalyDetail: (childId: string, anomalyId: string) =>
    request<WellbeingAnomalyDetail>(`/children/${childId}/wellbeing/anomalies/${anomalyId}`),
  updateStatus: (childId: string, anomalyId: string, data: { status: string; parent_response?: string }) =>
    request<{ status: string; anomaly_id: string }>(`/children/${childId}/wellbeing/anomalies/${anomalyId}/status`, {
      method: "PATCH", body: JSON.stringify(data),
    }),
  config: (childId: string) => request<WellbeingConfigData>(`/children/${childId}/wellbeing/config`),
  updateConfig: (childId: string, data: Record<string, unknown>) =>
    request<{ status: string; changes: object }>(`/children/${childId}/wellbeing/config`, {
      method: "PATCH", body: JSON.stringify(data),
    }),
  summary: (childId: string) => request<WellbeingSummary>(`/children/${childId}/wellbeing/summary`),
};

export interface WellbeingAnomalyItem {
  id: string;
  anomaly_type: string;
  severity: number;
  affected_subjects: string[];
  parent_message: string;
  status: string;
  sensitivity_level: string;
  created_at: string;
  false_positive: boolean | null;
  parent_response: string | null;
}

export interface WellbeingAnomalyDetail extends WellbeingAnomalyItem {
  evidence_json: Record<string, any>;
}

export interface WellbeingConfigData {
  enabled: boolean;
  sensitivity_level: string;
  custom_thresholds: Record<string, any>;
  threshold_adjustments: Record<string, number>;
  total_false_positives: number;
  is_default?: boolean;
}

export interface WellbeingSummary {
  total_active: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  total_resolved: number;
  total_dismissed: number;
  sensitivity_level: string;
  enabled: boolean;
  threshold_adjustments: Record<string, number>;
}

// Family invite endpoints live under the auth router prefix on the backend.
// See backend/app/api/auth.py: APIRouter(prefix="/auth").
export const familyInvites = {
  invite: (email: string, role: string) =>
    request<{ invited: boolean }>("/auth/household/invite", { method: "POST", body: JSON.stringify({ email, role }) }),
  list: () => request<any[]>("/auth/household/invites"),
  revoke: (inviteId: string) => request<{ revoked: boolean }>(`/auth/household/invites/${inviteId}`, { method: "DELETE" }),
  accept: (token: string, password: string, displayName: string) =>
    request<any>("/auth/accept-invite", { method: "POST", body: JSON.stringify({ token, password, display_name: displayName }) }),
};

// ── Resources ──
export const resources = {
  list: (params?: { resource_type?: string; subject_area?: string; status?: string }) => {
    const qs = params ? new URLSearchParams(Object.entries(params).filter(([, v]) => v) as string[][]).toString() : "";
    return request<any[]>(`/resources${qs ? `?${qs}` : ""}`);
  },
  create: (data: object) => request<any>("/resources", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: object) => request<any>(`/resources/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  remove: (id: string) => request<any>(`/resources/${id}`, { method: "DELETE" }),
  link: (id: string, nodeId: string) => request<any>(`/resources/${id}/link/${nodeId}`, { method: "POST" }),
  unlink: (id: string, nodeId: string) => request<any>(`/resources/${id}/link/${nodeId}`, { method: "DELETE" }),
};

// ── Activity Feedback ──
export const feedback = {
  create: (activityId: string, childId: string, message: string, feedbackType = "comment") =>
    request<object>(`/activities/${activityId}/feedback`, { method: "POST", body: JSON.stringify({ message, feedback_type: feedbackType, child_id: childId }) }),
  list: (activityId: string) => request<any[]>(`/activities/${activityId}/feedback`),
  recent: (childId: string, limit = 10) => request<any[]>(`/children/${childId}/feedback/recent?limit=${limit}`),
};

// ── Beta Feedback (parent-to-METHEAN) ──
export interface BetaFeedbackItem {
  id: string;
  feedback_type: "bug" | "feature_request" | "usability" | "content" | "general";
  page_context: string | null;
  rating: number | null;
  message: string;
  screenshot_url: string | null;
  status: "new" | "reviewed" | "in_progress" | "resolved" | "wont_fix";
  admin_notes: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export const betaFeedback = {
  submit: (data: {
    feedback_type: BetaFeedbackItem["feedback_type"];
    page_context?: string;
    rating?: number;
    message: string;
    screenshot_url?: string;
  }) =>
    request<BetaFeedbackItem>(`/feedback`, { method: "POST", body: JSON.stringify(data) }),
  list: (limit = 50) => request<BetaFeedbackItem[]>(`/feedback?limit=${limit}`),
  get: (id: string) => request<BetaFeedbackItem>(`/feedback/${id}`),
};

// ── Reading Log ──
export const readingLog = {
  create: (childId: string, data: object) =>
    request<object>(`/children/${childId}/reading-log`, { method: "POST", body: JSON.stringify(data) }),
  list: (childId: string, params?: { status?: string; subject_area?: string }) => {
    const qs = new URLSearchParams();
    if (params?.status) qs.set("status", params.status);
    if (params?.subject_area) qs.set("subject_area", params.subject_area);
    const q = qs.toString();
    return request<any[]>(`/children/${childId}/reading-log${q ? `?${q}` : ""}`);
  },
  update: (entryId: string, data: object) =>
    request<object>(`/reading-log/${entryId}`, { method: "PUT", body: JSON.stringify(data) }),
  stats: (childId: string) => request<any>(`/children/${childId}/reading-log/stats`),
  current: (childId: string) => request<any[]>(`/children/${childId}/reading-log/current`),
};

// ── Assessment ──
export const assessment = {
  create: (childId: string, data: object) =>
    request<object>(`/children/${childId}/assessments`, { method: "POST", body: JSON.stringify(data) }),
  list: (childId: string) => request<{ items: object[]; total: number }>(`/children/${childId}/assessments`),
  createPortfolio: (childId: string, data: object) =>
    request<object>(`/children/${childId}/portfolio`, { method: "POST", body: JSON.stringify(data) }),
  listPortfolio: (childId: string) => request<{ items: object[]; total: number }>(`/children/${childId}/portfolio`),
  transcript: (childId: string, year?: number) =>
    request<object>(`/children/${childId}/transcript${year ? `?year=${year}` : ""}`),
  exportPortfolio: (childId: string, start: string, end: string) =>
    request<object>(`/children/${childId}/portfolio/export?from=${start}&to=${end}`),
};

// ── Education Plan ──
export const educationPlan = {
  generate: (childId: string, data: object) =>
    request<object>(`/children/${childId}/education-plan/generate`, { method: "POST", body: JSON.stringify(data) }),
  get: (childId: string) => request<object>(`/children/${childId}/education-plan`),
  approve: (childId: string) =>
    request<object>(`/children/${childId}/education-plan/approve`, { method: "POST" }),
  update: (childId: string, data: object) =>
    request<object>(`/children/${childId}/education-plan`, { method: "PUT", body: JSON.stringify(data) }),
};

// ── Annual Curriculum ──
export const annualCurriculum = {
  generate: (childId: string, data: object) =>
    request<object>(`/children/${childId}/curricula/generate`, { method: "POST", body: JSON.stringify(data) }),
  list: (childId: string) =>
    request<any[]>(`/children/${childId}/curricula`),
  detail: (curriculumId: string) =>
    request<any>(`/curricula/${curriculumId}`),
  weekDetail: (curriculumId: string, weekNumber: number) =>
    request<any>(`/curricula/${curriculumId}/weeks/${weekNumber}`),
  approve: (curriculumId: string) =>
    request<object>(`/curricula/${curriculumId}/approve`, { method: "POST" }),
  updateWeekNotes: (curriculumId: string, weekNumber: number, notes: string) =>
    request<object>(`/curricula/${curriculumId}/weeks/${weekNumber}/notes`, { method: "PUT", body: JSON.stringify({ notes }) }),
  addActivity: (curriculumId: string, weekNumber: number, data: object) =>
    request<object>(`/curricula/${curriculumId}/weeks/${weekNumber}/activities`, { method: "POST", body: JSON.stringify(data) }),
  removeActivity: (curriculumId: string, weekNumber: number, activityId: string) =>
    request<object>(`/curricula/${curriculumId}/weeks/${weekNumber}/activities/${activityId}`, { method: "DELETE" }),
  editActivity: (curriculumId: string, weekNumber: number, activityId: string, data: object) =>
    request<object>(`/curricula/${curriculumId}/weeks/${weekNumber}/activities/${activityId}`, { method: "PUT", body: JSON.stringify(data) }),
  moveActivity: (curriculumId: string, weekNumber: number, activityId: string, targetWeek: number) =>
    request<object>(`/curricula/${curriculumId}/weeks/${weekNumber}/activities/${activityId}/move`, { method: "POST", body: JSON.stringify({ target_week_number: targetWeek }) }),
  completeWeek: (curriculumId: string, weekNumber: number, notes?: string) =>
    request<object>(`/curricula/${curriculumId}/weeks/${weekNumber}/complete${notes ? `?notes=${encodeURIComponent(notes)}` : ""}`, { method: "POST" }),
  history: (childId: string) =>
    request<any>(`/children/${childId}/curricula/history`),
  historyYear: (childId: string, year: string) =>
    request<any[]>(`/children/${childId}/curricula/history/${year}`),
};

// Types
export interface ChildDashboardResponse {
  child: {
    first_name: string;
    grade_level: string | null;
    streak: { current: number; longest: number; is_today_complete: boolean };
    recent_achievements: Array<{ title: string; icon: string; earned_at: string | null }>;
  };
  greeting: string;
  today: {
    total_activities: number;
    completed: number;
    estimated_minutes_remaining: number;
    activities: Array<{
      id: string; title: string; subject: string; subject_color: string;
      type: string; estimated_minutes: number | null; status: string;
      is_review: boolean; node_title: string; node_mastery: string;
      sequence_number: number;
    }>;
  };
  progress: {
    overall_mastery_percentage: number;
    nodes_mastered: number;
    nodes_total: number;
    subjects: Array<{ name: string; color: string; mastered: number; total: number; percentage: number }>;
    this_week: { activities_completed: number; time_spent_minutes: number; mastery_transitions_up: number; mastery_transitions_down: number };
  };
  journey_maps: Array<{
    map_id: string; subject: string; subject_color: string;
    nodes: Array<{ id: string; title: string; mastery: string; is_current: boolean; is_next: boolean }>;
    total_nodes: number; mastered_nodes: number;
  }>;
  encouragement: string;
  style_hints: { optimal_session_minutes: number | null; best_time_of_day: string | null; attention_pattern: string | null };
}

export interface ChildListItem {
  id: string;
  first_name: string;
  last_name: string | null;
  date_of_birth: string | null;
  grade_level: string | null;
  enrollment_count: number;
}

export interface User {
  id: string;
  household_id: string;
  email: string;
  display_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface ChildState {
  child_id: string;
  nodes: NodeState[];
  total_nodes: number;
  mastered_count: number;
  in_progress_count: number;
  not_started_count: number;
}

export interface NodeState {
  node_id: string;
  node_title: string;
  mastery_level: string;
  is_unlocked: boolean;
  attempts_count: number;
  time_spent_minutes: number;
  last_activity_at: string | null;
  fsrs_due: string | null;
  fsrs_stability: number | null;
  fsrs_retrievability: number | null;
  fsrs_state: number | null;
}

export interface RetentionSummary {
  child_id: string;
  total_nodes: number;
  mastered_count: number;
  in_progress_count: number;
  not_started_count: number;
  decaying_count: number;
  blocked_count: number;
  average_retrievability: number | null;
}

export interface MapState {
  child_id: string;
  learning_map_id: string;
  map_name: string;
  enrolled: boolean;
  progress_pct: number;
  nodes: MapNodeState[];
}

export interface MapNodeState {
  node_id: string;
  node_type: string;
  title: string;
  mastery_level: string;
  status: string;
  is_unlocked: boolean;
  prerequisites_met: boolean;
  prerequisite_node_ids: string[];
  attempts_count: number;
  time_spent_minutes: number;
}

export interface Plan {
  id: string;
  household_id: string;
  child_id: string;
  name: string;
  description: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  ai_generated: boolean;
  ai_run_id: string | null;
  created_at: string;
}

export interface PlanDetail extends Plan {
  activities: ActivityInPlan[];
}

export interface ActivityInPlan {
  id: string;
  title: string;
  activity_type: string;
  description: string | null;
  estimated_minutes: number | null;
  status: string;
  scheduled_date: string | null;
  node_id: string | null;
  sort_order: number;
}

export interface MapDetail {
  id: string;
  household_id: string;
  subject_id: string;
  name: string;
  description: string | null;
  version: number;
  is_published: boolean;
  nodes: MapNode[];
  edges: MapEdge[];
  created_at: string;
}

export interface MapNode {
  id: string;
  learning_map_id: string;
  household_id: string;
  node_type: string;
  title: string;
  description: string | null;
  content: object | null;
  estimated_minutes: number | null;
  sort_order: number;
  is_active: boolean;
  created_at: string;
}

export interface MapEdge {
  id: string;
  learning_map_id: string;
  from_node_id: string;
  to_node_id: string;
  relation: string;
  weight: number;
  created_at: string;
}

export interface LearningMap {
  id: string;
  household_id: string;
  subject_id: string;
  name: string;
  description: string | null;
  version: number;
  is_published: boolean;
  created_at: string;
}

export interface Subject {
  id: string;
  name: string;
  color: string | null;
}

export interface Template {
  template_id: string;
  name: string;
  description: string;
  subject_count: number;
  node_count: number;
}

export interface Attempt {
  id: string;
  activity_id: string;
  child_id: string;
  status: string;
  started_at: string;
  completed_at: string | null;
  duration_minutes: number | null;
  score: number | null;
  feedback: object | null;
}

export interface AttemptSubmitResult {
  attempt: Attempt;
  mastery_level: string;
  previous_mastery: string;
  fsrs_due: string | null;
  fsrs_rating: number;
  state_event_id: string;
  nodes_unblocked: string[];
}

export interface TutorResponse {
  message: string;
  hints: string[];
  encouragement: boolean;
  ai_run_id: string;
}

export interface GovernanceRule {
  id: string;
  household_id: string;
  rule_type: string;
  scope: string;
  name: string;
  description: string | null;
  parameters: object;
  is_active: boolean;
  priority: number;
  created_at: string;
}

export interface GovernanceEvaluation {
  rule: string;
  type: string;
  passed: boolean;
  reason: string;
}

export interface GovernanceEvent {
  id: string;
  household_id: string;
  user_id: string | null;
  action: string;
  target_type: string;
  target_id: string;
  reason: string | null;
  metadata_: { source?: string; evaluations?: GovernanceEvaluation[]; blocking_rules?: string[] } | null;
  created_at: string;
}

export interface AIRun {
  id: string;
  household_id: string;
  run_type: string;
  status: string;
  model_used: string | null;
  input_tokens: number | null;
  output_tokens: number | null;
  input_data: object | null;
  output_data: object | null;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface ContextDetailResponse {
  role: string;
  legacy: boolean;
  token_budget: number;
  tokens_used: number;
  sources: Array<{ name: string; tokens: number; required: boolean; truncated: boolean }>;
  sources_excluded: string[];
  context_text: string;
  raw_input?: object;
}

export interface AdvisorReport {
  id: string;
  child_id: string;
  report_type: string;
  period_start: string;
  period_end: string;
  content: object;
  recommendations: string[];
  parent_reviewed: boolean;
  created_at: string;
}

export interface StateEvent {
  id: string;
  child_id: string;
  node_id: string;
  event_type: string;
  from_state: string | null;
  to_state: string | null;
  trigger: string | null;
  created_at: string;
}

export interface DecisionTrace {
  plan_id: string;
  ai_run: object | null;
  activity_decisions: {
    activity_id: string;
    title: string;
    status: string;
    instructions: object;
    governance_events: {
      action: string;
      reason: string | null;
      created_at: string | null;
    }[];
  }[];
}
