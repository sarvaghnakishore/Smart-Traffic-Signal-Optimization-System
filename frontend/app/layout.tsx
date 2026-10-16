import '../styles/globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Smart City | Traffic Control Center',
  description: 'AI-Powered real-time traffic signal optimization and analytics dashboard.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.className} bg-slate-950 text-slate-200 antialiased selection:bg-blue-500/30`} suppressHydrationWarning>
        <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(30,58,138,0.15)_0%,transparent_50%)] pointer-events-none" />
        {children}
      </body>
    </html>
  )
}
