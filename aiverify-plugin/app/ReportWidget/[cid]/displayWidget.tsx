"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import GridLayout from "react-grid-layout";
// import button from '@mui/material/button';
// import widgetSchema from 'src/schemas/ai-verify.widget.schema.json';

import DisplayMetaInformation from "playground/components/displayMetaInformation";
import "react-grid-layout/css/styles.css";
import "react-resizable/css/styles.css";
import "./styles.module.css";
import "../../../playground/styles/standardReport.css";

import Widget from "playground/widget";
import DisplayProperties from "./displayProperties";

import mockTestData from "../../Algorithm/[folder]/mockTestData.json";
import mockModels from "../../Algorithm/[folder]/mockModels.json";
import mockTests from "./mockTestResults.json";

// const GRID_WIDTH = 774;
// const GRID_ROW_HEIGHT = 30;
const GRID_MAX_ROWS = 36;
const GRID_STRICT_STYLE: React.CSSProperties = { height: "1080px" };

const A4_WIDTH = 794; // ideal width of A4 page
const A4_HEIGHT = 1100; // ideal height of A4 page
const A4_MARGIN = 12; // margin of A4 page
const GRID_ROWS = 36; // number of rows of the grid
const GRID_COLUMNS = 12; // number of columns of the grid
const GRID_WIDTH = A4_WIDTH - A4_MARGIN * 2; // width of the grid within the A4 page
const GRID_HEIGHT = A4_HEIGHT - A4_MARGIN * 2; // height of the grid within the A4 page
const GRID_ROW_HEIGHT = GRID_HEIGHT / GRID_ROWS; // calculated height of each row in the grid
const CONTAINER_PAD = 100; // padding used to calculate virtual space at top and bottom of the free from content

export default function DisplayWidget({
  widget,
  pluginMeta,
  code,
  frontmatter,
  reportWidgetSchema,
}) {
  const router = useRouter();
  const [layout, setLayout] = useState<any>([]);
  const [properties, setProperties] = useState<any>({});
  const [selectedIndex, setSelectedIndex] = useState<number>(0);

  useEffect(() => {
    if (!widget) return;

    const dynamicHeight = widget.meta.dynamicHeight;
    setLayout([
      {
        i: widget.meta.cid,
        x: 0,
        y: 0,
        w: widget.meta.widgetSize.minW,
        h: dynamicHeight ? 36 : widget.meta.widgetSize.minH,
        minW: widget.meta.widgetSize.minW,
        minH: dynamicHeight ? 36 : widget.meta.widgetSize.minH,
        maxW: widget.meta.widgetSize.maxW,
        maxH: dynamicHeight ? 36 : widget.meta.widgetSize.maxH,
        // maxH: 12,
      },
    ]);
  }, [widget]);

  const handleLayoutChange = (layout) => {
    setLayout(layout);
  };

  const getWidgetSize = () => {
    if (!layout || layout.length == 0) return <></>;
    return (
      <div>
        Widget Size [width: {layout[0].w},&nbsp; height: {layout[0].h}]
      </div>
    );
  };

  return (
    <>
      <div className="block w-full h-full overflow-hidden">
        <div
          className="inline-block h-full overflow-y-auto align-top p-2"
          style={{ width: "calc(100% - 500px)" }}
        >
          <h3 className="text-bold text-xl p-0 m-0">{widget.meta.name}</h3>
          <div
            style={{ display: "flex", alignItems: "center", marginTop: "10px" }}
          >
            <button
              className="btn-primary mr-3"
              onClick={() => {
                router.refresh();
              }}
            >
              Refresh
            </button>
            {getWidgetSize()}
          </div>
          <div
            className="canvas standard-report-page text-black block relative bg-stone-50"
            style={{
              height: A4_HEIGHT,
              width: A4_WIDTH,
              margin: "10px auto 5px auto",
            }}
          >
            {/* {JSON.stringify(layout,null,2)} */}
            {layout && (
              <GridLayout
                layout={layout}
                onLayoutChange={handleLayoutChange}
                width={GRID_WIDTH}
                rowHeight={GRID_ROW_HEIGHT}
                // className="[&>*]:text-inherit"
                style={{
                  height: GRID_HEIGHT,
                  width: GRID_WIDTH,
                  margin: `${A4_MARGIN}px`,
                }}
                // style={GRID_STRICT_STYLE}
                maxRows={GRID_MAX_ROWS}
                margin={[0, 0]}
                compactType={null}
                isBounded
                isDraggable={false}
                isResizable={true}
                resizeHandles={["s", "e", "sw", "se"]}
              >
                <div
                  key={widget.meta.cid}
                  style={{
                    backgroundColor: "white",
                    overflow: widget.meta.dynamicHeight ? "visible" : "hidden",
                  }}
                >
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
              </GridLayout>
            )}
          </div>
        </div>
        <div
          className="inline-block h-full relative"
          style={{ width: "500px" }}
        >
          <div className="flex flex-row p-1">
            <button
              className="btn-primary mr-2"
              style={{
                backgroundColor:
                  selectedIndex == 0 ? "var(--color-primary-700)" : undefined,
              }}
              // variant='contained'
              // sx={{ marginRight:'5px', lineHeight:'normal', backgroundColor:(selectedIndex==0)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(0)}
            >
              Widget Meta
            </button>
            <button
              className="btn-primary"
              style={{
                backgroundColor:
                  selectedIndex == 1 ? "var(--color-primary-700)" : undefined,
              }}
              // variant='contained'
              // sx={{ backgroundColor:(selectedIndex==1)?"var(--color-button-selected)":undefined }}
              onClick={() => setSelectedIndex(1)}
            >
              Properties
            </button>
          </div>
          <div className="bg-stone-50 p-2 text-left text-black mt-1 h-full">
            {selectedIndex == 0 && (
              <DisplayMetaInformation
                component={widget}
                schema={reportWidgetSchema}
              />
            )}
            {selectedIndex == 1 && (
              <DisplayProperties
                widget={widget}
                properties={properties}
                setProperties={setProperties}
              />
            )}
          </div>
        </div>
      </div>
    </>
  );
}
