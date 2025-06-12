import jest from "jest";
import path from 'node:path';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';
import { cwd, chdir } from 'node:process';
import { getMdxWidgetBundle } from './bundler.mjs';
// import {bundleMDX} from 'mdx-bundler';
// import remarkMdxImages from 'remark-mdx-images';
// import remarkGfm from 'remark-gfm';


import { getPluginDir, getAlgorithmsFolder, listWidgetCIDs, listInputBlockCIDs, listAlgorithmsCIDs, getComponent } from './pluginManager.mjs';
import { rootDir, linkModulePath } from './utils.mjs';

/**
 * Bundle the MDX files here. Trying to bundle in Jest environment too challenging now.
 */

const CACHE_DIR = "cache";
async function myTestSetup(widgetCIDs, inputBlockCIDS) {
  const pluginDir = getPluginDir();
  const cacheDir = path.join(pluginDir,CACHE_DIR);
  if (!fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir);
  }
  
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

export async function runAlgoTests(argv) {
  process.env.pluginDir = argv._pluginDir;
  const algoCIDS = listAlgorithmsCIDs();

  const algoFolder = getAlgorithmsFolder();
  const python = process.env.PYTHON || "python";
  const currentDir = cwd();
  let count = 0;
  const silent = argv.silent;
  
  for (let cid of algoCIDS) {
    console.log("\n*****************************")
    console.log(`Running test for algo ${cid}..`);
    try {
      const algoPath = path.join(algoFolder, cid);
      chdir(algoPath);
      const res = execFileSync(python, ["."], { stdio:'pipe' })
      count++;
      console.log("Test success\n")
      if (!silent)
        console.log(res.toString());
    } catch (e) {
      console.log("Test failed\n")
      if (!silent)
        console.log(e.stdout.toString())
    }
  }
  console.log("************************************")
  console.log(`Number of algorithm tests run: ${algoCIDS.length}`)
  console.log(`Number of algorithm tests passed: ${count}`)
  console.log("************************************")

  // chdir back to original directory
  chdir(currentDir);
}

export async function runTest(argv) {
  process.env.NODE_ENV = 'test';
  process.env.pluginDir = argv._pluginDir;
  
  const widgetCIDs = listWidgetCIDs();
  const inputBlockCIDS = listInputBlockCIDs();

  if (widgetCIDs.length > 0 || inputBlockCIDS.length > 0) {
    // create symlink for node_modules
    linkModulePath();

    // console.log("test", argv._pluginDir)
    // const dir = path.join(srcDir, "..");
    await myTestSetup(widgetCIDs, inputBlockCIDS)

    argv['collectCoverageFrom'] = `${argv._pluginDir}/**/*.{ts,mdx}`;

    argv['_'] = ['test'];

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

  // if (algoCIDS.length > 0) {
  // }
  
}
