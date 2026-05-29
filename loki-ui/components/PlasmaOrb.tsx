"use client";

/**
 * PlasmaOrb — the 3D hero centerpiece (React Three Fiber).
 *
 * A swirling plasma sphere with a custom GLSL shader: animated simplex-noise
 * vertex displacement + neon cyan→magenta fragment gradient + fresnel rim glow.
 * Orbiting energy rings + a drifting particle field, all under bloom.
 *
 * Reacts to Loki's voice state via shader uniforms:
 *   idle      → slow calm breathing
 *   listening → gentle bright pulse
 *   thinking  → fast chaotic distortion
 *   speaking  → rhythmic ripples
 *   offline   → dim, desaturated, slow
 */

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";
import { type Status } from "@/hooks/useLoki";

// ── State → animation parameters ──────────────────────────────────────────────
interface OrbParams { speed: number; distort: number; intensity: number; hueShift: number; }
const STATE_PARAMS: Record<Status, OrbParams> = {
  idle:      { speed: 0.35, distort: 0.35, intensity: 0.85, hueShift: 0.0 },
  listening: { speed: 0.75, distort: 0.55, intensity: 1.25, hueShift: 0.08 },
  thinking:  { speed: 1.8,  distort: 1.05, intensity: 1.4,  hueShift: 0.18 },
  speaking:  { speed: 1.2,  distort: 0.8,  intensity: 1.55, hueShift: -0.06 },
  offline:   { speed: 0.12, distort: 0.18, intensity: 0.4,  hueShift: 0.4 },
};

// ── GLSL: 3D simplex noise (Ashima) ───────────────────────────────────────────
const NOISE_GLSL = `
vec4 permute(vec4 x){return mod(((x*34.0)+1.0)*x,289.0);}
vec4 taylorInvSqrt(vec4 r){return 1.79284291400159-0.85373472095314*r;}
float snoise(vec3 v){
  const vec2 C=vec2(1.0/6.0,1.0/3.0); const vec4 D=vec4(0.0,0.5,1.0,2.0);
  vec3 i=floor(v+dot(v,C.yyy)); vec3 x0=v-i+dot(i,C.xxx);
  vec3 g=step(x0.yzx,x0.xyz); vec3 l=1.0-g; vec3 i1=min(g.xyz,l.zxy); vec3 i2=max(g.xyz,l.zxy);
  vec3 x1=x0-i1+1.0*C.xxx; vec3 x2=x0-i2+2.0*C.xxx; vec3 x3=x0-1.0+3.0*C.xxx;
  i=mod(i,289.0);
  vec4 p=permute(permute(permute(i.z+vec4(0.0,i1.z,i2.z,1.0))+i.y+vec4(0.0,i1.y,i2.y,1.0))+i.x+vec4(0.0,i1.x,i2.x,1.0));
  float n_=1.0/7.0; vec3 ns=n_*D.wyz-D.xzx;
  vec4 j=p-49.0*floor(p*ns.z*ns.z);
  vec4 x_=floor(j*ns.z); vec4 y_=floor(j-7.0*x_);
  vec4 x=x_*ns.x+ns.yyyy; vec4 y=y_*ns.x+ns.yyyy; vec4 h=1.0-abs(x)-abs(y);
  vec4 b0=vec4(x.xy,y.xy); vec4 b1=vec4(x.zw,y.zw);
  vec4 s0=floor(b0)*2.0+1.0; vec4 s1=floor(b1)*2.0+1.0; vec4 sh=-step(h,vec4(0.0));
  vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy; vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
  vec3 p0=vec3(a0.xy,h.x); vec3 p1=vec3(a0.zw,h.y); vec3 p2=vec3(a1.xy,h.z); vec3 p3=vec3(a1.zw,h.w);
  vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
  p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;
  vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0); m=m*m;
  return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
}
`;

const VERT = `
uniform float uTime; uniform float uSpeed; uniform float uDistort;
varying float vNoise; varying vec3 vNormal; varying vec3 vPos;
${NOISE_GLSL}
void main(){
  vNormal = normal;
  float t = uTime * uSpeed;
  float n = snoise(position * 1.4 + vec3(t * 0.6));
  float n2 = snoise(position * 3.0 - vec3(t * 0.4));
  float displced = (n * 0.6 + n2 * 0.4) * uDistort;
  vNoise = displced;
  vec3 newPos = position + normal * displced;
  vPos = newPos;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(newPos, 1.0);
}
`;

const FRAG = `
precision highp float;
uniform float uTime; uniform float uIntensity; uniform float uHueShift;
uniform vec3 uColorA; uniform vec3 uColorB; uniform vec3 uColorC;
varying float vNoise; varying vec3 vNormal; varying vec3 vPos;
vec3 hueRotate(vec3 c, float a){
  const mat3 toY=mat3(0.299,0.587,0.114,-0.169,-0.331,0.5,0.5,-0.419,-0.081);
  const mat3 toR=mat3(1.0,0.0,1.402,1.0,-0.344,-0.714,1.0,1.772,0.0);
  vec3 y=toY*c; float s=sin(a),co=cos(a);
  y.yz=mat2(co,-s,s,co)*y.yz; return toR*y;
}
void main(){
  float mixv = clamp(vNoise * 1.6 + 0.5, 0.0, 1.0);
  vec3 col = mix(uColorA, uColorB, mixv);
  col = mix(col, uColorC, smoothstep(0.55, 1.0, mixv));
  // fresnel rim
  vec3 viewDir = normalize(cameraPosition - vPos);
  float fres = pow(1.0 - max(dot(normalize(vNormal), viewDir), 0.0), 2.2);
  col += uColorC * fres * 1.4;
  col = hueRotate(col, uHueShift);
  col *= uIntensity;
  gl_FragColor = vec4(col, 1.0);
}
`;

function lerp(a: number, b: number, t: number) { return a + (b - a) * t; }

function Orb({ status }: { status: Status }) {
  const matRef = useRef<THREE.ShaderMaterial>(null);
  const meshRef = useRef<THREE.Mesh>(null);
  const cur = useRef<OrbParams>({ ...STATE_PARAMS.idle });

  const uniforms = useMemo(() => ({
    uTime:      { value: 0 },
    uSpeed:     { value: 0.35 },
    uDistort:   { value: 0.35 },
    uIntensity: { value: 0.85 },
    uHueShift:  { value: 0.0 },
    uColorA:    { value: new THREE.Color("#00E5FF") }, // electric cyan
    uColorB:    { value: new THREE.Color("#6C4DFF") }, // indigo
    uColorC:    { value: new THREE.Color("#FF2E97") }, // hot magenta
  }), []);

  useFrame((_, delta) => {
    const target = STATE_PARAMS[status] ?? STATE_PARAMS.idle;
    const k = Math.min(delta * 2.5, 1);
    cur.current.speed     = lerp(cur.current.speed, target.speed, k);
    cur.current.distort   = lerp(cur.current.distort, target.distort, k);
    cur.current.intensity = lerp(cur.current.intensity, target.intensity, k);
    cur.current.hueShift  = lerp(cur.current.hueShift, target.hueShift, k);

    if (matRef.current) {
      const u = matRef.current.uniforms;
      u.uTime.value += delta;
      u.uSpeed.value = cur.current.speed;
      u.uDistort.value = cur.current.distort;
      u.uIntensity.value = cur.current.intensity;
      u.uHueShift.value = cur.current.hueShift;
    }
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.15 * cur.current.speed;
      meshRef.current.rotation.x += delta * 0.05;
    }
  });

  return (
    <mesh ref={meshRef}>
      {/* detail 24 ≈ 8k faces — smooth for noise displacement, light on the GPU */}
      <icosahedronGeometry args={[1.25, 24]} />
      <shaderMaterial
        ref={matRef}
        vertexShader={VERT}
        fragmentShader={FRAG}
        uniforms={uniforms}
      />
    </mesh>
  );
}

function EnergyRings({ status }: { status: Status }) {
  const g = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (!g.current) return;
    const sp = (STATE_PARAMS[status] ?? STATE_PARAMS.idle).speed;
    g.current.rotation.z += delta * 0.3 * sp;
    g.current.rotation.x += delta * 0.12 * sp;
  });
  return (
    <group ref={g}>
      <mesh rotation={[Math.PI / 2.4, 0, 0]}>
        <torusGeometry args={[2.0, 0.012, 16, 160]} />
        <meshBasicMaterial color="#00E5FF" toneMapped={false} />
      </mesh>
      <mesh rotation={[Math.PI / 1.7, Math.PI / 4, 0]}>
        <torusGeometry args={[2.35, 0.008, 16, 160]} />
        <meshBasicMaterial color="#FF2E97" toneMapped={false} />
      </mesh>
    </group>
  );
}

function ParticleField() {
  const ref = useRef<THREE.Points>(null);
  const { positions, count } = useMemo(() => {
    const N = 700;
    const arr = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const r = 3 + Math.random() * 7;
      const t = Math.random() * Math.PI * 2;
      const p = Math.acos(2 * Math.random() - 1);
      arr[i * 3]     = r * Math.sin(p) * Math.cos(t);
      arr[i * 3 + 1] = r * Math.sin(p) * Math.sin(t);
      arr[i * 3 + 2] = r * Math.cos(p);
    }
    return { positions: arr, count: N };
  }, []);

  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.02;
  });

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} count={count} />
      </bufferGeometry>
      <pointsMaterial size={0.03} color="#7DF9FF" transparent opacity={0.6} toneMapped={false} sizeAttenuation />
    </points>
  );
}

export default function PlasmaOrb({ status }: { status: Status }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 45 }}
      dpr={[1, 1.75]}
      gl={{ antialias: true, alpha: true }}
      style={{ width: "100%", height: "100%" }}
    >
      <Orb status={status} />
      <EnergyRings status={status} />
      <ParticleField />
      <EffectComposer>
        <Bloom intensity={1.1} luminanceThreshold={0.15} luminanceSmoothing={0.4} mipmapBlur radius={0.7} />
      </EffectComposer>
    </Canvas>
  );
}
