"use client";

/**
 * PlasmaOrb — holographic network globe (React Three Fiber).
 *
 * Nodes distributed on a sphere (fibonacci), each wired to its nearest
 * neighbours with thin glowing lines → a crisp "data sphere" / JARVIS-globe.
 * Bright energy core + animated data pulses travelling the network.
 * TIGHT bloom (small radius, high threshold) so it reads sharp, not blurry.
 *
 * Reacts to Loki's voice state: rotation speed, node brightness, pulse rate.
 */

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";
import { type Status } from "@/hooks/useLoki";

interface OrbParams { spin: number; bright: number; }
const STATE_PARAMS: Record<Status, OrbParams> = {
  idle:      { spin: 0.05, bright: 1.0 },
  listening: { spin: 0.10, bright: 1.35 },
  thinking:  { spin: 0.28, bright: 1.6 },
  speaking:  { spin: 0.16, bright: 1.8 },
  offline:   { spin: 0.02, bright: 0.4 },
};

const NODES = 150;          // network vertices
const NEIGHBORS = 3;        // edges per node → ~clean mesh
const R = 1.5;              // globe radius
const PULSES = 40;          // travelling data sparks

// Loki-green holographic palette (JARVIS globe, recoloured to Loki green #50fa7b)
const COL_NODE = new THREE.Color("#7CFFB0");  // bright node
const COL_LINE = new THREE.Color("#2FE38A");  // green network lines
const COL_CORE = new THREE.Color("#C8FFD8");  // pale green-white core
const COL_PULSE = new THREE.Color("#E8FFEF");  // bright travelling spark

// even point distribution on a sphere
function fibonacciSphere(n: number, r: number): THREE.Vector3[] {
  const pts: THREE.Vector3[] = [];
  const phi = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) {
    const y = 1 - (i / (n - 1)) * 2;
    const rad = Math.sqrt(1 - y * y);
    const th = phi * i;
    pts.push(new THREE.Vector3(Math.cos(th) * rad * r, y * r, Math.sin(th) * rad * r));
  }
  return pts;
}

function NetworkGlobe({ status }: { status: Status }) {
  const grp = useRef<THREE.Group>(null);
  const nodeMat = useRef<THREE.PointsMaterial>(null);
  const lineMat = useRef<THREE.LineBasicMaterial>(null);
  const coreMat = useRef<THREE.MeshBasicMaterial>(null);
  const pulseRef = useRef<THREE.Points>(null);
  const cur = useRef<OrbParams>({ ...STATE_PARAMS.idle });

  // Build nodes + nearest-neighbour edges + pulse paths once
  const { nodePos, linePos, edges } = useMemo(() => {
    const verts = fibonacciSphere(NODES, R);
    const nodeArr = new Float32Array(NODES * 3);
    verts.forEach((v, i) => { nodeArr[i*3] = v.x; nodeArr[i*3+1] = v.y; nodeArr[i*3+2] = v.z; });

    const edgeList: [number, number][] = [];
    const seen = new Set<string>();
    for (let i = 0; i < NODES; i++) {
      const dists = verts.map((v, j) => ({ j, d: verts[i].distanceToSquared(v) }))
        .filter(o => o.j !== i).sort((a, b) => a.d - b.d).slice(0, NEIGHBORS);
      for (const { j } of dists) {
        const key = i < j ? `${i}-${j}` : `${j}-${i}`;
        if (!seen.has(key)) { seen.add(key); edgeList.push([i, j]); }
      }
    }
    const lineArr = new Float32Array(edgeList.length * 6);
    edgeList.forEach(([a, b], k) => {
      lineArr.set([verts[a].x, verts[a].y, verts[a].z, verts[b].x, verts[b].y, verts[b].z], k * 6);
    });
    return { nodePos: nodeArr, linePos: lineArr, edges: edgeList, verts };
  }, []);

  // Travelling data pulses — each rides a random edge, t∈[0,1]
  const pulses = useMemo(() => Array.from({ length: PULSES }, () => ({
    edge: Math.floor(Math.random() * edges.length),
    t: Math.random(),
    speed: 0.3 + Math.random() * 0.7,
  })), [edges.length]);
  const pulsePos = useMemo(() => new Float32Array(PULSES * 3), []);

  useFrame((_, delta) => {
    const target = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const k = Math.min(delta * 2.0, 1);
    cur.current.spin += (target.spin - cur.current.spin) * k;
    cur.current.bright += (target.bright - cur.current.bright) * k;
    const pulse = status === "speaking" ? 1 + Math.sin(performance.now() * 0.005) * 0.18 : 1;
    const b = cur.current.bright * pulse;

    if (nodeMat.current) nodeMat.current.opacity = Math.min(1, 0.85 * b);
    if (lineMat.current) lineMat.current.opacity = Math.min(1, 0.28 * b);
    if (coreMat.current) coreMat.current.opacity = Math.min(1, 0.9 * b);
    if (grp.current) { grp.current.rotation.y += delta * cur.current.spin; grp.current.rotation.x = 0.28; }

    // advance pulses along their edges
    const geo = pulseRef.current?.geometry as THREE.BufferGeometry | undefined;
    if (geo) {
      for (let i = 0; i < PULSES; i++) {
        const p = pulses[i];
        p.t += delta * p.speed * (0.5 + cur.current.spin * 2);
        if (p.t > 1) { p.t = 0; p.edge = Math.floor(Math.random() * edges.length); }
        pulsePos[i*3]   = linePos[p.edge*6]   + (linePos[p.edge*6+3] - linePos[p.edge*6])   * p.t;
        pulsePos[i*3+1] = linePos[p.edge*6+1] + (linePos[p.edge*6+4] - linePos[p.edge*6+1]) * p.t;
        pulsePos[i*3+2] = linePos[p.edge*6+2] + (linePos[p.edge*6+5] - linePos[p.edge*6+2]) * p.t;
      }
      (geo.attributes.position as THREE.BufferAttribute).needsUpdate = true;
    }
  });

  return (
    <group ref={grp}>
      {/* bright energy core */}
      <mesh>
        <sphereGeometry args={[0.18, 32, 32]} />
        <meshBasicMaterial ref={coreMat} color={COL_CORE} transparent toneMapped={false} />
      </mesh>

      {/* network lines — thin, crisp, additive */}
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[linePos, 3]} count={linePos.length / 3} />
        </bufferGeometry>
        <lineBasicMaterial ref={lineMat} color={COL_LINE} transparent opacity={0.28}
          blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </lineSegments>

      {/* nodes — sharp bright points */}
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[nodePos, 3]} count={NODES} />
        </bufferGeometry>
        <pointsMaterial ref={nodeMat} color={COL_NODE} size={0.05} transparent opacity={0.85}
          sizeAttenuation blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </points>

      {/* travelling data pulses — bright sparks riding the lines */}
      <points ref={pulseRef}>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[pulsePos, 3]} count={PULSES} />
        </bufferGeometry>
        <pointsMaterial color={COL_PULSE} size={0.07} transparent opacity={0.95}
          sizeAttenuation blending={THREE.AdditiveBlending} depthWrite={false} toneMapped={false} />
      </points>
    </group>
  );
}

export default function PlasmaOrb({ status }: { status: Status }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 5.5], fov: 42 }}
      dpr={[1, 2]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <NetworkGlobe status={status} />
      {/* TIGHT bloom: only the hot nodes/core/pulses bloom → crisp, not blurry */}
      <EffectComposer>
        <Bloom intensity={0.9} luminanceThreshold={0.5} luminanceSmoothing={0.3} mipmapBlur radius={0.35} />
      </EffectComposer>
    </Canvas>
  );
}
