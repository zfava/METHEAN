"use client";

import { useEffect, useState } from "react";
import { readingLog } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Tabs from "@/components/ui/Tabs";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

type Tab = "reading" | "completed" | "to_read" | "all";

const genreColors: Record<string, string> = {
  fiction: "bg-(--color-accent-light) text-(--color-accent)",
  nonfiction: "bg-(--color-success-light) text-(--color-success)",
  poetry: "bg-(--color-warning-light) text-(--color-warning)",
  biography: "bg-(--color-constitutional-light) text-(--color-constitutional)",
  reference: "bg-(--color-page) text-(--color-text-secondary)",
};

export default function ReadingPage() {
  useEffect(() => { document.title = "Reading Log | METHEAN"; }, []);
  const { toast } = useToast();

  const { selectedChild } = useChild();
  const [tab, setTab] = useState<Tab>("reading");
  const [entries, setEntries] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Add form state
  const [newTitle, setNewTitle] = useState("");
  const [newAuthor, setNewAuthor] = useState("");
  const [newGenre, setNewGenre] = useState("");
  const [newSubject, setNewSubject] = useState("");
  const [newPages, setNewPages] = useState("");
  const [newStatus, setNewStatus] = useState("reading");

  // Update form state
  const [updatePages, setUpdatePages] = useState("");
  const [updateNarration, setUpdateNarration] = useState("");
  const [updateNotes, setUpdateNotes] = useState("");

  useEffect(() => {
    if (selectedChild) loadData();
  }, [selectedChild, tab]);

  async function loadData() {
    setLoading(true);
    try {
      const statusFilter = tab === "all" ? undefined : tab;
      const [list, s] = await Promise.all([
        readingLog.list(selectedChild!.id, { status: statusFilter }),
        readingLog.stats(selectedChild!.id),
      ]);
      setEntries(list);
      setStats(s);
    } catch (err: any) {
      setError(err.detail || "Failed to load reading log");
    } finally { setLoading(false); }
  }

  async function addBook() {
    if (!newTitle.trim() || !selectedChild) return;
    await readingLog.create(selectedChild.id, {
      book_title: newTitle, book_author: newAuthor || null,
      genre: newGenre || null, subject_area: newSubject || null,
      pages_total: newPages ? parseInt(newPages) : null,
      status: newStatus,
    });
    toast("Entry logged", "success");
    setNewTitle(""); setNewAuthor(""); setNewGenre(""); setNewSubject(""); setNewPages("");
    setShowAddForm(false);
    loadData();
  }

  async function updateEntry(entryId: string, data: object) {
    await readingLog.update(entryId, data);
    setEditingId(null);
    loadData();
  }

  async function markComplete(entryId: string) {
    await readingLog.update(entryId, { status: "completed" });
    toast("Book completed!", "success");
    loadData();
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;

  return (
    <div className="max-w-4xl">
      <PageHeader
        title={`${selectedChild.first_name}'s Reading Log`}
        subtitle="Track books, pages, and narrations."
        actions={
          <Button variant="primary" size="sm" onClick={() => setShowAddForm(!showAddForm)}>
            {showAddForm ? "Cancel" : "Add Book"}
          </Button>
        }
      />

      {/* Add book form */}
      {showAddForm && (
        <Card className="mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
            <input value={newTitle} onChange={(e) => setNewTitle(e.target.value)} placeholder="Book title *"
              className="col-span-2 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <input value={newAuthor} onChange={(e) => setNewAuthor(e.target.value)} placeholder="Author"
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <input value={newPages} onChange={(e) => setNewPages(e.target.value)} placeholder="Total pages" type="number"
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <select value={newGenre} onChange={(e) => setNewGenre(e.target.value)}
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="">Genre</option>
              <option value="fiction">Fiction</option><option value="nonfiction">Nonfiction</option>
              <option value="poetry">Poetry</option><option value="biography">Biography</option>
              <option value="reference">Reference</option><option value="other">Other</option>
            </select>
            <select value={newSubject} onChange={(e) => setNewSubject(e.target.value)}
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="">Subject area</option>
              <option value="history">History</option><option value="science">Science</option>
              <option value="literature">Literature</option><option value="math">Math</option>
              <option value="theology">Theology</option><option value="other">Other</option>
            </select>
          </div>
          <div className="flex items-center gap-3">
            <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)}
              className="px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)">
              <option value="to_read">To Read</option><option value="reading">Currently Reading</option>
            </select>
            <Button variant="primary" size="sm" onClick={addBook} disabled={!newTitle.trim()}>Add</Button>
          </div>
        </Card>
      )}

      {/* Tabs */}
      <Tabs<Tab>
        tabs={[
          { key: "reading", label: "Currently Reading" },
          { key: "completed", label: "Completed" },
          { key: "to_read", label: "To Read" },
          { key: "all", label: "All" },
        ]}
        active={tab}
        onChange={setTab}
      />

      <div className="mt-4">
        {loading ? <LoadingSkeleton variant="list" count={4} /> : (
          <>
            {entries.length === 0 ? (
              <EmptyState icon="empty"
                title={tab === "reading" ? "Not currently reading any books" : tab === "completed" ? "No completed books yet" : tab === "to_read" ? "No books on the reading list" : "No books tracked yet"}
                description={tab === "reading" ? "Add a book and set it to 'Currently Reading' to start tracking." : tab === "to_read" ? "Build a reading list for the year ahead." : `Add your first book to start building ${selectedChild?.first_name || "your child"}'s reading record.`} />
            ) : (
              <div className="space-y-3">
                {entries.map((entry) => {
                  const gc = genreColors[entry.genre] || genreColors.reference;
                  const pct = entry.pages_total && entry.pages_read ? Math.round((entry.pages_read / entry.pages_total) * 100) : null;
                  const isEditing = editingId === entry.id;

                  return (
                    <Card key={entry.id}>
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-medium text-(--color-text)">{entry.book_title}</span>
                            {entry.genre && <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${gc}`}>{entry.genre}</span>}
                          </div>
                          {entry.book_author && <p className="text-xs text-(--color-text-secondary)">{entry.book_author}</p>}

                          {/* Progress bar for reading books */}
                          {entry.status === "reading" && pct !== null && (
                            <div className="flex items-center gap-2 mt-2">
                              <div className="flex-1 h-1.5 rounded-full bg-(--color-border) overflow-hidden">
                                <div className="h-full rounded-full bg-(--color-accent) transition-all" style={{ width: `${pct}%` }} />
                              </div>
                              <span className="text-[10px] text-(--color-text-tertiary)">{entry.pages_read}/{entry.pages_total} pages ({pct}%)</span>
                            </div>
                          )}

                          {entry.status === "completed" && (
                            <div className="flex items-center gap-3 mt-1 text-[10px] text-(--color-text-tertiary)">
                              {entry.completed_date && <span>Completed {entry.completed_date}</span>}
                              {entry.pages_read && <span>{entry.pages_read} pages</span>}
                              {entry.child_rating && <span>{"★".repeat(entry.child_rating)}{"☆".repeat(5 - entry.child_rating)}</span>}
                            </div>
                          )}

                          {/* Narration snippet */}
                          {entry.narration && !isEditing && (
                            <p className="text-xs text-(--color-text-secondary) mt-2 italic line-clamp-2">"{entry.narration}"</p>
                          )}
                          {entry.parent_notes && !isEditing && (
                            <p className="text-[10px] text-(--color-text-tertiary) mt-1">Parent: {entry.parent_notes}</p>
                          )}
                        </div>

                        <div className="flex items-center gap-2 shrink-0 ml-3">
                          {entry.status === "reading" && (
                            <>
                              <Button variant="ghost" size="sm" onClick={() => { setEditingId(isEditing ? null : entry.id); setUpdatePages(String(entry.pages_read || "")); setUpdateNarration(""); setUpdateNotes(""); }}>
                                {isEditing ? "Cancel" : "Update"}
                              </Button>
                              <Button variant="success" size="sm" onClick={() => markComplete(entry.id)}>Done</Button>
                            </>
                          )}
                          {entry.status === "to_read" && (
                            <Button variant="primary" size="sm" onClick={() => updateEntry(entry.id, { status: "reading" })}>Start</Button>
                          )}
                        </div>
                      </div>

                      {/* Inline update form */}
                      {isEditing && (
                        <div className="mt-3 pt-3 border-t border-(--color-border) space-y-2">
                          <div className="flex gap-2">
                            <input value={updatePages} onChange={(e) => setUpdatePages(e.target.value)} placeholder="Pages read" type="number"
                              className="w-24 px-2 py-1.5 text-xs border border-(--color-border) rounded-[10px] bg-(--color-surface)" />
                            <span className="text-xs text-(--color-text-tertiary) self-center">of {entry.pages_total || "?"}</span>
                          </div>
                          <textarea value={updateNarration} onChange={(e) => setUpdateNarration(e.target.value)}
                            placeholder="Narration (what did they read about?)"
                            className="w-full h-16 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface) text-(--color-text)" />
                          <textarea value={updateNotes} onChange={(e) => setUpdateNotes(e.target.value)}
                            placeholder="Your notes (optional)"
                            className="w-full h-12 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] resize-none bg-(--color-surface) text-(--color-text)" />
                          <Button variant="primary" size="sm" onClick={() => updateEntry(entry.id, {
                            pages_read: updatePages ? parseInt(updatePages) : undefined,
                            narration: updateNarration || undefined,
                            parent_notes: updateNotes || undefined,
                          })}>Save</Button>
                        </div>
                      )}
                    </Card>
                  );
                })}
              </div>
            )}
          </>
        )}
      </div>

      {/* Stats section */}
      {stats && stats.total_books > 0 && (
        <Card className="mt-6">
          <h3 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider mb-3">Reading Stats</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold text-(--color-text)">{stats.total_books}</div>
              <div className="text-[10px] text-(--color-text-tertiary) truncate">Total books</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-(--color-success)">{stats.books_completed}</div>
              <div className="text-[10px] text-(--color-text-tertiary) truncate">Completed</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-(--color-accent)">{stats.pages_read_total.toLocaleString()}</div>
              <div className="text-[10px] text-(--color-text-tertiary) truncate">Pages read</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-(--color-warning)">{Math.round((stats.minutes_total || 0) / 60)}h</div>
              <div className="text-[10px] text-(--color-text-tertiary) truncate">Reading time</div>
            </div>
          </div>
          {Object.keys(stats.by_genre || {}).length > 0 && (
            <div className="mt-4 pt-3 border-t border-(--color-border)">
              <div className="text-[10px] text-(--color-text-tertiary) mb-1.5">By genre</div>
              <div className="flex flex-wrap gap-2">
                {Object.entries(stats.by_genre).map(([genre, count]) => (
                  <span key={genre} className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${genreColors[genre] || genreColors.reference}`}>
                    {genre}: {count as number}
                  </span>
                ))}
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
