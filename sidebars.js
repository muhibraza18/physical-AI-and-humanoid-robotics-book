// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  bookSidebar: [
    {
      type: 'category',
      label: 'Part I: Foundations',
      items: [
        'chapter-01', // Introduction to Physical AI and Embodied Intelligence
        'chapter-02', // A Brief History of Humanoid Robotics (1950–2025)
        'chapter-03', // Kinematics, Dynamics, and Control of Bipedal Humanoids
      ],
    },
    {
      type: 'category',
      label: 'Part II: Core Systems',
      items: [
        'chapter-04', // Sensing the Physical World: Vision, Depth, Tactile, Proprioception, and IMUs
        'chapter-05', // ROS 2 as the Robotic Nervous System
        'chapter-06', // High-Fidelity Simulation: Gazebo, Isaac Sim, and Digital Twins
        'chapter-07', // Perception for Humanoids: Visual SLAM, Scene Understanding, and Synthetic Data
        'chapter-08', // Locomotion and Balance: From ZMP to Deep Reinforcement Learning
        'chapter-09', // Manipulation and Dexterous Hands
      ],
    },
    {
      type: 'category',
      label: 'Part III: Advanced Topics & Integration',
      items: [
        'chapter-10', // Vision-Language-Action Models and Cognitive Architectures for Robots
        'chapter-11', // Sim-to-Real Transfer Techniques
        'chapter-12', // Current Humanoid Platforms: Technical Comparison (2025 Landscape)
      ],
    },
    {
      type: 'category',
      label: 'Part IV: Synthesis & Futures',
      items: [
        'chapter-13', // Safety, Ethics, and Societal Impact of Human-Scale Robots
        'chapter-14', // The Road Ahead: Research Frontiers and Open Problems
        'chapter-15', // Conclusion and Future Directions
      ],
    },
    'bibliography', // Master bibliography
  ],
};

export default sidebars;