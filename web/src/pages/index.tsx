import React from 'react';
import { useHistory } from 'react-router-dom';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import Link from '@docusaurus/Link';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-1-ros2/intro">
            Start Reading - ⏱️ 5min
          </Link>
        </div>
      </div>
    </header>
  );
}

const features = [
  {
    title: 'ROS 2',
    description: 'Learn the Robot Operating System 2 from scratch. Understand nodes, topics, services, and more.',
  },
  {
    title: 'Gazebo',
    description: 'Simulate your robots in a realistic 3D environment. Learn to create worlds and models.',
  },
  {
    title: 'Isaac Sim',
    description: 'Leverage the power of NVIDIA Isaac Sim for advanced robotics simulation and synthetic data generation.',
  },
  {
    title: 'Vision-Language-Action (VLA)',
    description: 'Explore the cutting-edge of AI with Vision-Language-Action models. Build a capstone project that sees, understands, and acts.',
  },
];

function Feature({title, description}) {
  return (
    <div className="col col--3">
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A comprehensive guide and development environment for AI-Humanoid Robotics">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
