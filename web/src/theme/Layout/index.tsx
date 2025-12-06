import React from 'react';
import clsx from 'clsx';
import ErrorBoundary from '@docusaurus/ErrorBoundary';
import { PageMetadata, SkipToContentLink } from '@docusaurus/theme-common';
import { useKeyboardNavigation } from '@docusaurus/theme-common/internal';
import Navbar from '@theme/Navbar';
import Footer from '@theme/Footer';
import LayoutProviders from '@theme/LayoutProviders';
import type { Props } from '@theme/Layout';
import { ThemeClassNames } from '@docusaurus/theme-common';
import styles from './styles.module.css';

export default function Layout(props: Props): JSX.Element {
  const {
    children,
    noFooter,
    wrapperClassName,
    // Not really used by layout.tsx, but useful for custom layouts
    title,
    description,
  } = props;

  useKeyboardNavigation();

  return (
    <LayoutProviders>
      <PageMetadata title={title} description={description} />

      <SkipToContentLink />

      <Navbar />

      <div
        id="docusaurus_skipToContent_target"
        className={clsx(ThemeClassNames.wrapper.main, wrapperClassName)}
      >
        <ErrorBoundary fallback={(_props) => <p>An error occurred.</p>}>
          {children}
        </ErrorBoundary>
      </div>

      {!noFooter && <Footer />}
    </LayoutProviders>
  );
}
