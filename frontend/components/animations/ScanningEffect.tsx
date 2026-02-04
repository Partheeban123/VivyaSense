'use client'

import { motion } from 'framer-motion'

export default function ScanningEffect() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {/* Scanning line effect */}
      <motion.div
        className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50"
        animate={{
          y: [0, 400, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      
      {/* Corner brackets */}
      <motion.div
        className="absolute top-4 left-4 w-12 h-12 border-t-2 border-l-2 border-blue-500"
        initial={{ opacity: 0 }}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
      <motion.div
        className="absolute top-4 right-4 w-12 h-12 border-t-2 border-r-2 border-blue-500"
        initial={{ opacity: 0 }}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
      />
      <motion.div
        className="absolute bottom-4 left-4 w-12 h-12 border-b-2 border-l-2 border-blue-500"
        initial={{ opacity: 0 }}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 2, repeat: Infinity, delay: 1 }}
      />
      <motion.div
        className="absolute bottom-4 right-4 w-12 h-12 border-b-2 border-r-2 border-blue-500"
        initial={{ opacity: 0 }}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 2, repeat: Infinity, delay: 1.5 }}
      />
      
      {/* Radar pulse */}
      <motion.div
        className="absolute top-1/2 left-1/2 w-32 h-32 -translate-x-1/2 -translate-y-1/2"
        initial={{ scale: 0, opacity: 0.8 }}
        animate={{ 
          scale: [0, 2, 0],
          opacity: [0.8, 0, 0]
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeOut"
        }}
      >
        <div className="w-full h-full rounded-full border-2 border-purple-500" />
      </motion.div>
    </div>
  )
}

