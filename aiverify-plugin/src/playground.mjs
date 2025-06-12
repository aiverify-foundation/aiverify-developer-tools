// server.js
import { createServer } from 'node:http';
import { parse } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
import { srcDir, linkModulePath } from './utils.mjs';
import next from 'next';

if (!process.env.NODE_ENV)
  process.env.NODE_ENV = 'development';
const dev = process.env.NODE_ENV !== 'production';
// const hostname = 'localhost'
// const port = 5000;
// when using middleware `hostname` and `port` must be provided below

export function runPlayground(argv) {
  // symlink node_modules
  linkModulePath();

  console.log("Loading playground..")
  process.env.pluginDir = argv._pluginDir;
  const dir = path.join(srcDir, "..");

  // console.log("dir", dir);
  
  const app = next({ dev, hostname: argv.hostname, port: argv.port, dir })
  const handle = app.getRequestHandler()
  
  // init normal http server
  return app.prepare().then(() => {
    createServer((req, res) => {
      const parsedUrl = parse(req.url, true)
      handle(req, res, parsedUrl)
    }).listen(argv.port)
    console.log(
      `> Playground listening at http://${argv.hostname}:${argv.port}`
    )
  })
}
