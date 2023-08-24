#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

import { rootDir } from './utils.mjs';
import * as dotenv from 'dotenv';
dotenv.config({ path: path.join(rootDir, ".env") })

import semver from 'semver';
import { URL } from 'node:url';
import { v4 as uuidv4 } from 'uuid';

import { generatePlugin, validatePlugin, zipPlugin, PLUGIN_META_FILE } from './plugin.mjs';
import { generateWidget } from './reportWidget.mjs';
import { generateInputBock } from './inputBlock.mjs';
import { generateAlgorithm } from './algorithms.mjs';
import { runPlayground } from './playground.mjs';
import { runTest, runAlgoTests } from './test.mjs';

function validateID (id) {
  return id.match(/^[a-zA-Z0-9][a-zA-Z0-9-._]*$/);
}

function validateURL (url) {
  try {
    new URL(url);
    return true;
  } catch (err) {
    console.log("err", err);
    return false;
  }
}

function validateNumber (n, min, max) {
  if (isNaN(n) || typeof(n) !== 'number')
    return false;
  if (min && n < min)
    return false;
  if (max && n > max)
    return false;
  return true;
} 

function findPluginRoot (argv) {
  let curDir = path.resolve(argv.pluginDir);
  while (!fs.existsSync(path.join(curDir, PLUGIN_META_FILE))) {
    if (curDir === "/") {
      throw new Error("Unable to find plugin root directory");
    }
    curDir = path.resolve(curDir, "..");
  }
  argv._pluginDir = curDir;
  return curDir;
}


import yargs from 'yargs/yargs';
const argv = yargs(process.argv.slice(2))
  .version(false)
  .scriptName("ai-verify-plugin")
  .usage('$0 <cmd> [args]')
  .command(['generate-plugin [gid]','gp'], 'Generate skeleton AI Verify plugin project', (yargs) => {
    yargs.positional('gid', {
      type: 'string',
      describe: 'Plugin Global ID',
      default: uuidv4(),
      defaultDescription: "If not specified, a random UUID will be generated.",
      requiresArg: true,
    }).option('name', {
      type: 'string',
      describe: 'Plugin name. If not provided will be set to same as gid.',
      requiresArg: true,
    }).option('version', {
      type: 'string',
      describe: 'Plugin version. Version should be a valid semantic version.',
      default: "1.0.0",
      requiresArg: true,
    }).option('author', {
      type: 'string',
      describe: 'Plugin author',
      requiresArg: true,
      default: "AI Verify"
    }).option('description', {
      type: 'string',
      describe: 'Plugin description',
      requiresArg: true,
    }).option('license', {
      type: 'string',
      describe: 'Plugin opensource license',
      requiresArg: true,
      choices: ["Apache Software License 2.0", "MIT", "BSD-3", "GNU GPL v3.0", "Mozilla Public License 2.0"],
      default: "Apache Software License 2.0",
    }).option('url', {
      type: 'string',
      describe: 'Plugin URL',
      requiresArg: true,
    }).option('force', {
      describe: 'Overwrite existing settings. By default existing settings will not be overwritten.',
      type: "boolean",
    })
    .check((argv, options) => {
      if (!validateID(argv.gid)) {
        throw new Error(`Invalid gid: ${argv.gid}`)
      }
      if (!semver.valid(argv.version)) {
        throw new Error(`Invalid version: ${argv.version}`);
      }
      if (argv.url && !validateURL(argv.url)) {
        throw new Error(`Invalid URL: ${argv.url}`)
      }
      return true;
    })
  }, function (argv) {
    // if (!argv.name) {
    //   argv.name = argv.gid;
    // }
    generatePlugin(argv);
  })
  .command(['generate-widget <cid>', 'gw'], 'Generate skeleton AI Verify widget', (yargs) => {
    yargs.positional('cid', {
      type: 'string',
      describe: 'Widget Component ID'
    }).option('name', {
      type: 'string',
      describe: 'Widget name. If not provided will be set to same as cid.',
      requiresArg: true,
    }).option('description', {
      type: 'string',
      describe: 'Widget description',
      requiresArg: true,
    }).option('tag', {
      describe: 'Allow users to search and filter by tags',
      requiresArg: true,
      array: true,
      type: 'string',
    }).option('minW', {
      describe: 'Specify the minimum widget width (1-12)',
      group: "Widget Sizes",
      type: 'number',
      requiresArg: true,
      default: 1,
    }).option('minH', {
      describe: 'Specify the minimum widget height (1-36)',
      group: "Widget Sizes",
      type: 'number',
      requiresArg: true,
      default: 1,
    }).option('maxW', {
      describe: 'Specify the maximum widget width (1-12)',
      group: "Widget Sizes",
      type: 'number',
      requiresArg: true,
      default: 12,
    }).option('maxH', {
      describe: 'Specify the maximum widget height (1-36)',
      group: "Widget Sizes",
      type: 'number',
      requiresArg: true,
      default: 36,
    }).option('dep', {
      describe: 'Option format: "<Algorithm|InputBlock>,cid[,gid,version]". Add the option as dependency in the widget meta config.',
      alias: "dependency",
      requiresArg: true,
      type: 'string',
      array: true,
    }).option('prop', {
      describe: 'Option format: "key[,helper][,default]". Add the option as property in the widget meta config.',
      alias: "property",
      requiresArg: true,
      type: 'string',
      array: true,
    }).option('dynamicHeight', {
      describe: 'Indicate that this widget has dynamic height.',
      type: "boolean",
    }).option('force', {
      describe: 'Overwrite existing settings. By default existing settings will not be overwritten.',
      type: "boolean",
    }).option('pluginDir', {
      describe: 'Path to plugin directory',
      type: "string",
      requiresArg: true,
      default: "."
    }).check((argv, options) => {
      // console.log("check", argv, options)
      findPluginRoot(argv);
      if (!validateNumber(argv.minW, 1, 12)) {
        throw new Error(`Invalid minW: ${argv.minW}`)
      }
      if (!validateNumber(argv.minH, 1, 36)) {
        throw new Error(`Invalid minH: ${argv.minH}`)
      }
      if (!validateNumber(argv.maxW, 1, 12)) {
        throw new Error(`Invalid maxW: ${argv.maxW}`)
      }
      if (!validateNumber(argv.maxH, 1, 36)) {
        throw new Error(`Invalid maxH: ${argv.maxH}`)
      }
      if (argv.minW > argv.maxW) {
        throw new Error(`minW cannot be larger than maxW`)
      }
      if (argv.minH > argv.maxH) {
        throw new Error(`minH cannot be larger than maxH`)
      }
      // validate dep arguments
      if (argv.dep) {
        argv._dep = [];
        for (let dep of argv.dep) {
          let words = dep.split(/,/);
          const count = words.length;
          if (count < 2 || count > 4) {
            throw new Error(`Invalid --dep option: ${dep}`)
          }
          if (!["Algorithm","InputBlock"].includes(words[0])) {
            throw new Error(`Invalid --dep option: Please specify "Algorithm" or "InputBlock" for type: ${dep}`)
          }
          if (count==4 && !semver.valid(words[3])) {
            throw new Error(`Invalid --dep option: Please specify a valid version number: ${dep}`)
          }
          argv._dep.push(words);
        }
      }
      // validate prop arguments
      if (argv.prop) {
        argv._prop = [];
        for (let prop of argv.prop) {
          let words = prop.split(/,/);
          const count = words.length;
          if (count < 1 || count > 3) {
            throw new Error(`Invalid --prop option: ${prop}`)
          }
          if (count < 2) {
            words.push(words[0]); // if helper text not set then just set to same as key
          }
          argv._prop.push(words);
        }
      }
      return true;
    })
  }, function (argv) {
    // if (!argv.name)
    //   argv.name = argv.cid;
    generateWidget(argv);
  })
  .command(['generate-inputblock <cid>','gib'], 'Generate skeleton AI Verify input block', (yargs) => {
    yargs.positional('cid', {
      type: 'string',
      describe: 'Input Block Component ID'
    }).option('name', {
      type: 'string',
      describe: 'Input Block name. If not provided will be set to same as cid.',
      requiresArg: true,
    }).option('description', {
      type: 'string',
      describe: 'Input Block description',
      requiresArg: true,
    }).option('group', {
      type: 'string',
      describe: 'Input Block group. Input blocks of the same group name (case-senstive) will be grouped together in the input block list',
      requiresArg: true,
    }).option('width', {
      type: 'string',
      describe: 'Width of input block dialog box. If not specified, dialog default width is md',
      requiresArg: true,
      choices: ["xs", "sm", "md", "lg", "xl"],
    }).option('fullScreen', {
      type: 'boolean',
      describe: 'Whether the input block dialog should be full screen',
    }).option('force', {
      describe: 'Overwrite existing files or settings. By default existing files and settings will not be overwritten.',
      type: "boolean",
    }).option('pluginDir', {
      describe: 'Path to plugin directory',
      type: "string",
      requiresArg: true,
      default: "."
    }).check((argv, options) => {
      // console.log("check", argv, options)
      findPluginRoot(argv);
      return true;
    })
  }, function (argv) {
    // if (!argv.name)
    //   argv.name = argv.cid;
    generateInputBock(argv);
  })
  .command(['generate-algorithm <cid>','ga'], 'Generate skeleton AI Verify algorithm', (yargs) => {
    yargs.positional('cid', {
      type: 'string',
      describe: 'Algorithm Component ID'
    }).option('interactive', {
      type: 'boolean',
      describe: 'Prompt for arguments (will ignore rest of command line options)',
    }).option('author', {
      type: 'string',
      describe: 'Author name',
      requiresArg: true,
      default: "Example Author"
    }).option('pluginVersion', {
      type: 'string',
      describe: 'Plugin version',
      requiresArg: true,
      default: "0.1.0",
    }).option('description', {
      type: 'string',
      describe: 'Algorithm description',
      requiresArg: true,
    }).option('tag', {
      describe: 'Allow users to search and filter by tags',
      requiresArg: true,
      array: true,
      type: 'string',
    }).option('modelSupport', {
      type: 'string',
      describe: 'Algoritm model support',
      choices: ["Classification", "Regression", "Both"],
      default: "Classification",
    }).option('requireGroundTruth', {
      describe: 'Whether this algorithm require ground truth (--no-requireGroundTruth to indicate not required)',
      type: "boolean",
      default: true,
    }).option('pluginDir', {
      describe: 'Path to plugin directory',
      type: "string",
      requiresArg: true,
      default: "."
    }).check((argv, options) => {
      // console.log("check", argv, options)
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    if (!argv.name)
      argv.name = argv.cid;
    if (!argv.description)
      argv.description = argv.name;
    await generateAlgorithm(argv);
  })
  .command('zip [pluginDir]', 'Create the plugin zip file', (yargs) => {
    yargs.positional('pluginDir', {
      type: 'string',
      describe: 'Path to plugin directory',
      requiresArg: true,
      default: "."
    }).option('skip-validation', {
      describe: 'Skip validation',
      type: "boolean",
    // }).option('skip-test', {
    //   describe: 'Skip running the unit tests',
    //   type: "boolean",
    })
    .check((argv, options) => {
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    if (!argv['skip-validation']) {
      if (!(await validatePlugin(argv))) {
        console.error("Invalid plugin");
        process.exit(-1);
      }  
    }
    zipPlugin(argv);
  })
  .command('validate', 'Validate AI Verify plugin', (yargs) => {
    yargs.option('pluginDir', {
      type: 'string',
      describe: 'Path to plugin directory',
      requiresArg: true,
      default: "."
    })
    .check((argv, options) => {
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    if ((await validatePlugin(argv))) {
      console.log("Plugin is valid")
    } else {
      console.log("Plugin is invalid")
    }
  })
  .command(['test-widget', 'testw'], 'Run the plugin tests for widgets and input blocks', (yargs) => {
    yargs.option('pluginDir', {
      type: 'string',
      describe: 'Path to plugin directory',
      requiresArg: true,
      default: "."
    })
    .option('coverage', {
      type: 'boolean',
      alias: "collectCoverage",
      describe: 'Indicates that test coverage information should be collected and reported in the output.',
      default: false,
    })
    .option('listTests', {
      type: 'boolean',
      describe: 'Lists all test files that Jest will run given the arguments, and exits.',
      default: false,
    })
    .option('showConfig', {
      type: 'boolean',
      describe: 'Print your Jest config and then exits.',
      default: false,
    })
    .option('watch', {
      type: 'boolean',
      describe: 'Watch files for changes and rerun tests related to changed files.',
      default: false,
    })
    .option('watchAll', {
      type: 'boolean',
      describe: 'Watch files for changes and rerun all tests when something changes.',
      default: false,
    })
    .option('ci', {
      type: 'boolean',
      describe: 'When this option is provided, Jest will assume it is running in a CI environment.',
      default: false,
    })
    .option('updateSnapshot', {
      type: 'boolean',
      alias: "u",
      describe: 'Use this flag to re-record every snapshot that fails during this test run.',
      default: false,
    })
    .option('json', {
      type: 'boolean',
      describe: 'Prints the test results in JSON. This mode will send all other test output and user messages to stderr.',
      default: false,
    })
    .option('outputFile', {
      type: 'string',
      describe: 'Write test results to a file when the --json option is also specified.',
      requiresArg: true,
    })
    .check((argv, options) => {
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    // console.log("This commmand is not implemented yet.")
    await runTest(argv);
  })
  .command(['test-algorithm', 'testa'], 'Run the plugin tests for algorithms', (yargs) => {
    yargs.option('pluginDir', {
      type: 'string',
      describe: 'Path to plugin directory',
      requiresArg: true,
      default: "."
    })
    .option('silent', {
      type: 'boolean',
      describe: 'Do not display the stdout from the algorithm tests on the console.',
      default: false,
    })
    .check((argv, options) => {
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    // console.log("This commmand is not implemented yet.")
    await runAlgoTests(argv);
  })
  .command('test-all', 'Run all the tests for widgets, input blocks and algorithms with default options', (yargs) => {
    yargs.option('pluginDir', {
      type: 'string',
      describe: 'Path to plugin directory',
      requiresArg: true,
      default: "."
    })
    .check((argv, options) => {
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    // console.log("This commmand is not implemented yet.")
    await runAlgoTests(argv);
    await runTest(argv);
  })
  .command('playground', 'Launch the plugin playround', (yargs) => {
    yargs.option('pluginDir', {
      type: 'string',
      describe: 'Path to plugin directory',
      requiresArg: true,
      default: "."
    })
    yargs.option('port', {
      type: 'number',
      describe: 'Playground port to listen on',
      default: 5000,
      requiresArg: true,
    })
    yargs.option('hostname', {
      type: 'string',
      describe: 'Playground hostname to listen on',
      default: "localhost",
      requiresArg: true,
    })
    .check((argv, options) => {
      findPluginRoot(argv);
      return true;
    })
  }, async function (argv) {
    // console.log("This commmand is not implemented yet.");
    await runPlayground(argv);
  })
  .demandCommand()
  .help()

argv.wrap(argv.terminalWidth()).argv;