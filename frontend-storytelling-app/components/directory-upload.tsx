"use client"

import { useState } from "react"
import { Upload, FolderOpen } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import type { StoryData } from "@/types/story"

interface DirectoryUploadProps {
  onUpload: (data: StoryData) => void
}

export function DirectoryUpload({ onUpload }: DirectoryUploadProps) {
  const [isProcessing, setIsProcessing] = useState(false)

  const handleFileSelect = async () => {
    setIsProcessing(true)

    // Simulate processing delay
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Mock data for demonstration
    const mockStoryData: StoryData = {
      images: [
        {
          url: "/mountain-landscape-sunset-adventure.jpg",
          location: "Rocky Mountains, Colorado",
          date: "July 15, 2024",
          narration:
            "The journey began at dawn, as golden light painted the peaks in hues of amber and rose. Each step forward revealed new vistas, each more breathtaking than the last. The crisp mountain air filled our lungs with possibility.",
        },
        {
          url: "/forest-trail-hiking-adventure.jpg",
          location: "Redwood National Park, California",
          date: "July 18, 2024",
          narration:
            "Among the ancient giants, time seemed to slow. These towering sentinels had witnessed centuries pass, and in their presence, our own stories felt both small and significant. The forest whispered secrets of resilience and growth.",
        },
        {
          url: "/coastal-sunset-ocean-waves.jpg",
          location: "Big Sur, California",
          date: "July 22, 2024",
          narration:
            "Where land meets sea, we found our rhythm. The waves crashed with ancient persistence, carving stories into the cliffs. As the sun dipped below the horizon, we understood that every ending is also a beginning.",
        },
        {
          url: "/desert-landscape-stars-night-sky.jpg",
          location: "Joshua Tree, California",
          date: "July 25, 2024",
          narration:
            "Under a canopy of stars, the desert revealed its magic. The silence was profound, broken only by the whisper of wind through twisted branches. In this vast emptiness, we found ourselves completely full.",
        },
      ],
      comicPanels: [
        {
          thumbnail: "/mountain-landscape-comic-panel.jpg",
          title: "Chapter 1",
          subtitle: "The Ascent",
        },
        {
          thumbnail: "/forest-trail-comic-panel.jpg",
          title: "Chapter 2",
          subtitle: "Ancient Woods",
        },
        {
          thumbnail: "/coastal-sunset-comic-panel.jpg",
          title: "Chapter 3",
          subtitle: "Ocean's Edge",
        },
        {
          thumbnail: "/desert-stars-comic-panel.jpg",
          title: "Chapter 4",
          subtitle: "Desert Dreams",
        },
      ],
    }

    onUpload(mockStoryData)
    setIsProcessing(false)
  }

  return (
    <div className="flex h-screen w-full items-center justify-center bg-background p-8">
      <Card className="w-full max-w-2xl border-2 border-primary/20 bg-card p-12">
        <div className="flex flex-col items-center gap-8 text-center">
          <div className="rounded-full bg-primary/10 p-6">
            <FolderOpen className="h-16 w-16 text-primary" />
          </div>

          <div className="space-y-3">
            <h1 className="text-balance text-4xl font-bold tracking-tight text-foreground">Transform Your Memories</h1>
            <p className="text-pretty text-lg leading-relaxed text-muted-foreground">
              Upload a directory filled with your images and documents. Our AI will craft a compelling narrative,
              bringing your adventures to life through interactive storytelling.
            </p>
          </div>

          <div className="flex flex-col gap-4">
            <Button size="lg" onClick={handleFileSelect} disabled={isProcessing} className="gap-2 px-8 text-lg">
              {isProcessing ? (
                <>
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
                  Processing Your Story...
                </>
              ) : (
                <>
                  <Upload className="h-5 w-5" />
                  Select Directory
                </>
              )}
            </Button>

            <p className="text-sm text-muted-foreground">Supports images, PDFs, and text documents</p>
          </div>
        </div>
      </Card>
    </div>
  )
}
