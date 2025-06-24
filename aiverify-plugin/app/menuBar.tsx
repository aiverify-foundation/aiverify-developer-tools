"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams, usePathname } from "next/navigation";
// import "aiverify-shared-library/styles.css";

const SELECTED_COLOR = "var(--color-primary-950)";
// const NOT_SELECTED_COLOR = '#cf539b';
const NOT_SELECTED_COLOR = "var(--color-primary-700)";

function compareName(a, b) {
  if (a.meta.name < b.meta.name) return -1;
  else if (a.meta.name > b.meta.name) return 1;
  else return 0;
}

export default function MenuBar({
  pluginMata,
  widgets,
  inputBlocks,
  algorithms,
}) {
  const router = useRouter();
  const params = useParams();
  const pathname = usePathname();
  const [selectedComponent, setSelectedComponent] = useState<any>(null);

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
  }, [pathname]);

  const selectComponent = (comp) => {
    if (selectedComponent && comp.meta.cid === selectedComponent.cid) {
      // setSelectedComponent(null);
      router.push("/");
      return;
    } else {
      // setSelectedComponent(comp);
      router.push(`/${comp.type}/${comp.meta.cid}`);
    }
  };

  return (
    <div
      className="bg-stone-900 p-3 inline-block w-full h-full bg-black shrink-0 text-left text-stone-200 overflow-y-auto"
      style={{ textAlign: 'left' }}
    >
      <h2 className="p-0 m-0">{pluginMata.name}</h2>
      <div
        className="text-left text-base wrap-break-word p-2"
      >
        <div>GID: {pluginMata.gid}</div>
        <div>Version: {pluginMata.version}</div>
        <div>Description: {pluginMata.description}</div>
        <div>Author: {pluginMata.author}</div>
        <div>URL: {pluginMata.url}</div>
      </div>
      <div className="sectionDivider"></div>
      {widgets && widgets.length > 0 && (
        <div className="mt-2"><h2>Widgets</h2></div>
      )}
      {widgets.sort(compareName).map((widget) => (
        <button
          key={`link-${widget.meta.cid}`}
          className="btn-primary mt-1 mr-1 text-left"
          style={{ backgroundColor:(selectedComponent && selectedComponent.cid === widget.meta.cid)?SELECTED_COLOR:NOT_SELECTED_COLOR }}
          // style={{ marginTop:"10px", marginRight:'5px', textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.cid === widget.meta.cid)?SELECTED_COLOR:NOT_SELECTED_COLOR }}
          onClick={() => selectComponent(widget)}
        >
          {widget.meta.name}
        </button>
      ))}
      {inputBlocks && inputBlocks.length > 0 && (
        <h2 style={{ marginTop: "10px" }}>Input Blocks</h2>
      )}
      {inputBlocks.sort(compareName).map((ib) => (
        <button
          key={`link-${ib.meta.cid}`}
          className="btn-primary mt-1 mr-1 text-left"
          style={{ backgroundColor:(selectedComponent && selectedComponent.cid === ib.meta.cid)?SELECTED_COLOR:NOT_SELECTED_COLOR }}
          // variant="contained"
          // sx={{ marginTop:"10px", marginRight:'5px', textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.cid === ib.meta.cid)?SELECTED_COLOR:NOT_SELECTED_COLOR }}
          onClick={() => selectComponent(ib)}
        >
          {ib.meta.name}
        </button>
      ))}
      {algorithms && algorithms.length > 0 && (
        <h2 style={{ marginTop: "10px" }}>Algorithms</h2>
      )}
      {algorithms.sort(compareName).map((algo) => (
        <button
          key={`link-${algo.meta.cid}`}
          className="btn-primary mt-1 mr-1 text-left"
          style={{ backgroundColor:(selectedComponent && selectedComponent.cid === algo.meta.cid)?SELECTED_COLOR:NOT_SELECTED_COLOR }}
          // variant="contained"
          // sx={{ marginTop:"10px", marginRight:'5px', textAlign:'left', backgroundColor:(selectedComponent && selectedComponent.cid === algo.meta.cid)?SELECTED_COLOR:NOT_SELECTED_COLOR }}
          onClick={() => selectComponent(algo)}
        >
          {algo.meta.name}
        </button>
      ))}
    </div>
  );
}
