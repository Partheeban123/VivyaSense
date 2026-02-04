import { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface TypographyProps {
  children: ReactNode
  className?: string
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'p' | 'span' | 'div'
}

// Display - Extra large hero text
export function Display({ children, className, as: Component = 'h1' }: TypographyProps) {
  return (
    <Component className={cn('text-6xl md:text-7xl lg:text-8xl font-black tracking-tight', className)}>
      {children}
    </Component>
  )
}

// H1 - Main page heading
export function H1({ children, className, as: Component = 'h1' }: TypographyProps) {
  return (
    <Component className={cn('text-5xl md:text-6xl font-extrabold tracking-tight', className)}>
      {children}
    </Component>
  )
}

// H2 - Section heading
export function H2({ children, className, as: Component = 'h2' }: TypographyProps) {
  return (
    <Component className={cn('text-4xl md:text-5xl font-bold tracking-tight', className)}>
      {children}
    </Component>
  )
}

// H3 - Subsection heading
export function H3({ children, className, as: Component = 'h3' }: TypographyProps) {
  return (
    <Component className={cn('text-3xl md:text-4xl font-bold tracking-tight', className)}>
      {children}
    </Component>
  )
}

// H4 - Card/Component heading
export function H4({ children, className, as: Component = 'h4' }: TypographyProps) {
  return (
    <Component className={cn('text-2xl md:text-3xl font-semibold', className)}>
      {children}
    </Component>
  )
}

// H5 - Small heading
export function H5({ children, className, as: Component = 'h5' }: TypographyProps) {
  return (
    <Component className={cn('text-xl md:text-2xl font-semibold', className)}>
      {children}
    </Component>
  )
}

// H6 - Smallest heading
export function H6({ children, className, as: Component = 'h6' }: TypographyProps) {
  return (
    <Component className={cn('text-lg md:text-xl font-semibold', className)}>
      {children}
    </Component>
  )
}

// Lead - Large body text for introductions
export function Lead({ children, className, as: Component = 'p' }: TypographyProps) {
  return (
    <Component className={cn('text-xl md:text-2xl text-gray-600 leading-relaxed', className)}>
      {children}
    </Component>
  )
}

// Body - Standard body text
export function Body({ children, className, as: Component = 'p' }: TypographyProps) {
  return (
    <Component className={cn('text-base md:text-lg text-gray-700 leading-relaxed', className)}>
      {children}
    </Component>
  )
}

// Small - Smaller text for captions, labels
export function Small({ children, className, as: Component = 'p' }: TypographyProps) {
  return (
    <Component className={cn('text-sm text-gray-600', className)}>
      {children}
    </Component>
  )
}

// Muted - De-emphasized text
export function Muted({ children, className, as: Component = 'p' }: TypographyProps) {
  return (
    <Component className={cn('text-sm text-gray-500', className)}>
      {children}
    </Component>
  )
}

// Label - Form labels and UI labels
export function Label({ children, className, as: Component = 'label' }: TypographyProps) {
  return (
    <Component className={cn('text-sm font-medium text-gray-700', className)}>
      {children}
    </Component>
  )
}

// Code - Inline code
export function Code({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <code className={cn('px-1.5 py-0.5 text-sm font-mono bg-gray-100 text-gray-900 rounded', className)}>
      {children}
    </code>
  )
}

// Blockquote
export function Blockquote({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <blockquote className={cn('pl-6 border-l-4 border-gray-300 italic text-gray-700', className)}>
      {children}
    </blockquote>
  )
}

