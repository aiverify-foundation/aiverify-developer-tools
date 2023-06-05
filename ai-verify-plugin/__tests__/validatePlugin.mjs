import { getComponent } from 'src/pluginManager.mjs';
import { validatePluginOnly } from 'src/plugin.mjs';
import { validateWidget } from 'src/reportWidget.mjs';
import { validateInputBlock } from 'src/inputBlock.mjs';

describe("Validate plugin and components", () => {
  let widgets = {};
  let inputBlocks = {};

  const iteach = (condition) => condition ? it.each : it.skip.each;

  beforeAll(() => {
    widgets = global.plugin.widgetCIDs.reduce((acc, cid) => {
      acc[cid] = getComponent(cid);
      return acc;
    }, {})
    inputBlocks = global.plugin.inputBlockCIDS.reduce((acc, cid) => {
      acc[cid] = getComponent(cid);
      return acc;
    }, {})
  });

  it('Validate plugin', () => {
    const argv = {
      _pluginDir: global.pluginDir,
    }
    expect(validatePluginOnly(argv)).toBe(true);
  });

  iteach(global.plugin.widgetCIDs.length > 0)(global.plugin.widgetCIDs)(
    "Validate widget %s",
    async (cid) => {
      const argv = {
        _pluginDir: global.pluginDir,
      }  
      // console.log("widgets[cid]", widgets[cid])
      expect(await validateWidget(argv, widgets[cid].meta, true)).toBe(true);
    }
  );

  iteach(global.plugin.inputBlockCIDS.length > 0)(global.plugin.inputBlockCIDS)(
    "Validate input block %s",
    async (cid) => {
      const argv = {
        _pluginDir: global.pluginDir,
      }  
      // expect(1+1).toBe(2);
      // console.log("widgets[cid]", widgets[cid])
      expect(await validateInputBlock(argv, inputBlocks[cid].meta, true)).toBe(true);
    }
  );
})
