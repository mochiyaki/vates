"use client"

import { useState } from "react"
import { ComicSidebar } from "@/components/comic-sidebar"
import { CircularGallery } from "@/components/circular-gallery"
import { NarrationPanel } from "@/components/narration-panel"
import { VoiceAgentPanel } from "@/components/voice-agent-panel"
import { DirectoryUpload } from "@/components/directory-upload"
import type { StoryData } from "@/types/story"

export default function StorytellerApp() {
  const [storyData, setStoryData] = useState<StoryData | null>(null)
  const [currentImageIndex, setCurrentImageIndex] = useState(0)

  const handleDirectoryUpload = (data: StoryData) => {
    setStoryData(data)
    setCurrentImageIndex(0)
  }

  const handlePanelClick = (index: number) => {
    setCurrentImageIndex(index)
  }

  if (!storyData) {
    return <DirectoryUpload onUpload={handleDirectoryUpload} />
  }

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Left Panel - Voice Agent & Narration */}
      <div className="flex w-[420px] flex-col border-r border-border bg-card">
        <VoiceAgentPanel
          onNarrationUpdate={(newNarration) => {
            const updatedImages = [...storyData.images]
            updatedImages[currentImageIndex].narration = newNarration
            setStoryData({ ...storyData, images: updatedImages })
          }}
        />
        <NarrationPanel narration={storyData.images[currentImageIndex].narration} />
      </div>

      {/* Center - Circular Gallery */}
      <div className="flex flex-1 flex-col">
        <CircularGallery
          images={storyData.images}
          currentIndex={currentImageIndex}
          onImageChange={setCurrentImageIndex}
        />
      </div>

      {/* Right Panel - Story Chapters */}
      <ComicSidebar panels={storyData.comicPanels} currentIndex={currentImageIndex} onPanelClick={handlePanelClick} />
    </div>
  )
}
