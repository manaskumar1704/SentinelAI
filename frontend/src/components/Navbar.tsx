"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Sparkles, LayoutDashboard, MessageSquare, Map, GraduationCap, FileText, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { UserButton } from "@clerk/nextjs";

export function Navbar() {
    const pathname = usePathname();

    const navItems = [
        { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
        { href: "/counsellor", label: "AI Counsellor", icon: Sparkles },
        { href: "/universities", label: "Universities", icon: GraduationCap },
        { href: "/guidance", label: "Guidance", icon: Map },
    ];

    if (pathname === "/" || pathname.includes("/onboarding")) return null;

    return (
        <motion.nav
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="sticky top-0 z-50 w-full border-b border-white/10 bg-white/5 backdrop-blur-xl supports-[backdrop-filter]:bg-white/5"
        >
            <div className="container flex h-16 items-center px-4 md:px-6">
                <Link href="/dashboard" className="mr-8 flex items-center space-x-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600">
                        <Sparkles className="h-4 w-4 text-white" />
                    </div>
                    <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
                        SentinelAI
                    </span>
                </Link>

                <div className="flex items-center space-x-1 md:space-x-4 flex-1">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "group flex items-center rounded-full px-4 py-2 text-sm font-medium transition-all duration-300",
                                    isActive
                                        ? "bg-indigo-500/10 text-indigo-500 shadow-[0_0_20px_rgba(99,102,241,0.2)]"
                                        : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
                                )}
                            >
                                <item.icon className={cn("mr-2 h-4 w-4 transition-transform group-hover:scale-110", isActive && "text-indigo-500")} />
                                <span className="hidden sm:inline-block">{item.label}</span>
                            </Link>
                        );
                    })}
                </div>

                <div className="ml-auto flex items-center space-x-4">
                    <Link
                        href="/profile"
                        className={cn(
                            "p-2 rounded-full transition-colors hover:bg-white/10",
                            pathname === "/profile" ? "text-indigo-500" : "text-muted-foreground"
                        )}
                    >
                        <User className="h-5 w-5" />
                    </Link>
                    <div className="h-8 w-px bg-white/10" />
                    <UserButton
                        afterSignOutUrl="/"
                        appearance={{
                            elements: {
                                avatarBox: "h-9 w-9 ring-2 ring-indigo-500/20 hover:ring-indigo-500/50 transition-all"
                            }
                        }}
                    />
                </div>
            </div>
        </motion.nav>
    );
}
