"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { motion } from "framer-motion";
import { CheckCircle2, Circle, FileText, Calendar, Clock, ChevronRight, CircleDollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

// Mock data for guidance (since backend endpoints for this part were identified as missing)
const GUIDANCE_STEPS = [
    {
        title: "Preparation Phase",
        tasks: [
            { id: "sop", title: "Draft Statement of Purpose", type: "document", status: "pending" },
            { id: "lor", title: "Request Letters of Recommendation", type: "document", status: "completed" },
        ]
    },
    {
        title: "Application Phase",
        tasks: [
            { id: "app_form", title: "Fill University Portal Form", type: "action", status: "pending" },
            { id: "fee", title: "Pay Application Fee", type: "payment", status: "pending" },
        ]
    }
];

export default function GuidancePage() {
    const { getToken } = useAuth();
    const [lockedUnis, setLockedUnis] = useState<any[]>([]);
    const [selectedUni, setSelectedUni] = useState<string | null>(null);

    useEffect(() => {
        const fetchLocked = async () => {
            try {
                const token = await getToken();
                const res = await fetch("http://localhost:8000/api/universities/shortlist", {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (res.ok) {
                    const list = await res.json();
                    const locked = list.filter((u: any) => u.is_locked);
                    setLockedUnis(locked);
                    if (locked.length > 0) setSelectedUni(locked[0].university.name);
                }
            } catch (e) {
                console.error(e);
            }
        };
        fetchLocked();
    }, [getToken]);

    if (lockedUnis.length === 0) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center">
                <h2 className="text-2xl font-bold mb-4">No Universities Locked</h2>
                <p className="text-muted-foreground mb-8">Lock a university from your shortlist to unlock detailed application guidance.</p>
                <Button asChild>
                    <a href="/universities">Go to Universities</a>
                </Button>
            </div>
        );
    }

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen bg-background p-6 md:p-12"
        >
            <div className="mx-auto max-w-6xl grid grid-cols-1 lg:grid-cols-4 gap-8">

                {/* Sidebar: Locked Universities */}
                <div className="space-y-4">
                    <h2 className="text-xl font-bold mb-4">Your Applications</h2>
                    {lockedUnis.map((uni) => (
                        <div
                            key={uni.university.name}
                            onClick={() => setSelectedUni(uni.university.name)}
                            className={cn(
                                "cursor-pointer p-4 rounded-xl border transition-all",
                                selectedUni === uni.university.name
                                    ? "border-indigo-500 bg-indigo-500/10 shadow-md"
                                    : "border-white/10 bg-white/5 hover:bg-white/10"
                            )}
                        >
                            <h3 className="font-semibold">{uni.university.name}</h3>
                            <p className="text-sm text-muted-foreground">{uni.university.country}</p>
                        </div>
                    ))}
                </div>

                {/* Main Content */}
                <div className="lg:col-span-3 space-y-8">
                    <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-indigo-900/20 to-purple-900/20 p-8">
                        <div className="flex items-center justify-between mb-6">
                            <div>
                                <h1 className="text-3xl font-bold">{selectedUni}</h1>
                                <p className="text-indigo-300">Fall 2027 Intake</p>
                            </div>
                            <div className="text-right">
                                <div className="text-2xl font-bold">25%</div>
                                <div className="text-xs uppercase tracking-wide text-muted-foreground">Complete</div>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="h-2 w-full bg-black/20 rounded-full overflow-hidden">
                            <div className="h-full w-1/4 bg-indigo-500" />
                        </div>
                    </div>

                    <div className="space-y-8">
                        {GUIDANCE_STEPS.map((step, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.1 }}
                            >
                                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                                    <span className="flex h-6 w-6 items-center justify-center rounded-full bg-white/10 text-xs">{idx + 1}</span>
                                    {step.title}
                                </h3>
                                <div className="space-y-3">
                                    {step.tasks.map((task) => (
                                        <div key={task.id} className="flex items-center justify-between p-4 rounded-xl border border-white/5 bg-white/5 hover:border-white/10 transition-colors">
                                            <div className="flex items-center gap-3">
                                                {task.status === "completed"
                                                    ? <CheckCircle2 className="h-5 w-5 text-green-500" />
                                                    : <Circle className="h-5 w-5 text-muted-foreground" />
                                                }
                                                <span className={task.status === "completed" ? "line-through text-muted-foreground" : ""}>
                                                    {task.title}
                                                </span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                {task.type === "document" && <FileText className="h-4 w-4 text-muted-foreground" />}
                                                {task.type === "payment" && <CircleDollarSign className="h-4 w-4 text-muted-foreground" />}
                                                <ChevronRight className="h-4 w-4 text-muted-foreground" />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

            </div>
        </motion.div>
    );
}

