"use client";

import React, { useState, useEffect, createRef } from "react";
import { useRouter } from "next/navigation";
import "../../../playground/styles/form-styles.css";
import { UiSchema, RJSFSchema, hasWidget, getSchemaType } from "@rjsf/utils";
import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";
import { parseRJSFSchema } from "aiverify-shared-library/lib";
import _ from "lodash";

const defaultUISchema: UiSchema = {
  "ui:options": {
    submitButtonOptions: {
      norender: true,
    },
  },
};

// import { algorithmSchema } from 'src/schemas.mjs'
import DisplayMetaInformation from "playground/components/displayMetaInformation";
// import styles from "./styles.module.css";

import mockTestData from "./mockTestData.json";

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

export default function DisplayAlgorithm({
  algorithm,
  pluginMeta,
  algorithmSchema,
}) {
  const router = useRouter();
  const [formData, setFormData] = useState(algorithm.meta);
  const [selectedIndex, setSelectedIndex] = useState<number>(0);
  // const [rjsfSchema, setRjsfSchema] = useState<RJSFSchema>({});
  const [uiSchema, setUISchema] = useState<UiSchema>({});
  const formRef = createRef<Form<any, any, any>>();

  const getDatasets = () => {
    return Promise.resolve(mockTestData);
  };

  const schema = _.cloneDeep(algorithm.inputSchema);
  const rjsfSchema = algorithm?schema:{};

  useEffect(() => {
    console.log("algorithm:", algorithm);
    const schema = _.cloneDeep(algorithm.inputSchema);
    const uiw = parseRJSFSchema(schema, getDatasets, mockTestData[0]);
    // const uiw = traverseSchema(schema, mockTestData, mockTestData[0]);
    // setRjsfSchema({
    //   ...(schema || {}),
    //   title: "",
    //   description: "",
    // });
    setUISchema({
      ...defaultUISchema,
      ...uiw,
    });
    setFormData(algorithm.meta);
  }, [algorithm]);

  return (
    <>
      <div className="block w-full h-screen overflow-hidden relative">
        {/* Central bar */}
        <div
          className="inline-block align-top h-full p-2"
          style={{ width: "calc(100% - 500px)" }}
        >
          <h3 className="text-bold text-xl p-0 m-0">
            {algorithm.meta.name}
          </h3>
          <div className="flex items-center mt-2">
            <button
              className="btn-primary"
              onClick={() => {
                router.refresh();
              }}
            >
              Refresh
            </button>
          </div>
          <div className="block overflow-hidden h-full mx-auto w-full p-3"
          >
            {rjsfSchema && (
              <div className='overflow-y-auto overflow-x-hidden w-full p-3 mb-2 text-gray-100 bg-secondary-950'>
                <Form
                  ref={formRef}
                  schema={rjsfSchema}
                  className="custom-form"
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
        <div
          style={{
            display: "inline-block",
            width: "500px",
            height: "calc(100vh - 20px)",
          }}
        >
          <div style={{ display: "flex" }}>
            <button
              // variant='contained'
              className="aiv-button c-secondary"
              style={{
                marginRight: "5px",
                lineHeight: "normal",
                backgroundColor:
                  selectedIndex == 0
                    ? "var(--color-button-selected)"
                    : undefined,
              }}
              onClick={() => setSelectedIndex(0)}
            >
              Algorithm Meta
            </button>
            <button
              // variant='contained'
              className="aiv-button c-secondary"
              style={{
                marginRight: "5px",
                lineHeight: "normal",
                backgroundColor:
                  selectedIndex == 1
                    ? "var(--color-button-selected)"
                    : undefined,
              }}
              onClick={() => setSelectedIndex(1)}
            >
              Input Schema
            </button>
            <button
              // variant='contained'
              className="aiv-button c-secondary"
              style={{
                marginRight: "5px",
                lineHeight: "normal",
                backgroundColor:
                  selectedIndex == 2
                    ? "var(--color-button-selected)"
                    : undefined,
              }}
              onClick={() => setSelectedIndex(2)}
            >
              Output Schema
            </button>
            <button
              // variant='contained'
              className="aiv-button c-secondary"
              style={{
                lineHeight: "normal",
                backgroundColor:
                  selectedIndex == 3
                    ? "var(--color-button-selected)"
                    : undefined,
              }}
              onClick={() => setSelectedIndex(3)}
            >
              Output
            </button>
          </div>
          <div
            className="aiv-panel"
            style={{
              backgroundColor: "white",
              marginTop: "5px",
              height: "100%",
              overflow: "hidden",
            }}
          >
            {selectedIndex == 0 && (
              <DisplayMetaInformation
                component={algorithm}
                schema={algorithmSchema}
              />
            )}
            {selectedIndex == 1 && (
              <pre className="text-left text-black overflow-auto h-full">
                {JSON.stringify(algorithm.inputSchema, null, 2)}
              </pre>
            )}
            {selectedIndex == 2 && (
              <pre className="text-left text-black overflow-auto h-full">
                {JSON.stringify(algorithm.outputSchema, null, 2)}
              </pre>
            )}
            {selectedIndex == 3 && (
              <pre className="text-left text-black overflow-auto h-full">
                {JSON.stringify(formData, null, 2)}
              </pre>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
