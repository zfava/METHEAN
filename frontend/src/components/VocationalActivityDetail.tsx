"use client";

interface VocationalProps {
  instructions: {
    tools_required?: string[];
    materials?: Array<{ item: string; quantity: string; estimated_cost?: number }>;
    safety_notes?: string;
    workspace?: string;
    estimated_material_cost?: number;
    certification_alignment?: string;
    cross_subject_tags?: string[];
    cross_subject_notes?: string;
  } | null;
}

export default function VocationalActivityDetail({ instructions }: VocationalProps) {
  if (!instructions) return null;
  const { tools_required, materials, safety_notes, workspace, estimated_material_cost, certification_alignment } = instructions;
  const hasVocational = tools_required?.length || materials?.length || safety_notes;
  if (!hasVocational) return null;

  return (
    <div className="mt-3 pt-3 border-t border-(--color-border) space-y-2">
      {tools_required && tools_required.length > 0 && (
        <div>
          <div className="text-xs font-medium text-(--color-text-secondary) mb-1">Tools needed</div>
          <div className="flex flex-wrap gap-1">
            {tools_required.map((t, i) => (
              <span key={i} className="text-xs px-2 py-0.5 bg-(--color-page) border border-(--color-border) rounded">
                🔧 {t}
              </span>
            ))}
          </div>
        </div>
      )}
      {materials && materials.length > 0 && (
        <div>
          <div className="text-xs font-medium text-(--color-text-secondary) mb-1">
            Materials {estimated_material_cost ? `(~$${estimated_material_cost.toFixed(2)})` : ""}
          </div>
          {materials.map((m, i) => (
            <div key={i} className="text-xs text-(--color-text-secondary)">
              {m.quantity}× {m.item} {m.estimated_cost ? `($${m.estimated_cost.toFixed(2)})` : ""}
            </div>
          ))}
        </div>
      )}
      {safety_notes && (
        <div className="flex items-start gap-2 p-2 bg-(--color-danger-light) border border-(--color-danger)/20 rounded-[6px]">
          <span className="text-sm shrink-0">⚠️</span>
          <div className="text-xs text-(--color-danger)">{safety_notes}</div>
        </div>
      )}
      {workspace && (
        <div className="text-xs text-(--color-text-tertiary)">Workspace: {workspace}</div>
      )}
      {certification_alignment && (
        <div className="text-xs">
          <span className="text-(--color-text-tertiary)">Certification: </span>
          <span className="text-(--color-constitutional)">{certification_alignment}</span>
        </div>
      )}
    </div>
  );
}
