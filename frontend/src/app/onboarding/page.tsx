"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import { useAuth } from "@clerk/nextjs";
import { ArrowRight, Check, ChevronLeft, GraduationCap, Globe, Banknote, BookOpen, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

// Types matching backend models
type OnboardingData = {
    academic_background: {
        current_education_level: string;
        degree_major: string;
        graduation_year: number;
        gpa: number;
    };
    study_goal: {
        intended_degree: string;
        field_of_study: string;
        target_intake_year: number;
        preferred_countries: string[];
    };
    budget: {
        budget_range_per_year: string;
        funding_plan: string;
    };
    exams_readiness: {
        ielts_toefl_status: string;
        ielts_toefl_score: number | null;
        gre_gmat_status: string;
        gre_gmat_score: number | null;
        sop_status: string;
    };
};

const INITIAL_DATA: OnboardingData = {
    academic_background: {
        current_education_level: "bachelors",
        degree_major: "",
        graduation_year: 2026,
        gpa: 0,
    },
    study_goal: {
        intended_degree: "masters",
        field_of_study: "",
        target_intake_year: 2027,
        preferred_countries: [],
    },
    budget: {
        budget_range_per_year: "20k_40k",
        funding_plan: "self_funded",
    },
    exams_readiness: {
        ielts_toefl_status: "not_started",
        ielts_toefl_score: null,
        gre_gmat_status: "not_started",
        gre_gmat_score: null,
        sop_status: "not_started",
    },
};

const STEPS = [
    { id: 1, title: "Academic Background", icon: GraduationCap, description: "Tell us about your current education." },
    { id: 2, title: "Study Goals", icon: Globe, description: "Where do you want to go?" },
    { id: 3, title: "Budget & Finance", icon: Banknote, description: "Plan your investment." },
    { id: 4, title: "Readiness", icon: BookOpen, description: "How prepared are you?" },
];

export default function OnboardingPage() {
    const router = useRouter();
    const { getToken } = useAuth();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState<OnboardingData>(INITIAL_DATA);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const updateField = (section: keyof OnboardingData, field: string, value: any) => {
        setFormData((prev) => ({
            ...prev,
            [section]: {
                ...prev[section],
                [field]: value,
            },
        }));
    };

    const nextStep = () => {
        if (step < STEPS.length) {
            setStep(step + 1);
        } else {
            handleSubmit();
        }
    };

    const prevStep = () => {
        if (step > 1) setStep(step - 1);
    };

    const handleSubmit = async () => {
        try {
            setIsSubmitting(true);
            const token = await getToken();

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/onboarding`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) throw new Error("Failed to submit");

            router.push("/dashboard");
        } catch (error) {
            console.error(error);
            setIsSubmitting(false);
        }
    };

    const renderStepContent = () => {
        switch (step) {
            case 1:
                return (
                    <div className="space-y-6">
                        <div className="space-y-4">
                            <Label>Current Education Level</Label>
                            <div className="grid grid-cols-2 gap-3">
                                {["High School", "Bachelors", "Masters", "PhD"].map((level) => (
                                    <div
                                        key={level}
                                        onClick={() => updateField("academic_background", "current_education_level", level.toLowerCase().replace(" ", "_"))}
                                        className={cn(
                                            "cursor-pointer rounded-xl border border-primary/10 bg-primary/5 p-4 text-center transition-all hover:border-primary/30",
                                            formData.academic_background.current_education_level === level.toLowerCase().replace(" ", "_") && "border-primary bg-primary/20 shadow-[0_0_15px_rgba(253,224,71,0.3)] text-primary-foreground font-semibold"
                                        )}
                                    >
                                        {level}
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2">
                            <div className="space-y-2">
                                <Label>Major / Degree</Label>
                                <Input
                                    value={formData.academic_background.degree_major}
                                    onChange={(e) => updateField("academic_background", "degree_major", e.target.value)}
                                    placeholder="e.g. Computer Science"
                                    className="bg-white/5 border-white/10 focus-visible:ring-primary"
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Graduation Year</Label>
                                <Input
                                    type="number"
                                    value={formData.academic_background.graduation_year}
                                    onChange={(e) => updateField("academic_background", "graduation_year", parseInt(e.target.value))}
                                    className="bg-white/5 border-white/10 focus-visible:ring-primary"
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label>GPA / Percentage (Optional)</Label>
                            <Input
                                type="number"
                                step="0.01"
                                value={formData.academic_background.gpa || ""}
                                onChange={(e) => updateField("academic_background", "gpa", parseFloat(e.target.value))}
                                placeholder="e.g. 3.8 or 85"
                                className="bg-white/5 border-white/10 focus-visible:ring-primary"
                            />
                        </div>
                    </div>
                );

            case 2:
                return (
                    <div className="space-y-6">
                        <div className="space-y-4">
                            <Label>Intended Degree</Label>
                            <div className="grid grid-cols-2 gap-3">
                                {["Bachelors", "Masters", "MBA", "PhD"].map((degree) => (
                                    <div
                                        key={degree}
                                        onClick={() => updateField("study_goal", "intended_degree", degree.toLowerCase())}
                                        className={cn(
                                            "cursor-pointer rounded-xl border border-primary/10 bg-primary/5 p-4 text-center transition-all hover:border-primary/30",
                                            formData.study_goal.intended_degree === degree.toLowerCase() && "border-primary bg-primary/20 shadow-[0_0_15px_rgba(253,224,71,0.3)] text-primary-foreground font-semibold"
                                        )}
                                    >
                                        {degree}
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="grid gap-4 sm:grid-cols-2">
                            <div className="space-y-2">
                                <Label>Target Field of Study</Label>
                                <Input
                                    value={formData.study_goal.field_of_study}
                                    onChange={(e) => updateField("study_goal", "field_of_study", e.target.value)}
                                    placeholder="e.g. Data Science"
                                    className="bg-white/5 border-white/10 focus-visible:ring-primary"
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Target Intake Year</Label>
                                <Input
                                    type="number"
                                    value={formData.study_goal.target_intake_year}
                                    onChange={(e) => updateField("study_goal", "target_intake_year", parseInt(e.target.value))}
                                    className="bg-white/5 border-white/10 focus-visible:ring-primary"
                                />
                            </div>
                        </div>

                        <div className="space-y-4">
                            <Label>Preferred Countries (Select multiple)</Label>
                            <div className="flex flex-wrap gap-2">
                                {["United States", "United Kingdom", "Canada", "Australia", "Germany", "Ireland", "Singapore"].map((country) => {
                                    const isSelected = formData.study_goal.preferred_countries.includes(country);
                                    return (
                                        <div
                                            key={country}
                                            onClick={() => {
                                                const current = formData.study_goal.preferred_countries;
                                                const updated = isSelected
                                                    ? current.filter(c => c !== country)
                                                    : [...current, country];
                                                updateField("study_goal", "preferred_countries", updated);
                                            }}
                                            className={cn(
                                                "cursor-pointer rounded-full px-4 py-2 text-sm border transition-all",
                                                isSelected
                                                    ? "border-primary bg-primary/20 text-primary-foreground font-medium"
                                                    : "border-white/10 bg-white/5 hover:bg-white/10"
                                            )}
                                        >
                                            {country}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    </div>
                );

            case 3:
                return (
                    <div className="space-y-6">
                        <div className="space-y-4">
                            <Label>Annual Budget Range (USD)</Label>
                            <div className="grid gap-3">
                                {[
                                    { label: "Under $10k", value: "under_10k" },
                                    { label: "$10k - $20k", value: "10k_20k" },
                                    { label: "$20k - $40k", value: "20k_40k" },
                                    { label: "$40k - $60k", value: "40k_60k" },
                                    { label: "Above $60k", value: "above_60k" },
                                ].map((budget) => (
                                    <div
                                        key={budget.value}
                                        onClick={() => updateField("budget", "budget_range_per_year", budget.value)}
                                        className={cn(
                                            "cursor-pointer rounded-xl border border-primary/10 bg-primary/5 p-4 flex items-center justify-between transition-all hover:border-primary/30",
                                            formData.budget.budget_range_per_year === budget.value && "border-primary bg-primary/20 shadow-[0_0_15px_rgba(253,224,71,0.3)] text-primary-foreground font-semibold"
                                        )}
                                    >
                                        <span>{budget.label}</span>
                                        {formData.budget.budget_range_per_year === budget.value && <Check className="h-4 w-4 text-primary-foreground" />}
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="space-y-4">
                            <Label>Funding Plan</Label>
                            <div className="grid grid-cols-3 gap-3">
                                {[
                                    { label: "Self Funded", value: "self_funded" },
                                    { label: "Loan", value: "loan_dependent" },
                                    { label: "Scholarship", value: "scholarship_dependent" },
                                ].map((plan) => (
                                    <div
                                        key={plan.value}
                                        onClick={() => updateField("budget", "funding_plan", plan.value)}
                                        className={cn(
                                            "cursor-pointer rounded-xl border border-primary/10 bg-primary/5 p-4 text-center text-sm transition-all hover:border-primary/30",
                                            formData.budget.funding_plan === plan.value && "border-primary bg-primary/20 shadow-[0_0_15px_rgba(253,224,71,0.3)] text-primary-foreground font-semibold"
                                        )}
                                    >
                                        {plan.label}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );

            case 4:
                return (
                    <div className="space-y-6">
                        <div className="space-y-4">
                            <Label>IELTS / TOEFL Status</Label>
                            <div className="flex flex-wrap gap-2">
                                {["Not Started", "Preparing", "Scheduled", "Completed"].map((status) => {
                                    const val = status.toLowerCase().replace(" ", "_");
                                    return (
                                        <div
                                            key={status}
                                            onClick={() => updateField("exams_readiness", "ielts_toefl_status", val)}
                                            className={cn(
                                                "cursor-pointer rounded-full px-4 py-2 text-sm border transition-all",
                                                formData.exams_readiness.ielts_toefl_status === val
                                                    ? "border-green-500 bg-green-500/20 text-green-200"
                                                    : "border-white/10 bg-white/5 hover:bg-white/10"
                                            )}
                                        >
                                            {status}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        <div className="space-y-4">
                            <Label>GRE / GMAT Status</Label>
                            <div className="flex flex-wrap gap-2">
                                {["Not Started", "Preparing", "Completed", "Not Required"].map((status) => {
                                    const val = status.toLowerCase().replace(" ", "_");
                                    return (
                                        <div
                                            key={status}
                                            onClick={() => updateField("exams_readiness", "gre_gmat_status", val)}
                                            className={cn(
                                                "cursor-pointer rounded-full px-4 py-2 text-sm border transition-all",
                                                formData.exams_readiness.gre_gmat_status === val
                                                    ? "border-blue-500 bg-blue-500/20 text-blue-200"
                                                    : "border-white/10 bg-white/5 hover:bg-white/10"
                                            )}
                                        >
                                            {status}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        <div className="space-y-4">
                            <Label>Statement of Purpose (SOP)</Label>
                            <div className="flex flex-wrap gap-2">
                                {["Not Started", "Draft", "Ready"].map((status) => {
                                    const val = status.toLowerCase().replace(" ", "_");
                                    return (
                                        <div
                                            key={status}
                                            onClick={() => updateField("exams_readiness", "sop_status", val)}
                                            className={cn(
                                                "cursor-pointer rounded-full px-4 py-2 text-sm border transition-all",
                                                formData.exams_readiness.sop_status === val
                                                    ? "border-purple-500 bg-purple-500/20 text-purple-200"
                                                    : "border-white/10 bg-white/5 hover:bg-white/10"
                                            )}
                                        >
                                            {status}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    </div>
                );
        }
    };

    const CurrentIcon = STEPS[step - 1].icon;

    return (
        <div className="min-h-screen w-full flex items-center justify-center p-4 bg-background font-sans">

            {/* Background blobs similar to landing page */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
                <div className="absolute top-[-20%] left-[10%] w-[50vw] h-[50vw] bg-primary/5 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-20%] right-[10%] w-[40vw] h-[40vw] bg-secondary/5 rounded-full blur-[100px]" />
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-2xl"
            >
                <div className="mb-8 flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-foreground mb-2 font-heading">Build Your Profile</h1>
                        <p className="text-muted-foreground">Step {step} of 4: {STEPS[step - 1].title}</p>
                    </div>
                    <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center border border-primary/20">
                        <CurrentIcon className="h-6 w-6 text-primary" />
                    </div>
                </div>

                {/* Progress Bar */}
                <div className="h-2 w-full bg-white/5 rounded-full mb-8 overflow-hidden">
                    <motion.div
                        className="h-full bg-gradient-to-r from-primary to-secondary"
                        initial={{ width: 0 }}
                        animate={{ width: `${(step / STEPS.length) * 100}%` }}
                        transition={{ type: "spring", stiffness: 50 }}
                    />
                </div>

                <div className="relative rounded-2xl border border-white/10 bg-card/40 backdrop-blur-xl p-8 shadow-2xl glass-card">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={step}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ duration: 0.3 }}
                        >
                            {renderStepContent()}
                        </motion.div>
                    </AnimatePresence>

                    <div className="mt-10 flex justify-between pt-6 border-t border-white/5">
                        <Button
                            variant="ghost"
                            onClick={prevStep}
                            disabled={step === 1}
                            className={cn("text-muted-foreground hover:text-foreground hover:bg-white/5", step === 1 && "invisible")}
                        >
                            <ChevronLeft className="mr-2 h-4 w-4" /> Back
                        </Button>

                        <Button
                            onClick={nextStep}
                            disabled={isSubmitting}
                            className="bg-primary hover:bg-primary/90 text-primary-foreground min-w-[120px]"
                        >
                            {isSubmitting ? (
                                <Loader2 className="h-4 w-4 animate-spin" />
                            ) : step === STEPS.length ? (
                                "Complete"
                            ) : (
                                <>Next <ArrowRight className="ml-2 h-4 w-4" /></>
                            )}
                        </Button>
                    </div>
                </div>

                <p className="text-center text-xs text-muted-foreground mt-8">
                    Your data is used solely to generate personalized study abroad recommendations.
                </p>
            </motion.div>
        </div>
    );
}
