"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { curriculum, type MapDetail, type MapNode, type MapEdge } from "@/lib/api";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

const typeColors: Record<string, string> = {
  root: "bg-(--color-text) text-white",
  milestone: "bg-(--color-accent-light) text-(--color-accent)",
  concept: "bg-(--color-warning-light) text-(--color-warning)",
  skill: "bg-(--color-success-light) text-(--color-success)",
};

interface EditorNode {
  id: string;
  title: string;
  node_type: string;
  description: string;
  estimated_minutes: number | null;
  sort_order: number;
  is_new?: boolean;
  is_deleted?: boolean;
  is_modified?: boolean;
}

interface EditorEdge {
  id: string;
  from_node_id: string;
  to_node_id: string;
  is_new?: boolean;
  is_deleted?: boolean;
}

// Build tier layout
function buildTiers(nodes: EditorNode[], edges: EditorEdge[]): EditorNode[][] {
  const active = nodes.filter((n) => !n.is_deleted);
  const activeEdges = edges.filter((e) => !e.is_deleted);
  const depths = new Map<string, number>();
  const childMap = new Map<string, string[]>();

  active.forEach((n) => {
    const incoming = activeEdges.filter((e) => e.to_node_id === n.id);
    if (incoming.length === 0) depths.set(n.id, 0);
  });

  activeEdges.forEach((e) => {
    const children = childMap.get(e.from_node_id) || [];
    children.push(e.to_node_id);
    childMap.set(e.from_node_id, children);
  });

  const queue = [...depths.keys()];
  while (queue.length > 0) {
    const id = queue.shift()!;
    const d = depths.get(id) || 0;
    (childMap.get(id) || []).forEach((cid) => {
      if ((depths.get(cid) ?? -1) < d + 1) {
        depths.set(cid, d + 1);
        queue.push(cid);
      }
    });
  }

  active.forEach((n) => { if (!depths.has(n.id)) depths.set(n.id, 0); });
  const maxD = Math.max(...depths.values(), 0);
  const tiers: EditorNode[][] = Array.from({ length: maxD + 1 }, () => []);
  active.forEach((n) => tiers[depths.get(n.id) || 0].push(n));
  return tiers;
}

export default function EditorPage() {
  const params = useSearchParams();
  const mapId = params.get("map_id") || "";

  const [mapName, setMapName] = useState("");
  const [nodes, setNodes] = useState<EditorNode[]>([]);
  const [edges, setEdges] = useState<EditorEdge[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [connecting, setConnecting] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { if (mapId) loadMap(); }, [mapId]);

  async function loadMap() {
    setLoading(true);
    try {
      const detail = await curriculum.getMap(mapId);
      setMapName(detail.name);
      setNodes(detail.nodes.filter((n) => n.is_active).map((n) => ({
        id: n.id, title: n.title, node_type: n.node_type,
        description: n.description || "", estimated_minutes: n.estimated_minutes,
        sort_order: n.sort_order,
      })));
      setEdges(detail.edges.map((e) => ({
        id: e.id, from_node_id: e.from_node_id, to_node_id: e.to_node_id,
      })));
    } catch {} finally { setLoading(false); }
  }

  function addNode(nodeType: string) {
    const id = `new-${Date.now()}`;
    setNodes([...nodes, {
      id, title: `New ${nodeType}`, node_type: nodeType,
      description: "", estimated_minutes: 30, sort_order: nodes.length,
      is_new: true,
    }]);
    setSelected(id);
  }

  function updateNode(id: string, field: string, value: any) {
    setNodes(nodes.map((n) => n.id === id ? { ...n, [field]: value, is_modified: !n.is_new } : n));
  }

  function deleteNode(id: string) {
    if (nodes.find((n) => n.id === id)?.is_new) {
      setNodes(nodes.filter((n) => n.id !== id));
      setEdges(edges.filter((e) => e.from_node_id !== id && e.to_node_id !== id));
    } else {
      setNodes(nodes.map((n) => n.id === id ? { ...n, is_deleted: true } : n));
      setEdges(edges.map((e) =>
        e.from_node_id === id || e.to_node_id === id ? { ...e, is_deleted: true } : e
      ));
    }
    if (selected === id) setSelected(null);
  }

  function startConnect(fromId: string) {
    setConnecting(fromId);
  }

  function finishConnect(toId: string) {
    if (!connecting || connecting === toId) { setConnecting(null); return; }
    // Check if edge already exists
    const exists = edges.some((e) =>
      !e.is_deleted && e.from_node_id === connecting && e.to_node_id === toId
    );
    if (!exists) {
      setEdges([...edges, {
        id: `new-edge-${Date.now()}`, from_node_id: connecting, to_node_id: toId, is_new: true,
      }]);
    }
    setConnecting(null);
  }

  function deleteEdge(edgeId: string) {
    if (edges.find((e) => e.id === edgeId)?.is_new) {
      setEdges(edges.filter((e) => e.id !== edgeId));
    } else {
      setEdges(edges.map((e) => e.id === edgeId ? { ...e, is_deleted: true } : e));
    }
  }

  async function saveAll() {
    setSaving(true);
    setError("");
    setSaved(false);
    try {
      const csrf = getCsrf();
      const resp = await fetch(`${API}/learning-maps/${mapId}/batch`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify({
          nodes_create: nodes.filter((n) => n.is_new && !n.is_deleted).map((n) => ({
            node_type: n.node_type, title: n.title, description: n.description,
            estimated_minutes: n.estimated_minutes, sort_order: n.sort_order,
          })),
          nodes_update: nodes.filter((n) => n.is_modified && !n.is_new && !n.is_deleted).map((n) => ({
            id: n.id, title: n.title, description: n.description,
            node_type: n.node_type, estimated_minutes: n.estimated_minutes, sort_order: n.sort_order,
          })),
          nodes_delete: nodes.filter((n) => n.is_deleted && !n.is_new).map((n) => n.id),
          edges_create: edges.filter((e) => e.is_new && !e.is_deleted).map((e) => ({
            from_node_id: e.from_node_id, to_node_id: e.to_node_id,
          })),
          edges_delete: edges.filter((e) => e.is_deleted && !e.is_new).map((e) => e.id),
        }),
      });
      if (resp.ok) {
        setSaved(true);
        await loadMap(); // Reload to get real IDs
        setTimeout(() => setSaved(false), 3000);
      } else {
        const d = await resp.json();
        setError(d.detail || "Save failed");
      }
    } catch (e: any) {
      setError(e.message || "Save failed");
    } finally { setSaving(false); }
  }

  async function enrichAll() {
    const csrf = getCsrf();
    await fetch(`${API}/learning-maps/${mapId}/enrich`, {
      method: "POST", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
    });
  }

  if (!mapId) return <div className="p-8 text-sm text-(--color-text-secondary)">No map selected. Go to Maps and click Edit.</div>;
  if (loading) return <div className="p-8 text-sm text-(--color-text-secondary)">Loading editor...</div>;

  const activeNodes = nodes.filter((n) => !n.is_deleted);
  const activeEdges = edges.filter((e) => !e.is_deleted);
  const tiers = buildTiers(nodes, edges);
  const selectedNode = selected ? nodes.find((n) => n.id === selected) : null;
  const hasChanges = nodes.some((n) => n.is_new || n.is_modified || n.is_deleted) ||
                     edges.some((e) => e.is_new || e.is_deleted);

  return (
    <div className="flex flex-col md:flex-row h-auto md:h-[calc(100vh-4rem)] -m-4 md:-m-8">
      {/* LEFT PANEL */}
      <div className="w-full md:w-52 bg-(--color-surface) border-b md:border-b-0 md:border-r border-(--color-border) p-4 flex flex-col shrink-0">
        <input value={mapName} onChange={(e) => setMapName(e.target.value)}
          className="text-sm font-semibold text-(--color-text) mb-3 px-2 py-1 border border-transparent hover:border-(--color-border) rounded-[6px]" />

        <div className="text-xs text-(--color-text-secondary) mb-3">
          {activeNodes.length} nodes &middot; {activeEdges.length} edges
        </div>

        <div className="space-y-1 mb-4">
          {["root", "milestone", "concept", "skill"].map((t) => (
            <button key={t} onClick={() => addNode(t)}
              className="w-full text-left px-2.5 py-1.5 text-xs rounded-[6px] border border-(--color-border) hover:bg-(--color-page) capitalize">
              + {t}
            </button>
          ))}
        </div>

        <div className="mt-auto space-y-2">
          <Button onClick={enrichAll} variant="secondary" size="sm" className="w-full text-(--color-accent)">
            Enrich All
          </Button>
          <Button onClick={saveAll} disabled={saving || !hasChanges} size="sm" className="w-full">
            {saving ? "Saving..." : hasChanges ? "Save Changes" : "No Changes"}
          </Button>
          {saved && <p className="text-[10px] text-(--color-success)">Saved!</p>}
          {error && <p className="text-[10px] text-(--color-danger)">{error}</p>}
        </div>
      </div>

      {/* MAIN CANVAS */}
      <div className="flex-1 overflow-auto bg-(--color-page) p-6">
        {connecting && (
          <div className="fixed top-16 left-1/2 -translate-x-1/2 bg-(--color-accent) text-white text-xs px-3 py-1.5 rounded-full z-10 shadow">
            Click a target node to connect &middot; <button onClick={() => setConnecting(null)} className="underline">Cancel</button>
          </div>
        )}

        <div className="space-y-2">
          {tiers.map((tier, tierIdx) => (
            <div key={tierIdx}>
              {tierIdx > 0 && <div className="flex justify-center py-1"><div className="w-px h-4 bg-(--color-border-strong)" /></div>}
              <div className="flex flex-wrap justify-center gap-3">
                {tier.map((node) => {
                  const isSelected = selected === node.id;
                  const isConnectTarget = connecting && connecting !== node.id;
                  const tc = typeColors[node.node_type] || "bg-(--color-page) text-(--color-text-secondary)";
                  return (
                    <div key={node.id}
                      onClick={() => isConnectTarget ? finishConnect(node.id) : setSelected(node.id)}
                      className={cn(
                        "relative w-44 p-3 rounded-[10px] border-2 cursor-pointer transition-all bg-(--color-surface) hover:shadow-sm",
                        isSelected ? "border-(--color-accent) ring-2 ring-(--color-accent)/20" :
                        isConnectTarget ? "border-(--color-success) ring-1 ring-(--color-success)/20" :
                        node.is_new ? "border-dashed border-(--color-accent)/50" :
                        node.is_modified ? "border-(--color-warning)" : "border-(--color-border)"
                      )}
                    >
                      <div className="flex items-center gap-1.5 mb-1">
                        <span className={`text-[9px] font-bold uppercase px-1 py-0.5 rounded-[4px] ${tc}`}>
                          {node.node_type}
                        </span>
                        {node.is_new && <span className="text-[9px] text-(--color-accent)">NEW</span>}
                      </div>
                      <div className="text-xs font-medium text-(--color-text) truncate">{node.title}</div>
                      {node.estimated_minutes && (
                        <div className="text-[10px] text-(--color-text-secondary) mt-0.5">{node.estimated_minutes}m</div>
                      )}
                      {!connecting && (
                        <button onClick={(e) => { e.stopPropagation(); startConnect(node.id); }}
                          className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-(--color-accent) border-2 border-white hover:bg-(--color-accent-hover)" title="Connect" />
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {activeNodes.length === 0 && (
          <div className="text-center py-16 text-sm text-(--color-text-secondary)">
            Add nodes from the left panel to start building.
          </div>
        )}
      </div>

      {/* RIGHT PANEL */}
      <div className="w-full md:w-72 bg-(--color-surface) border-t md:border-t-0 md:border-l border-(--color-border) p-4 shrink-0 overflow-y-auto">
        {selectedNode ? (
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider">Node Details</h3>

            <div>
              <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Title</label>
              <input value={selectedNode.title}
                onChange={(e) => updateNode(selectedNode.id, "title", e.target.value)}
                className="w-full px-2 py-1.5 text-sm border border-(--color-border) rounded-[6px]" />
            </div>

            <div>
              <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Type</label>
              <select value={selectedNode.node_type}
                onChange={(e) => updateNode(selectedNode.id, "node_type", e.target.value)}
                className="w-full px-2 py-1.5 text-sm border border-(--color-border) rounded-[6px]">
                {["root", "milestone", "concept", "skill"].map((t) => (
                  <option key={t} value={t} className="capitalize">{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Description</label>
              <textarea value={selectedNode.description}
                onChange={(e) => updateNode(selectedNode.id, "description", e.target.value)}
                className="w-full px-2 py-1.5 text-xs border border-(--color-border) rounded-[6px] h-16 resize-none" />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Minutes</label>
                <input type="number" value={selectedNode.estimated_minutes || ""}
                  onChange={(e) => updateNode(selectedNode.id, "estimated_minutes", parseInt(e.target.value) || null)}
                  className="w-full px-2 py-1.5 text-sm border border-(--color-border) rounded-[6px]" />
              </div>
              <div>
                <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Order</label>
                <input type="number" value={selectedNode.sort_order}
                  onChange={(e) => updateNode(selectedNode.id, "sort_order", parseInt(e.target.value) || 0)}
                  className="w-full px-2 py-1.5 text-sm border border-(--color-border) rounded-[6px]" />
              </div>
            </div>

            {/* Prerequisites */}
            <div>
              <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Prerequisites</label>
              <div className="space-y-1">
                {activeEdges.filter((e) => e.to_node_id === selectedNode.id).map((e) => {
                  const from = nodes.find((n) => n.id === e.from_node_id);
                  return (
                    <div key={e.id} className="flex items-center justify-between text-xs bg-(--color-page) rounded-[6px] px-2 py-1">
                      <span className="text-(--color-text-secondary)">{from?.title || "?"}</span>
                      <button onClick={() => deleteEdge(e.id)} className="text-(--color-danger) hover:opacity-80 text-[10px]">remove</button>
                    </div>
                  );
                })}
                {activeEdges.filter((e) => e.to_node_id === selectedNode.id).length === 0 && (
                  <span className="text-[10px] text-(--color-text-secondary)">None (root-level node)</span>
                )}
              </div>
            </div>

            {/* Dependents */}
            <div>
              <label className="block text-[10px] text-(--color-text-secondary) mb-0.5">Unlocks</label>
              <div className="space-y-1">
                {activeEdges.filter((e) => e.from_node_id === selectedNode.id).map((e) => {
                  const to = nodes.find((n) => n.id === e.to_node_id);
                  return (
                    <div key={e.id} className="text-xs text-(--color-text-secondary) bg-(--color-page) rounded-[6px] px-2 py-1">
                      {to?.title || "?"}
                    </div>
                  );
                })}
              </div>
            </div>

            <Button onClick={() => { if (confirm("Delete this node?")) deleteNode(selectedNode.id); }}
              variant="danger" size="sm" className="w-full mt-4">
              Delete Node
            </Button>
          </div>
        ) : (
          <div className="text-center py-8 text-xs text-(--color-text-secondary)">
            Select a node to edit its details.
          </div>
        )}
      </div>
    </div>
  );
}
