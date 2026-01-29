"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle, ArrowRight, Sparkles, AlertCircle } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { createClient } from "@/lib/supabase/client";
import { Session } from "@supabase/supabase-js";

// Types
type Stage = {
    number: number;
    name: string;
};

type UserStage = {
    stage: number;
    stage_name: string;
    stages: Stage[];
};

type UserProfile = {
    id: string;
    full_name: string;
    email: string;
    onboarding_completed: boolean;
};

// Mock data to start with (will replace with API calls)
const MOCK_TASKS = [
    { id: 1, text: "Complete academic profile", completed: true },
    { id: 2, text: "Shortlist 5 universities", completed: false },
    { id: 3, text: "Begin SOP draft", completed: false },
    { id: 4, text: "Check IELTS dates", completed: false },
];

export default function DashboardPage() {
    const router = useRouter();
    const [session, setSession] = useState<Session | null>(null);
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [stageInfo, setStageInfo] = useState<UserStage | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const supabase = createClient();

        const fetchData = async () => {
            try {
                const { data: { session } } = await supabase.auth.getSession();
                setSession(session);

                if (!session) {
                    router.push("/");
                    return;
                }

                const token = session.access_token;

                const [profileRes, stageRes] = await Promise.all([
                    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/user/profile`, {
                        headers: { Authorization: `Bearer ${token}` }
                    }),
                    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/user/stage`, {
                        headers: { Authorization: `Bearer ${token}` }
                    })
                ]);

                if (profileRes.ok) {
                    const profileData = await profileRes.json();
                    setProfile(profileData);

                    // Logic flow: If onboarding not completed, redirect
                    if (profileData && profileData.onboarding_completed === false) {
                        router.push("/onboarding");
                        return;
                    }
                }

                if (stageRes.ok) setStageInfo(await stageRes.json());
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [router]);

    if (loading) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-background">
                <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
            </div>
        );
    }

    const currentStage = stageInfo?.stage || 1;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen bg-background p-6 md:p-12"
        >
            <div className="mx-auto max-w-6xl space-y-8">

                {/* Welcome Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col gap-2"
                >
                    <div className="flex items-center gap-2 text-primary">
                        <Sparkles className="h-5 w-5" />
                        <span className="text-sm font-medium uppercase tracking-wider">Control Center</span>
                    </div>
                    <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/60 font-heading">
                        Welcome back, {profile?.full_name?.split(" ")[0] || session?.user?.user_metadata?.full_name?.split(" ")[0] || "Student"}.
                    </h1>
                    <p className="text-muted-foreground">Here is what you need to focus on today.</p>
                </motion.div>

                {/* Stage Indicator */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="grid grid-cols-1 md:grid-cols-4 gap-4"
                >
                    {stageInfo?.stages.map((s) => {
                        const isActive = s.number === currentStage;
                        const isPast = s.number < currentStage;
                        return (
                            <div
                                key={s.number}
                                className={`relative overflow-hidden rounded-xl border p-4 transition-all ${isActive
                                    ? "border-primary/50 bg-primary/10 shadow-[0_0_15px_var(--primary)]"
                                    : isPast
                                        ? "border-green-500/30 bg-green-500/5 opacity-60"
                                        : "border-white/5 bg-white/5 opacity-40"
                                    }`}
                            >
                                <div className="flex items-center justify-between mb-2">
                                    <span className={`text-xs font-bold uppercase ${isActive ? "text-primary" : ""}`}>
                                        Stage 0{s.number}
                                    </span>
                                    {isPast && <CheckCircle className="h-4 w-4 text-green-500" />}
                                    {isActive && <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />}
                                </div>
                                <h3 className="font-semibold">{s.name}</h3>
                            </div>
                        );
                    })}
                </motion.div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Actions Column */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Profile Strength */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.2 }}
                            className="rounded-2xl border border-white/10 bg-gradient-to-br from-primary/10 to-purple-900/10 p-6 backdrop-blur-sm"
                        >
                            <div className="flex items-start justify-between">
                                <div>
                                    <h2 className="text-xl font-semibold mb-2">Profile Strength</h2>
                                    <p className="text-muted-foreground text-sm max-w-md">
                                        Based on your profile, you have a strong academic background but need to focus on standardized tests.
                                    </p>
                                </div>
                                <div className="text-right">
                                    <div className="text-4xl font-bold text-primary">72%</div>
                                    <div className="text-xs text-muted-foreground uppercase tracking-wide">Ready</div>
                                </div>
                            </div>
                            <div className="mt-6 h-2 w-full rounded-full bg-white/5 overflow-hidden">
                                <div className="h-full w-[72%] bg-gradient-to-r from-primary to-purple-500" />
                            </div>
                        </motion.div>

                        {/* AI To-Do List */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                        >
                            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                                <CheckCircle className="h-5 w-5 text-primary" />
                                Action Items
                            </h3>
                            <div className="space-y-3">
                                {MOCK_TASKS.map((task) => (
                                    <div
                                        key={task.id}
                                        className="group flex items-center justify-between rounded-xl border border-white/5 bg-white/5 p-4 transition-colors hover:border-primary/30 hover:bg-white/10"
                                    >
                                        <div className="flex items-center gap-3">
                                            <div className={`h-5 w-5 rounded-full border flex items-center justify-center transition-colors ${task.completed ? "bg-green-500/20 border-green-500/50" : "border-white/20 group-hover:border-primary"
                                                }`}>
                                                {task.completed && <CheckCircle className="h-3 w-3 text-green-500" />}
                                            </div>
                                            <span className={task.completed ? "text-muted-foreground line-through" : ""}>
                                                {task.text}
                                            </span>
                                        </div>
                                        {!task.completed && (
                                            <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity hover:text-primary">
                                                Start
                                            </Button>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    </div>

                    {/* Sidebar */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.4 }}
                        className="space-y-6"
                    >
                        {/* Quick Links */}
                        <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                            <h3 className="font-semibold mb-4">Quick Links</h3>
                            <div className="space-y-2">
                                <Link href="/universities">
                                    <Button variant="outline" className="w-full justify-start h-12 border-white/10 hover:bg-primary/10 hover:text-primary hover:border-primary/20">
                                        <ArrowRight className="mr-2 h-4 w-4" /> Browse Universities
                                    </Button>
                                </Link>
                                <Link href="/counsellor">
                                    <Button variant="outline" className="w-full justify-start h-12 border-white/10 hover:bg-primary/10 hover:text-primary hover:border-primary/20">
                                        <ArrowRight className="mr-2 h-4 w-4" /> Ask Counsellor
                                    </Button>
                                </Link>
                            </div>
                        </div>

                        {/* Insight Card */}
                        <div className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-6">
                            <div className="flex items-center gap-2 text-yellow-500 mb-2">
                                <AlertCircle className="h-5 w-5" />
                                <span className="font-semibold">Insight</span>
                            </div>
                            <p className="text-sm text-muted-foreground">
                                University of Toronto applications for Fall 2027 open in 3 months. Prepare your SOP now.
                            </p>
                        </div>
                    </motion.div>
                </div>
            </div>
        </motion.div>
    );
}
