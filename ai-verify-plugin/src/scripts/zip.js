#!/usr/bin/env node
const fs = require("node:fs");
const AdmZip = require("adm-zip");
const pluginMeta = require("../plugin.meta.json");

const zip = new AdmZip();
zip.addLocalFile("plugin.meta.json");

if (fs.existsSync("widgets")) {
  zip.addFile("widgets/", null)
  zip.addLocalFolder("widgets", "widgets")
}

if (fs.existsSync("inputs")) {
  zip.addFile("widgets/", null)
  zip.addLocalFolder("inputs", "inputs")
}

// write to disk
zip.writeZip(`${pluginMeta.gid}-${pluginMeta.version}.zip`)
