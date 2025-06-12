const path = require("node:path");

module.exports = {
  // resolves from test to snapshot path
  resolveSnapshotPath: (testPath, snapshotExtension) => {
    const relpath = path.relative(__dirname, testPath);
    return path.resolve(process.env.pluginDir, relpath.replace('__tests__', '__snapshots__') + snapshotExtension)
  },

  // resolves from snapshot to test path
  resolveTestPath: (snapshotFilePath, snapshotExtension) => {
    const relpath = path.relative(process.env.pluginDir, snapshotFilePath);
    return path.resolve(__dirname,relpath.replace('__snapshots__', '__tests__').slice(0, -snapshotExtension.length))
  },

  // Example test path, used for preflight consistency check of the implementation above
  testPathForConsistencyCheck: __dirname + '/__tests__/example.test.js',
};