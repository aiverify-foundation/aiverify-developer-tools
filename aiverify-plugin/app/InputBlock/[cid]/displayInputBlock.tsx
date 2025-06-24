'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

import DisplayMetaInformation from 'playground/components/displayMetaInformation';
import InputBlock from 'playground/inputBlock';
import { InputDataContext, InputDataContextType } from "aiverify-shared-library/lib";


export default function DisplayInputBlock ({inputBlock, pluginMeta, code, frontmatter, inputBlockSchema}) {
  const router = useRouter();
  const [ selectedIndex, setSelectedIndex ] = useState<number>(0);
  // const [ data, setData ] = useState({});
  const [inputBlockContext, setInputBlockContext] = useState<InputDataContextType>({
    data: {},
    meta: inputBlock.meta,
    onChangeData: (key, value) => {
      setInputBlockContext(prevState => ({
        ...prevState,
        data: {
          ...prevState.data,
          [key]: value
        }
      }))
    }
  });

  function calculateCSSWidth() {
    if (!inputBlock)
      return;

    if (inputBlock.meta.fullScreen) {
      return '100vw';
    }
    
    switch (inputBlock.meta.width) {
      case 'xs':
        return '300px';
      case 'sm':
        return '500px';
      case 'md':
        return '700px';
      case 'lg':
        return '1200px';
      case 'xl':
        return '1400px';
      default:
        return '700px'; // default is md
    }
  }
  
  return (
    <InputDataContext.Provider value={inputBlockContext}>
      <div 
        className='block w-full h-screen overflow-hidden p-1 relative'
      >
        <div 
          className='inline-block align-top h-full overflow-auto'
          style={{ width:'calc(100% - 500px)' }}
        >
            <button className='btn-primary mb-1' onClick={() => {router.refresh()}}>Refresh</button>
            <div className='h-full w-full m-0'>
              {/* <div className="bg-primary-900 p-2" style={{ width:calculateCSSWidth() }}>{inputBlock.meta.name} Dialog</div> */}
              <div 
                className='p-0 text-white h-full w-full'
                style={{ width:calculateCSSWidth() }}
              >
                <InputBlock inputBlock={inputBlock} code={code} frontmatter={frontmatter} />
              </div>
            </div>
        </div>
        <div className='inline-block h-full p-0'
          style={{ width: '500px' }}
          // style={{ display:'inline-block', height:'calc(100vh - 60px)', width: '500px', padding:'5px' }}
        >
          <div className='flex p-1'>
            <button
              className="btn-primary mr-1"
              style={{ backgroundColor:(selectedIndex==0)?"var(--color-primary-700)":undefined }}
              // sx={{ lineHeight:'normal', marginRight:'5px',  }}
              onClick={() => setSelectedIndex(0)}
            >Input Block Meta</button>
            <button
              className="btn-primary"
              style={{ backgroundColor:(selectedIndex==1)?"var(--color-primary-700)":undefined }}
              // variant='contained' 
              // sx={{ lineHeight:'normal', backgroundColor:(selectedIndex==1)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(1)}
            >Data Output</button>
          </div>
          <div className='p-2 bg-white text-black h-full overflow-hidden'
            // style={{ backgroundColor:'white', color:'#676767', marginTop:'5px', height:'100%', overflow:'hidden' }}
          >
            {selectedIndex==0 && <DisplayMetaInformation component={inputBlock} schema={inputBlockSchema} />}
            {selectedIndex==1 && <pre style={{ padding:'10px', margin:'10px', height:'calc(100% - 20px)', overflowY:'auto', textAlign:'left' }}>{JSON.stringify(inputBlockContext.data, null, 2)}</pre>}
          </div>
        </div>
      </div>
    </InputDataContext.Provider>
  )
}