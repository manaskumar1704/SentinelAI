"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { MapPin, Lock, Unlock, AlertTriangle, CheckCircle2, Bookmark, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { createClient } from "@/lib/supabase/client";
import { Session } from "@supabase/supabase-js";

type University = {
    name: string;
    country: string;
    alpha_two_code: string;
    web_pages: string[];
};

type UniversityRecommendation = {
    university: University;
    category: "dream" | "target" | "safe";
    fit_reasons: string[];
    risks: string[];
    cost_level: "low" | "medium" | "high";
    acceptance_chance: "low" | "medium" | "high";
};

type ShortlistedUniversity = {
    university: University;
    category: string;
    is_locked: boolean;
    added_at: string;
};

export default function UniversitiesPage() {
    const router = useRouter();
    const [session, setSession] = useState<Session | null>(null);
    const [activeTab, setActiveTab] = useState<"recommendations" | "shortlist">("recommendations");
    const [recommendations, setRecommendations] = useState<UniversityRecommendation[]>([]);
    const [shortlist, setShortlist] = useState<ShortlistedUniversity[]>([]);
    const [loading, setLoading] = useState(true);

    const getToken = useCallback(async () => {
        if (!session) return null;
        return session.access_token;
    }, [session]);

    // Initialize session
    useEffect(() => {
        const supabase = createClient();
        supabase.auth.getSession().then(({ data: { session } }) => {
            setSession(session);
            if (!session) {
                router.push("/");
            }
        });
    }, [router]);

    // Fetch data
    useEffect(() => {
        const fetchData = async () => {
            if (!session) return;

            try {
                const token = session.access_token;

                setLoading(true);
                const [recsRes, shortRes] = await Promise.all([
                    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/universities/recommendations`, { headers: { Authorization: `Bearer ${token}` } }),
                    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/universities/shortlist`, { headers: { Authorization: `Bearer ${token}` } })
                ]);

                if (recsRes.ok) setRecommendations(await recsRes.json());
                if (shortRes.ok) setShortlist(await shortRes.json());
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [session, activeTab]);

    const addToShortlist = async (uni: University, category: string) => {
        try {
            const token = await getToken();
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/universities/shortlist`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    university_name: uni.name,
                    country: uni.country,
                    category
                })
            });
            // Refresh
            setActiveTab("shortlist");
        } catch (err) {
            console.error(err);
        }
    };

    const lockUniversity = async (name: string, country: string) => {
        try {
            const token = await getToken();
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/universities/lock`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ university_name: name, country })
            });
            // Refresh
            const shortRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/universities/shortlist`, { headers: { Authorization: `Bearer ${token}` } });
            if (shortRes.ok) setShortlist(await shortRes.json());
        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="min-h-screen bg-background p-6 md:p-12">
            <div className="mx-auto max-w-7xl space-y-8">

                <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-foreground font-heading">Universities</h1>
                        <p className="text-muted-foreground">Discover and manage your target schools.</p>
                    </div>

                    <div className="flex p-1 bg-white/5 rounded-full border border-white/10">
                        <button
                            onClick={() => setActiveTab("recommendations")}
                            className={cn(
                                "px-6 py-2 rounded-full text-sm font-medium transition-all",
                                activeTab === "recommendations" ? "bg-primary text-primary-foreground shadow-lg" : "text-muted-foreground hover:text-foreground"
                            )}
                        >
                            Recommendations
                        </button>
                        <button
                            onClick={() => setActiveTab("shortlist")}
                            className={cn(
                                "px-6 py-2 rounded-full text-sm font-medium transition-all",
                                activeTab === "shortlist" ? "bg-primary text-primary-foreground shadow-lg" : "text-muted-foreground hover:text-foreground"
                            )}
                        >
                            Shortlist ({shortlist.length})
                        </button>
                    </div>
                </div>

                {loading ? (
                    <div className="flex justify-center py-20"><div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" /></div>
                ) : activeTab === "recommendations" ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {recommendations.map((rec, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                className="group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 hover:border-primary/30 hover:bg-white/10 transition-all font-sans"
                            >
                                <div>
                                    <div className="flex justify-between items-start mb-4">
                                        <Badge className={cn(
                                            "uppercase tracking-wider",
                                            rec.category === "dream" ? "bg-purple-500/20 text-purple-300 hover:bg-purple-500/30" :
                                                rec.category === "target" ? "bg-primary/20 text-primary hover:bg-primary/30" :
                                                    "bg-green-500/20 text-green-300 hover:bg-green-500/30"
                                        )}>
                                            {rec.category}
                                        </Badge>
                                        <div className="flex gap-2">
                                            {rec.acceptance_chance === "high" && <Badge variant="outline" className="border-green-500/50 text-green-400">High Chance</Badge>}
                                        </div>
                                    </div>

                                    <h3 className="text-xl font-bold mb-1 line-clamp-2">{rec.university.name}</h3>
                                    <div className="flex items-center text-sm text-muted-foreground mb-4">
                                        <MapPin className="h-4 w-4 mr-1" /> {rec.university.country}
                                    </div>

                                    <div className="space-y-3 mb-6">
                                        <div className="space-y-1">
                                            <p className="text-xs font-semibold text-muted-foreground uppercase">Why it fits</p>
                                            {rec.fit_reasons.map((r, i) => (
                                                <div key={i} className="flex items-start gap-2 text-sm">
                                                    <CheckCircle2 className="h-4 w-4 text-green-500 shrink-0 mt-0.5" />
                                                    <span>{r}</span>
                                                </div>
                                            ))}
                                        </div>

                                        {rec.risks.length > 0 && (
                                            <div className="space-y-1">
                                                <p className="text-xs font-semibold text-muted-foreground uppercase">Risks</p>
                                                {rec.risks.map((r, i) => (
                                                    <div key={i} className="flex items-start gap-2 text-sm text-yellow-500/90">
                                                        <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
                                                        <span>{r}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                </div>

                                <Button
                                    onClick={() => addToShortlist(rec.university, rec.category)}
                                    className="w-full gap-2 bg-white/10 hover:bg-primary hover:text-primary-foreground transition-colors text-foreground"
                                >
                                    <Bookmark className="h-4 w-4" /> Shortlist
                                </Button>
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {shortlist.length === 0 ? (
                            <div className="col-span-full text-center py-20 text-muted-foreground">
                                No universities shortlisted yet. Go to Recommendations to add some.
                            </div>
                        ) : shortlist.map((item, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className={cn(
                                    "relative flex flex-col justify-between overflow-hidden rounded-2xl border p-6 transition-all",
                                    item.is_locked
                                        ? "border-yellow-500/50 bg-yellow-500/10 shadow-[0_0_20px_rgba(234,179,8,0.1)]"
                                        : "border-white/10 bg-white/5 hover:border-primary/30"
                                )}
                            >
                                <div>
                                    <div className="flex justify-between items-start mb-4">
                                        <Badge variant="secondary">{item.category}</Badge>
                                        {item.is_locked ? (
                                            <div className="flex items-center gap-1 text-yellow-500 bg-yellow-500/20 px-2 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                                                <Lock className="h-3 w-3" /> Locked
                                            </div>
                                        ) : (
                                            <div className="flex items-center gap-1 text-muted-foreground bg-white/5 px-2 py-1 rounded-full text-xs">
                                                <Unlock className="h-3 w-3" /> Open
                                            </div>
                                        )}
                                    </div>

                                    <h3 className="text-xl font-bold mb-1">{item.university.name}</h3>
                                    <div className="flex items-center text-sm text-muted-foreground mb-6">
                                        <MapPin className="h-4 w-4 mr-1" /> {item.university.country}
                                    </div>
                                </div>

                                {item.is_locked ? (
                                    <Link href="/guidance">
                                        <Button className="w-full gap-2 bg-yellow-600 hover:bg-yellow-700 text-white">
                                            View Application Guide <ArrowRight className="h-4 w-4" />
                                        </Button>
                                    </Link>
                                ) : (
                                    <Button
                                        onClick={() => lockUniversity(item.university.name, item.university.country)}
                                        variant="outline"
                                        className="w-full gap-2 border-yellow-500/50 text-yellow-500 hover:bg-yellow-500/10"
                                    >
                                        <Lock className="h-4 w-4" /> Lock & Start Application
                                    </Button>
                                )}
                            </motion.div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
