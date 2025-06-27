import React, { useMemo, useState, useEffect, useRef } from "react";
import { getMDXComponent } from "mdx-bundler/client";
import moment from "moment";
// import 'aiverify-shared-library/styles.css';

export default function Widget({
  widget,
  pluginMeta,
  code,
  frontmatter,
  properties = {},
  testDataset = {},
  model = {},
  tests = [],
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [frozen, setFrozen] = useState<any>(null);
  const Component = useMemo(() => getMDXComponent(code), [code]);
  const resizeObserver = useRef<ResizeObserver>();
  const [container, setContainer] = useState<any>({
    observing: false,
    width: 0,
    height: 0,
  });

  useEffect(() => {
    // setContainer({
    // 	width: ref?.current?.parentElement?.offsetWidth,
    // 	height: ref?.current?.parentElement?.offsetHeight,
    // })
  }, [
    ref?.current?.parentElement?.offsetWidth,
    ref?.current?.parentElement?.offsetHeight,
  ]);

  useEffect(() => {
    // const properties = ctx[mykey]?ctx[mykey].properties:{};
    // console.log("widget", widget);
    // console.log("pluginMeta", pluginMeta);
    let result = {};
    let inputBlockData = {};
    if (widget.meta.mockdata) {
      for (let mock of widget.meta.mockdata) {
        const gid = mock.gid
          ? `${mock.gid}:${mock.cid}`
          : `${pluginMeta.gid}:${mock.cid}`;
        if (mock.type === "Algorithm") {
          result[gid] = mock.data;
        } else {
          inputBlockData[gid] = mock.data;
        }
      }
      // console.log("result", result);
      // console.log("inputBlockData", inputBlockData);
    }
    const timeStart = moment();
    const timeTaken = Math.floor(Math.random() * 1000 + 1);
    const reportDate = timeStart.add(timeTaken, "seconds");
    let resizeObserver: ResizeObserver | null = null;
    const obj = Object.freeze({
      inputBlockData,
      result,
      meta: widget.meta,
      properties: properties,
      getContainerObserver: (
        callback: (width: number, height: number) => void
      ) => {
        resizeObserver = new ResizeObserver(() => {
          if (ref.current && ref.current.parentElement) {
            // console.log("callback", ref.current.parentElement.offsetWidth, ref.current.parentElement.offsetHeight)
            callback(
              ref.current.parentElement.offsetWidth - 20,
              ref.current.parentElement.offsetHeight - 20
            );
          }
        });
        if (ref.current && ref.current.parentElement)
          resizeObserver.observe(ref.current.parentElement);
        return resizeObserver;
      },
      container: {
        width: "100%",
        height: "100%",
      },
      // additional properties added
      getResults(cid: string, gid: null | string = null) {
        const key =
          gid && gid.length > 0 ? `${gid}:${cid}` : `${pluginMeta.gid}:${cid}`;
        return result[key];
      },
      getIBData(cid: string, gid: null | string = null) {
        const key =
          gid && gid.length > 0 ? `${gid}:${cid}` : `${pluginMeta.gid}:${cid}`;
        return inputBlockData[key];
      },
      report: {
        timeStart: timeStart.toDate(),
        timeTaken,
        totalTestTimeTaken: timeTaken - 1,
        reportDate: reportDate.toDate(),
      },
      modelAndDatasets: {
        // todo: mock
        testDataset: testDataset,
        model: model,
        groundTruthDataset: testDataset,
        groundTruthColumn: "Fake GroundTruth",
      },
      tests,
      getTest(cid: string, gid: null | string = null) {
        // todo mock based on input schema
        if (!tests) return undefined;
        const key =
          gid && gid.length > 0 ? `${gid}:${cid}` : `${pluginMeta.gid}:${cid}`;
        return tests.find((k) => k.algorithmGID === key);
      },
    });
    // console.log("frozen", obj)
    setFrozen(obj);

    return () => {
      if (resizeObserver) resizeObserver.disconnect();
    };
  }, [widget, container]);

  if (!code || !frozen) {
    return <div>Invalid Widget</div>;
  }

  return (
    <div ref={ref} className="relative p-2 w-full h-full">
      <Component {...frozen} frontmatter={frontmatter} width={"100%"} height={"100%"} />
    </div>
  );
}
