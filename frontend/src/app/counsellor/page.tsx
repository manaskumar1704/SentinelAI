"use client";

import { useState, useRef, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Sparkles, User, Bot, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

type Message = {
    id: string;
    role: "user" | "assistant";
    content: string;
};

export default function CounsellorPage() {
    const { getToken } = useAuth();
    const [messages, setMessages] = useState<Message[]>([
        {
            id: "welcome",
            role: "assistant",
            content: "Hello! I'm your AI Study Abroad Counsellor. I've analyzed your profile. How can I help you today?"
        }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: "user",
            content: input
        };

        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const token = await getToken();

            // We'll use the non-streaming endpoint for simplicity in this version, 
            // or implement basic streaming handling if preferred. 
            // Let's implement full streaming for a premium feel.

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/counsellor/stream`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    messages: [...messages, userMessage].map(m => ({ role: m.role, content: m.content }))
                })
            });

            if (!response.ok) throw new Error("Failed to send message");

            const reader = response.body?.getReader();
            if (!reader) throw new Error("No reader");

            const decoder = new TextDecoder();
            let aiResponse = "";
            const aiMessageId = (Date.now() + 1).toString();

            // Add placeholder message
            setMessages(prev => [...prev, { id: aiMessageId, role: "assistant", content: "" }]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split("\n\n");

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        const data = line.slice(6);
                        if (data === "[DONE]") break;

                        aiResponse += data;

                        // Update last message
                        setMessages(prev => {
                            const newMessages = [...prev];
                            const lastMsg = newMessages[newMessages.length - 1];
                            if (lastMsg.id === aiMessageId) {
                                lastMsg.content = aiResponse;
                            }
                            return newMessages;
                        });
                    }
                }
            }

        } catch (error) {
            console.error(error);
            // Remove the failed placeholder if it exists and is empty, or add error message
        } finally {
            setLoading(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col h-[calc(100dvh-64px)] bg-background"
        >
            <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
                <div className="mx-auto max-w-3xl space-y-6">
                    <AnimatePresence initial={false}>
                        {messages.map((message) => (
                            <motion.div
                                key={message.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={cn(
                                    "flex items-start gap-4",
                                    message.role === "user" ? "flex-row-reverse" : "flex-row"
                                )}
                            >
                                <div className={cn(
                                    "flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full border shadow",
                                    message.role === "user"
                                        ? "bg-primary border-primary text-primary-foreground"
                                        : "bg-white/10 border-white/20 text-primary"
                                )}>
                                    {message.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                                </div>

                                <div className={cn(
                                    "group relative flex-1 space-y-2 overflow-hidden px-4 py-3 shadow-sm",
                                    message.role === "user"
                                        ? "rounded-2xl rounded-tr-none bg-primary text-primary-foreground"
                                        : "rounded-2xl rounded-tl-none border border-white/10 bg-white/5"
                                )}>
                                    <div className="prose prose-invert prose-p:leading-relaxed prose-pre:p-0 break-words text-sm md:text-base">
                                        {message.content || <span className="animate-pulse">...</span>}
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    <div ref={messagesEndRef} />
                </div>
            </div>

            <div className="border-t border-white/10 bg-background p-4 md:p-6">
                <div className="mx-auto max-w-3xl">
                    <form onSubmit={handleSubmit} className="relative flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 p-2 shadow-inner focus-within:ring-1 focus-within:ring-primary">
                        <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="text-muted-foreground hover:text-primary"
                        >
                            <Sparkles className="h-5 w-5" />
                        </Button>
                        <Input
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask about universities, budget, or application tips..."
                            className="border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 px-2"
                        />
                        <Button
                            type="submit"
                            size="icon"
                            disabled={loading || !input.trim()}
                            className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg"
                        >
                            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                        </Button>
                    </form>
                    <p className="mt-2 text-center text-xs text-muted-foreground">
                        AI can make mistakes. Verify important information.
                    </p>
                </div>
            </div>
        </motion.div>
    );
}

