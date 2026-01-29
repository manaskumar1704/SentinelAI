import { type Metadata } from 'next'
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs'
import { Inter, Outfit } from 'next/font/google'
import './globals.css'
import { Navbar } from '@/components/Navbar'

const inter = Inter({
  variable: '--font-inter',
  subsets: ['latin'],
})

const outfit = Outfit({
  variable: '--font-outfit',
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
        <body className={`${inter.variable} ${outfit.variable} antialiased min-h-screen bg-background text-foreground font-sans`}>
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
                  <button className="text-sm font-medium hover:text-primary transition-colors">
                    Sign In
                  </button>
                </SignInButton>
                <SignUpButton mode="modal">
                  <button className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-full font-medium text-sm h-10 px-5 transition-all shadow-lg shadow-primary/20">
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

