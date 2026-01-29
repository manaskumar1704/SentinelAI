"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { motion, AnimatePresence } from "framer-motion";
import { Save, User, GraduationCap, Globe, Banknote, BookOpen, ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

// Reusing types from onboarding (in a real app, these would be in a shared types file)
type OnboardingData = {
    academic_background: any;
    study_goal: any;
    budget: any;
    exams_readiness: any;
};

const SECTIONS = [
    { id: "academic_background", title: "Academic Background", icon: GraduationCap },
    { id: "study_goal", title: "Study Goals", icon: Globe },
    { id: "budget", title: "Budget & Finance", icon: Banknote },
    { id: "exams_readiness", title: "Readiness", icon: BookOpen },
];

export default function ProfilePage() {
    const { getToken } = useAuth();
    const [data, setData] = useState<OnboardingData | null>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [openSection, setOpenSection] = useState<string | null>("academic_background");

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = await getToken();
                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/onboarding`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (res.ok) {
                    const json = await res.json();
                    if (json.data) setData(json.data);
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, [getToken]);

    const handleSave = async () => {
        if (!data) return;
        setSaving(true);
        try {
            const token = await getToken();
            await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/onboarding`, {
                method: "POST", // Using POST to overwrite/update
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });
        } catch (err) {
            console.error(err);
        } finally {
            setSaving(false);
        }
    };

    const updateField = (section: string, field: string, value: any) => {
        if (!data) return;
        setData({
            ...data,
            [section]: {
                ...data[section as keyof OnboardingData],
                [field]: value
            }
        });
    };

    if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin h-8 w-8 text-primary" /></div>;
    if (!data) return <div className="text-center py-20">Please complete onboarding first.</div>;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="min-h-screen bg-background p-6 md:p-12"
        >
            <div className="mx-auto max-w-4xl space-y-8">

                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-foreground font-heading">Profile</h1>
                        <p className="text-muted-foreground">Manage your study abroad preferences.</p>
                    </div>
                    <Button onClick={handleSave} disabled={saving} className="bg-primary hover:bg-primary/90 text-primary-foreground">
                        {saving ? <Loader2 className="animate-spin mr-2 h-4 w-4" /> : <Save className="mr-2 h-4 w-4" />}
                        Save Changes
                    </Button>
                </div>

                <div className="space-y-4">
                    {SECTIONS.map((section) => (
                        <div key={section.id} className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
                            <button
                                onClick={() => setOpenSection(openSection === section.id ? null : section.id)}
                                className="flex w-full items-center justify-between p-6 transition-colors hover:bg-white/5"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-primary">
                                        <section.icon className="h-5 w-5" />
                                    </div>
                                    <span className="font-semibold text-lg">{section.title}</span>
                                </div>
                                {openSection === section.id ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
                            </button>

                            <AnimatePresence>
                                {openSection === section.id && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: "auto", opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.2 }}
                                    >
                                        <div className="border-t border-white/5 p-6 space-y-4">
                                            {/* 
                          Ideally we'd reuse the form fields from Onboarding here.
                          For MVP brevity, I'll render a JSON dump or basic inputs. 
                          Let's render basic inputs for the main fields.
                       */}

                                            {Object.keys(data[section.id as keyof OnboardingData]).map((key) => {
                                                const val = (data[section.id as keyof OnboardingData] as any)[key];
                                                if (typeof val === 'object' && val !== null && !Array.isArray(val)) return null; // Skip nested objects if any

                                                return (
                                                    <div key={key} className="space-y-2">
                                                        <Label className="capitalize">{key.replace(/_/g, " ")}</Label>
                                                        <Input
                                                            value={Array.isArray(val) ? val.join(", ") : val || ""}
                                                            onChange={(e) => {
                                                                const newVal = Array.isArray(val) ? e.target.value.split(", ") : e.target.value;
                                                                updateField(section.id, key, newVal);
                                                            }}
                                                            className="bg-black/20 border-white/10 focus-visible:ring-primary"
                                                        />
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    ))}
                </div>

            </div>
        </motion.div>
    );
}
