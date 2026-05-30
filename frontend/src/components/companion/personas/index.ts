export { Sage } from "./Sage";
export { Pip } from "./Pip";
export { Atlas } from "./Atlas";
export { Nova } from "./Nova";
export { Echo } from "./Echo";
export type { PersonaProps, Gaze } from "./types";

import { type ComponentType } from "react";

import { Sage } from "./Sage";
import { Pip } from "./Pip";
import { Atlas } from "./Atlas";
import { Nova } from "./Nova";
import { Echo } from "./Echo";
import type { PersonaProps } from "./types";

/** Persona id (profile.companion_voice) -> component. */
export const PERSONA_BY_ID: Record<string, ComponentType<PersonaProps>> = {
  default_warm: Sage,
  default_bright: Pip,
  default_steady: Atlas,
  default_playful: Nova,
  default_gentle: Echo,
};

/** Resolve a persona component from an id, falling back to Sage. */
export function personaFromId(id: string | null | undefined): ComponentType<PersonaProps> {
  return (id && PERSONA_BY_ID[id]) || Sage;
}
