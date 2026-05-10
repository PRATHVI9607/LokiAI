import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Loki — AI Desktop Assistant",
  description: "Elite Norse AI assistant for your desktop.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="overflow-hidden">{children}</body>
    </html>
  );
}
