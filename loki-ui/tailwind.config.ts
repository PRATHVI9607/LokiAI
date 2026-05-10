import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        loki: {
          bg:      "#050B18",
          surface: "#0C1830",
          card:    "#101E38",
          border:  "#1E3A5F",
          gold:    "#F5C518",
          "gold-bright": "#FFE033",
          "gold-dim":    "rgba(245,197,24,0.12)",
          purple:  "#8B5CF6",
          "purple-dim": "rgba(139,92,246,0.15)",
          green:   "#10D97E",
          blue:    "#38BDF8",
          red:     "#F87171",
          text:    "#F1F5F9",
          muted:   "#94A3B8",
          dim:     "#475569",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      animation: {
        "orb-pulse": "orb-pulse 2.5s ease-in-out infinite",
        "orb-listen": "orb-listen 0.9s ease-in-out infinite",
        "orb-think":  "orb-think 1.2s linear infinite",
        "orb-speak":  "orb-speak 0.5s ease-in-out infinite",
        "shimmer":    "shimmer 2.5s linear infinite",
        "fade-in":    "fade-in 0.3s ease-out",
        "slide-up":   "slide-up 0.35s ease-out",
      },
      keyframes: {
        "orb-pulse": {
          "0%,100%": { transform: "scale(1)", opacity: "0.75" },
          "50%":     { transform: "scale(1.12)", opacity: "1" },
        },
        "orb-listen": {
          "0%,100%": { transform: "scale(1)", opacity: "0.85" },
          "50%":     { transform: "scale(1.22)", opacity: "1" },
        },
        "orb-think": {
          "0%":   { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        "orb-speak": {
          "0%,100%": { transform: "scaleY(1)" },
          "50%":     { transform: "scaleY(1.3)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% center" },
          "100%": { backgroundPosition: "200% center" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to:   { opacity: "1" },
        },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(12px)" },
          to:   { opacity: "1", transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
