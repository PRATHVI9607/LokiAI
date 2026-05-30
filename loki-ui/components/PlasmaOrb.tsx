"use client";

/**
 * PlasmaOrb — green plasma "black hole" with a sparkling node network.
 *
 * Layers (back → front):
 *   1. EventHorizon  — dark core sphere with a green fresnel rim (lensing glow)
 *   2. AccretionDisk — tilted swirling ring of plasma particles spiralling in
 *   3. NodeNetwork   — fibonacci nodes (TWINKLING sparkle shader) + glow lines
 *   4. DataPulses    — bright sparks travelling the network edges
 *   + tight bloom so it reads crisp, not blurry.
 *
 * Tilted + parallax-rotated for real 3D depth. Reacts to Loki's voice state.
 */

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";
import { type Status } from "@/hooks/useLoki";

interface OrbParams { spin: number; bright: number; }
const STATE_PARAMS: Record<Status, OrbParams> = {
  idle:      { spin: 0.06, bright: 1.0 },
  listening: { spin: 0.12, bright: 1.35 },
  thinking:  { spin: 0.34, bright: 1.6 },
  speaking:  { spin: 0.20, bright: 1.8 },
  offline:   { spin: 0.02, bright: 0.35 },
};

const NODES = 130;
const NEIGHBORS = 3;
const R = 1.45;
const DISK = 3200;
const PULSES = 48;

const C_NODE = new THREE.Color("#9DFFC0");
const C_LINE = new THREE.Color("#2FE38A");
const C_DISK_IN = new THREE.Color("#C8FFD8");
const C_DISK_OUT = new THREE.Color("#0E8F52");
const C_PULSE = new THREE.Color("#EAFFF2");
const C_RIM = new THREE.Color("#3BFF9E");

function fib(n: number, r: number): THREE.Vector3[] {
  const p: THREE.Vector3[] = []; const g = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) {
    const y = 1 - (i / (n - 1)) * 2; const rad = Math.sqrt(1 - y * y); const t = g * i;
    p.push(new THREE.Vector3(Math.cos(t) * rad * r, y * r, Math.sin(t) * rad * r));
  }
  return p;
}

// ── Event horizon: dark core + green fresnel rim ──────────────────────────────
const CORE_VERT = `
varying vec3 vN; varying vec3 vP;
void main(){ vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position,1.0); vP = -mv.xyz; gl_Position = projectionMatrix * mv; }
`;
const CORE_FRAG = `
precision highp float; uniform vec3 uRim; uniform float uBright;
varying vec3 vN; varying vec3 vP;
void main(){
  vec3 v = normalize(vP);
  float fres = pow(1.0 - max(dot(vN, v), 0.0), 3.0);
  vec3 col = mix(vec3(0.005,0.02,0.012), uRim * uBright, fres);
  gl_FragColor = vec4(col, 1.0);
}
`;

function EventHorizon({ status }: { status: Status }) {
  const mat = useRef<THREE.ShaderMaterial>(null);
  const u = useMemo(() => ({ uRim: { value: C_RIM.clone() }, uBright: { value: 1 } }), []);
  useFrame(() => {
    const t = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    if (mat.current) mat.current.uniforms.uBright.value += (t.bright - mat.current.uniforms.uBright.value) * 0.05;
  });
  return (
    <mesh>
      <sphereGeometry args={[R * 0.62, 48, 48]} />
      <shaderMaterial ref={mat} vertexShader={CORE_VERT} fragmentShader={CORE_FRAG} uniforms={u} />
    </mesh>
  );
}

// ── Sparkling node shader ─────────────────────────────────────────────────────
const NODE_VERT = `
uniform float uTime; attribute float aSeed; attribute float aScale;
varying float vTw;
void main(){
  float tw = 0.5 + 0.5 * sin(uTime * 3.0 + aSeed * 6.2831);
  vTw = tw;
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  gl_PointSize = aScale * (1.0 + tw * 0.9) * (300.0 / -mv.z);
  gl_Position = projectionMatrix * mv;
}
`;
const NODE_FRAG = `
precision highp float; uniform vec3 uColor; uniform float uBright; varying float vTw;
void main(){
  vec2 uv = gl_PointCoord - 0.5; float d = length(uv);
  if (d > 0.5) discard;
  float core = smoothstep(0.5, 0.0, d);
  float spark = pow(core, 2.2) + core * 0.25;        // sharp centre + soft halo
  gl_FragColor = vec4(uColor, spark * (0.35 + vTw * 0.65) * uBright);
}
`;

// ── Accretion disk shader (spiral inflow) ─────────────────────────────────────
const DISK_VERT = `
uniform float uTime; uniform float uSpin;
attribute float aR; attribute float aA; attribute float aScale; attribute vec3 aColor;
varying vec3 vCol; varying float vA;
void main(){
  float ang = aA + uTime * uSpin * (1.6 / (aR + 0.3));   // inner spins faster
  float x = cos(ang) * aR;
  float z = sin(ang) * aR;
  float y = sin(ang * 2.0 + aR * 4.0) * 0.04;             // slight warp
  vec3 p = vec3(x, y, z);
  vCol = aColor; vA = smoothstep(3.0, 1.2, aR);
  vec4 mv = modelViewMatrix * vec4(p, 1.0);
  gl_PointSize = aScale * (220.0 / -mv.z);
  gl_Position = projectionMatrix * mv;
}
`;
const DISK_FRAG = `
precision highp float; uniform float uBright; varying vec3 vCol; varying float vA;
void main(){
  vec2 uv = gl_PointCoord - 0.5; float d = length(uv);
  if (d > 0.5) discard;
  float g = smoothstep(0.5, 0.0, d);
  gl_FragColor = vec4(vCol, g * vA * uBright);
}
`;

function BlackHole({ status }: { status: Status }) {
  const grp = useRef<THREE.Group>(null);
  const nodeMat = useRef<THREE.ShaderMaterial>(null);
  const diskMat = useRef<THREE.ShaderMaterial>(null);
  const lineMat = useRef<THREE.LineBasicMaterial>(null);
  const pulseRef = useRef<THREE.Points>(null);
  const cur = useRef<OrbParams>({ ...STATE_PARAMS.idle });

  // nodes + edges
  const { nodePos, nodeScale, nodeSeed, linePos, edges } = useMemo(() => {
    const verts = fib(NODES, R);
    const np = new Float32Array(NODES * 3), ns = new Float32Array(NODES), nd = new Float32Array(NODES);
    verts.forEach((v, i) => { np.set([v.x, v.y, v.z], i*3); ns[i] = 1.6 + Math.random() * 2.4; nd[i] = Math.random(); });
    const el: [number, number][] = []; const seen = new Set<string>();
    for (let i = 0; i < NODES; i++) {
      const near = verts.map((v, j) => ({ j, d: verts[i].distanceToSquared(v) })).filter(o => o.j !== i)
        .sort((a, b) => a.d - b.d).slice(0, NEIGHBORS);
      for (const { j } of near) { const k = i < j ? `${i}-${j}` : `${j}-${i}`; if (!seen.has(k)) { seen.add(k); el.push([i, j]); } }
    }
    const lp = new Float32Array(el.length * 6);
    el.forEach(([a, b], k) => lp.set([verts[a].x, verts[a].y, verts[a].z, verts[b].x, verts[b].y, verts[b].z], k * 6));
    return { nodePos: np, nodeScale: ns, nodeSeed: nd, linePos: lp, edges: el };
  }, []);

  // accretion disk
  const disk = useMemo(() => {
    const r = new Float32Array(DISK), a = new Float32Array(DISK), s = new Float32Array(DISK), c = new Float32Array(DISK * 3);
    const tmp = new THREE.Color();
    for (let i = 0; i < DISK; i++) {
      const rr = 1.15 + Math.pow(Math.random(), 1.5) * 1.9;   // dense inner
      r[i] = rr; a[i] = Math.random() * Math.PI * 2; s[i] = 0.5 + Math.random() * 1.3;
      tmp.copy(C_DISK_IN).lerp(C_DISK_OUT, (rr - 1.15) / 1.9);
      c.set([tmp.r, tmp.g, tmp.b], i*3);
    }
    return { aR: r, aA: a, aScale: s, aColor: c };
  }, []);

  const pulses = useMemo(() => Array.from({ length: PULSES }, () => ({ e: Math.floor(Math.random() * edges.length), t: Math.random(), sp: 0.3 + Math.random() * 0.7 })), [edges.length]);
  const pulsePos = useMemo(() => new Float32Array(PULSES * 3), []);

  const nodeU = useMemo(() => ({ uTime: { value: 0 }, uColor: { value: C_NODE.clone() }, uBright: { value: 1 } }), []);
  const diskU = useMemo(() => ({ uTime: { value: 0 }, uSpin: { value: 0.3 }, uBright: { value: 1 } }), []);

  useFrame((_, delta) => {
    const t = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const k = Math.min(delta * 2, 1);
    cur.current.spin += (t.spin - cur.current.spin) * k;
    cur.current.bright += (t.bright - cur.current.bright) * k;
    const pulseB = status === "speaking" ? 1 + Math.sin(performance.now() * 0.005) * 0.15 : 1;
    const b = cur.current.bright * pulseB;

    if (nodeMat.current) { nodeMat.current.uniforms.uTime.value += delta; nodeMat.current.uniforms.uBright.value = b; }
    if (diskMat.current) { diskMat.current.uniforms.uTime.value += delta; diskMat.current.uniforms.uSpin.value = 0.3 + cur.current.spin * 2; diskMat.current.uniforms.uBright.value = b * 0.85; }
    if (lineMat.current) lineMat.current.opacity = Math.min(1, 0.22 * b);
    if (grp.current) { grp.current.rotation.y += delta * cur.current.spin; grp.current.rotation.x = 0.42; grp.current.rotation.z = 0.12; }

    const geo = pulseRef.current?.geometry as THREE.BufferGeometry | undefined;
    if (geo) {
      for (let i = 0; i < PULSES; i++) {
        const p = pulses[i]; p.t += delta * p.sp * (0.5 + cur.current.spin * 2);
        if (p.t > 1) { p.t = 0; p.e = Math.floor(Math.random() * edges.length); }
        const o = p.e * 6;
        pulsePos[i*3]   = linePos[o]   + (linePos[o+3] - linePos[o])   * p.t;
        pulsePos[i*3+1] = linePos[o+1] + (linePos[o+4] - linePos[o+1]) * p.t;
        pulsePos[i*3+2] = linePos[o+2] + (linePos[o+5] - linePos[o+2]) * p.t;
      }
      (geo.attributes.position as THREE.BufferAttribute).needsUpdate = true;
    }
  });

  return (
    <group ref={grp}>
      {/* accretion disk (tilted plane via the group's x/z rotation) */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[new Float32Array(DISK * 3), 3]} count={DISK} />
          <bufferAttribute attach="attributes-aR"     args={[disk.aR, 1]} count={DISK} />
          <bufferAttribute attach="attributes-aA"     args={[disk.aA, 1]} count={DISK} />
          <bufferAttribute attach="attributes-aScale" args={[disk.aScale, 1]} count={DISK} />
          <bufferAttribute attach="attributes-aColor" args={[disk.aColor, 3]} count={DISK} />
        </bufferGeometry>
        <shaderMaterial ref={diskMat} vertexShader={DISK_VERT} fragmentShader={DISK_FRAG} uniforms={diskU}
          transparent depthWrite={false} blending={THREE.AdditiveBlending} />
      </points>

      {/* network lines */}
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[linePos, 3]} count={linePos.length / 3} />
        </bufferGeometry>
        <lineBasicMaterial ref={lineMat} color={C_LINE} transparent opacity={0.22}
          blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </lineSegments>

      {/* sparkling nodes */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[nodePos, 3]} count={NODES} />
          <bufferAttribute attach="attributes-aScale"   args={[nodeScale, 1]} count={NODES} />
          <bufferAttribute attach="attributes-aSeed"    args={[nodeSeed, 1]} count={NODES} />
        </bufferGeometry>
        <shaderMaterial ref={nodeMat} vertexShader={NODE_VERT} fragmentShader={NODE_FRAG} uniforms={nodeU}
          transparent depthWrite={false} blending={THREE.AdditiveBlending} />
      </points>

      {/* data pulses */}
      <points ref={pulseRef}>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[pulsePos, 3]} count={PULSES} />
        </bufferGeometry>
        <pointsMaterial color={C_PULSE} size={0.075} transparent opacity={0.95}
          sizeAttenuation blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </points>

      <EventHorizon status={status} />
    </group>
  );
}

export default function PlasmaOrb({ status }: { status: Status }) {
  return (
    <Canvas
      camera={{ position: [0, 0.4, 6], fov: 42 }}
      dpr={[1, 2]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <BlackHole status={status} />
      <EffectComposer>
        <Bloom intensity={0.95} luminanceThreshold={0.45} luminanceSmoothing={0.35} mipmapBlur radius={0.4} />
      </EffectComposer>
    </Canvas>
  );
}
