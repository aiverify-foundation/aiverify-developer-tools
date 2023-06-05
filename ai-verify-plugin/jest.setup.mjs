import '@testing-library/jest-dom/extend-expect'
import path from 'node:path';
import { getPluginDir, listWidgetCIDs, listInputBlockCIDs } from './src/pluginManager.mjs';
import { readJSON } from './src/utils.mjs';

// console.log("In setupFilesAfterEnv")
const pluginDir = getPluginDir();
global.pluginDir = pluginDir;
global.plugin = {
  meta: readJSON(path.join(pluginDir, "plugin.meta.json")),
  widgetCIDs: listWidgetCIDs(),
  inputBlockCIDS: listInputBlockCIDs(),
}

import ResizeObserver from 'resize-observer-polyfill';
global.ResizeObserver = ResizeObserver;
// import * as sharedLibr from 'ai-verify-shared-library';
// console.log("global.pluginDir", global.pluginDir);
// console.log("global.plugin", global.plugin);
