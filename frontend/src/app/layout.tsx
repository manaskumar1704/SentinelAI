import { type Metadata } from 'next'
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs'
import { Geist, Geist_Mono } from 'next/font/google'
import './globals.css'
import { Navbar } from '@/components/Navbar'

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
})

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
})

export const metadata: Metadata = {
  title: 'SentinelAI | Your Future, Guided.',
  description: 'Plan your study-abroad journey with a guided AI counsellor.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <ClerkProvider>
      <html lang="en" className="dark">
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-background text-foreground`}>
          <Navbar />
          {/* Landing page header only shows when signed out or on landing page - handled by Navbar logic or specific page layouts, 
              but here we kept the original header logic for the landing page auth buttons if needed, 
              though Navbar handles most authenticated nav. 
              Let's hide the old header if we are using the new Navbar, or condition it. 
              Actually, the original header was nice for the landing page. 
              Let's keep a simplified version for SignedOut state only. */}

          <SignedOut>
            {/* Only show this simple header on landing page when signed out */}
            <header className="absolute top-0 right-0 z-50 p-6">
              <div className="flex gap-4">
                <SignInButton mode="modal">
                  <button className="text-sm font-medium hover:text-indigo-400 transition-colors">
                    Sign In
                  </button>
                </SignInButton>
                <SignUpButton mode="modal">
                  <button className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-full font-medium text-sm h-10 px-5 transition-all shadow-lg shadow-indigo-500/20">
                    Sign Up
                  </button>
                </SignUpButton>
              </div>
            </header>
          </SignedOut>

          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
