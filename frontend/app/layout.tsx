import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Vivya Sense - Intelligent Video Surveillance',
  description: 'AI-powered video surveillance platform with PPE detection, fall detection, and fire/smoke detection',
  keywords: ['AI', 'video surveillance', 'computer vision', 'PPE detection', 'fall detection', 'fire detection', 'Vivya Sense'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}

