import fs from 'node:fs';
import path from 'node:path';
import { validate } from 'jsonschema';
import AdmZip from "adm-zip";

import { srcDir, readJSON } from './utils.mjs';

import { pluginSchema } from './schemas.mjs';
import { validateAllWidgets } from './reportWidget.mjs';
import { validateAllInputBlocks } from './inputBlock.mjs';
import { validateAllAlgorithms } from './algorithms.mjs';


export const PLUGIN_META_FILE = "plugin.meta.json"; 

/**
 * Generate plugin.
 * 
 * @param {object} argv 
 */
export function generatePlugin(argv) {
  console.log(`Generating skeleton project for ${argv.gid}..`)

  // create director 
  const pluginDir = argv.gid;
  if (!fs.existsSync(pluginDir))
    fs.mkdirSync(pluginDir);

  // Note: remove generation of npm files

  /*
  // create package.json
  const packagePath = path.join(pluginDir, "package.json");
  let mypackage = {};
  if (fs.existsSync(packagePath)) {
    mypackage = readJSON(packagePath);
  }
  const packageName = argv.name.toLowerCase().replaceAll(/[^a-z0-9-]/g,'-')
  const mypackage2 = {
    "name": packageName,
    "version": argv.version,
    "description": argv.description || "",
    "scripts": {
      "zip": "node scripts/zip.js",
      "test": "echo \"Error: no test specified\" && exit 1"
    },
    "author": argv.author || "",
    "license": "ISC",
    "devDependencies": {
      "adm-zip": "latest"
    }
  }
  if (argv.force) {
    mypackage = {
      ...mypackage,
      ...mypackage2,
    }
  } else {
    mypackage = {
      ...mypackage2,
      ...mypackage,
    }
  }
  fs.writeFileSync(packagePath, JSON.stringify(mypackage, null, 2) + "\n")
  */
  
  // create gitignore
  const gitignorePath = path.join(pluginDir, ".gitignore");
  if (!fs.existsSync(gitignorePath) || argv.force) {
    const gitignore = `
node_modules
node_modules/
build/
*.zip
*.log
lib-cov
coverage
cache
      `
      fs.writeFileSync(gitignorePath, gitignore.trim() + "\n")    
  }

  // create README
  const readmePath = path.join(pluginDir, "README.md");
  if (!fs.existsSync(readmePath) || argv.force) {
    const readme = `
# Project for ${argv.gid} plugin

For more information on AI Verify plugin developer, please refer to the [Developer Documentation](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-developers-documentation/-/tree/master/docs).

## Push project to GIT repo
1. Create a new blank GIT project.
2. Run the following commands to push the project to the GIT repo.

\`\`\`
cd existing_folder
git init
git checkout -b "main"
git remote add origin <repo-url>
git add .
git commit -m "Initial commit"
git push -u origin main
\`\`\`

## Create zip file for Plugin installation
Install the [ai-verify-plugin](https://gitlab.com/imda_dsl/t2po/ai-verify/ai-verify-portal/ai-verify-plugin) tool.

\`\`\`
ai-verify-plugin zip --pluginPath=<path to plugin directory>
\`\`\`
`

    fs.writeFileSync(readmePath, readme.trim() + "\n")
  }

  /*
  // create zip script
  const scriptPath = path.join(pluginDir, "scripts");
  if (!fs.existsSync(scriptPath)) {
    fs.mkdirSync(scriptPath);
  }

  fs.cpSync(path.join(srcDir,"scripts"), scriptPath, { recursive: true, force: true });
  */

  // create plugin meta
  const metaFile = path.join(pluginDir, PLUGIN_META_FILE)
  let meta = {
    gid: argv.gid,
  };
  if (fs.existsSync(metaFile)) {
    meta = readJSON(metaFile);
  }
  for (let key of ["name","version","description","author","url"]) {
    if (key in argv) {
      if (!meta[key] || argv.force)
        meta[key] = argv[key];
    }
  }
  if (!meta.name)
    meta.name = meta.gid;
  fs.writeFileSync(metaFile, JSON.stringify(meta, null, 2) + "\n")
}

/**
 * Validate plugin.
 * @todo Add script validation
 * 
 * @param {object} argv 
 * @returns 
 */
export async function validatePlugin(argv) {
  const pluginDir = argv._pluginDir;

  if (!validatePluginOnly(argv)) {
    return false;
  }
  // const metaFile = path.join(pluginDir, PLUGIN_META_FILE)

  // if (!fs.existsSync(metaFile)) {
  //   console.log("Plugin meta is missing")
  //   return false;
  // }
  
  // const meta = readJSON(metaFile);
  // // console.log("meta", meta);

  // try {
  //   const res = validate(meta, pluginSchema);
  //   if (!res.valid) {
  //     console.error("Plugin meta validation error", res.errors);
  //     return false;
  //   }
  // } catch (err) {
  //   console.error("Invalid meta object", err)
  //   return false;
  // }

  if (fs.existsSync(path.join(pluginDir, "widgets"))) {
    if (!(await validateAllWidgets(argv)))
      return false;
  }

  if (fs.existsSync(path.join(pluginDir, "inputs"))) {
    if (!(await validateAllInputBlocks(argv)))
      return false;
  }

  if (fs.existsSync(path.join(pluginDir, "algorithms"))) {
    if (!(await validateAllAlgorithms(argv)))
      return false;
  }

  return true;
}

export function validatePluginOnly(argv) {
  const pluginDir = argv._pluginDir;

  const metaFile = path.join(pluginDir, PLUGIN_META_FILE)

  if (!fs.existsSync(metaFile)) {
    console.log("Plugin meta is missing")
    return false;
  }
  
  const meta = readJSON(metaFile);
  // console.log("meta", meta);

  try {
    const res = validate(meta, pluginSchema);
    if (!res.valid) {
      console.error("Plugin meta validation error", res.errors);
      return false;
    }
  } catch (err) {
    console.error("Invalid meta object", err)
    return false;
  }

  return true;
}

export function zipPlugin (argv) {
  const pluginDir = argv._pluginDir;

  const metaFile = path.join(argv._pluginDir, PLUGIN_META_FILE);
  const pluginMeta = readJSON(metaFile);

  const zip = new AdmZip();
  zip.addLocalFile(metaFile);
  
  if (fs.existsSync("widgets")) {
    zip.addFile("widgets/", null)
    zip.addLocalFolder(path.join(pluginDir, "widgets"), "widgets")
  }
  
  if (fs.existsSync("inputs")) {
    zip.addFile("widgets/", null)
    zip.addLocalFolder(path.join(pluginDir, "inputs"), "inputs")
  }
  
  if (fs.existsSync("templates")) {
    zip.addFile("templates/", null)
    zip.addLocalFolder(path.join(pluginDir, "templates"), "templates")
  }
  
  if (fs.existsSync("algorithms")) {
    zip.addFile("algorithms/", null)
    // zip.addLocalFolder(path.join(pluginDir, "algorithms"), "algorithms")
    const algoRootPath = path.join(pluginDir, "algorithms");
    const subdirs = fs.readdirSync(algoRootPath);
    for (const algo of subdirs) {
      const algoPath = path.join(algoRootPath, algo);
      const metaPath = path.join(algoPath, `${algo}.meta.json`);
      if (!fs.existsSync(metaPath)) {
        console.log(`Meta file ${metaPath} does not exists`);
        continue;
      }
      zip.addFile(`algorithms/${algo}/`, null)
      const meta = readJSON(metaPath);
      if (Array.isArray(meta.requiredFiles)) {
        for (let f of meta.requiredFiles) {
          const subpath = path.join(algoPath, f);
          const stat = fs.lstatSync(subpath);
          if (stat.isDirectory()) {
            console.log("isDirectory", f)
            zip.addFile(`algorithms/${algo}/${f}/`, null)
            zip.addLocalFolder(subpath, `algorithms/${algo}`);
          } else {
            zip.addLocalFile(subpath, `algorithms/${algo}`);
          }
        }
      }
    }
  }

  const distPath = path.join(pluginDir, "dist");
  if (!fs.existsSync(distPath)) {
    fs.mkdirSync(distPath);
  }
  
  // write to disk
  const zipFilename = `${pluginMeta.gid}-${pluginMeta.version}.zip`;
  const zipPath = path.join(distPath, zipFilename)
  zip.writeZip(zipPath);

  console.log(`Plugin zip "${zipFilename}" is created.`)
}