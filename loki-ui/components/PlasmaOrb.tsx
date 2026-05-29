"use client";

/**
 * PlasmaOrb — a half-destroyed planet (React Three Fiber).
 *
 * A dark solid planet core with a fractured neon-green particle shell — chunks
 * of the surface are "destroyed" (noise-gated gaps) and debris drifts outward.
 * The centre stays DARK; the glow radiates from the broken green crust.
 * Controlled bloom (no white blowout).
 *
 * Reacts to Loki's voice state via glow intensity + rotation speed.
 */

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";
import { type Status } from "@/hooks/useLoki";

interface OrbParams { spin: number; glow: number; }
const STATE_PARAMS: Record<Status, OrbParams> = {
  idle:      { spin: 0.06, glow: 1.0 },
  listening: { spin: 0.12, glow: 1.3 },
  thinking:  { spin: 0.30, glow: 1.55 },
  speaking:  { spin: 0.18, glow: 1.7 },
  offline:   { spin: 0.02, glow: 0.35 },
};

const SHELL_COUNT  = 2600;   // crust particles (fewer, as requested)
const DEBRIS_COUNT = 700;    // floating destroyed fragments
const R = 1.25;              // planet radius

// neon green palette (dark inner → bright neon → cyan spark)
const C_DEEP = new THREE.Color("#063b2a");  // dark emerald (crust base)
const C_MID  = new THREE.Color("#16f58a");  // neon green
const C_HOT  = new THREE.Color("#9dffc6");  // bright green-white spark
const C_RIM  = new THREE.Color("#00E5FF");  // cyan accent

// hash-based pseudo-noise for "destroyed" gaps (deterministic per direction)
function craterMask(x: number, y: number, z: number): number {
  // sum of a few sine bands → continents/craters; >thresh = solid crust
  const n =
    Math.sin(x * 3.1 + y * 1.7) * 0.5 +
    Math.sin(y * 2.3 - z * 2.9) * 0.5 +
    Math.sin(z * 3.7 + x * 1.3) * 0.5;
  return n; // ~[-1.5, 1.5]
}

const VERT = `
uniform float uTime; uniform float uGlow;
attribute float aScale; attribute vec3 aColor; attribute float aSeed;
varying vec3 vColor; varying float vA;
void main(){
  vColor = aColor;
  vec3 p = position;
  // tiny shimmer/drift per particle
  p += normalize(p) * sin(uTime * 1.2 + aSeed * 6.2831) * 0.012;
  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  vA = uGlow;
  gl_PointSize = aScale * (260.0 / -mv.z);
  gl_Position = projectionMatrix * mv;
}
`;

const FRAG = `
precision highp float;
varying vec3 vColor; varying float vA;
void main(){
  vec2 uv = gl_PointCoord - 0.5;
  float d = length(uv);
  if (d > 0.5) discard;
  float glow = smoothstep(0.5, 0.05, d);
  gl_FragColor = vec4(vColor, glow * vA);
}
`;

function buildShell() {
  const pos: number[] = [], col: number[] = [], scl: number[] = [], sd: number[] = [];
  const tmp = new THREE.Color();
  let made = 0, attempts = 0;
  while (made < SHELL_COUNT && attempts < SHELL_COUNT * 4) {
    attempts++;
    // random point on sphere
    const u = Math.random(), v = Math.random();
    const theta = u * Math.PI * 2;
    const phi = Math.acos(2 * v - 1);
    const nx = Math.sin(phi) * Math.cos(theta);
    const ny = Math.cos(phi);
    const nz = Math.sin(phi) * Math.sin(theta);
    // DESTROYED gaps: skip where crust is "blown away"
    if (craterMask(nx * 2, ny * 2, nz * 2) < -0.15) continue;
    const rr = R + (Math.random() - 0.5) * 0.06; // thin crust thickness
    pos.push(nx * rr, ny * rr, nz * rr);
    // brighter on jagged high points, neon green base, rare cyan spark
    const t = Math.random();
    if (t < 0.78)      tmp.copy(C_DEEP).lerp(C_MID, Math.random());
    else if (t < 0.96) tmp.copy(C_MID).lerp(C_HOT, Math.random() * 0.7);
    else               tmp.copy(C_RIM);
    col.push(tmp.r, tmp.g, tmp.b);
    scl.push(0.7 + Math.random() * 1.6);
    sd.push(Math.random());
    made++;
  }
  return {
    positions: new Float32Array(pos),
    colors: new Float32Array(col),
    scales: new Float32Array(scl),
    seeds: new Float32Array(sd),
    count: made,
  };
}

function buildDebris() {
  const pos = new Float32Array(DEBRIS_COUNT * 3);
  const col = new Float32Array(DEBRIS_COUNT * 3);
  const scl = new Float32Array(DEBRIS_COUNT);
  const sd  = new Float32Array(DEBRIS_COUNT);
  const tmp = new THREE.Color();
  for (let i = 0; i < DEBRIS_COUNT; i++) {
    const rr = R * (1.15 + Math.random() * 1.4); // floating outward
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    pos[i*3]   = rr * Math.sin(phi) * Math.cos(theta);
    pos[i*3+1] = rr * Math.cos(phi);
    pos[i*3+2] = rr * Math.sin(phi) * Math.sin(theta);
    tmp.copy(C_MID).lerp(C_DEEP, Math.random() * 0.6);
    col[i*3] = tmp.r; col[i*3+1] = tmp.g; col[i*3+2] = tmp.b;
    scl[i] = 0.4 + Math.random() * 0.9;
    sd[i]  = Math.random();
  }
  return { positions: pos, colors: col, scales: scl, seeds: sd };
}

function Planet({ status }: { status: Status }) {
  const grp = useRef<THREE.Group>(null);
  const shellMat = useRef<THREE.ShaderMaterial>(null);
  const debrisMat = useRef<THREE.ShaderMaterial>(null);
  const cur = useRef<OrbParams>({ ...STATE_PARAMS.idle });

  const shell  = useMemo(buildShell, []);
  const debris = useMemo(buildDebris, []);

  const shellU = useMemo(() => ({ uTime: { value: 0 }, uGlow: { value: 1 } }), []);
  const debrisU = useMemo(() => ({ uTime: { value: 0 }, uGlow: { value: 1 } }), []);

  useFrame((_, delta) => {
    const target = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const k = Math.min(delta * 2.0, 1);
    cur.current.spin += (target.spin - cur.current.spin) * k;
    cur.current.glow += (target.glow - cur.current.glow) * k;
    const pulse = status === "speaking" ? 1 + Math.sin(performance.now() * 0.005) * 0.12 : 1;
    if (shellMat.current)  { shellMat.current.uniforms.uTime.value += delta; shellMat.current.uniforms.uGlow.value = cur.current.glow * pulse; }
    if (debrisMat.current) { debrisMat.current.uniforms.uTime.value += delta; debrisMat.current.uniforms.uGlow.value = cur.current.glow * 0.7; }
    if (grp.current) { grp.current.rotation.y += delta * cur.current.spin; grp.current.rotation.x = 0.35; }
  });

  return (
    <group ref={grp}>
      {/* dark solid planet body — keeps the centre dark + occludes back-side particles */}
      <mesh>
        <sphereGeometry args={[R * 0.94, 48, 48]} />
        <meshStandardMaterial color="#02120b" roughness={1} metalness={0} emissive="#031f14" emissiveIntensity={0.25} />
      </mesh>

      {/* fractured neon-green crust */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[shell.positions, 3]} count={shell.count} />
          <bufferAttribute attach="attributes-aColor"   args={[shell.colors, 3]} count={shell.count} />
          <bufferAttribute attach="attributes-aScale"   args={[shell.scales, 1]} count={shell.count} />
          <bufferAttribute attach="attributes-aSeed"    args={[shell.seeds, 1]} count={shell.count} />
        </bufferGeometry>
        <shaderMaterial ref={shellMat} vertexShader={VERT} fragmentShader={FRAG} uniforms={shellU}
          transparent depthWrite={false} depthTest blending={THREE.AdditiveBlending} />
      </points>

      {/* drifting destroyed debris */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[debris.positions, 3]} count={DEBRIS_COUNT} />
          <bufferAttribute attach="attributes-aColor"   args={[debris.colors, 3]} count={DEBRIS_COUNT} />
          <bufferAttribute attach="attributes-aScale"   args={[debris.scales, 1]} count={DEBRIS_COUNT} />
          <bufferAttribute attach="attributes-aSeed"    args={[debris.seeds, 1]} count={DEBRIS_COUNT} />
        </bufferGeometry>
        <shaderMaterial ref={debrisMat} vertexShader={VERT} fragmentShader={FRAG} uniforms={debrisU}
          transparent depthWrite={false} depthTest blending={THREE.AdditiveBlending} />
      </points>
    </group>
  );
}

export default function PlasmaOrb({ status }: { status: Status }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 6.5], fov: 40 }}
      dpr={[1, 1.75]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <ambientLight intensity={0.3} />
      <pointLight position={[3, 2, 4]} intensity={1.2} color="#16f58a" />
      <Planet status={status} />
      {/* controlled bloom — only the brightest green sparks glow, no white blowout */}
      <EffectComposer>
        <Bloom intensity={0.55} luminanceThreshold={0.4} luminanceSmoothing={0.5} mipmapBlur radius={0.6} />
      </EffectComposer>
    </Canvas>
  );
}
