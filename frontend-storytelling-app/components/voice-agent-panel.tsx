"use client"

import { useState } from "react"
import { Mic, MicOff, Sparkles, Wand2 } from "lucide-react"
import { Button } from "@/components/ui/button"
// import { useNavigate } from "react-router-dom";

interface VoiceAgentPanelProps {
  onNarrationUpdate: (narration: string) => void
}

export function VoiceAgentPanel({ onNarrationUpdate }: VoiceAgentPanelProps) {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState("")

  // const navigate = useNavigate();

  const toggleListening = () => {
    setIsListening(!isListening)

    if (!isListening) {
      // Simulate voice input
      setTimeout(() => {
        const mockTranscript = "Make the story more dramatic and add details about the weather"
        setTranscript(mockTranscript)
        setIsListening(false)
      }, 2000)
    }
  }

  const enhanceNarration = () => {
    // Simulate AI enhancement
    const enhancedNarration =
      "The journey began at dawn, as golden light painted the peaks in hues of amber and rose. A fierce wind howled through the valleys, carrying with it the promise of adventure. Each step forward revealed new vistas, each more breathtaking than the last. The crisp mountain air filled our lungs with possibility, while storm clouds gathered on the distant horizon."
    onNarrationUpdate(enhancedNarration)
    setTranscript("")
  }

  return (
    <div className="border-b border-border bg-gradient-to-br from-card via-card to-primary/5 p-6">
      <div className="space-y-5">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-primary/10 p-2.5 ring-1 ring-primary/20">
            <Wand2 className="h-5 w-5 text-primary" />
          </div>
          <div className="flex-1">
            <h3 className="flex items-center gap-2 font-bold text-card-foreground">
              Voice Story Agent
              <Sparkles className="h-4 w-4 text-accent" />
            </h3>
            <p className="text-xs text-muted-foreground">Shape your narrative with your voice</p>
          </div>
        </div>

        <div className="space-y-3">
          <Button
            size="lg"
            variant={isListening ? "destructive" : "default"}
            onClick={toggleListening}
            className="w-full gap-2 shadow-lg transition-all hover:scale-[1.02]"
          >
            {isListening ? (
              <>
                <MicOff className="h-5 w-5 animate-pulse" />
                Stop Listening
              </>
            ) : (
              <>
                <Mic className="h-5 w-5" />
                Speak to Enhance Story
              </>
            )}
          </Button>

          {isListening && (
            <div className="flex items-center justify-center gap-2 rounded-lg border border-primary/30 bg-primary/10 p-4 shadow-inner">
              <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-primary shadow-lg shadow-primary/50" />
              <div
                className="h-2.5 w-2.5 animate-pulse rounded-full bg-primary shadow-lg shadow-primary/50"
                style={{ animationDelay: "0.2s" }}
              />
              <div
                className="h-2.5 w-2.5 animate-pulse rounded-full bg-primary shadow-lg shadow-primary/50"
                style={{ animationDelay: "0.4s" }}
              />
              <span className="ml-2 text-sm font-medium text-primary">Listening to your voice...</span>
            </div>
          )}

          {transcript && (
            <div className="space-y-3 rounded-lg border border-primary/20 bg-gradient-to-br from-muted/50 to-primary/5 p-4 shadow-md">
              <div className="flex items-center gap-2">
                <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Your Request</p>
              </div>
              <p className="text-pretty text-sm leading-relaxed text-card-foreground">"{transcript}"</p>
              <Button
                size="sm"
                onClick={enhanceNarration}
                className="w-full gap-2 shadow-md transition-all hover:scale-[1.02]"
              >
                <Sparkles className="h-4 w-4" />
                Transform Story
              </Button>
            </div>
          )}
        </div>

        {!isListening && !transcript && (
          <div className="rounded-lg border border-dashed border-border/50 bg-muted/20 p-4">
            <p className="text-center text-xs leading-relaxed text-muted-foreground">
              Click the button above to add drama, emotion, or details to your story using your voice
            </p>
          </div>
        )}
      </div>

          <Button
            size="lg"
            onClick={toggleListening}
            className="w-full gap-2 shadow-lg transition-all bg-gray-400"
          > Story Generator - Plus! </Button>

    </div>
  )
}
