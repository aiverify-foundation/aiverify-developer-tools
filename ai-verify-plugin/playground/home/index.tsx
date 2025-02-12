import { useState, useEffect } from 'react';
import 'aiverify-shared-library/styles.css';
import "node_modules/react-grid-layout/css/styles.css";
import "node_modules/react-resizable/css/styles.css";


import DisplayWidget from '../../app/ReportWidget/[cid]/displayWidget';

export default function Home ({ widgets }) {
  const [ selectedComponent, setSelectedComponent ] = useState<any>(null);

  const getComponent = () => {
    if (!selectedComponent)
      return <div></div>;

    switch (selectedComponent.type) {
      case 'ReportWidget':
        return <DisplayWidget widget={selectedComponent} />
      default:
        return <div>{JSON.stringify(selectedComponent)}</div>
    }
  }

  const selectComponent = (comp) => {
    if (selectedComponent && comp.meta.cid === selectedComponent.meta.cid) {
      setSelectedComponent(null);
      return;
    } else {
      setSelectedComponent(comp);
    }
  }

  return (
    <div style={{ display:'flex' }}>
      <div className="aiv-panel" style={{ width: '360px', height:'100vh', flexShrink:0, textAlign:'left' }}>
        <h2>Widgets</h2>
        {widgets.map(widget => (
          <div>
            <button
              className="aiv-button c-secondary"
              style={{ marginTop:"5px", textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.meta.cid === widget.meta.cid)?"#4b255a":undefined }}
              onClick={() => selectComponent(widget)}
            >
                {widget.meta.name}
            </button>
          </div>
        ))}        
      </div>
      <div style={{ flexGrow:1, padding:"10px", overflow:'auto' }}>
        {getComponent()}
      </div>
    </div>
  );
}