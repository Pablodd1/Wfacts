import type { Metadata } from "next";
import { Inter, Playfair_Display, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains" });

export const metadata: Metadata = {
  title: "WatchFacts Hermes AI",
  description: "The OS for the luxury watch market.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={cn(
          "min-h-screen bg-[#050505] font-sans antialiased text-[#e8e8e8]",
          inter.variable,
          playfair.variable,
          jetbrains.variable
        )}
      >
        <div className="flex min-h-screen">
          {/* Sidebar */}
          <aside className="w-64 border-r border-[#333] bg-[#0a0a0a] flex flex-col">
            <div className="h-16 flex items-center px-6 border-b border-[#333]">
              <span className="font-serif text-xl font-bold text-[#d4af37]">HERMES AI</span>
            </div>
            <nav className="flex-1 px-4 py-4 space-y-2">
              <Link href="/dashboard" className="block px-4 py-2 rounded hover:bg-[#d4af37]/10 hover:text-[#d4af37] transition-colors">
                Dashboard
              </Link>
              <Link href="/exceptions" className="block px-4 py-2 rounded hover:bg-[#d4af37]/10 hover:text-[#d4af37] transition-colors">
                Exception Queue
              </Link>
              <Link href="/seller" className="block px-4 py-2 rounded hover:bg-[#d4af37]/10 hover:text-[#d4af37] transition-colors">
                Seller App
              </Link>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 overflow-y-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
