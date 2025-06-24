import { useMemo, useState, useEffect, useRef, useContext, createContext } from 'react';
import {getMDXComponent} from 'mdx-bundler/client';
import { InputDataContext, getComponents, InputDataContextType } from "aiverify-shared-library/lib";
const components = getComponents();
import 'aiverify-shared-library/styles.css';
import styles from  './inputBlock.module.css'

// const components = getComponents();

export default function InputBlock({ inputBlock, code, frontmatter }) {
  const ctx = useContext(InputDataContext);
  const Component = useMemo(() => getMDXComponent(code), [code])

  if (!code) {
    return <div>Invalid Widget</div>
  }

  return (
    <div className={styles['mdx-wrapper'] + ' block p-2 m-0 overflow-auto relative'} >
      <Component {...ctx} frontmatter={frontmatter} components={components} />
    </div>
  );
}