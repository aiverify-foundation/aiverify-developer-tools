import React, { useMemo, useState, useEffect, useRef } from 'react';
import {getMDXComponent} from 'mdx-bundler/client';
import moment from 'moment';
import 'ai-verify-shared-library/styles.css';

export default function Widget({ widget, pluginMeta, code, frontmatter, properties={}, testDataset={}, model={}, tests=[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const [ frozen, setFrozen ] = useState<any>(null);
  const Component = useMemo(() => getMDXComponent(code), [code])
  const [ container, setContainer ] = useState<any>({
		width: 0,
		height: 0,
	});

  useEffect(() => {
		setContainer({
			width: ref?.current?.parentElement?.offsetWidth,
			height: ref?.current?.parentElement?.offsetHeight,
		})
  },[ref?.current?.parentElement?.offsetWidth, ref?.current?.parentElement?.offsetHeight]);

  useEffect(() => {
		// const properties = ctx[mykey]?ctx[mykey].properties:{};
    // console.log("widget", widget);
    // console.log("pluginMeta", pluginMeta);
    let result = {};
    let inputBlockData = {};
    if (widget.meta.mockdata) {
      for (let mock of widget.meta.mockdata) {
        const gid = mock.gid?`${mock.gid}:${mock.cid}`:`${pluginMeta.gid}:${mock.cid}`
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
    const timeTaken = Math.floor((Math.random() * 1000) + 1);
		const reportDate = timeStart.add(timeTaken, 'seconds');
		const obj = Object.freeze({
			inputBlockData,
			result,
			meta: widget.meta,
			properties: properties,
      container,
      // additional properties added
			getResults(cid: string, gid:(null|string)=null) {
				const key = (gid && gid.length > 0)?`${gid}:${cid}`:`${pluginMeta.gid}:${cid}`;
				return result[key];
			},
			getIBData(cid: string, gid:(null|string)=null) {
				const key = (gid && gid.length > 0)?`${gid}:${cid}`:`${pluginMeta.gid}:${cid}`;
				return inputBlockData[key];
			},
			report: {
				timeStart: timeStart.toDate(),
				timeTaken,
				totalTestTimeTaken: timeTaken-1,
				reportDate: reportDate.toDate(),
			},
			modelAndDatasets: { // todo: mock
				testDataset: testDataset,
				model: model,
				groundTruthDataset: testDataset,
				groundTruthColumn: "Fake GroundTruth",
			},
			tests,
			getTest(cid: string, gid:(null|string)=null) {
				// todo mock based on input schema
				if (!tests)
					return undefined;
				const key = (gid && gid.length > 0)?`${gid}:${cid}`:`${pluginMeta.gid}:${cid}`;
				return tests.find(k => k.algorithmGID === key)
			}
		});
		// console.log("frozen", obj)
		setFrozen(obj);
	}, [widget, container])

  if (!code || !frozen) {
    return <div>Invalid Widget</div>
  }


  return (
    <div ref={ref} style={{ padding:'10px', textAlign:'justify' }}>
      <Component {...frozen} frontmatter={frontmatter} />
    </div>
  );
}