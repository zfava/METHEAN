"use client";

import { useEffect, useState } from "react";
import { resources } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Tabs from "@/components/ui/Tabs";
import EmptyState from "@/components/ui/EmptyState";

type Tab = "all" | "textbook" | "workbook" | "digital" | "other";

const typeBadge: Record<string, string> = {
  textbook: "bg-(--color-accent-light) text-(--color-accent)",
  workbook: "bg-(--color-success-light) text-(--color-success)",
  digital: "bg-(--color-warning-light) text-(--color-warning)",
  manipulative: "bg-(--color-constitutional-light) text-(--color-constitutional)",
  other: "bg-(--color-page) text-(--color-text-secondary)",
};

export default function ResourcesPage() {
  useEffect(() => { document.title = "Resources | METHEAN"; }, []);

  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [tab, setTab] = useState<Tab>("all");
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form state
  const [fName, setFName] = useState("");
  const [fType, setFType] = useState("textbook");
  const [fSubject, setFSubject] = useState("");
  const [fPublisher, setFPublisher] = useState("");
  const [fGrade, setFGrade] = useState("");
  const [fNotes, setFNotes] = useState("");
  const [fStatus, setFStatus] = useState("owned");

  useEffect(() => { loadData(); }, [tab]);

  async function loadData() {
    setLoading(true);
    setError("");
    try {
      const filter = tab === "all" ? {} : { resource_type: tab };
      setItems(await resources.list(filter));
    } catch (err: any) {
      setError(err.detail || err.message || "Failed to load resources.");
    } finally {
      setLoading(false);
    }
  }

  function resetForm() {
    setFName(""); setFType("textbook"); setFSubject(""); setFPublisher("");
    setFGrade(""); setFNotes(""); setFStatus("owned"); setEditingId(null);
  }

  async function handleSubmit() {
    if (!fName.trim()) return;
    try {
      if (editingId) {
        await resources.update(editingId, {
          name: fName, resource_type: fType, subject_area: fSubject || undefined,
          publisher: fPublisher || undefined, grade_range: fGrade || undefined,
          notes: fNotes || undefined, status: fStatus,
        });
      } else {
        await resources.create({
          name: fName, resource_type: fType, subject_area: fSubject || undefined,
          publisher: fPublisher || undefined, grade_range: fGrade || undefined,
          notes: fNotes || undefined, status: fStatus,
        });
      }
      resetForm();
      setShowForm(false);
      await loadData();
    } catch (err: any) {
      setError(err.detail || "Failed to save resource.");
    }
  }

  async function handleDelete(id: string) {
    await resources.remove(id);
    loadData();
  }

  function startEdit(item: any) {
    setFName(item.name); setFType(item.resource_type); setFSubject(item.subject_area || "");
    setFPublisher(item.publisher || ""); setFGrade(item.grade_range || "");
    setFNotes(item.notes || ""); setFStatus(item.status); setEditingId(item.id);
    setShowForm(true);
  }

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Resource Library"
        subtitle="Track your family's educational materials."
        actions={
          <Button variant="primary" size="sm" onClick={() => { resetForm(); setShowForm(!showForm); }}>
            {showForm ? "Cancel" : "Add Resource"}
          </Button>
        }
      />

      {/* Error */}
      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); loadData(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* Add/Edit form */}
      {showForm && (
        <Card className="mb-6">
          <h3 className="text-sm font-semibold text-(--color-text) mb-3">{editingId ? "Edit Resource" : "Add Resource"}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
            <input value={fName} onChange={(e) => setFName(e.target.value)} placeholder="Resource name *"
              className="col-span-1 md:col-span-2 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <select value={fType} onChange={(e) => setFType(e.target.value)}
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="textbook">Textbook</option>
              <option value="workbook">Workbook</option>
              <option value="digital">Digital</option>
              <option value="manipulative">Manipulative</option>
              <option value="other">Other</option>
            </select>
            <select value={fSubject} onChange={(e) => setFSubject(e.target.value)}
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="">Subject area</option>
              <option value="mathematics">Mathematics</option>
              <option value="language_arts">Language Arts</option>
              <option value="science">Science</option>
              <option value="history">History</option>
              <option value="art">Art</option>
              <option value="music">Music</option>
              <option value="other">Other</option>
            </select>
            <input value={fPublisher} onChange={(e) => setFPublisher(e.target.value)} placeholder="Publisher"
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <input value={fGrade} onChange={(e) => setFGrade(e.target.value)} placeholder="Grade range (e.g. K-3, 6-8)"
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <select value={fStatus} onChange={(e) => setFStatus(e.target.value)}
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="owned">Owned</option>
              <option value="borrowed">Borrowed</option>
              <option value="wishlist">Wishlist</option>
              <option value="digital_access">Digital Access</option>
            </select>
            <textarea value={fNotes} onChange={(e) => setFNotes(e.target.value)} placeholder="Notes"
              className="col-span-1 md:col-span-2 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) h-16 resize-none" />
          </div>
          <div className="flex gap-2">
            <Button variant="primary" size="sm" onClick={handleSubmit} disabled={!fName.trim()}>
              {editingId ? "Save Changes" : "Add"}
            </Button>
            {editingId && <Button variant="ghost" size="sm" onClick={() => { resetForm(); setShowForm(false); }}>Cancel</Button>}
          </div>
        </Card>
      )}

      {/* Tabs */}
      <Tabs<Tab>
        tabs={[
          { key: "all", label: "All" },
          { key: "textbook", label: "Textbooks" },
          { key: "workbook", label: "Workbooks" },
          { key: "digital", label: "Digital" },
          { key: "other", label: "Other" },
        ]}
        active={tab}
        onChange={setTab}
      />

      <div className="mt-4">
        {loading ? (
          <LoadingSkeleton variant="card" count={4} />
        ) : items.length === 0 ? (
          <EmptyState
            icon="empty"
            title="No resources tracked yet"
            description="Add your textbooks, workbooks, and materials to keep everything organized in one place."
          />
        ) : (
          <div className="space-y-3">
            {items.map((item) => {
              const badge = typeBadge[item.resource_type] || typeBadge.other;
              return (
                <Card key={item.id}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-medium text-(--color-text)">{item.name}</span>
                        <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${badge}`}>{item.resource_type}</span>
                        {item.status !== "owned" && (
                          <span className="text-[10px] text-(--color-text-tertiary) capitalize">{item.status}</span>
                        )}
                      </div>
                      <div className="flex items-center gap-3 text-[10px] text-(--color-text-tertiary)">
                        {item.publisher && <span>{item.publisher}</span>}
                        {item.subject_area && <span className="capitalize">{item.subject_area.replace("_", " ")}</span>}
                        {item.grade_range && <span>Grades {item.grade_range}</span>}
                        {item.linked_node_ids?.length > 0 && (
                          <span className="text-(--color-accent)">{item.linked_node_ids.length} linked node{item.linked_node_ids.length !== 1 ? "s" : ""}</span>
                        )}
                      </div>
                      {item.notes && (
                        <p className="text-xs text-(--color-text-secondary) mt-1 line-clamp-2">{item.notes}</p>
                      )}
                    </div>
                    <div className="flex items-center gap-1.5 shrink-0 ml-3">
                      <Button variant="ghost" size="sm" onClick={() => startEdit(item)}>Edit</Button>
                      <Button variant="ghost" size="sm" onClick={() => handleDelete(item.id)} className="text-(--color-danger)">Delete</Button>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
