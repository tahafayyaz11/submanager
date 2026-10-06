import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Subsfolio — Subscription Intelligence Platform",
  description: "AI-powered subscription intelligence, management, analytics, and renewal-tracking platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
