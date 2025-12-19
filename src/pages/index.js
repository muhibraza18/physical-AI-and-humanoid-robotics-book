import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHero() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--dark', styles.heroBanner)}>
      <div className="container hero-container">
        <div className="hero-content">
          <span className="beta-badge">BETA V1.0 AVAILABLE</span>
          <Heading as="h1" className="hero-title">
            <span className="text-white">Physical AI & </span>
            <span className="text-gradient">Humanoid Robotics</span>
          </Heading>
          <p className="hero-subtitle">
            Bridge the gap between Sim and Real. Master Embodied Intelligence, Reinforcement Learning, and Whole-Body Control for the next generation of humanoid robots.
          </p>
          <div className="tech-badges">
            <span className="tech-badge">ROS 2</span>
            <span className="tech-badge">NVIDIA Isaac</span>
            <span className="tech-badge">PyTorch</span>
            <span className="tech-badge">Gazebo</span>
          </div>
          <div className={styles.buttons}>
            <Link
              className="button button--primary button--lg glow-effect"
              to="/docs/chapter-01">
              Start Learning →
            </Link>
            <Link
              className="button button--outline button--lg glow-effect"
              href="https://github.com/muhibraza18/physical-ai-and-humanoid-robotics-book">
              GitHub Repo
            </Link>
          </div>
          <div className="start-journey">
            <p>START A JOURNEY</p>
            <i className="fas fa-arrow-down"></i> {/* Placeholder for down arrow icon */}
          </div>
        </div>
        <div className="hero-illustration">
          {/* Placeholder for code editor mockup or robot illustration */}
          <img src="/img/robot-illustration.jpeg" alt="Robot Illustration" /> {/* Example illustration */}
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A Definitive University-Level Reference on Physical AI and Humanoid Robotics.">
      <HomepageHero />
      <main>
        {/* Additional sections can go here if needed */}
      </main>
    </Layout>
  );
}
