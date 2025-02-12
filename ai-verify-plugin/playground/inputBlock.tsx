import { useMemo, useState, useEffect, useRef, useContext, createContext } from 'react';
import {getMDXComponent} from 'mdx-bundler/client';
import { InputDataContext, getComponents, InputDataContextType } from "aiverify-shared-library/lib";
const components = getComponents();
import 'aiverify-shared-library/styles.css';

// const components = getComponents();

export default function InputBlock({ inputBlock, code, frontmatter }) {
  const ctx = useContext(InputDataContext);
  const Component = useMemo(() => getMDXComponent(code), [code])

  if (!code) {
    return <div>Invalid Widget</div>
  }

  return (
    <div style={{ display:'block', padding:0, margin:0, overflow:'auto', position:"relative" }}>
      <Component {...ctx} frontmatter={frontmatter} components={components} />
    </div>
  );
}