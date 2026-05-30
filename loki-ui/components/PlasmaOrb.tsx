"use client";

/**
 * PlasmaOrb — a BROKEN green network globe on a dark void.
 *
 * Not a perfect sphere: nodes are noise-displaced (irregular crust) and whole
 * sections are missing (shattered gaps), with fragments drifting off. Thin
 * crisp green lines + sharp twinkling nodes. Dark core, LOW bloom — reads as a
 * delicate luminous wireframe in the dark, never a bright blob.
 *
 * Reacts to Loki's voice state (rotation + node brightness).
 */

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";
import { type Status } from "@/hooks/useLoki";

interface OrbParams { spin: number; bright: number; }
const STATE_PARAMS: Record<Status, OrbParams> = {
  idle:      { spin: 0.05, bright: 1.0 },
  listening: { spin: 0.11, bright: 1.3 },
  thinking:  { spin: 0.30, bright: 1.5 },
  speaking:  { spin: 0.18, bright: 1.65 },
  offline:   { spin: 0.02, bright: 0.35 },
};

const RAW_NODES = 220;     // before shatter-culling
const NEIGHBORS = 3;
const R = 1.55;
const FRAGS = 260;         // drifting broken debris

const C_NODE = new THREE.Color("#86FFB8");
const C_LINE = new THREE.Color("#1FB870");
const C_FRAG = new THREE.Color("#2FE38A");

// deterministic banded noise → continents/craters (which chunks survive)
function shatter(x: number, y: number, z: number): number {
  return Math.sin(x * 2.7 + y * 1.6) * 0.5
       + Math.sin(y * 2.1 - z * 3.0) * 0.5
       + Math.sin(z * 3.3 + x * 1.2) * 0.5;
}

const NODE_VERT = `
uniform float uTime; attribute float aSeed; attribute float aScale;
varying float vTw;
void main(){
  float tw = 0.5 + 0.5 * sin(uTime * 2.6 + aSeed * 6.2831);
  vTw = tw;
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  gl_PointSize = aScale * (0.8 + tw * 0.9) * (280.0 / -mv.z);
  gl_Position = projectionMatrix * mv;
}
`;
const NODE_FRAG = `
precision highp float; uniform vec3 uColor; uniform float uBright; varying float vTw;
void main(){
  vec2 uv = gl_PointCoord - 0.5; float d = length(uv);
  if (d > 0.5) discard;
  float core = smoothstep(0.5, 0.0, d);
  float spark = pow(core, 2.4) + core * 0.18;
  gl_FragColor = vec4(uColor, spark * (0.3 + vTw * 0.7) * uBright);
}
`;

function BrokenGlobe({ status }: { status: Status }) {
  const grp = useRef<THREE.Group>(null);
  const nodeMat = useRef<THREE.ShaderMaterial>(null);
  const lineMat = useRef<THREE.LineBasicMaterial>(null);
  const fragMat = useRef<THREE.PointsMaterial>(null);
  const cur = useRef<OrbParams>({ ...STATE_PARAMS.idle });

  const { nodePos, nodeScale, nodeSeed, linePos } = useMemo(() => {
    // fibonacci sphere → cull shattered regions → noise-displace survivors
    const g = Math.PI * (3 - Math.sqrt(5));
    const verts: THREE.Vector3[] = [];
    for (let i = 0; i < RAW_NODES; i++) {
      const y = 1 - (i / (RAW_NODES - 1)) * 2;
      const rad = Math.sqrt(1 - y * y);
      const t = g * i;
      const nx = Math.cos(t) * rad, ny = y, nz = Math.sin(t) * rad;
      if (shatter(nx * 2, ny * 2, nz * 2) < -0.25) continue;   // shattered gap
      // irregular crust: radius wobbles with noise
      const wob = 1 + (shatter(nx * 4, ny * 4, nz * 4)) * 0.06;
      verts.push(new THREE.Vector3(nx, ny, nz).multiplyScalar(R * wob));
    }
    const N = verts.length;
    const np = new Float32Array(N * 3), nsc = new Float32Array(N), nsd = new Float32Array(N);
    verts.forEach((v, i) => { np.set([v.x, v.y, v.z], i*3); nsc[i] = 1.3 + Math.random() * 2.2; nsd[i] = Math.random(); });

    const el: [number, number][] = []; const seen = new Set<string>();
    for (let i = 0; i < N; i++) {
      const near = verts.map((v, j) => ({ j, d: verts[i].distanceToSquared(v) })).filter(o => o.j !== i)
        .sort((a, b) => a.d - b.d).slice(0, NEIGHBORS);
      for (const { j } of near) {
        // skip long bridges across gaps → keeps the broken look
        if (verts[i].distanceTo(verts[j]) > R * 0.55) continue;
        const k = i < j ? `${i}-${j}` : `${j}-${i}`;
        if (!seen.has(k)) { seen.add(k); el.push([i, j]); }
      }
    }
    const lp = new Float32Array(el.length * 6);
    el.forEach(([a, b], k) => lp.set([verts[a].x, verts[a].y, verts[a].z, verts[b].x, verts[b].y, verts[b].z], k * 6));
    return { nodePos: np, nodeScale: nsc, nodeSeed: nsd, linePos: lp };
  }, []);

  // drifting fragments (the broken-off pieces)
  const fragPos = useMemo(() => {
    const a = new Float32Array(FRAGS * 3);
    for (let i = 0; i < FRAGS; i++) {
      const rr = R * (1.05 + Math.random() * 1.3);
      const th = Math.random() * Math.PI * 2, ph = Math.acos(2 * Math.random() - 1);
      a.set([rr*Math.sin(ph)*Math.cos(th), rr*Math.cos(ph)*0.8, rr*Math.sin(ph)*Math.sin(th)], i*3);
    }
    return a;
  }, []);

  const nodeU = useMemo(() => ({ uTime: { value: 0 }, uColor: { value: C_NODE.clone() }, uBright: { value: 1 } }), []);

  useFrame((_, delta) => {
    const t = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const k = Math.min(delta * 2, 1);
    cur.current.spin += (t.spin - cur.current.spin) * k;
    cur.current.bright += (t.bright - cur.current.bright) * k;
    const pb = status === "speaking" ? 1 + Math.sin(performance.now() * 0.005) * 0.12 : 1;
    const b = cur.current.bright * pb;
    if (nodeMat.current) { nodeMat.current.uniforms.uTime.value += delta; nodeMat.current.uniforms.uBright.value = b; }
    if (lineMat.current) lineMat.current.opacity = Math.min(0.6, 0.16 * b);
    if (fragMat.current) fragMat.current.opacity = Math.min(0.7, 0.45 * b);
    if (grp.current) { grp.current.rotation.y += delta * cur.current.spin; grp.current.rotation.x = 0.38; grp.current.rotation.z = 0.1; }
  });

  return (
    <group ref={grp}>
      {/* dark inner sphere — keeps the centre dark + occludes back faces */}
      <mesh>
        <sphereGeometry args={[R * 0.82, 40, 40]} />
        <meshBasicMaterial color="#05130d" />
      </mesh>

      {/* thin crisp network lines */}
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[linePos, 3]} count={linePos.length / 3} />
        </bufferGeometry>
        <lineBasicMaterial ref={lineMat} color={C_LINE} transparent opacity={0.16}
          blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </lineSegments>

      {/* twinkling nodes */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[nodePos, 3]} count={nodePos.length / 3} />
          <bufferAttribute attach="attributes-aScale"   args={[nodeScale, 1]} count={nodeScale.length} />
          <bufferAttribute attach="attributes-aSeed"    args={[nodeSeed, 1]} count={nodeSeed.length} />
        </bufferGeometry>
        <shaderMaterial ref={nodeMat} vertexShader={NODE_VERT} fragmentShader={NODE_FRAG} uniforms={nodeU}
          transparent depthWrite={false} blending={THREE.AdditiveBlending} />
      </points>

      {/* drifting broken fragments */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[fragPos, 3]} count={FRAGS} />
        </bufferGeometry>
        <pointsMaterial ref={fragMat} color={C_FRAG} size={0.028} transparent opacity={0.45}
          sizeAttenuation blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </points>
    </group>
  );
}

export default function PlasmaOrb({ status }: { status: Status }) {
  return (
    <Canvas
      camera={{ position: [0, 0.3, 6], fov: 42 }}
      dpr={[1, 2]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <BrokenGlobe status={status} />
      {/* LOW bloom: thin crisp glow on dark, never a white blob */}
      <EffectComposer>
        <Bloom intensity={0.45} luminanceThreshold={0.55} luminanceSmoothing={0.3} mipmapBlur radius={0.3} />
      </EffectComposer>
    </Canvas>
  );
}
