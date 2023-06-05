import fs from 'node:fs';
import path from 'node:path';
import { validate } from 'jsonschema';
// import {bundleMDX} from 'mdx-bundler';
import { readJSON, srcDir, copyAndRenameTemplates } from './utils.mjs';

import { algorithmSchema } from './schemas.mjs';

const ALGORITHM_SUBDIR = "algorithms";

export async function validateAlgorithm(argv, meta) {
  // validate meta
  try {
    const res = validate(meta, algorithmSchema);
    if (!res.valid) {
      console.error(`Input block meta for ${meta.cid} validation errors:`, res.errors);
      return false;
    }
  } catch (err) {
    console.error(`Input block meta for ${meta.cid} is invalid`, err)
    return false;
  }

  return true;
}

export async function validateAllAlgorithms(argv) {
  const pluginDir = argv._pluginDir;
  
  const algorithmDir = path.join(pluginDir, ALGORITHM_SUBDIR)
  if (!fs.existsSync(algorithmDir)) {
    console.log("algorithms directory is missing")
    return true;
  }

  const mysubdirs = fs.readdirSync(algorithmDir);
  for (let cid of mysubdirs) {
    const subdir = path.join(algorithmDir, cid);
    if (!fs.lstatSync(subdir).isDirectory())
      continue;

    if (!fs.existsSync(path.join(subdir,"input.schema.json"))) {
      console.log("input.schema.json not found");
      return false;
    }
    
    if (!fs.existsSync(path.join(subdir,"output.schema.json"))) {
      console.log("output.schema.json not found");
      return false;
    }

    const metaFilename = path.join(subdir, `${cid}.meta.json`);
    if (!fs.existsSync(metaFilename)) {
      console.log(`Meta file ${metaFilename} not found`);
      return false;
    }

    // console.log("validating", f);
    const meta = readJSON(metaFilename);
    if (!meta.cid) {
      console.error("Invalid algorithm meta file", f);
      return false;
    }

    if (!(await validateAlgorithm(argv, meta)))
      return false;
  }

  return true;
}
