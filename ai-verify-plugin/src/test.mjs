import jest from "jest";
import path from 'node:path';
import fs from 'node:fs';
import { getMdxWidgetBundle } from './bundler.mjs';
// import {bundleMDX} from 'mdx-bundler';
// import remarkMdxImages from 'remark-mdx-images';
// import remarkGfm from 'remark-gfm';


import { getPluginDir, listWidgetCIDs, listInputBlockCIDs, getComponent } from './pluginManager.mjs';
import { rootDir, linkModulePath } from './utils.mjs';

/**
 * Bundle the MDX files here. Trying to bundle in Jest environment too challenging now.
 */

const CACHE_DIR = "cache";
async function myTestSetup() {
  const pluginDir = getPluginDir();
  const cacheDir = path.join(pluginDir,CACHE_DIR);
  if (!fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir);
  }
  
  // console.log("In setupFilesAfterEnv")
  // const meta = readJSON(path.join(pluginDir, "plugin.meta.json")),
  const widgetCIDs = listWidgetCIDs();
  const inputBlockCIDS = listInputBlockCIDs();

  for (const cid of widgetCIDs) {
    const widgetFile = path.join(cacheDir,`${cid}.widget`);
    const resultFile = path.join(cacheDir,`${cid}.result`);
    const widget = getComponent(cid);
    const result = await getMdxWidgetBundle(widget.mdxPath); 
    if (result.result) {
      // const {code, frontmatter} = result || {};
      fs.writeFileSync(resultFile,JSON.stringify(result.result));
      fs.writeFileSync(widgetFile,JSON.stringify(widget));
    } else {
      console.log("error", result.error);
      fs.rmSync(resultFile, { force: true }); 
      fs.rmSync(widgetFile, { force: true }); 
    }
  }

  for (const cid of inputBlockCIDS) {
    const inputBlockFile = path.join(cacheDir,`${cid}.inputBlock`);
    const resultFile = path.join(cacheDir,`${cid}.result`);
    const inputBlock = getComponent(cid);
    const result = await getMdxWidgetBundle(inputBlock.mdxPath);
    if (result.result) {
      // const {code, frontmatter} = result || {};
      fs.writeFileSync(resultFile,JSON.stringify(result.result));
      fs.writeFileSync(inputBlockFile,JSON.stringify(inputBlock));
    } else {
      console.log("error", result.error);
      fs.rmSync(resultFile, { force: true }); 
      fs.rmSync(inputBlockFile, { force: true }); 
    }
  }
}

function myTestTeardown() {
  const pluginDir = getPluginDir();
  const cacheDir = path.join(pluginDir,CACHE_DIR);
  fs.rmSync(cacheDir, { force:true, recursive:true })
}

export async function runTest(argv) {
  // create symlink for node_modules
  linkModulePath();

  process.env.NODE_ENV = 'test';
  process.env.pluginDir = argv._pluginDir;
  // console.log("test", argv._pluginDir)
  // const dir = path.join(srcDir, "..");
  await myTestSetup()

  argv['collectCoverageFrom'] = `${argv._pluginDir}/**/*.{ts,mdx}`;

  // jest.run(args);
  await jest
    .runCLI(argv, [rootDir])
    .then((success) => {
      // console.log(success);
      // console.log("Tests completed successfully")
    })
    .catch((failure) => {
      console.log("Jest run error", failure)
      // console.error(failure);
    });
  
  myTestTeardown();
}
