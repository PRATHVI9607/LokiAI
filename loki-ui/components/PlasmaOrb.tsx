"use client";

/**
 * PlasmaOrb — 3D particle-galaxy centerpiece (React Three Fiber).
 *
 * Thousands of glowing particles in a spherical cloud with a dense bright core
 * (accretion-orb look). Additive blending + bloom give the energy-gas glow.
 * Soft circular sprites via a custom points shader.
 *
 * Reacts to Loki's voice state:
 *   idle      → slow rotation, calm core
 *   listening → brighter core, gentle swell
 *   thinking  → fast swirl, energetic
 *   speaking  → rhythmic core pulse
 *   offline   → dim, slow, desaturated
 */

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";
import { type Status } from "@/hooks/useLoki";

interface OrbParams { spin: number; bright: number; swell: number; }
const STATE_PARAMS: Record<Status, OrbParams> = {
  idle:      { spin: 0.10, bright: 1.0, swell: 1.0 },
  listening: { spin: 0.18, bright: 1.35, swell: 1.05 },
  thinking:  { spin: 0.45, bright: 1.5, swell: 1.08 },
  speaking:  { spin: 0.28, bright: 1.7, swell: 1.12 },
  offline:   { spin: 0.03, bright: 0.4, swell: 0.92 },
};

const COUNT = 9000;
const RADIUS = 1.35;

// Color stops: white-hot core → gold → amber → cyan rim sparkle
const C_CORE = new THREE.Color("#FFF6E0");
const C_MID  = new THREE.Color("#FFB23E");
const C_EDGE = new THREE.Color("#FF5E2B");
const C_RIM  = new THREE.Color("#00E5FF");

const PVERT = `
uniform float uTime; uniform float uSpin; uniform float uSwell; uniform float uBright;
attribute float aScale; attribute float aSeed;
varying vec3 vColor; varying float vAlpha;
attribute vec3 aColor;
void main(){
  vColor = aColor;
  // swirl: rotate each particle around Y by angle scaled by inverse radius (galaxy shear)
  vec3 p = position * uSwell;
  float rad = length(p.xz) + 0.0001;
  float ang = uTime * uSpin * (0.6 + 1.2 / (rad + 0.4));
  float c = cos(ang), s = sin(ang);
  p.xz = mat2(c, -s, s, c) * p.xz;
  // gentle vertical bob per-particle
  p.y += sin(uTime * 0.6 + aSeed * 6.2831) * 0.02;
  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  float dist = length(p);
  vAlpha = uBright * (0.35 + 0.65 * smoothstep(RADIUS_PLACEHOLDER, 0.0, dist));
  gl_PointSize = aScale * (300.0 / -mv.z);
  gl_Position = projectionMatrix * mv;
}
`.replace("RADIUS_PLACEHOLDER", (RADIUS * 1.1).toFixed(3));

const PFRAG = `
precision highp float;
varying vec3 vColor; varying float vAlpha;
void main(){
  // soft circular sprite
  vec2 uv = gl_PointCoord - 0.5;
  float d = length(uv);
  if (d > 0.5) discard;
  float glow = smoothstep(0.5, 0.0, d);
  gl_FragColor = vec4(vColor, glow * vAlpha);
}
`;

function Galaxy({ status }: { status: Status }) {
  const matRef = useRef<THREE.ShaderMaterial>(null);
  const ptsRef = useRef<THREE.Points>(null);
  const cur = useRef<OrbParams>({ ...STATE_PARAMS.idle });

  const { positions, colors, scales, seeds } = useMemo(() => {
    const pos = new Float32Array(COUNT * 3);
    const col = new Float32Array(COUNT * 3);
    const scl = new Float32Array(COUNT);
    const sd  = new Float32Array(COUNT);
    const tmp = new THREE.Color();
    for (let i = 0; i < COUNT; i++) {
      // density biased toward the core: r = R * u^1.8
      const u = Math.random();
      const r = RADIUS * Math.pow(u, 1.8);
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      // slight disc flattening for galaxy feel
      pos[i*3]   = r * Math.sin(phi) * Math.cos(theta);
      pos[i*3+1] = r * Math.cos(phi) * 0.55;
      pos[i*3+2] = r * Math.sin(phi) * Math.sin(theta);

      // color by radius: core white → gold → amber → cyan rim
      const t = u; // 0 center, 1 edge
      if (t < 0.35)      tmp.copy(C_CORE).lerp(C_MID, t / 0.35);
      else if (t < 0.7)  tmp.copy(C_MID).lerp(C_EDGE, (t - 0.35) / 0.35);
      else               tmp.copy(C_EDGE).lerp(C_RIM, (t - 0.7) / 0.3);
      col[i*3] = tmp.r; col[i*3+1] = tmp.g; col[i*3+2] = tmp.b;

      scl[i] = (1.0 - t) * 2.2 + 0.5;  // bigger near core
      sd[i]  = Math.random();
    }
    return { positions: pos, colors: col, scales: scl, seeds: sd };
  }, []);

  const uniforms = useMemo(() => ({
    uTime:   { value: 0 },
    uSpin:   { value: 0.1 },
    uSwell:  { value: 1.0 },
    uBright: { value: 1.0 },
  }), []);

  useFrame((_, delta) => {
    const target = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const k = Math.min(delta * 2.2, 1);
    cur.current.spin   += (target.spin - cur.current.spin) * k;
    cur.current.bright += (target.bright - cur.current.bright) * k;
    cur.current.swell  += (target.swell - cur.current.swell) * k;
    if (matRef.current) {
      const u = matRef.current.uniforms;
      u.uTime.value += delta;
      u.uSpin.value = cur.current.spin;
      u.uBright.value = cur.current.bright;
      // speaking adds a subtle pulse on top of swell
      const pulse = status === "speaking" ? 1 + Math.sin(u.uTime.value * 6) * 0.03 : 1;
      u.uSwell.value = cur.current.swell * pulse;
    }
    if (ptsRef.current) ptsRef.current.rotation.y += delta * 0.04;
  });

  return (
    <points ref={ptsRef}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} count={COUNT} />
        <bufferAttribute attach="attributes-aColor"   args={[colors, 3]} count={COUNT} />
        <bufferAttribute attach="attributes-aScale"   args={[scales, 1]} count={COUNT} />
        <bufferAttribute attach="attributes-aSeed"    args={[seeds, 1]} count={COUNT} />
      </bufferGeometry>
      <shaderMaterial
        ref={matRef}
        vertexShader={PVERT}
        fragmentShader={PFRAG}
        uniforms={uniforms}
        transparent
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

// Bright glowing core point at the very center
function Core({ status }: { status: Status }) {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((_, delta) => {
    if (!ref.current) return;
    const target = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const base = 0.18 * target.bright;
    const pulse = status === "speaking" ? Math.sin(performance.now() * 0.006) * 0.03 : 0;
    const s = base + pulse;
    ref.current.scale.setScalar(Math.max(0.05, s));
  });
  return (
    <mesh ref={ref}>
      <sphereGeometry args={[1, 24, 24]} />
      <meshBasicMaterial color="#FFF6E0" toneMapped={false} />
    </mesh>
  );
}

export default function PlasmaOrb({ status }: { status: Status }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 42 }}
      dpr={[1, 1.75]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <Galaxy status={status} />
      <Core status={status} />
      <EffectComposer>
        <Bloom intensity={1.35} luminanceThreshold={0.1} luminanceSmoothing={0.5} mipmapBlur radius={0.85} />
      </EffectComposer>
    </Canvas>
  );
}
