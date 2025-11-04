"use client"

import { MapPin, Calendar } from "lucide-react"

interface MainImageDisplayProps {
  image: string
  location: string
  date: string
}

export function MainImageDisplay({ image, location, date }: MainImageDisplayProps) {
  return (
    <div className="relative flex h-full w-full flex-col">
      {/* Header with Location and Date */}
      <div className="border-b border-border bg-card/50 px-8 py-6 backdrop-blur-sm">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <MapPin className="h-5 w-5 text-primary" />
            <span className="text-lg font-semibold text-foreground">{location}</span>
          </div>
          <div className="h-6 w-px bg-border" />
          <div className="flex items-center gap-2">
            <Calendar className="h-5 w-5 text-muted-foreground" />
            <span className="text-lg text-muted-foreground">{date}</span>
          </div>
        </div>
      </div>

      {/* Main Image */}
      <div className="relative flex-1 overflow-hidden bg-black">
        <img src={image || "/placeholder.svg"} alt={`${location} - ${date}`} className="h-full w-full object-contain" />

        {/* Subtle vignette effect */}
        <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/20" />
      </div>
    </div>
  )
}
