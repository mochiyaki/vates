export interface ImageData {
  url: string
  location: string
  date: string
  narration: string
}

export interface ComicPanel {
  thumbnail: string
  title: string
  subtitle: string
}

export interface StoryData {
  images: ImageData[]
  comicPanels: ComicPanel[]
}
