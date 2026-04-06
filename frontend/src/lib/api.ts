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
// Children
export const children = {
  list: () => request<ChildListItem[]>("/children"),
  state: (childId: string) => request<ChildState>(`/children/${childId}/state`),
  mapState: (childId: string, mapId: string) =>
    request<MapState>(`/children/${childId}/map-state/${mapId}`),
  allMapState: (childId: string) =>
    request<MapState[]>(`/children/${childId}/map-state`),
  retentionSummary: (childId: string) =>
    request<RetentionSummary>(`/children/${childId}/retention-summary`),
  nodeHistory: (childId: string, nodeId: string) =>
    request<StateEvent[]>(`/children/${childId}/nodes/${nodeId}/history`),
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
};

// Tutor
export const tutor = {
  message: (activityId: string, childId: string, message: string) =>
    request<TutorResponse>(`/tutor/${activityId}/message`, {
      method: "POST",
      body: JSON.stringify({ child_id: childId, message }),
    }),
};

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
  initDefaults: () => request<GovernanceRule[]>("/governance-rules/defaults", { method: "POST" }),
  events: (limit?: number) => request<GovernanceEvent[]>(`/governance-events?limit=${limit || 50}`),
};

// AI
export const ai = {
  runs: (params?: { role?: string }) =>
    request<AIRun[]>(`/ai-runs${params?.role ? `?role=${params.role}` : ""}`),
  run: (runId: string) => request<AIRun>(`/ai-runs/${runId}`),
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

// ── Activity Feedback ──
export const feedback = {
  create: (activityId: string, childId: string, message: string, feedbackType = "comment") =>
    request<object>(`/activities/${activityId}/feedback`, { method: "POST", body: JSON.stringify({ message, feedback_type: feedbackType, child_id: childId }) }),
  list: (activityId: string) => request<any[]>(`/activities/${activityId}/feedback`),
  recent: (childId: string, limit = 10) => request<any[]>(`/children/${childId}/feedback/recent?limit=${limit}`),
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

export interface GovernanceEvent {
  id: string;
  household_id: string;
  user_id: string | null;
  action: string;
  target_type: string;
  target_id: string;
  reason: string | null;
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
