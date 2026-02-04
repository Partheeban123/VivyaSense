'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { FaShieldAlt, FaVideo, FaBrain, FaChartLine, FaHardHat, FaFire, FaUserInjured, FaBell, FaLock } from 'react-icons/fa'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import AnimatedIcon from '@/components/animations/AnimatedIcon'
import AnimatedButton from '@/components/animations/AnimatedButton'
import ScanningEffect from '@/components/animations/ScanningEffect'
import ParticleBackground from '@/components/animations/ParticleBackground'
import ScrollReveal from '@/components/animations/ScrollReveal'
import KineticText from '@/components/animations/KineticText'
import MicroInteraction from '@/components/animations/MicroInteraction'
import ParallaxScroll from '@/components/animations/ParallaxScroll'
import CounterAnimation from '@/components/animations/CounterAnimation'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100">
      {/* Skip to main content link for keyboard navigation */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:px-6 focus:py-3 focus:bg-blue-600 focus:text-white focus:rounded-lg focus:font-semibold focus:shadow-lg"
      >
        Skip to main content
      </a>

      <Navbar />

      {/* Hero Section */}
      <section
        id="main-content"
        className="pt-40 pb-32 px-4 relative overflow-hidden"
        aria-labelledby="hero-heading"
      >
        {/* Background decorative elements - hidden from screen readers */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
          <div className="absolute top-20 left-10 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-blob"></div>
          <div className="absolute top-40 right-10 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-blob animation-delay-2000"></div>
          <div className="absolute -bottom-8 left-1/2 w-96 h-96 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-blob animation-delay-4000"></div>
        </div>

        {/* Particle Background - decorative only */}
        <div aria-hidden="true">
          <ParticleBackground />
        </div>

        {/* Scanning Effect - decorative only */}
        <div className="max-w-4xl mx-auto relative" aria-hidden="true">
          <ScanningEffect />
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 id="hero-heading" className="sr-only">
              See Everything. Protect Everyone. AI-Powered Vision Platform
            </h1>
            <KineticText
              text="See Everything."
              className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black text-gray-900 mb-4 tracking-tight"
              type="word"
              aria-hidden="true"
            />
            <KineticText
              text="Protect Everyone."
              className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-8 tracking-tight"
              type="word"
              delay={0.3}
              aria-hidden="true"
            />

            <motion.p
              className="text-lg sm:text-xl md:text-2xl text-gray-700 mb-12 max-w-4xl mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              Transform your security cameras into intelligent guardians that never sleep, never miss a detail,
              and alert you the moment something matters
            </motion.p>

            <motion.div
              className="flex flex-col sm:flex-row gap-6 justify-center items-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <Link href="/detection" aria-label="Try our AI detection demo with live video analysis">
                <AnimatedButton variant="primary">
                  Experience the Demo →
                </AnimatedButton>
              </Link>
              <Link href="/dashboard" aria-label="View analytics dashboard with real-time insights">
                <AnimatedButton variant="secondary">
                  Explore Analytics
                </AnimatedButton>
              </Link>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section
        className="py-32 px-4 bg-white/90 backdrop-blur-sm"
        aria-labelledby="features-heading"
      >
        <div className="max-w-7xl mx-auto">
          <ScrollReveal direction="up" className="text-center mb-20">
            <h2 id="features-heading" className="sr-only">
              Why Businesses Trust Our Platform
            </h2>
            <KineticText
              text="Why Businesses Trust Our Platform"
              className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-6 tracking-tight"
              type="word"
              aria-hidden="true"
            />
            <motion.p
              className="text-lg sm:text-xl md:text-2xl text-gray-700 max-w-3xl mx-auto leading-relaxed"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              From construction sites to warehouses, from factories to offices—we keep your people safe and your operations running smoothly
            </motion.p>
          </ScrollReveal>

          <div className="grid md:grid-cols-3 gap-10">
            {[
              {
                icon: <FaShieldAlt className="text-7xl text-blue-600" aria-hidden="true" />,
                iconLabel: 'Shield icon representing safety',
                title: 'Proactive Safety',
                description: 'Stop incidents before they happen. Our AI identifies risks in real-time, giving you the power to act instantly and prevent accidents'
              },
              {
                icon: <FaBrain className="text-7xl text-purple-600" aria-hidden="true" />,
                iconLabel: 'Brain icon representing intelligence',
                title: 'Smart Automation',
                description: 'No more watching hours of footage. Let AI do the heavy lifting—monitoring 24/7, analyzing every frame, and alerting you only when it matters'
              },
              {
                icon: <FaChartLine className="text-7xl text-pink-600" aria-hidden="true" />,
                iconLabel: 'Chart icon representing analytics',
                title: 'Actionable Insights',
                description: 'Turn video data into business intelligence. Track compliance, identify patterns, and make data-driven decisions that improve safety and efficiency'
              }
            ].map((feature, index) => (
              <ScrollReveal key={index} direction="up" delay={index * 0.2}>
                <article className="p-10 bg-white rounded-2xl border border-gray-100 h-full">
                  <MicroInteraction type="icon" className="mb-6 flex justify-center">
                    <span role="img" aria-label={feature.iconLabel}>
                      {feature.icon}
                    </span>
                  </MicroInteraction>
                  <h3 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-4 text-center">{feature.title}</h3>
                  <p className="text-base md:text-lg text-gray-700 leading-relaxed text-center">{feature.description}</p>
                </article>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-32 px-4 bg-gradient-to-br from-gray-50 to-blue-50 relative overflow-hidden">
        <ParallaxScroll speed={0.3} className="absolute top-20 right-10 opacity-10">
          <FaBrain className="text-[300px] text-blue-600" />
        </ParallaxScroll>

        <div className="max-w-7xl mx-auto relative z-10">
          <ScrollReveal direction="scale" className="text-center mb-20">
            <KineticText
              text="Enterprise-Grade Intelligence"
              className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-6 tracking-tight"
              type="word"
            />
            <motion.p
              className="text-lg sm:text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              Built for scale, designed for simplicity, trusted by industry leaders
            </motion.p>
          </ScrollReveal>

          <div className="grid md:grid-cols-4 gap-8 mb-16">
            {[
              { icon: <FaBrain />, title: 'AI That Learns', desc: 'Continuously improving accuracy with every frame analyzed' },
              { icon: <FaBell />, title: 'Instant Alerts', desc: 'Get notified in seconds, not minutes—when every moment counts' },
              { icon: <FaLock />, title: 'Privacy First', desc: 'Your data stays yours. Bank-level encryption and compliance' },
              { icon: <FaChartLine />, title: 'Visual Analytics', desc: 'Beautiful dashboards that tell the story behind the data' }
            ].map((tech, index) => (
              <ScrollReveal key={index} direction="up" delay={index * 0.1}>
                <MicroInteraction type="card" className="p-8 bg-white rounded-2xl text-center border border-gray-100 h-full">
                  <MicroInteraction type="icon" className="text-6xl text-blue-600 mb-6 flex justify-center">
                    {tech.icon}
                  </MicroInteraction>
                  <h4 className="text-xl md:text-2xl font-semibold text-gray-900 mb-4">{tech.title}</h4>
                  <p className="text-base md:text-lg text-gray-600 leading-relaxed">{tech.desc}</p>
                </MicroInteraction>
              </ScrollReveal>
            ))}
          </div>

          {/* Stats Section with Counter Animation */}
          <ScrollReveal direction="up" delay={0.4}>
            <div className="grid md:grid-cols-3 gap-8 mt-20">
              {[
                { value: 99.9, suffix: '%', label: 'Detection Accuracy' },
                { value: 100, suffix: 'ms', label: 'Response Time' },
                { value: 24, suffix: '/7', label: 'Monitoring' }
              ].map((stat, index) => (
                <MicroInteraction key={index} type="card" className="p-8 bg-white/80 backdrop-blur rounded-2xl text-center border border-blue-200">
                  <div className="text-4xl md:text-5xl font-extrabold text-blue-600 mb-2">
                    <CounterAnimation value={stat.value} suffix={stat.suffix} duration={2} />
                  </div>
                  <p className="text-base md:text-lg text-gray-600 font-medium">{stat.label}</p>
                </MicroInteraction>
              ))}
            </div>
          </ScrollReveal>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 relative overflow-hidden">
        {/* Animated background elements */}
        <motion.div
          className="absolute top-10 left-10 w-64 h-64 bg-white/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{ duration: 4, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-10 right-10 w-64 h-64 bg-white/10 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.5, 0.3, 0.5]
          }}
          transition={{ duration: 4, repeat: Infinity }}
        />

        <div className="max-w-5xl mx-auto text-center relative z-10">
          <ScrollReveal direction="scale">
            <KineticText
              text="Your Safety. Our Mission."
              className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-8 tracking-tight"
              type="word"
            />
            <motion.p
              className="text-lg sm:text-xl md:text-2xl text-white/90 mb-12 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              Join hundreds of organizations protecting their people with intelligent video analytics.
              See the difference AI can make in minutes, not months.
            </motion.p>

            <motion.div
              className="flex flex-col sm:flex-row gap-6 justify-center items-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
            >
              <Link href="/detection">
                <MicroInteraction type="button">
                  <motion.button
                    className="px-12 py-6 text-xl bg-white text-blue-600 rounded-xl font-bold shadow-2xl"
                    whileHover={{ scale: 1.05, boxShadow: "0 30px 60px -15px rgba(0, 0, 0, 0.3)" }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Start Free Trial →
                  </motion.button>
                </MicroInteraction>
              </Link>
              <Link href="/contact">
                <MicroInteraction type="button">
                  <motion.button
                    className="px-12 py-6 text-xl bg-transparent text-white border-2 border-white rounded-xl font-bold shadow-2xl"
                    whileHover={{
                      scale: 1.05,
                      backgroundColor: "rgba(255, 255, 255, 1)",
                      color: "#2563eb"
                    }}
                    whileTap={{ scale: 0.95 }}
                  >
                    Talk to an Expert
                  </motion.button>
                </MicroInteraction>
              </Link>
            </motion.div>
          </ScrollReveal>
        </div>
      </section>

      <Footer />
    </main>
  )
}

