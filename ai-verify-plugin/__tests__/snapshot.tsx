import { render } from '@testing-library/react'
import React from 'react';
// import WidgetPage from '../pages/widget/[cid]';
import Widget from 'playground/widget';
import InputBlock from 'playground/inputBlock';
import path from 'node:path';
import fs from 'node:fs';
// const { ResizeObserver } = window;

import { readJSON } from 'src/utils.mjs';

describe("Snapshot tests", () => {
  let cacheDir;
  const iteach = (condition) => condition ? it.each : it.skip.each;

  beforeAll(async () => {
    cacheDir = path.join(global.pluginDir, "cache");
  });

  beforeEach(() => {
    jest.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(1050);
    jest.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(1400);
  });

  afterEach(() => {
    // window.ResizeObserver = ResizeObserver;
    // jest.restoreAllMocks();
  });


  iteach(global.plugin.widgetCIDs.length > 0)(global.plugin.widgetCIDs)(
    "renders widget %s unchanged",
    (cid) => {
      const widgetFile = path.join(cacheDir, `${cid}.widget`);
      const resultFile = path.join(cacheDir, `${cid}.result`);
      expect(fs.existsSync(widgetFile)).toBe(true);
      expect(fs.existsSync(resultFile)).toBe(true);
      const widget = readJSON(widgetFile);
      const result = readJSON(resultFile);
      const {code, frontmatter} = result || {};
      const { container } = render(
        <div style={{ width:"1400px", height:"1050px", display:"block", position:"relative" }}>
          <Widget pluginMeta={global.plugin.meta} widget={widget} code={code} frontmatter={frontmatter} />
        </div>
      );
      expect(container).toMatchSnapshot()
    }
  );

  iteach(global.plugin.inputBlockCIDS.length > 0)(global.plugin.inputBlockCIDS)(
    "renders input blocks %s unchanged",
    (cid) => {
      const inputBlockFile = path.join(cacheDir, `${cid}.inputBlock`);
      const resultFile = path.join(cacheDir, `${cid}.result`);
      expect(fs.existsSync(inputBlockFile)).toBe(true);
      expect(fs.existsSync(resultFile)).toBe(true);
      const inputBlock = readJSON(inputBlockFile);
      const result = readJSON(resultFile);
      const {code, frontmatter} = result || {};
      const { container } = render(
        <div style={{ width:"1400px", height:"1050px", display:"block", position:"relative" }}>
          <InputBlock inputBlock={inputBlock} code={code} frontmatter={frontmatter} />
        </div>
      );
      expect(container).toMatchSnapshot()
    }
  );

});
