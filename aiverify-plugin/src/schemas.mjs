import { readJSON, rootDir } from "./utils.mjs";
import path from "path";

const baseSchemaPath = path.join(rootDir,"../../aiverify/common/schemas")

export const pluginSchema = readJSON(path.join(baseSchemaPath,"./aiverify.plugin.schema.json"));

export const reportWidgetSchema = readJSON(path.join(baseSchemaPath,"./aiverify.widget.schema.json"));

export const inputBlockSchema = readJSON(path.join(baseSchemaPath,"./aiverify.inputBlock.schema.json"));

export const algorithmSchema = readJSON(path.join(baseSchemaPath,"./aiverify.algorithm.schema.json"));
