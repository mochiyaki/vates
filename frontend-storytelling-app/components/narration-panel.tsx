"use client"

import { BookOpen, Sparkles } from "lucide-react"

interface NarrationPanelProps {
  narration: string
}

export function NarrationPanel({ narration }: NarrationPanelProps) {
  return (
    <div className="flex-1 overflow-y-auto border-t border-border bg-gradient-to-b from-card to-card/95 p-6">
      <div className="space-y-4">
        <div className="flex items-center gap-3 pb-4">
          <div className="rounded-lg bg-primary/10 p-2.5 ring-1 ring-primary/20">
            <BookOpen className="h-5 w-5 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="flex items-center gap-2 font-bold text-card-foreground">
              Story Narration
              <Sparkles className="h-4 w-4 text-accent" />
            </h3>
            <p className="text-xs text-muted-foreground">Your adventure comes alive</p>
          </div>
        </div>

        <div className="relative rounded-lg border border-border/50 bg-sidebar/30 p-6 shadow-inner">
          {/* Decorative quote marks */}
          <div className="absolute left-3 top-3 text-4xl font-serif text-primary/20">"</div>
          <div className="absolute bottom-3 right-3 text-4xl font-serif text-primary/20">"</div>

          <div className="relative space-y-4">
            <p className="text-pretty font-serif text-base leading-relaxed text-card-foreground/90">{narration}</p>
          </div>

          {/* Subtle page texture overlay */}
          <div className="pointer-events-none absolute inset-0 rounded-lg bg-gradient-to-br from-transparent via-primary/5 to-transparent opacity-50" />
        </div>

        {/* Story progress indicator */}
        <div className="flex items-center justify-center gap-2 pt-2">
          <div className="h-1 w-1 rounded-full bg-primary/40" />
          <div className="h-1 w-1 rounded-full bg-primary/60" />
          <div className="h-1 w-1 rounded-full bg-primary" />
        </div>
      </div>
    </div>
  )
}
