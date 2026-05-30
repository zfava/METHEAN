import type { ComponentType } from "react";

import { VibeBackdropCalm } from "@/components/vibes/backdrops/VibeBackdropCalm";
import { VibeBackdropField } from "@/components/vibes/backdrops/VibeBackdropField";
import { VibeBackdropOrbit } from "@/components/vibes/backdrops/VibeBackdropOrbit";
import { VibeBackdropWorkshop } from "@/components/vibes/backdrops/VibeBackdropWorkshop";
import { VibeBackdropStudio } from "@/components/vibes/backdrops/VibeBackdropStudio";
import { VibeBackdropBold } from "@/components/vibes/backdrops/VibeBackdropBold";
import { MotifsCalm } from "@/components/vibes/motifs/MotifsCalm";
import { MotifsField } from "@/components/vibes/motifs/MotifsField";
import { MotifsOrbit } from "@/components/vibes/motifs/MotifsOrbit";
import { MotifsWorkshop } from "@/components/vibes/motifs/MotifsWorkshop";
import { MotifsStudio } from "@/components/vibes/motifs/MotifsStudio";
import { MotifsBold } from "@/components/vibes/motifs/MotifsBold";
import type { MotifLayerProps } from "@/components/vibes/motifs/shared";

// Frontend-only per-vibe environmental world. The backend continues to
// serve only the vibe id + tokens; the world (backdrop + motif layer) is
// resolved here from the id. Typography is handled via [data-vibe] CSS in
// globals.css. Unknown ids fall back to the calm world (same fallback
// philosophy as SPRING_BY_VIBE and CALM_VIBE_FALLBACK).

export interface VibeWorld {
  Backdrop: ComponentType;
  Motifs: ComponentType<MotifLayerProps>;
}

export const VIBE_WORLDS: Record<string, VibeWorld> = {
  calm: { Backdrop: VibeBackdropCalm, Motifs: MotifsCalm },
  field: { Backdrop: VibeBackdropField, Motifs: MotifsField },
  orbit: { Backdrop: VibeBackdropOrbit, Motifs: MotifsOrbit },
  workshop: { Backdrop: VibeBackdropWorkshop, Motifs: MotifsWorkshop },
  studio: { Backdrop: VibeBackdropStudio, Motifs: MotifsStudio },
  bold: { Backdrop: VibeBackdropBold, Motifs: MotifsBold },
};

export function worldFromVibe(vibe: string | null | undefined): VibeWorld {
  return (vibe && VIBE_WORLDS[vibe]) || VIBE_WORLDS.calm;
}
