"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Menu, X, User, LogOut, Settings, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { createClient } from "@/lib/supabase/client";
import { Session } from "@supabase/supabase-js";

const navItems = [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Universities", href: "/universities" },
    { label: "Counsellor", href: "/counsellor" },
    { label: "Guidance", href: "/guidance" },
];

export function Navbar() {
    const pathname = usePathname();
    const router = useRouter();
    const [open, setOpen] = useState(false);
    const [session, setSession] = useState<Session | null>(null);
    const [userMenuOpen, setUserMenuOpen] = useState(false);

    useEffect(() => {
        const supabase = createClient();

        supabase.auth.getSession().then(({ data: { session } }) => {
            setSession(session);
        });

        const { data: { subscription } } = supabase.auth.onAuthStateChange(
            (_event, session) => {
                setSession(session);
            }
        );

        return () => subscription.unsubscribe();
    }, []);

    const handleSignOut = async () => {
        const supabase = createClient();
        await supabase.auth.signOut();
        router.push("/");
        router.refresh();
    };

    // Don't show navbar on auth pages
    if (pathname?.startsWith("/auth")) {
        return null;
    }

    const userName = session?.user?.user_metadata?.full_name || session?.user?.email?.split("@")[0] || "User";
    const userInitial = userName.charAt(0).toUpperCase();

    return (
        <motion.header
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ type: "spring", stiffness: 100 }}
            className="sticky top-0 z-50 w-full border-b border-white/10 bg-background/80 backdrop-blur-xl"
        >
            <nav className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
                <Link href="/" className="flex items-center gap-2 font-heading text-xl font-bold text-foreground hover:text-primary transition-colors">
                    <span className="bg-gradient-to-r from-primary to-amber-300 bg-clip-text text-transparent">SentinelAI</span>
                </Link>

                {/* Desktop Nav */}
                <div className="hidden md:flex items-center gap-6">
                    {session && navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "text-sm font-medium transition-colors hover:text-primary",
                                pathname === item.href ? "text-primary" : "text-muted-foreground"
                            )}
                        >
                            {item.label}
                        </Link>
                    ))}

                    {session ? (
                        <div className="relative">
                            <button
                                onClick={() => setUserMenuOpen(!userMenuOpen)}
                                className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-sm font-medium hover:bg-white/10 transition-colors"
                            >
                                <div className="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-bold">
                                    {userInitial}
                                </div>
                                <span className="hidden sm:inline max-w-[100px] truncate">{userName}</span>
                                <ChevronDown className={cn("h-4 w-4 transition-transform", userMenuOpen && "rotate-180")} />
                            </button>

                            {userMenuOpen && (
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className="absolute right-0 mt-2 w-48 rounded-xl border border-white/10 bg-card/95 backdrop-blur-xl shadow-xl overflow-hidden"
                                >
                                    <Link
                                        href="/profile"
                                        onClick={() => setUserMenuOpen(false)}
                                        className="flex items-center gap-2 px-4 py-3 text-sm hover:bg-white/5 transition-colors"
                                    >
                                        <User className="h-4 w-4" /> Profile
                                    </Link>
                                    <button
                                        onClick={handleSignOut}
                                        className="flex w-full items-center gap-2 px-4 py-3 text-sm text-red-400 hover:bg-red-500/10 transition-colors"
                                    >
                                        <LogOut className="h-4 w-4" /> Sign Out
                                    </button>
                                </motion.div>
                            )}
                        </div>
                    ) : (
                        <div className="flex items-center gap-2">
                            <Link href="/auth/login">
                                <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                                    Sign In
                                </Button>
                            </Link>
                            <Link href="/auth/signup">
                                <Button size="sm" className="bg-primary hover:bg-primary/90 text-primary-foreground">
                                    Get Started
                                </Button>
                            </Link>
                        </div>
                    )}
                </div>

                {/* Mobile Menu Toggle */}
                <button
                    className="md:hidden h-10 w-10 flex items-center justify-center rounded-lg hover:bg-white/10"
                    onClick={() => setOpen(!open)}
                >
                    {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
                </button>
            </nav>

            {/* Mobile Nav Panel */}
            {open && (
                <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    className="md:hidden border-t border-white/10 bg-background/95 backdrop-blur-xl"
                >
                    <div className="container px-4 py-4 space-y-2">
                        {session ? (
                            <>
                                {navItems.map((item) => (
                                    <Link
                                        key={item.href}
                                        href={item.href}
                                        onClick={() => setOpen(false)}
                                        className={cn(
                                            "block px-4 py-3 rounded-lg text-sm font-medium transition-colors",
                                            pathname === item.href ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-white/5"
                                        )}
                                    >
                                        {item.label}
                                    </Link>
                                ))}
                                <Link
                                    href="/profile"
                                    onClick={() => setOpen(false)}
                                    className="flex items-center gap-2 px-4 py-3 rounded-lg text-sm font-medium text-muted-foreground hover:bg-white/5"
                                >
                                    <Settings className="h-4 w-4" /> Profile
                                </Link>
                                <button
                                    onClick={() => { handleSignOut(); setOpen(false); }}
                                    className="flex w-full items-center gap-2 px-4 py-3 rounded-lg text-sm font-medium text-red-400 hover:bg-red-500/10"
                                >
                                    <LogOut className="h-4 w-4" /> Sign Out
                                </button>
                            </>
                        ) : (
                            <div className="space-y-2">
                                <Link
                                    href="/auth/login"
                                    onClick={() => setOpen(false)}
                                    className="block px-4 py-3 rounded-lg text-sm font-medium text-muted-foreground hover:bg-white/5"
                                >
                                    Sign In
                                </Link>
                                <Link
                                    href="/auth/signup"
                                    onClick={() => setOpen(false)}
                                    className="block px-4 py-3 rounded-lg text-sm font-medium bg-primary text-primary-foreground text-center"
                                >
                                    Get Started
                                </Link>
                            </div>
                        )}
                    </div>
                </motion.div>
            )}
        </motion.header>
    );
}
