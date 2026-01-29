"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { ArrowRight, CheckCircle2, Globe2, ShieldCheck, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { createClient } from "@/lib/supabase/client";
import { Session } from "@supabase/supabase-js";

export default function Home() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const supabase = createClient();

    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);

      if (session) {
        router.push("/dashboard");
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
        if (session) {
          router.push("/dashboard");
        }
      }
    );

    return () => subscription.unsubscribe();
  }, [router]);

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  if (session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center gap-4"
        >
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          <p className="text-muted-foreground animate-pulse">Redirecting to dashboard...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-background to-background overflow-hidden relative selection:bg-primary/30">

      {/* Abstract Background Elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none opacity-50">
        <div className="absolute top-[-10%] left-[20%] w-[40vw] h-[40vw] bg-primary/20 rounded-full blur-[100px] animate-blob mix-blend-multiply dark:mix-blend-screen" />
        <div className="absolute top-[20%] right-[10%] w-[35vw] h-[35vw] bg-secondary/20 rounded-full blur-[100px] animate-blob animation-delay-2000 mix-blend-multiply dark:mix-blend-screen" />
        <div className="absolute bottom-[-10%] left-[30%] w-[50vw] h-[50vw] bg-accent/20 rounded-full blur-[100px] animate-blob animation-delay-4000 mix-blend-multiply dark:mix-blend-screen" />
      </div>

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="container px-4 md:px-6 flex flex-col items-center text-center space-y-8 z-10"
      >
        <motion.div variants={item} className="space-y-4 max-w-4xl">
          <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary backdrop-blur-sm mb-4">
            <Sparkles className="mr-2 h-3.5 w-3.5" />
            <span>AI-Powered Study Abroad</span>
          </div>

          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight text-foreground text-balance font-heading">
            Your Future, <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-amber-300">
              Guided by Intelligence.
            </span>
          </h1>

          <p className="mx-auto max-w-[700px] text-lg md:text-xl text-muted-foreground md:leading-relaxed">
            Plan your study-abroad journey with a guided AI counsellor.
            Deterministic paths, personalized advice, and a clear roadmap to your dream university.
          </p>
        </motion.div>

        <motion.div variants={item} className="flex flex-col sm:flex-row gap-4 w-full justify-center">
          <Link href="/auth/signup">
            <Button size="lg" className="h-12 px-8 text-base rounded-full shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all duration-300 bg-primary text-primary-foreground hover:bg-primary/90">
              Get Started <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
          <Link href="/auth/login">
            <Button variant="outline" size="lg" className="h-12 px-8 text-base rounded-full border-2 hover:bg-muted/50 transition-all duration-300 border-primary/20 text-foreground hover:text-primary">
              Sign In
            </Button>
          </Link>
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
            <div key={idx} className="group relative overflow-hidden rounded-2xl border bg-background/50 p-6 hover:bg-background/80 transition-colors duration-300 backdrop-blur-sm border-white/10">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-amber-500/5 opacity-0 group-hover:opacity-100 transition-opacity" />
              <div className="relative z-10">
                <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <feature.icon className="h-5 w-5" />
                </div>
                <h3 className="text-lg font-semibold mb-2 font-heading">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.desc}</p>
              </div>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </main>
  );
}
