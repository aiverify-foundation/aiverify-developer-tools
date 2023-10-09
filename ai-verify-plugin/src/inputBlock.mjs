import fs from 'node:fs';
import path from 'node:path';
import { validate } from 'jsonschema';
// import {bundleMDX} from 'mdx-bundler';
import { readJSON, srcDir, copyAndRenameTemplates } from './utils.mjs';

import { inputBlockSchema } from './schemas.mjs';

const INPUT_BLOCK_SUBDIR = "inputs";

export function generateInputBock(argv) {
  console.log("Generating skeleton input block..")

  // create director 
  // const pluginDir = argv.pluginDir;
  // const pluginDir = path.resolve(".");
  const pluginDir = argv._pluginDir;
  
  if (!fs.existsSync(pluginDir)) {
    console.error("Plugin directory does not exists")
    process.exit(-1);
  }

  // create widget dir
  const inputBlockDir = path.join(pluginDir, INPUT_BLOCK_SUBDIR)
  if (!fs.existsSync(inputBlockDir)) {
    fs.mkdirSync(inputBlockDir);
  }

  // create meta file
  const metaFile = path.join(inputBlockDir, `${argv.cid}.meta.json`)
  let meta = {
    cid: argv.cid,
  };
  if (fs.existsSync(metaFile)) {
    meta = readJSON(metaFile);
  }
  for (let key of ["name","description","author","version","tag","group","width","fullScreen"]) {
    if (key in argv) {
      switch (key) {
        case 'tag':
          if (!meta['tags'] || argv.force)
            meta['tags'] = argv[key];
          break;
        default:
          if (!meta[key] || argv.force)
            meta[key] = argv[key];
          break;
      }
    }
  }
  if (!meta.name)
    meta.name = meta.cid;
  fs.writeFileSync(metaFile, JSON.stringify(meta, null, 2))

  // create sample MDX file
  // const mdxFile = path.join(inputBlockDir, `${argv.cid}.mdx`);
  // fs.writeFileSync(mdxFile, MDX_TEMPLATE + "\n")

  // create sample summary ts
  // const summaryFile = path.join(inputBlockDir, `${argv.cid}.ts`);
  // fs.writeFileSync(summaryFile, SUMMARY_TEMPLATE.trim() + "\n")

  copyAndRenameTemplates(path.join(srcDir,"inputs"), "sample-input-block", inputBlockDir, argv.cid)
}

export async function validateInputBlock(argv, meta, skipMDXValidation=false) {
  const pluginDir = argv._pluginDir;

  const inputBlockDir = path.join(pluginDir, INPUT_BLOCK_SUBDIR)

  // validate meta
  try {
    const res = validate(meta, inputBlockSchema);
    if (!res.valid) {
      console.error(`Input block meta for ${meta.cid} validation errors:`, res.errors);
      return false;
    }
  } catch (err) {
    console.error(`Input block meta for ${meta.cid} is invalid`, err)
    return false;
  }

  const summaryFile = path.join(inputBlockDir, `${meta.cid}.summary.mdx`)
  if (!fs.existsSync(summaryFile)) {
    console.log(`Summary file ${meta.cid}.summary.mdx is missing`)
    return false;
  }

  const mdxFile = path.join(inputBlockDir, `${meta.cid}.mdx`)
  if (!fs.existsSync(mdxFile)) {
    console.log(`Widget MDX ${meta.cid}.mdx is missing`)
    return false;
  }
  
  // validate mdx
  if (!skipMDXValidation) {
    // validate widget mdx
    const {bundleMDX} = await import('mdx-bundler');
    const remarkMdxImages = await import('remark-mdx-images');
    const remarkGfm = await import('remark-gfm');
    try {
      await bundleMDX({
        cwd: pluginDir,
        file: mdxFile,
        mdxOptions: options => {
          options.remarkPlugins = [...(options.remarkPlugins ?? []), remarkMdxImages, remarkGfm]
          return options
        },
        esbuildOptions: options => {
          options.loader = {
            ...options.loader,
            '.png': 'dataurl',
          }
          return options
        },
      })
    } catch(e) {
      console.log("MDX error", e);
      return false;
    }

    // validate widget mdx
    try {
      await bundleMDX({
        cwd: pluginDir,
        file: summaryFile,
        mdxOptions: options => {
          options.remarkPlugins = [...(options.remarkPlugins ?? []), remarkMdxImages, remarkGfm]
          return options
        },
        esbuildOptions: options => {
          options.loader = {
            ...options.loader,
            '.png': 'dataurl',
          }
          return options
        },
      })
    } catch(e) {
      console.log("MDX error", e);
      return false;
    }
  }

  return true;
}

export async function validateAllInputBlocks(argv) {
  const pluginDir = argv._pluginDir;
  
  // const widgetDir = path.join(argv.pluginDir, WIDGET_SUBDIR)
  const inputBlockDir = path.join(pluginDir, INPUT_BLOCK_SUBDIR)
  if (!fs.existsSync(inputBlockDir)) {
    console.log("inputs directory is missing")
    return true;
  }

  const myfiles = fs.readdirSync(inputBlockDir);
  for (let f of myfiles) {
    if (!f.endsWith(".meta.json"))
      continue;
    // console.log("validating", f);
    const meta = readJSON(path.join(inputBlockDir, f));
    if (!meta.cid) {
      console.error("Invalid input block meta file", f);
      return false;
    }  
    if (!(await validateInputBlock(argv, meta)))
      return false;
}

  return true;
}