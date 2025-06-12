'use client';

import React, { useState, useEffect, createRef } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@mui/material/Button';
import { UiSchema, RJSFSchema, hasWidget, getSchemaType } from "@rjsf/utils";
import validator from '@rjsf/validator-ajv8';
import Form from '@rjsf/mui';
import { parseRJSFSchema } from 'aiverify-shared-library/lib';
import _ from 'lodash';

const defaultUISchema: UiSchema = {
  "ui:options": {
    "submitButtonOptions": {
      "norender": true,
    }
  }
};

import AlgorithmSchema from 'src/schemas/ai-verify.algorithm.schema.json';
import DisplayMetaInformation from 'playground/components/displayMetaInformation';
import styles from './styles.module.css';

import mockTestData from './mockTestData.json';

/**
 * For testing
 * @param props 
 * @returns 
 */
/*
const MyCustomWidget = (props: WidgetProps) => {
  return (
    <input
      type='text'
      style={{ backgroundColor:'olive', color:'white' }}
      value={props.value}
      required={props.required}
      onChange={(event) => props.onChange(event.target.value)}
    />
  );
};

const widgets: RegistryWidgetsType = {
  myCustomWidget: MyCustomWidget,
};
*/

export default function DisplayAlgorithm ({algorithm, pluginMeta}) {
  const router = useRouter();
  const [ formData, setFormData ] = useState({});
  const [ selectedIndex, setSelectedIndex ] = useState<number>(0);
  const [ rjsfSchema, setRjsfSchema ] = useState<RJSFSchema>({});
  const [ uiSchema, setUISchema ] = useState<UiSchema>({});
  const formRef = createRef<Form<any, any, any>>();

  const getDatasets = () => {
    return Promise.resolve(mockTestData);
  }

  useEffect(() => {
    const schema = _.cloneDeep(algorithm.inputSchema);
    const uiw = parseRJSFSchema(schema, getDatasets, mockTestData[0]);
    // const uiw = traverseSchema(schema, mockTestData, mockTestData[0]);
    setRjsfSchema({
      ...(schema || {}),
      title:"",
      description:"",
    })
    setUISchema({
      ...defaultUISchema,
      ...uiw,
    })
  },[algorithm])

  return (
    <>
      <div style={{ display:'block', width:'100%', height:'100%', overflow:'hidden' }}>
        <div style={{ display: 'inline-block', width:'calc(100% - 500px)', verticalAlign:'top' }}>
          <h3 className="c-primary" style={{ padding:0, margin:0 }}>{algorithm.meta.name}</h3>
          <div style={{ display:'flex', alignItems:'center', marginTop:'10px' }}>
            <Button className='aiv-button c-secondary' onClick={() => {router.refresh()}}>Refresh</Button>
          </div>
          <div style={{ display:'block', width:'600px', height:'calc(100% - 200px)', overflowY:'scroll', margin:'10px auto 0 auto' }}>
            {rjsfSchema && (
              <div className={styles.schemaform}>
                <Form
                  ref={formRef}
                  schema={rjsfSchema}
                  formData={formData}
                  onChange={(e) => setFormData(e.formData)}
                  uiSchema={uiSchema}
                  validator={validator}
                  // widgets={widgets}
                  liveValidate 
                />
              </div>
            )}
          </div>
          {/* <pre className={styles.formdata}>
            {JSON.stringify(formData,null,2)}
          </pre> */}
        </div>
        <div style={{ display:'inline-block', width:'500px', height:'calc(100vh - 20px)' }}>
          <div style={{ display:'flex' }}>
            <Button
              variant='contained' 
              // className="aiv-button c-secondary"
              style={{ marginRight:'5px', lineHeight:'normal', backgroundColor:(selectedIndex==0)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(0)}
            >Algorithm Meta</Button>
            <Button
              variant='contained' 
              // className="aiv-button c-secondary"
              style={{ marginRight:'5px', lineHeight:'normal', backgroundColor:(selectedIndex==1)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(1)}
            >Input Schema</Button>
            <Button
              variant='contained' 
              // className="aiv-button c-secondary"
              style={{ marginRight:'5px', lineHeight:'normal', backgroundColor:(selectedIndex==2)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(2)}
            >Output Schema</Button>
            <Button
              variant='contained' 
              // className="aiv-button c-secondary"
              style={{ lineHeight:'normal', backgroundColor:(selectedIndex==3)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(3)}
            >Output</Button>
          </div>
          <div className='aiv-panel' style={{ backgroundColor:'white', marginTop:'5px', height:'100%', overflow:'hidden' }}>
            {selectedIndex==0 && <DisplayMetaInformation component={algorithm} schema={AlgorithmSchema} />}
            {selectedIndex==1 && <pre className={styles.mytab}>{JSON.stringify(algorithm.inputSchema,null,2)}</pre>}
            {selectedIndex==2 && <pre className={styles.mytab}>{JSON.stringify(algorithm.outputSchema,null,2)}</pre>}
            {selectedIndex==3 && <pre className={styles.mytab}>{JSON.stringify(formData,null,2)}</pre>}
          </div>
        </div>
      </div>
    </>
  )
}