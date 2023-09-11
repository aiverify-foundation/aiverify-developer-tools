import path from 'node:path';

// import "bootstrap/dist/css/bootstrap.css";
// import theme from '../src/lib/theme';
import ThemeRegistry from './components/theme/themeRegistry';
import "playground/styles/styles.css";
import 'playground/styles/color-palette.css';
import { listWidgetCIDs, listInputBlockCIDs, getComponent, getPluginDir, listAlgorithmsCIDs, getAlgorithm } from 'src/pluginManager.mjs';
import { readJSON } from "src/utils.mjs";

import MenuBar from './menuBar';

export const metadata = {
  title: 'Playground',
  description: 'AI Verify Plugin Playground',
}

function getWidgets() {
  return listWidgetCIDs().map(cid => getComponent(cid) );
}

function getInputBlocks() {
  return listInputBlockCIDs().map(cid => getComponent(cid) );
}

function getAlgorithms() {
  return listAlgorithmsCIDs().map(cid => getAlgorithm(cid))
}

function getPluginMeta() {
  const metaPath = path.join(getPluginDir(), "plugin.meta.json");
  return readJSON(metaPath);
}

export default function RootLayout({
  // Layouts must accept a children prop.
  // This will be populated with nested layouts or pages
  children,
}: {
  children: React.ReactNode;
}) {
  const widgets = getWidgets();
  const inputBlocks = getInputBlocks();
  const algorithms = getAlgorithms();
  const pluginMata = getPluginMeta();

  return (
    <html lang="en">
       <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        {/* <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" /> */}
        <link href='https://fonts.googleapis.com/css?family=Inter' rel='stylesheet'></link>
       </head>
      <body>
        <ThemeRegistry options={{ key: 'mui' }}>
          <div style={{ display:'flex' }}>
            <MenuBar pluginMata={pluginMata} widgets={widgets} inputBlocks={inputBlocks} algorithms={algorithms} />
            <div style={{ flexGrow:1, padding:'10px' }}>
              {children}
            </div>
          </div>
        </ThemeRegistry>
      </body>
    </html>
  );
}