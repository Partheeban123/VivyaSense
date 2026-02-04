'use client'

import { motion } from 'framer-motion'
import { ReactNode } from 'react'

interface MicroInteractionProps {
  children: ReactNode
  type?: 'card' | 'button' | 'icon' | 'image'
  className?: string
}

export default function MicroInteraction({ 
  children, 
  type = 'card',
  className = ''
}: MicroInteractionProps) {
  
  const interactions = {
    card: {
      whileHover: { 
        y: -8,
        scale: 1.02,
        boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
        transition: { type: "spring", stiffness: 300, damping: 20 }
      },
      whileTap: { scale: 0.98 }
    },
    button: {
      whileHover: { 
        scale: 1.05,
        transition: { type: "spring", stiffness: 400, damping: 10 }
      },
      whileTap: { scale: 0.95 }
    },
    icon: {
      whileHover: { 
        rotate: [0, -10, 10, -10, 0],
        scale: 1.2,
        transition: { duration: 0.5 }
      },
      whileTap: { scale: 0.9 }
    },
    image: {
      whileHover: { 
        scale: 1.1,
        transition: { duration: 0.3 }
      }
    }
  }

  return (
    <motion.div
      className={className}
      {...interactions[type]}
    >
      {children}
    </motion.div>
  )
}

