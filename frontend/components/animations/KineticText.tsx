'use client'

import { motion } from 'framer-motion'

interface KineticTextProps {
  text: string
  className?: string
  delay?: number
  type?: 'word' | 'letter' | 'line'
}

export default function KineticText({ 
  text, 
  className = '',
  delay = 0,
  type = 'word'
}: KineticTextProps) {
  
  const container = {
    hidden: { opacity: 0 },
    visible: (i = 1) => ({
      opacity: 1,
      transition: { 
        staggerChildren: type === 'letter' ? 0.03 : 0.12, 
        delayChildren: delay 
      },
    }),
  }

  const child = {
    hidden: {
      opacity: 0,
      y: 20,
    },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        damping: 12,
        stiffness: 100,
      },
    },
  }

  if (type === 'letter') {
    const letters = text.split('')
    return (
      <motion.div
        className={className}
        variants={container}
        initial="hidden"
        animate="visible"
      >
        {letters.map((letter, index) => (
          <motion.span
            key={index}
            variants={child}
            style={{ display: 'inline-block', whiteSpace: letter === ' ' ? 'pre' : 'normal' }}
          >
            {letter === ' ' ? '\u00A0' : letter}
          </motion.span>
        ))}
      </motion.div>
    )
  }

  // Word animation
  const words = text.split(' ')
  return (
    <motion.div
      className={className}
      variants={container}
      initial="hidden"
      animate="visible"
    >
      {words.map((word, index) => (
        <motion.span
          key={index}
          variants={child}
          style={{ display: 'inline-block', marginRight: '0.25em' }}
        >
          {word}
        </motion.span>
      ))}
    </motion.div>
  )
}

