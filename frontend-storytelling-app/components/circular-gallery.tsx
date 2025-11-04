"use client"

import { useState } from "react"
import { ChevronLeft, ChevronRight, MapPin, Calendar } from "lucide-react"
import { cn } from "@/lib/utils"
import type { StoryImage } from "@/types/story"

interface CircularGalleryProps {
  images: StoryImage[]
  currentIndex: number
  onImageChange: (index: number) => void
}

export function CircularGallery({ images, currentIndex, onImageChange }: CircularGalleryProps) {
  const [isTransitioning, setIsTransitioning] = useState(false)

  const handlePrevious = () => {
    if (isTransitioning) return
    setIsTransitioning(true)
    onImageChange(currentIndex === 0 ? images.length - 1 : currentIndex - 1)
    setTimeout(() => setIsTransitioning(false), 500)
  }

  const handleNext = () => {
    if (isTransitioning) return
    setIsTransitioning(true)
    onImageChange(currentIndex === images.length - 1 ? 0 : currentIndex + 1)
    setTimeout(() => setIsTransitioning(false), 500)
  }

  const currentImage = images[currentIndex]
  const prevIndex = currentIndex === 0 ? images.length - 1 : currentIndex - 1
  const nextIndex = currentIndex === images.length - 1 ? 0 : currentIndex + 1

  return (
    <div className="relative flex h-full w-full flex-col bg-gradient-to-br from-background via-background to-background/95">
      {/* Story Header */}
      <div className="border-b border-border bg-card/80 px-8 py-6 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <MapPin className="h-5 w-5 text-primary" />
              <span className="text-balance text-xl font-bold text-foreground">{currentImage.location}</span>
            </div>
            <div className="h-6 w-px bg-border" />
            <div className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-muted-foreground" />
              <span className="text-lg text-muted-foreground">{currentImage.date}</span>
            </div>
          </div>
          <div className="text-sm text-muted-foreground">
            Chapter {currentIndex + 1} of {images.length}
          </div>
        </div>
      </div>

      {/* Circular Gallery Container */}
      <div className="relative flex flex-1 items-center justify-center overflow-hidden p-12">
        {/* Background ambient glow */}
        <div className="absolute inset-0 bg-gradient-radial from-primary/5 via-transparent to-transparent" />

        {/* Previous Image (Left) */}
        <div
          className={cn(
            "absolute left-[5%] top-1/2 z-10 -translate-y-1/2 cursor-pointer transition-all duration-500",
            "h-[280px] w-[200px] opacity-40 hover:opacity-60",
          )}
          onClick={handlePrevious}
        >
          <div className="relative h-full w-full overflow-hidden rounded-xl border-2 border-border/50 shadow-2xl">
            <img
              src={images[prevIndex].url || "/placeholder.svg"}
              alt={images[prevIndex].location}
              className="h-full w-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          </div>
        </div>

        {/* Current Image (Center) */}
        <div
          className={cn(
            "relative z-20 transition-all duration-500",
            "h-[500px] w-[700px]",
            isTransitioning && "scale-95 opacity-80",
          )}
        >
          <div className="relative h-full w-full overflow-hidden rounded-2xl border-4 border-primary/30 shadow-2xl shadow-primary/20">
            <img
              src={currentImage.url || "/placeholder.svg"}
              alt={currentImage.location}
              className="h-full w-full object-cover"
            />
            {/* Story overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
            <div className="absolute inset-x-0 bottom-0 p-8">
              <h3 className="text-balance text-3xl font-bold text-white drop-shadow-lg">{currentImage.location}</h3>
              <p className="mt-2 text-pretty text-sm leading-relaxed text-white/90 drop-shadow-md">
                {currentImage.narration.split(" ").slice(0, 20).join(" ")}...
              </p>
            </div>
          </div>

          {/* Decorative corner accents */}
          <div className="absolute -left-2 -top-2 h-8 w-8 border-l-4 border-t-4 border-primary" />
          <div className="absolute -right-2 -top-2 h-8 w-8 border-r-4 border-t-4 border-primary" />
          <div className="absolute -bottom-2 -left-2 h-8 w-8 border-b-4 border-l-4 border-primary" />
          <div className="absolute -bottom-2 -right-2 h-8 w-8 border-b-4 border-r-4 border-primary" />
        </div>

        {/* Next Image (Right) */}
        <div
          className={cn(
            "absolute right-[5%] top-1/2 z-10 -translate-y-1/2 cursor-pointer transition-all duration-500",
            "h-[280px] w-[200px] opacity-40 hover:opacity-60",
          )}
          onClick={handleNext}
        >
          <div className="relative h-full w-full overflow-hidden rounded-xl border-2 border-border/50 shadow-2xl">
            <img
              src={images[nextIndex].url || "/placeholder.svg"}
              alt={images[nextIndex].location}
              className="h-full w-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          </div>
        </div>

        {/* Navigation Buttons */}
        <button
          onClick={handlePrevious}
          disabled={isTransitioning}
          className="absolute left-8 top-1/2 z-30 -translate-y-1/2 rounded-full border-2 border-primary/50 bg-card/90 p-4 text-primary backdrop-blur-sm transition-all hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-50"
        >
          <ChevronLeft className="h-8 w-8" />
        </button>
        <button
          onClick={handleNext}
          disabled={isTransitioning}
          className="absolute right-8 top-1/2 z-30 -translate-y-1/2 rounded-full border-2 border-primary/50 bg-card/90 p-4 text-primary backdrop-blur-sm transition-all hover:border-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-50"
        >
          <ChevronRight className="h-8 w-8" />
        </button>

        {/* Progress Dots */}
        <div className="absolute bottom-8 left-1/2 z-30 flex -translate-x-1/2 gap-2">
          {images.map((_, index) => (
            <button
              key={index}
              onClick={() => {
                if (!isTransitioning) {
                  setIsTransitioning(true)
                  onImageChange(index)
                  setTimeout(() => setIsTransitioning(false), 500)
                }
              }}
              className={cn(
                "h-2 rounded-full transition-all duration-300",
                index === currentIndex ? "w-8 bg-primary" : "w-2 bg-muted-foreground/40 hover:bg-muted-foreground/60",
              )}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
