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
          bg: "#0d0d1a",
          panel: "#111128",
          gold: "#c4a45a",
          purple: "#2a2a5a",
          "purple-light": "#3d3d7a",
          text: "#cdd6f4",
          muted: "#6b6ba8",
          success: "#50fa7b",
          error: "#ff5555",
          info: "#8be9fd",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      animation: {
        "pulse-gold": "pulse-gold 2s ease-in-out infinite",
        "orb-idle": "orb-idle 3s ease-in-out infinite",
        "orb-listen": "orb-listen 1s ease-in-out infinite",
        "orb-think": "orb-think 0.6s ease-in-out infinite",
        "orb-speak": "orb-speak 0.4s ease-in-out infinite",
        "shimmer": "shimmer 2s linear infinite",
      },
      keyframes: {
        "pulse-gold": {
          "0%, 100%": { opacity: "0.6" },
          "50%": { opacity: "1" },
        },
        "orb-idle": {
          "0%, 100%": { transform: "scale(1)", opacity: "0.7" },
          "50%": { transform: "scale(1.08)", opacity: "1" },
        },
        "orb-listen": {
          "0%, 100%": { transform: "scale(1)", boxShadow: "0 0 20px #c4a45a66" },
          "50%": { transform: "scale(1.15)", boxShadow: "0 0 40px #c4a45aaa" },
        },
        "orb-think": {
          "0%, 100%": { transform: "scale(1) rotate(0deg)" },
          "50%": { transform: "scale(1.1) rotate(180deg)" },
        },
        "orb-speak": {
          "0%, 100%": { transform: "scaleY(1)" },
          "50%": { transform: "scaleY(1.2)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
};
export default config;
