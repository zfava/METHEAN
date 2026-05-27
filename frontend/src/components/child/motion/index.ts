/**
 * Motion primitives barrel. Tree-shakable named exports.
 *
 * Every primitive reads useMotion() internally and degrades to instant
 * render under reduceMotion. Public API:
 *
 *   <AmbientField mode={...} intensity={...} />
 *   <MotionCard breathing hoverLift onPress phase depth />
 *   <MotionButton variant size onPress />
 *   <MotionText as weight entrance delay />
 *   <Stagger gap children />
 *   <PageTransition viewKey mode children />
 *   <ShieldDraw size color delay variant />
 *   <Pulse intensity color children />
 *   <TactileInput children />
 *   <MilestoneMoment trigger soundCue children />
 */

export { AmbientField } from "./AmbientField";
export { MotionCard } from "./MotionCard";
export { MotionButton } from "./MotionButton";
export { MotionText } from "./MotionText";
export { Stagger } from "./Stagger";
export { PageTransition } from "./PageTransition";
export { ShieldDraw } from "./ShieldDraw";
export { Pulse } from "./Pulse";
export { TactileInput } from "./TactileInput";
export { MilestoneMoment } from "./MilestoneMoment";
