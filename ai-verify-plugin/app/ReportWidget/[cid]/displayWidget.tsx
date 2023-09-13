'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import GridLayout from "react-grid-layout";
import Button from '@mui/material/Button';
import widgetSchema from 'src/schemas/ai-verify.widget.schema.json';

import DisplayMetaInformation from 'playground/components/displayMetaInformation';
import styles from './styles.module.css';
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";

import Widget from 'playground/widget';
import DisplayProperties from './displayProperties';

import mockTestData from '../../Algorithm/[cid]/mockTestData.json';
import mockModels from '../../Algorithm/[cid]/mockModels.json';
import mockTests from './mockTestResults.json';

const GRID_WIDTH = 774;
const GRID_ROW_HEIGHT = 30;
const GRID_MAX_ROWS = 36;
const GRID_STRICT_STYLE: React.CSSProperties = { height: '1080px' };

export default function DisplayWidget ({widget, pluginMeta, code, frontmatter}) {
  const router = useRouter();
  const [ layout, setLayout ] = useState<any>([]);
  const [ properties, setProperties ] = useState<any>({});
  const [ selectedIndex, setSelectedIndex ] = useState<number>(0);

  useEffect(() => {
    if (!widget)
      return;
    
    const dynamicHeight = widget.meta.dynamicHeight;
    setLayout([
      {
        i: widget.meta.cid,
        x: 0, y: 0,
        w: widget.meta.widgetSize.minW,
        h: dynamicHeight?36:widget.meta.widgetSize.minH,
        minW: widget.meta.widgetSize.minW,
        minH: dynamicHeight?36:widget.meta.widgetSize.minH,
        maxW: widget.meta.widgetSize.maxW,
        maxH: dynamicHeight?36:widget.meta.widgetSize.maxH,
        // maxH: 12,
      }
    ])
  }, [widget]);

  const handleLayoutChange = (layout) => {
    setLayout(layout)
  }


  const getWidgetSize = () => {
    if (!layout || layout.length == 0)
      return <></>;
    return (
      <div>
        Widget Size [width: {layout[0].w},&nbsp;
        height: {layout[0].h}]
      </div>
    )
  }

  return (
    <>
      <div style={{ display:'block', width:'100%', height:'100%', overflow:'hidden' }}>
        <div style={{ display:'inline-block', width:'calc(100% - 400px)', verticalAlign:'top' }}>
          <h3 className="c-primary" style={{ padding:0, margin:0 }}>{widget.meta.name}</h3>
          <div style={{ display:'flex', alignItems:'center', marginTop:'10px' }}>
            <Button variant='contained' sx={{ marginRight:'5px' }} onClick={() => {router.refresh()}}>Refresh</Button>
            {getWidgetSize()}
          </div>
          <div className={styles.canvas} style={{ display:'block', height:'calc(100% - 100px)', width:'810px', overflowY:'scroll', margin:'10px auto 0 auto' }}>
            {/* {JSON.stringify(layout,null,2)} */}
            {layout && <GridLayout
              layout={layout}
              onLayoutChange={handleLayoutChange}
              width={GRID_WIDTH}
              rowHeight={GRID_ROW_HEIGHT}
              maxRows={GRID_MAX_ROWS}
              margin={[0, 0]}
              compactType={null}
              style={GRID_STRICT_STYLE}
              isBounded
              isDraggable={false}
              isResizable={true}
              resizeHandles={['s','e','sw','se']}
            >
              <div key={widget.meta.cid} style={{ backgroundColor:'white', overflow:widget.meta.dynamicHeight?'visible':'hidden' }}>
                <Widget
                  widget={widget} 
                  pluginMeta={pluginMeta} 
                  code={code} 
                  frontmatter={frontmatter} 
                  properties={properties}
                  model={mockModels[0]}
                  testDataset={mockTestData[0]}
                  tests={mockTests}
                />
              </div>
            </GridLayout>}
          </div>
        </div>
        <div style={{ display:'inline-block', width:'400px', height:'100%' }}>
          <div style={{ display:'flex' }}>
            <Button
              // className="aiv-button c-secondary"
              variant='contained'
              sx={{ marginRight:'5px', lineHeight:'normal', backgroundColor:(selectedIndex==0)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(0)}
            >Widget Meta</Button>
            <Button 
              // className="aiv-button c-secondary"
              variant='contained'
              sx={{ backgroundColor:(selectedIndex==1)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(1)}
            >Properties</Button>
          </div>
          <div className='aiv-panel' style={{ backgroundColor:'white', marginTop:'5px', height:'100%', overflow:'hidden' }}>
            {selectedIndex==0 && <DisplayMetaInformation component={widget} schema={widgetSchema} />}
            {selectedIndex==1 && <DisplayProperties widget={widget} properties={properties} setProperties={setProperties} />}            
          </div>
        </div>
      </div>
    </>
  )
}