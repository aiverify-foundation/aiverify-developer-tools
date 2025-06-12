import fs from "node:fs";
import path from "node:path";
import { spawn, execFileSync } from "node:child_process";
import { chdir, exit } from "node:process";
import * as readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { validate } from "jsonschema";
// import {bundleMDX} from 'mdx-bundler';
import { readJSON, rootDir } from "./utils.mjs";

import { algorithmSchema } from "./schemas.mjs";

const ALGORITHM_SUBDIR = "algorithms";
const SYNTAX_CHECKER = "syntax_checker.py";

export async function validateAlgorithm(argv, meta, subdir) {
  const python = process.env.PYTHON || "python";

  const checkerScript = path.join(subdir, SYNTAX_CHECKER);
  const mainScript = path.join(subdir, `${meta.cid}.py`);

  // validate meta
  try {
    // validate algo meta
    const res = validate(meta, algorithmSchema);
    if (!res.valid) {
      console.error(
        `Input block meta for ${meta.cid} validation errors:`,
        res.errors
      );
      return false;
    }
    // validate python script syntax
    const res2 = execFileSync(python, [checkerScript, mainScript]);
  } catch (err) {
    console.error(`Algorithm ${meta.cid} is invalid`, err);
    return false;
  }

  return true;
}

export async function validateAllAlgorithms(argv) {
  const pluginDir = argv._pluginDir;

  const algorithmDir = path.join(pluginDir, ALGORITHM_SUBDIR);
  if (!fs.existsSync(algorithmDir)) {
    console.log("algorithms directory is missing");
    return true;
  }

  const mysubdirs = fs.readdirSync(algorithmDir);
  for (let cid of mysubdirs) {
    const subdir = path.join(algorithmDir, cid);
    if (!fs.lstatSync(subdir).isDirectory()) continue;

    if (!fs.existsSync(path.join(subdir, "input.schema.json"))) {
      console.log("input.schema.json not found");
      return false;
    }

    if (!fs.existsSync(path.join(subdir, "output.schema.json"))) {
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

    if (!(await validateAlgorithm(argv, meta, subdir))) return false;
  }

  return true;
}

export async function generateAlgorithm(argv) {
  const COOKIECUTTER = process.env.COOKIECUTTER || "cookiecutter";

  console.log("Generating skeleton algorithm..");

  // create director
  // const pluginDir = argv.pluginDir;
  // const pluginDir = path.resolve(".");
  const pluginDir = argv._pluginDir;

  if (!fs.existsSync(pluginDir)) {
    console.error("Plugin directory does not exists");
    process.exit(-1);
  }

  // create widget dir
  const algoDir = path.join(pluginDir, ALGORITHM_SUBDIR);
  if (!fs.existsSync(algoDir)) {
    fs.mkdirSync(algoDir);
  }

  // check algo component directory does not exists
  const compDir = path.join(algoDir, argv.cid);
  if (fs.existsSync(compDir)) {
    console.error(`Algorithm component ${argv.cid} already exists`);
    exit(-1);
  }

  const templateDir = path.join(rootDir, "../ai-verify-algorithm-template");
  const configFile = path.join(algoDir, `${argv.cid}-config.yaml`);

  const cleanupFiles = () => {
    if (fs.existsSync(configFile)) {
      fs.unlinkSync(configFile);
    }
    const licenseFile = path.join(compDir, "LICENSE");
    if (fs.existsSync(licenseFile)) fs.unlinkSync(licenseFile);
    const pluginMetaFile = path.join(compDir, "plugin.meta.json");
    if (fs.existsSync(pluginMetaFile)) fs.unlinkSync(pluginMetaFile);
  };

  try {
    chdir(algoDir);

    // create config file for cookie cutter
    fs.writeFileSync(
      configFile,
      `
default_context:
  author: "${argv.author}"
  plugin_name: "${argv.name}"
  project_slug: "${argv.cid}"
  plugin_version: "${argv.pluginVersion}"
  plugin_description: "${argv.description || ""}"
  algo_model_support: "${argv.modelSupport}"
  require_ground_truth: "${argv.requireGroundTruth ? "True" : "False"}"
`
    );

    const args = ["--config-file", configFile, "-o", algoDir, templateDir];
    if (!argv.interactive) {
      args.unshift("--no-input");
    }

    const rl = readline.createInterface({ input, output });
    const cc = spawn(COOKIECUTTER, args);
    cc.stdout.on("data", async (data) => {
      const qn = data.toString();
      if (qn.includes("license")) {
        cc.stdin.write("\n");
      } else {
        const ans = await rl.question(qn);
        cc.stdin.write(ans + "\n");
      }
    });
    cc.on("close", (code) => {
      rl.close();
      cleanupFiles();

      // update meta
      const metaFilename = path.join(compDir, `${argv.cid}.meta.json`);
      const meta = readJSON(metaFilename)
      if (argv.tag) {
        meta.tags = argv.tag;
      }
      fs.writeFile(metaFilename, JSON.stringify(meta, null, 2), err => {
        if (err) {
          console.error("Error updating algorithm meta file");
        }
      });
    });
  } catch (e) {
    console.error("Error executing cookiecutter", e.stdout.toString());
    cleanupFiles();
  }
}
