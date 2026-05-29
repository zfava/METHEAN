// Canvas particle engine for the celebration layer. Direct canvas +
// requestAnimationFrame (no third-party particle library) so we own the
// physics, color, and per-vibe theming. Physics are delta-time based so
// motion is frame-rate independent, and an FPS watchdog auto-scales the
// particle budget down if a slow device dips below 50fps.

export interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  rotation: number;
  rotationVelocity: number;
  life: number; // 0..1, 1 = just spawned, 0 = dead
  lifeDecay: number; // life lost per second (delta-time scaled)
  shape: ParticleShape;
  baseColor: [number, number, number]; // RGB at spawn
  endColor: [number, number, number]; // RGB at death, lerps as life decays
  size: number;
  opacity: number;
  /** Downward acceleration in px/s^2. 0 for drifting particles. */
  gravity: number;
}

export type ParticleShape = "circle" | "star" | "sparkle" | "leaf" | "ember" | "ring";

const MAX_PARTICLES = 500;
const FPS_WINDOW = 30;
const LOW_FPS = 50;
const LOW_SAMPLES_TO_SCALE = 5;
const MIN_TARGET = 25;
const MAX_DT = 0.05; // clamp huge gaps (tab was backgrounded)

function makeBlankParticle(): Particle {
  return {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    rotation: 0,
    rotationVelocity: 0,
    life: 0,
    lifeDecay: 1,
    shape: "circle",
    baseColor: [255, 255, 255],
    endColor: [255, 255, 255],
    size: 4,
    opacity: 1,
    gravity: 0,
  };
}

export class ParticleEngine {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private particles: Particle[] = [];
  private freeList: Particle[] = [];
  private rafId: number | null = null;
  private running = false;
  private lastFrameTime = 0;
  private cssWidth = 0;
  private cssHeight = 0;

  // Auto-scaler state.
  private targetCount = MAX_PARTICLES;
  private fpsBuffer: number[] = [];
  private frameCounter = 0;
  private lowSampleStreak = 0;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    const ctx = canvas.getContext("2d");
    if (!ctx) throw new Error("ParticleEngine: 2d context unavailable");
    this.ctx = ctx;
    // Pre-allocate the pool so steady-state emission does not allocate.
    for (let i = 0; i < MAX_PARTICLES; i++) this.freeList.push(makeBlankParticle());
    this.resize();
    window.addEventListener("resize", this.resize);
  }

  resize = () => {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    this.cssWidth = rect.width;
    this.cssHeight = rect.height;
    // Setting width/height resets the context transform, so scaling by
    // dpr once here is correct and does not compound across resizes.
    this.canvas.width = Math.max(1, Math.round(rect.width * dpr));
    this.canvas.height = Math.max(1, Math.round(rect.height * dpr));
    this.ctx.scale(dpr, dpr);
  };

  get width(): number {
    return this.cssWidth;
  }

  get height(): number {
    return this.cssHeight;
  }

  /** Push particles into the active pool, respecting the auto-scaled budget. */
  emit(incoming: Particle[]): void {
    for (const p of incoming) {
      if (this.particles.length >= this.targetCount) break;
      const slot = this.freeList.pop();
      if (slot) {
        // Reuse a dead slot to avoid allocation.
        slot.x = p.x;
        slot.y = p.y;
        slot.vx = p.vx;
        slot.vy = p.vy;
        slot.rotation = p.rotation;
        slot.rotationVelocity = p.rotationVelocity;
        slot.life = p.life;
        slot.lifeDecay = p.lifeDecay;
        slot.shape = p.shape;
        slot.baseColor = p.baseColor;
        slot.endColor = p.endColor;
        slot.size = p.size;
        slot.opacity = p.opacity;
        slot.gravity = p.gravity;
        this.particles.push(slot);
      } else {
        this.particles.push(p);
      }
    }
    if (!this.running) this.start();
  }

  start(): void {
    if (this.running) return;
    this.running = true;
    this.lastFrameTime = 0;
    this.rafId = window.requestAnimationFrame(this.frame);
  }

  stop(): void {
    this.running = false;
    if (this.rafId !== null) {
      window.cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
  }

  private frame = (t: number) => {
    if (!this.running) return;

    if (this.lastFrameTime === 0) {
      this.lastFrameTime = t;
      this.rafId = window.requestAnimationFrame(this.frame);
      return;
    }
    const dt = Math.min(MAX_DT, (t - this.lastFrameTime) / 1000);
    this.lastFrameTime = t;
    if (dt > 0) this.monitorFps(1 / dt);

    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.cssWidth, this.cssHeight);

    let alive = 0;
    for (let i = 0; i < this.particles.length; i++) {
      const p = this.particles[i];
      // Physics (delta-time scaled).
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += p.gravity * dt;
      p.rotation += p.rotationVelocity * dt;
      p.life -= p.lifeDecay * dt;

      if (p.life <= 0) {
        this.freeList.push(p);
        continue;
      }
      this.particles[alive++] = p;
      this.draw(p);
    }
    this.particles.length = alive;

    if (this.particles.length === 0) {
      ctx.clearRect(0, 0, this.cssWidth, this.cssHeight);
      this.stop();
      return;
    }
    this.rafId = window.requestAnimationFrame(this.frame);
  };

  private monitorFps(fps: number): void {
    this.fpsBuffer.push(fps);
    if (this.fpsBuffer.length > FPS_WINDOW) this.fpsBuffer.shift();
    this.frameCounter++;
    // One sample per full window.
    if (this.frameCounter % FPS_WINDOW !== 0 || this.fpsBuffer.length < FPS_WINDOW) return;
    const avg = this.fpsBuffer.reduce((a, b) => a + b, 0) / this.fpsBuffer.length;
    if (avg < LOW_FPS) {
      this.lowSampleStreak++;
      if (this.lowSampleStreak >= LOW_SAMPLES_TO_SCALE) {
        this.targetCount = Math.max(MIN_TARGET, Math.floor(this.targetCount / 2));
        this.lowSampleStreak = 0;
      }
    } else {
      this.lowSampleStreak = 0;
    }
  }

  private draw(p: Particle): void {
    const age = 1 - p.life; // 0 at spawn, 1 at death
    const r = Math.round(p.baseColor[0] + (p.endColor[0] - p.baseColor[0]) * age);
    const g = Math.round(p.baseColor[1] + (p.endColor[1] - p.baseColor[1]) * age);
    const b = Math.round(p.baseColor[2] + (p.endColor[2] - p.baseColor[2]) * age);
    // Ease-out opacity over (1 - life)^2.
    const alpha = Math.max(0, p.opacity * (1 - age * age));

    const ctx = this.ctx;
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rotation);
    const color = `rgb(${r}, ${g}, ${b})`;
    ctx.fillStyle = color;
    ctx.strokeStyle = color;

    switch (p.shape) {
      case "circle":
        this.drawCircle(p);
        break;
      case "star":
        this.drawStar(p);
        break;
      case "sparkle":
        this.drawSparkle(p);
        break;
      case "leaf":
        this.drawLeaf(p);
        break;
      case "ember":
        this.drawEmber(p, r, g, b, alpha);
        break;
      case "ring":
        this.drawRing(p);
        break;
    }
    ctx.restore();
  }

  private drawCircle(p: Particle): void {
    const ctx = this.ctx;
    ctx.beginPath();
    ctx.arc(0, 0, p.size, 0, Math.PI * 2);
    ctx.fill();
  }

  private drawStar(p: Particle): void {
    const ctx = this.ctx;
    const spikes = 5;
    const outer = p.size;
    const inner = p.size * 0.45;
    ctx.beginPath();
    for (let i = 0; i < spikes * 2; i++) {
      const radius = i % 2 === 0 ? outer : inner;
      const angle = (Math.PI / spikes) * i - Math.PI / 2;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fill();
  }

  private drawSparkle(p: Particle): void {
    // Four-pointed sparkle: two crossed tapered spikes with a bright core.
    const ctx = this.ctx;
    const s = p.size;
    const w = Math.max(0.6, s * 0.18);
    ctx.beginPath();
    ctx.moveTo(0, -s);
    ctx.lineTo(w, 0);
    ctx.lineTo(0, s);
    ctx.lineTo(-w, 0);
    ctx.closePath();
    ctx.moveTo(-s, 0);
    ctx.lineTo(0, w);
    ctx.lineTo(s, 0);
    ctx.lineTo(0, -w);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.arc(0, 0, w * 1.2, 0, Math.PI * 2);
    ctx.fill();
  }

  private drawLeaf(p: Particle): void {
    // Teardrop: a point at the top sweeping into a rounded base.
    const ctx = this.ctx;
    const s = p.size;
    ctx.beginPath();
    ctx.moveTo(0, -s);
    ctx.quadraticCurveTo(s, -s * 0.1, 0, s);
    ctx.quadraticCurveTo(-s, -s * 0.1, 0, -s);
    ctx.closePath();
    ctx.fill();
  }

  private drawEmber(p: Particle, r: number, g: number, b: number, alpha: number): void {
    // Small circle with a soft radial glow.
    const ctx = this.ctx;
    const s = p.size;
    const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, s * 2);
    grad.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${alpha})`);
    grad.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, ${alpha * 0.5})`);
    grad.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`);
    // The gradient already encodes alpha, so draw at full globalAlpha.
    const prev = ctx.globalAlpha;
    ctx.globalAlpha = 1;
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(0, 0, s * 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = prev;
  }

  private drawRing(p: Particle): void {
    const ctx = this.ctx;
    ctx.lineWidth = Math.max(0.8, p.size * 0.25);
    ctx.beginPath();
    ctx.arc(0, 0, p.size, 0, Math.PI * 2);
    ctx.stroke();
  }

  destroy(): void {
    this.stop();
    window.removeEventListener("resize", this.resize);
    this.particles.length = 0;
    this.freeList.length = 0;
  }
}
