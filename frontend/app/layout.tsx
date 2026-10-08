import { ClerkProvider } from "@clerk/nextjs";
import { dark } from "@clerk/themes";
import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";
import { Navbar } from "@/components/Navbar";

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
      <body className="min-h-screen bg-slate-950 font-sans antialiased text-slate-100">
        <ClerkProvider appearance={{ baseTheme: dark }}>
          <AuthProvider>
            <Navbar />
            {children}
          </AuthProvider>
        </ClerkProvider>
      </body>
    </html>
  );
}