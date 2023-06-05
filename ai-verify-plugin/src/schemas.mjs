import { readJSON, srcDir } from "./utils.mjs";
import path from "node:path";

export const pluginSchema = readJSON(path.join(srcDir,"./schemas/ai-verify.plugin.schema.json"));

export const reportWidgetSchema = readJSON(path.join(srcDir,"./schemas/ai-verify.widget.schema.json"));

export const inputBlockSchema = readJSON(path.join(srcDir,"./schemas/ai-verify.inputBlock.schema.json"));

export const algorithmSchema = readJSON(path.join(srcDir,"./schemas/ai-verify.algorithm.schema.json"));
