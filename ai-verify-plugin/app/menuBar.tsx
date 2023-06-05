'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams, usePathname  } from 'next/navigation';
import 'ai-verify-shared-library/styles.css';

const SELECTED_COLOR = '#4b255a';

function compareName(a, b) {
  if (a.meta.name < b.meta.name)
    return -1;
  else if (a.meta.name > b.meta.name)
    return 1;
  else
    return 0;
}


export default function MenuBar({ pluginMata, widgets, inputBlocks, algorithms }) {
  const router = useRouter()
  const params = useParams();
  const pathname = usePathname();
  const [ selectedComponent, setSelectedComponent ] = useState<any>(null);

  useEffect(() => {
    if (pathname.startsWith("/ReportWidget")) {
      setSelectedComponent(params);
      return;
    }
    if (pathname.startsWith("/InputBlock")) {
      setSelectedComponent(params);
      return;
    }
    if (pathname.startsWith("/Algorithm")) {
      setSelectedComponent(params);
      return;
    }
    setSelectedComponent(null);
  }, [pathname])

  const selectComponent = (comp) => {
    if (selectedComponent && comp.meta.cid === selectedComponent.cid) {
      // setSelectedComponent(null);
      router.push('/')
      return;
    } else {
      // setSelectedComponent(comp);
      router.push(`/${comp.type}/${comp.meta.cid}`)
    }
  }

  return (
    <div className="aiv-panel" style={{ width: '360px', height:'100vh', flexShrink:0, textAlign:'left', overflowY:'auto' }}>
      <h2 style={{ padding:0, margin:0 }}>{pluginMata.name}</h2>
      <div className='aiv-card c-info' style={{ textAlign:'left' }}>
        <div>GID: {pluginMata.gid}</div>
        <div>Version: {pluginMata.version}</div>
        <div>Description: {pluginMata.description}</div>
        <div>Author: {pluginMata.author}</div>
        <div>URL: {pluginMata.url}</div>
      </div>
      {widgets && widgets.length > 0 && <h2 style={{ marginTop:'10px' }}>Widgets</h2>}
      {widgets.sort(compareName).map(widget => (
        <button
          key={`link-${widget.meta.cid}`}
          className="aiv-button c-secondary"
          style={{ marginTop:"10px", textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.cid === widget.meta.cid)?SELECTED_COLOR:undefined }}
          onClick={() => selectComponent(widget)}
        >
            {widget.meta.name}
        </button>
      ))}        
      {inputBlocks && inputBlocks.length > 0 && <h2 style={{ marginTop:'10px' }}>Input Blocks</h2>}
      {inputBlocks.sort(compareName).map(ib => (
        <button
          key={`link-${ib.meta.cid}`}
          className="aiv-button c-secondary"
          style={{ marginTop:"10px", textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.cid === ib.meta.cid)?SELECTED_COLOR:undefined }}
          onClick={() => selectComponent(ib)}
        >
            {ib.meta.name}
        </button>
      ))}        
      {algorithms && algorithms.length > 0 && <h2 style={{ marginTop:'10px' }}>Algorithms</h2>}
      {algorithms.sort(compareName).map(algo => (
        <button
          key={`link-${algo.meta.cid}`}
          className="aiv-button c-secondary"
          style={{ marginTop:"10px", textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.cid === algo.meta.cid)?SELECTED_COLOR:undefined }}
          onClick={() => selectComponent(algo)}
        >
            {algo.meta.name}
        </button>
      ))}        
    </div>
  )
}