/**
 * Canonical pedagogical philosophy options for the parent app.
 *
 * Mirrors the backend allowed set (CURRICULUM_PHILOSOPHIES). Each
 * option carries a one-line, plain-language description so a parent
 * who does not know the jargon can still choose well.
 */

export type CurriculumPhilosophy =
  | "traditional"
  | "classical"
  | "charlotte_mason"
  | "montessori"
  | "unschooling"
  | "eclectic";

export interface PhilosophyOption {
  id: CurriculumPhilosophy;
  label: string;
  description: string;
}

export const PHILOSOPHY_OPTIONS: PhilosophyOption[] = [
  {
    id: "traditional",
    label: "Traditional",
    description: "Step-by-step lessons, clear grade-level goals, practice and review.",
  },
  {
    id: "classical",
    label: "Classical",
    description: "Memorization, recitation, and great books, in a logical order.",
  },
  {
    id: "charlotte_mason",
    label: "Charlotte Mason",
    description: "Short lessons, living books, narration, and nature study.",
  },
  {
    id: "montessori",
    label: "Montessori",
    description: "Hands-on materials and self-paced discovery, concrete before abstract.",
  },
  {
    id: "unschooling",
    label: "Unschooling",
    description: "Interest-led learning through real life, no fixed lessons.",
  },
  {
    id: "eclectic",
    label: "Eclectic",
    description: "Mix and match a different approach for each subject.",
  },
];

/** Per-subject choices for the eclectic case exclude "eclectic" itself. */
export const ECLECTIC_SUBJECT_OPTIONS: PhilosophyOption[] = PHILOSOPHY_OPTIONS.filter(
  (o) => o.id !== "eclectic",
);

/** Subjects offered for per-subject philosophy in the eclectic case. */
export const ECLECTIC_SUBJECTS: Array<{ id: string; label: string }> = [
  { id: "mathematics", label: "Mathematics" },
  { id: "phonics_reading", label: "Phonics and Reading" },
  { id: "writing_grammar", label: "Writing and Grammar" },
  { id: "literature", label: "Literature" },
  { id: "science", label: "Science" },
  { id: "history", label: "History" },
];

export const DEFAULT_PHILOSOPHY: CurriculumPhilosophy = "traditional";
