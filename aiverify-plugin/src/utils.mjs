import fs from 'fs';

import path from 'path';
import url from 'url';

const __filename = url.fileURLToPath(import.meta.url);
export const srcDir = path.dirname(__filename);
export const rootDir = path.join(srcDir, "..")
// console.log("srcDir", srcDir)
// console.log("rootDir", rootDir)

export function readJSON (filepath) {
  try {
    const data = fs.readFileSync(filepath, "utf-8");
    return JSON.parse(data);
  } catch (err) {
    console.error("Error reading JSON", err);
    return {};
  }
}

export function copyAndRenameTemplates (srcDir, srcBaseName, targetDir, targetBaseName) {
  try {
    const files = fs.readdirSync(srcDir);
    for (let srcFile of files) {
      let targetFile = srcFile;
      if (srcFile.startsWith(srcBaseName)) {
        targetFile = srcFile.replace(srcBaseName, targetBaseName)
      }
      fs.copyFileSync(path.join(srcDir,srcFile), path.join(targetDir, targetFile))
    }
  } catch (err) {
    console.err("Error generating templates", err);
  }
}

/**
 * Create a symlink between the app's node_modules to the plugin node_modules
 */
export function linkModulePath() {
  const modulePath = path.resolve("./node_modules");
  if (!fs.existsSync(modulePath)) {
    const srcModulePath = path.join(rootDir, "./node_modules");
    fs.symlinkSync(srcModulePath, modulePath);
  }
}