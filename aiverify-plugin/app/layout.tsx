import path from 'node:path';

import './globals.css'
// import "aiverify-shared-library/styles.css";
// import "bootstrap/dist/css/bootstrap.css";
// import theme from '../src/lib/theme';
// import ThemeRegistry from './components/theme/themeRegistry';
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
          <div 
            className='block h-screen w-screen overflow-hidden p-0 m-0 bg-primary-950 p-0 m-0 text-white antialiased'
          >
            <div 
              className='inline-block h-full'
              style={{ width: '360px' }}
              // style={{ display:'inline-block', width:'360px', height:'100%', verticalAlign:'top' }}
            >
              <MenuBar pluginMata={pluginMata} widgets={widgets} inputBlocks={inputBlocks} algorithms={algorithms} />
            </div>
            <div 
              className='inline-block h-screen p-1 m-0'
              style={{ width:'calc(100vw - 360px)' }}
              // style={{ display:'inline-block', verticalAlign:'top', width:'calc(100% - 360px)', height:'100%', padding:'10px', margin:'0px' }}
            >
              {children}
            </div>
          </div>
      </body>
    </html>
  );
}