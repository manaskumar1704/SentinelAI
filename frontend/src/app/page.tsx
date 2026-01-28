"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { ArrowRight, CheckCircle2, Globe2, ShieldCheck, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { SignedIn, SignedOut, SignInButton, useUser } from "@clerk/nextjs";

export default function Home() {
  const { isSignedIn, isLoaded } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      router.push("/dashboard");
    }
  }, [isLoaded, isSignedIn, router]);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3,
      },
    },
  };

  const item = {
    hidden: { y: 20, opacity: 0 },
    show: { y: 0, opacity: 1, transition: { type: "spring" as const, stiffness: 50 } },
  };

  if (isLoaded && isSignedIn) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center gap-4"
        >
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
          <p className="text-muted-foreground animate-pulse">Redirecting to dashboard...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-100 via-background to-background dark:from-indigo-950 dark:via-background dark:to-background overflow-hidden relative selection:bg-indigo-500/30">

      {/* Abstract Background Elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div className="absolute top-[-10%] left-[20%] w-[40vw] h-[40vw] bg-purple-500/10 rounded-full blur-[100px] animate-blob mix-blend-multiply dark:mix-blend-layout" />
        <div className="absolute top-[20%] right-[10%] w-[35vw] h-[35vw] bg-indigo-500/10 rounded-full blur-[100px] animate-blob animation-delay-2000 mix-blend-multiply dark:mix-blend-layout" />
        <div className="absolute bottom-[-10%] left-[30%] w-[50vw] h-[50vw] bg-blue-500/10 rounded-full blur-[100px] animate-blob animation-delay-4000 mix-blend-multiply dark:mix-blend-layout" />
      </div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="container px-4 md:px-6 flex flex-col items-center text-center space-y-8 z-10"
      >
        <motion.div variants={item} className="space-y-4 max-w-4xl">
          <div className="inline-flex items-center rounded-full border border-indigo-200/50 dark:border-indigo-800/50 bg-indigo-50/50 dark:bg-indigo-950/30 px-3 py-1 text-sm font-medium text-indigo-800 dark:text-indigo-300 backdrop-blur-sm mb-4">
            <Sparkles className="mr-2 h-3.5 w-3.5" />
            <span>AI-Powered Study Abroad</span>
          </div>

          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight text-foreground text-balance">
            Your Future, <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400">
              Guided by Intelligence.
            </span>
          </h1>

          <p className="mx-auto max-w-[700px] text-lg md:text-xl text-muted-foreground md:leading-relaxed">
            Plan your study-abroad journey with a guided AI counsellor.
            Deterministic paths, personalized advice, and a clear roadmap to your dream university.
          </p>
        </motion.div>

        <motion.div variants={item} className="flex flex-col sm:flex-row gap-4 w-full justify-center">
          <SignedOut>
            <SignInButton mode="modal">
              <Button size="lg" className="h-12 px-8 text-base rounded-full shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/40 transition-all duration-300">
                Get Started <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <Link href="/dashboard">
              <Button size="lg" className="h-12 px-8 text-base rounded-full shadow-lg shadow-indigo-500/20 hover:shadow-indigo-500/40 transition-all duration-300">
                Go to Dashboard <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </SignedIn>
          <Button variant="outline" size="lg" className="h-12 px-8 text-base rounded-full border-2 hover:bg-muted/50 transition-all duration-300">
            Learn Flow
          </Button>
        </motion.div>

        {/* Feature Grid */}
        <motion.div variants={item} className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 w-full max-w-5xl text-left">
          {[
            {
              icon: Globe2,
              title: "Global Reach",
              desc: "Access a database of thousands of universities worldwide personalized to your profile."
            },
            {
              icon: ShieldCheck,
              title: "Deterministic Guidance",
              desc: "No hallucinations. Just clear, step-by-step verified application paths."
            },
            {
              icon: CheckCircle2,
              title: "Profile Strength",
              desc: "Real-time analysis of your application strength and improvement tips."
            }
          ].map((feature, idx) => (
            <div key={idx} className="group relative overflow-hidden rounded-2xl border bg-background/50 p-6 hover:bg-background/80 transition-colors duration-300 backdrop-blur-sm">
              <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="relative z-10">
                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-100/50 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400">
                  <feature.icon className="h-5 w-5" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.desc}</p>
              </div>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </main>
  );
}
