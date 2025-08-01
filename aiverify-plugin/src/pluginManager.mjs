import fs from "node:fs";
import path from "node:path";
import { getModuleNameFromPyProject } from "./algorithms.mjs";

import { readJSON } from "./utils.mjs";

export function getPluginDir() {
  return process.env.pluginDir;
}

export function getWidgetFolder() {
  return path.join(process.env.pluginDir, "widgets");
}

export function getInputBlockFolder() {
  return path.join(process.env.pluginDir, "inputs");
}

export function getAlgorithmsFolder() {
  return path.join(process.env.pluginDir, "algorithms");
}

export function getPluginMeta() {
  const p = path.join(getPluginDir(), "plugin.meta.json");
  return readJSON(p);
}

export function listWidgetCIDs() {
  const widgetsDir = getWidgetFolder();
  if (!fs.existsSync(widgetsDir)) return [];
  let cids = [];
  const metaFiles = fs
    .readdirSync(widgetsDir)
    .filter((f) => f.endsWith(".meta.json"));
  for (let file of metaFiles) {
    // do a quick validation of the file.
    const widget = readJSON(path.join(widgetsDir, file));
    if (!widget.cid) {
      console.log(`Missing CID in ${file}`);
      continue;
    }
    const basename = path.basename(file);
    if (`${widget.cid}.meta.json` !== basename) {
      console.log(`Widget meta filename ${basename} does not match CID`);
      continue;
    }
    let mdxPath = path.join(widgetsDir, `${widget.cid}.mdx`);
    if (!fs.existsSync(mdxPath)) {
      console.log(`Missing MDX file for ${widget.cid}`);
      continue;
    }
    cids.push(widget.cid);
  }
  // console.log("cids", cids);
  return cids;
}

export function listInputBlockCIDs() {
  const inputsDir = getInputBlockFolder();
  if (!fs.existsSync(inputsDir)) return [];
  let cids = [];
  const metaFiles = fs
    .readdirSync(inputsDir)
    .filter((f) => f.endsWith(".meta.json"));
  for (let file of metaFiles) {
    // do a quick validation of the file.
    const ib = readJSON(path.join(inputsDir, file));
    if (!ib.cid) {
      console.log(`Missing CID in ${file}`);
      continue;
    }
    const basename = path.basename(file);
    if (`${ib.cid}.meta.json` !== basename) {
      console.log(`Widget meta filename ${basename} does not match CID`);
      continue;
    }
    let mdxPath = path.join(inputsDir, `${ib.cid}.mdx`);
    if (!fs.existsSync(mdxPath)) {
      console.log(`Missing MDX file for ${ib.cid}`);
      continue;
    }
    let summaryPath = path.join(inputsDir, `${ib.cid}.summary.mdx`);
    if (!fs.existsSync(summaryPath)) {
      console.log(`Missing summary file for ${ib.cid}`);
      continue;
    }
    cids.push(ib.cid);
  }
  // console.log("cids", cids);
  return cids;
}

export function getComponent(cid) {
  const widgetsDir = getWidgetFolder();
  let mdxPath = path.join(widgetsDir, `${cid}.mdx`);
  let metaPath = path.join(widgetsDir, `${cid}.meta.json`);
  let type = "ReportWidget";
  let obj = {
    type,
    mdxPath,
    // meta: readJSON(metaPath),
  };
  if (!fs.existsSync(mdxPath) || !fs.existsSync(metaPath)) {
    const inputsDir = getInputBlockFolder();
    mdxPath = path.join(inputsDir, `${cid}.mdx`);
    obj.mdxPath = mdxPath;
    metaPath = path.join(inputsDir, `${cid}.meta.json`);
    const summaryPath = path.join(inputsDir, `${cid}.meta.json`);
    obj.type = "InputBlock";
    if (
      !fs.existsSync(mdxPath) ||
      !fs.existsSync(metaPath) ||
      !fs.existsSync(summaryPath)
    ) {
      console.log(`Component ${cid} not found`);
      return null;
    }
    obj.summaryPath = summaryPath;
  }
  obj.meta = readJSON(metaPath);
  if (obj.type === "ReportWidget") {
    if (obj.meta.mockdata) {
      for (let mock of obj.meta.mockdata) {
        let datapath = path.join(widgetsDir, mock.datapath);
        mock.data = readJSON(datapath);
      }
    }
  } else {
    // InputBlock
  }
  // console.log("obj", JSON.stringify(obj, null, 2));
  return obj;
}

export function listAlgorithmsCIDs() {
  const algoDir = getAlgorithmsFolder();
  if (!fs.existsSync(algoDir)) return [];
  const cids = fs.readdirSync(algoDir).filter((cid) => {
    const d = path.join(algoDir, cid);
    // console.log(d)
    if (!fs.lstatSync(d).isDirectory()) return false;
    if (!fs.existsSync(path.join(d, "pyproject.toml"))) return false;
    const moduleName = getModuleNameFromPyProject(
      path.join(d, "pyproject.toml")
    );
    if (!moduleName) {
      return false;
    }
    const srcDir = path.join(d, moduleName);
    if (!fs.existsSync(path.join(srcDir, `algo.meta.json`))) return false;
    if (!fs.existsSync(path.join(srcDir, `input.schema.json`))) return false;
    if (!fs.existsSync(path.join(srcDir, `output.schema.json`))) return false;
    return true;
  });
  return cids;
}

export function listAlgorithms() {
  const algoDir = getAlgorithmsFolder();
  if (!fs.existsSync(algoDir)) return [];
  const algos = fs.readdirSync(algoDir).reduce((acc, folder) => {
    const d = path.join(algoDir, folder);
    // console.log(d)
    if (!fs.lstatSync(d).isDirectory()) return acc;
    if (!fs.existsSync(path.join(d, "pyproject.toml"))) return acc;
    const moduleName = getModuleNameFromPyProject(
      path.join(d, "pyproject.toml")
    );
    if (!moduleName) {
      return acc;
    }
    const srcDir = path.join(d, moduleName);
    if (!fs.existsSync(path.join(srcDir, `algo.meta.json`))) return acc;
    if (!fs.existsSync(path.join(srcDir, `input.schema.json`))) return acc;
    if (!fs.existsSync(path.join(srcDir, `output.schema.json`))) return acc;
    const algo = getAlgorithm(folder)
    acc.push({
      folder,
      moduleName,
      meta: algo.meta,
      algo
    })
    return acc;
  }, []);
  return algos;
}


export function getAlgorithm(folder) {
  const algoDir = path.join(getAlgorithmsFolder(), folder);
  // console.log("algoDir", algoDir)
  const moduleName = getModuleNameFromPyProject(path.join(algoDir, "pyproject.toml"))
  const srcDir = path.join(algoDir, moduleName);
  const meta = readJSON(path.join(srcDir, 'algo.meta.json'))
  const algo = {
    cid: meta["cid"],
    type: "Algorithm",
    meta,
    inputSchema: readJSON(path.join(srcDir, "input.schema.json")),
    outputSchema: readJSON(path.join(srcDir, "output.schema.json")),
  };
  return algo;
}
