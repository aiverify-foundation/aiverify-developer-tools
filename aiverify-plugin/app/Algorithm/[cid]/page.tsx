import { getMdxWidgetBundle } from 'src/bundler.mjs';
import { listAlgorithmsCIDs, getAlgorithm, getPluginMeta } from 'src/pluginManager.mjs';
import DisplayAlgorithm from './displayAlgorithm';

export const dynamicParams = false;

export async function generateStaticParams() {
  const paths = listAlgorithmsCIDs().map(cid => ({
    cid
  }));
  // console.log("paths", paths);
  return paths;
}

function readAlgo(params) {
  const cid = params.cid;
  const algo = getAlgorithm(cid);
  if (!algo) {
    return {
      error: "Algorithm not found"
    }
  }
  return algo;
}

export default async function Page({params}: { params: { cid: string } }) {
  const pluginMeta = getPluginMeta();
  const algo = readAlgo(params);

  return (
    <DisplayAlgorithm algorithm={algo} pluginMeta={pluginMeta} />
  )
}
