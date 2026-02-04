'use client'

import { motion } from 'framer-motion'
import { ReactNode, useEffect, useState } from 'react'

interface AnimatedButtonProps {
  children: ReactNode
  onClick?: () => void
  variant?: 'primary' | 'secondary'
  className?: string
  href?: string
}

export default function AnimatedButton({
  children,
  onClick,
  variant = 'primary',
  className = ''
}: AnimatedButtonProps) {
  // Check for reduced motion preference
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setPrefersReducedMotion(mediaQuery.matches)

    const handleChange = (e: MediaQueryListEvent) => {
      setPrefersReducedMotion(e.matches)
    }

    mediaQuery.addEventListener('change', handleChange)
    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [])

  const baseClasses = variant === 'primary'
    ? 'min-w-[44px] min-h-[44px] px-10 py-5 text-lg bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white rounded-xl font-bold shadow-2xl'
    : 'min-w-[44px] min-h-[44px] px-10 py-5 text-lg bg-white text-blue-600 border-2 border-blue-600 rounded-xl font-bold shadow-xl'

  return (
    <motion.button
      onClick={onClick}
      className={`${baseClasses} ${className}`}
      whileHover={prefersReducedMotion ? {} : {
        scale: 1.05,
        y: -2,
        boxShadow: variant === 'primary'
          ? '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
          : '0 20px 40px -12px rgba(0, 0, 0, 0.2)'
      }}
      whileTap={prefersReducedMotion ? {} : { scale: 0.98 }}
      initial={prefersReducedMotion ? {} : { opacity: 0, y: 20 }}
      animate={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
      transition={prefersReducedMotion ? { duration: 0 } : {
        type: "spring",
        stiffness: 300,
        damping: 20
      }}
    >
      <motion.span
        className="inline-block"
        whileHover={prefersReducedMotion ? {} : { x: variant === 'primary' ? 5 : 0 }}
      >
        {children}
      </motion.span>
    </motion.button>
  )
}

