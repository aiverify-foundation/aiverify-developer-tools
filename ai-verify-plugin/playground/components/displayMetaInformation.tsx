import React, { useEffect, useState, createRef } from 'react';
// import styles from './displayMetaInformation.module.css'
import { UiSchema, RJSFSchema } from "@rjsf/utils";
import validator from '@rjsf/validator-ajv8';
import Form from '@rjsf/mui';

const uiSchema: UiSchema = {
  "ui:options": {
    "submitButtonOptions": {
      "norender": true,
    }
  }
};

export default function DisplayMetaInformation ({ component, schema }) {
  const [ rjsfSchema, setRjsfSchema ] = useState<RJSFSchema>({});
  const formRef = createRef<Form<any, any, any>>();

  useEffect(() => {
    const newSchema = {
      ...(schema || {}),
      title:"",
      description:"",
      // "$schema": "https://json-schema.org/draft/2020-12/schema",
    };
    delete newSchema['$schema'];
    setRjsfSchema(newSchema)
  },[schema])


  if (!component || !schema)
    return <div></div>

  return (
    <div style={{ overflowY:'auto', overflowX:'hidden', height:'100%', width:'100%', padding:'5px', paddingBottom:'30px' }}>
      <Form
        ref={formRef}
        schema={rjsfSchema}
        formData={component.meta}
        // onChange={e => _onChangeData(e.formData)}
        uiSchema={uiSchema}
        validator={validator}
        liveValidate 
      />
    </div>
 )
}