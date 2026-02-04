'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface AnimatedIconProps {
  children: ReactNode
  delay?: number
  type?: 'pulse' | 'bounce' | 'rotate' | 'scale' | 'float'
}

export default function AnimatedIcon({ children, delay = 0, type = 'pulse' }: AnimatedIconProps) {
  const animations = {
    pulse: {
      scale: [1, 1.1, 1],
      transition: {
        duration: 2,
        repeat: Infinity,
        delay,
        ease: "easeInOut"
      }
    },
    bounce: {
      y: [0, -10, 0],
      transition: {
        duration: 2,
        repeat: Infinity,
        delay,
        ease: "easeInOut"
      }
    },
    rotate: {
      rotate: [0, 360],
      transition: {
        duration: 20,
        repeat: Infinity,
        delay,
        ease: "linear"
      }
    },
    scale: {
      scale: [1, 1.2, 1],
      transition: {
        duration: 3,
        repeat: Infinity,
        delay,
        ease: "easeInOut"
      }
    },
    float: {
      y: [0, -15, 0],
      x: [0, 5, 0],
      transition: {
        duration: 4,
        repeat: Infinity,
        delay,
        ease: "easeInOut"
      }
    }
  }

  return (
    <motion.div
      animate={animations[type]}
      whileHover={{ scale: 1.15 }}
      className="inline-block"
    >
      {children}
    </motion.div>
  )
}

