"use client"

import { cn } from "@/lib/utils"
import type { ComicPanel } from "@/types/story"
import { BookOpen, Sparkles } from "lucide-react"

interface ComicSidebarProps {
  panels: ComicPanel[]
  currentIndex: number
  onPanelClick: (index: number) => void
}

const comicColors = [
  "bg-[oklch(0.68_0.26_280)]", // Purple
  "bg-[oklch(0.72_0.22_45)]", // Orange
  "bg-[oklch(0.75_0.24_330)]", // Pink
  "bg-[oklch(0.7_0.22_200)]", // Cyan
  "bg-[oklch(0.85_0.18_85)]", // Yellow
]

export function ComicSidebar({ panels, currentIndex, onPanelClick }: ComicSidebarProps) {
  return (
    <div className="flex w-[320px] flex-col border-l-4 border-primary bg-sidebar shadow-2xl">
      <div className="relative overflow-hidden border-b-4 border-primary bg-gradient-to-br from-primary via-accent to-secondary p-6">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.1),transparent)]" />
        <div className="relative flex items-center gap-3">
          <div className="rounded-full bg-white/20 p-2 backdrop-blur-sm">
            <BookOpen className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-balance text-2xl font-black tracking-tight text-white">Story Chapters</h2>
            <p className="flex items-center gap-1 text-sm font-bold text-white/90">
              <Sparkles className="h-3 w-3" />
              AI Generated Comic Strip
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto bg-gradient-to-b from-sidebar to-sidebar-accent p-4">
        <div className="space-y-6">
          {panels.map((panel, index) => {
            const colorClass = comicColors[index % comicColors.length]
            const isActive = currentIndex === index

            return (
              <button
                key={index}
                onClick={() => onPanelClick(index)}
                className={cn(
                  "group relative w-full overflow-visible transition-all duration-300",
                  isActive && "animate-comic-pop",
                )}
              >
                {/* Comic Panel Frame */}
                <div
                  className={cn(
                    "relative overflow-hidden rounded-xl border-4 transition-all duration-300",
                    isActive
                      ? "comic-shadow scale-105 border-white shadow-2xl"
                      : "border-border hover:scale-102 hover:border-primary/50",
                  )}
                >
                  {/* Panel Image */}
                  <div className="aspect-[3/4] w-full overflow-hidden bg-sidebar-accent">
                    <img
                      src={panel.thumbnail || "/placeholder.svg"}
                      alt={panel.title}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
                    />
                    {/* Comic Book Halftone Overlay */}
                    <div className="absolute inset-0 bg-[radial-gradient(circle,transparent_1px,rgba(0,0,0,0.05)_1px)] bg-[length:4px_4px] mix-blend-multiply" />
                  </div>

                  {/* Speech Bubble with Narration Excerpt */}
                  <div
                    className={cn(
                      "absolute left-3 top-3 max-w-[70%] rounded-2xl border-3 border-black bg-white px-4 py-2 shadow-lg transition-all duration-300",
                      isActive && "animate-speech-bubble",
                    )}
                  >
                    <div className="relative">
                      <p className="text-pretty text-xs font-bold leading-tight text-black">{panel.title}</p>
                      {/* Speech bubble tail */}
                      <div className="absolute -bottom-3 left-4 h-0 w-0 border-l-[8px] border-r-[8px] border-t-[12px] border-l-transparent border-r-transparent border-t-white" />
                      <div className="absolute -bottom-4 left-4 h-0 w-0 border-l-[9px] border-r-[9px] border-t-[13px] border-l-transparent border-r-transparent border-t-black" />
                    </div>
                  </div>

                  {/* Chapter Number Badge */}
                  <div
                    className={cn(
                      "absolute right-3 top-3 flex h-12 w-12 items-center justify-center rounded-full border-3 border-black font-black text-white shadow-lg transition-all duration-300",
                      colorClass,
                      isActive && "scale-110",
                    )}
                  >
                    <span className="text-lg">{index + 1}</span>
                  </div>

                  {/* Bottom Caption Bar */}
                  <div
                    className={cn(
                      "absolute inset-x-0 bottom-0 border-t-3 border-black px-3 py-2 transition-all duration-300",
                      colorClass,
                      isActive && "py-3",
                    )}
                  >
                    <p className="text-pretty text-sm font-black uppercase leading-tight tracking-wide text-white">
                      {panel.subtitle}
                    </p>
                  </div>
                </div>

                {/* Active Indicator - Comic Book Style "POW!" */}
                {isActive && (
                  <div className="absolute -right-4 -top-4 z-10 animate-pulse-glow">
                    <div className="relative flex h-16 w-16 items-center justify-center">
                      {/* Star burst background */}
                      <div className="absolute inset-0 rotate-0 bg-[oklch(0.85_0.18_85)] [clip-path:polygon(50%_0%,61%_35%,98%_35%,68%_57%,79%_91%,50%_70%,21%_91%,32%_57%,2%_35%,39%_35%)]" />
                      <div className="absolute inset-0 rotate-45 bg-[oklch(0.85_0.18_85)] [clip-path:polygon(50%_0%,61%_35%,98%_35%,68%_57%,79%_91%,50%_70%,21%_91%,32%_57%,2%_35%,39%_35%)]" />
                      <span className="relative z-10 rotate-12 text-xs font-black text-black">NOW!</span>
                    </div>
                  </div>
                )}
              </button>
            )
          })}
        </div>
      </div>

      {/* Comic Book Footer */}
      <div className="border-t-4 border-primary bg-gradient-to-r from-primary via-accent to-secondary p-4">
        <p className="text-center text-xs font-bold text-white">
          Scroll through your adventure • {panels.length} chapters
        </p>
      </div>
    </div>
  )
}
