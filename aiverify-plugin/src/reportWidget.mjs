import fs from "node:fs";
import path from "node:path";
import { validate } from "jsonschema";

import { srcDir, readJSON, copyAndRenameTemplates } from "./utils.mjs";

import { reportWidgetSchema } from "./schemas.mjs";

const WIDGET_SUBDIR = "widgets";

export function generateWidget(argv) {
  console.log(`Generating skeleton report widget for ${argv.cid}..`);

  // create director
  // const pluginDir = argv.pluginDir;
  // if (!fs.existsSync(pluginDir)) {
  //   console.error("Plugin directory does not exists")
  //   process.exit(-1);
  // }
  // const pluginDir = path.resolve(".");
  const pluginDir = argv._pluginDir;

  // create widget dir
  const widgetDir = path.join(pluginDir, WIDGET_SUBDIR);
  if (!fs.existsSync(widgetDir)) {
    fs.mkdirSync(widgetDir);
  }

  // create meta file
  const metaFile = path.join(widgetDir, `${argv.cid}.meta.json`);
  let meta = {
    cid: argv.cid,
    widgetSize: {},
  };
  if (fs.existsSync(metaFile)) {
    meta = readJSON(metaFile);
  }
  for (let key of [
    "name",
    "description",
    "version",
    "author",
    "tag",
    "minW",
    "minH",
    "maxW",
    "maxH",
    "dynamicHeight",
  ]) {
    if (key in argv) {
      switch (key) {
        case "minW":
        case "minH":
        case "maxW":
        case "maxH":
          if (!meta.widgetSize[key] || argv.force)
            meta.widgetSize[key] = argv[key];
          break;
        case "tag":
          if (!meta["tags"] || argv.force) meta["tags"] = argv[key];
          break;
        default:
          if (!meta[key] || argv.force) meta[key] = argv[key];
          break;
      }
    }
  }

  if (!meta.name) meta.name = meta.cid;

  if (argv._dep && (!meta.dependencies || argv.force)) {
    let dependencies = [];
    let mockdata = [];
    for (let dep of argv._dep) {
      // <Algorithm|InputBlock>,gid[,version]
      const datapath = `${dep[1]}.sample.json`;
      const cid = dep[1];
      let obj = {
        cid,
      };
      const count = dep.length;
      if (count >= 3) {
        obj["gid"] = dep[2];
      }
      if (count == 4) {
        obj["version"] = dep[3];
      }
      dependencies.push(obj);
      mockdata.push({
        type: dep[0],
        cid,
        datapath,
      });
      let datapathJoined = path.join(widgetDir, datapath);
      if (!fs.existsSync(datapathJoined)) {
        fs.writeFileSync(datapathJoined, "{}");
      }
    }
    meta.dependencies = dependencies;
    meta.mockdata = mockdata;
  }

  if (argv._prop && (!meta.properties || argv.force)) {
    let properties = [];
    for (let prop of argv._prop) {
      properties.push({
        key: prop[0],
        helper: prop[1],
        default: prop[2],
      });
    }
    meta.properties = properties;
  }

  fs.writeFileSync(metaFile, JSON.stringify(meta, null, 2));

  // create sample MDX file
  // const mdxFile = path.join(widgetDir, `${argv.cid}.mdx`);
  // fs.writeFileSync(mdxFile, MDX_TEMPLATE + "\n")
  // fs.cpSync(path.join(srcDir,"widgets"), widgetDir, { recursive: true });
  copyAndRenameTemplates(
    path.join(srcDir, "widgets"),
    "sample-widget",
    widgetDir,
    argv.cid
  );
}

export async function validateWidget(argv, meta, skipMDXValidation = false) {
  const pluginDir = argv._pluginDir;

  const widgetDir = path.join(pluginDir, WIDGET_SUBDIR);
  // if (!fs.existsSync(widgetDir)) {
  //   console.log("widgets directory is missing")
  //   return false;
  // }

  try {
    const res = validate(meta, reportWidgetSchema);
    if (!res.valid) {
      console.error(
        `Widget meta for ${meta.cid} has validation errors:`,
        res.errors
      );
      return false;
    }
  } catch (err) {
    console.error(`Widget meta for ${meta.cid} is invalid`, err);
    return false;
  }

  const mdxFile = path.join(widgetDir, `${meta.cid}.mdx`);
  if (!fs.existsSync(mdxFile)) {
    console.error(`Widget MDX ${meta.cid}.mdx is missing`);
    return false;
  }

  // validate mdx
  if (!skipMDXValidation) {
    const { getMdxWidgetBundle } = await import("./bundler.mjs");
    try {
      const result = await getMdxWidgetBundle(mdxFile);
      if (!result) {
        console.log("MDX error")
        return false
      }
    } catch (e) {
      console.log("MDX error", e);
      return false;
    }
  }

  return true;
}

export async function validateAllWidgets(argv) {
  const pluginDir = argv._pluginDir;

  // const widgetDir = path.join(argv.pluginDir, WIDGET_SUBDIR)
  const widgetDir = path.join(pluginDir, WIDGET_SUBDIR);
  if (!fs.existsSync(widgetDir)) {
    console.log("widgets directory is missing");
    return true;
  }

  const myfiles = fs.readdirSync(widgetDir);
  for (let f of myfiles) {
    if (!f.endsWith(".meta.json")) continue;
    // console.log("validating", f);
    const meta = readJSON(path.join(widgetDir, f));
    if (!meta.cid) {
      console.error("Invalid widget meta file", f);
      return false;
    }
    if (!(await validateWidget(argv, meta))) return false;
  }

  return true;
}
