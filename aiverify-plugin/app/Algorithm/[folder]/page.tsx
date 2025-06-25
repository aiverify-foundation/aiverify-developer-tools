import { getMdxWidgetBundle } from 'src/bundler.mjs';
import { listAlgorithms, getAlgorithm, getPluginMeta } from 'src/pluginManager.mjs';
import DisplayAlgorithm from './displayAlgorithm';
import { algorithmSchema } from 'src/schemas.mjs'



export const dynamicParams = false;

export async function generateStaticParams() {
  const paths = listAlgorithms().map(algo => ({
    folder: algo.folder
  }));
  return paths;
}

function readAlgo(params) {
  const folder = params.folder;
  const algo = getAlgorithm(folder);
  if (!algo) {
    return {
      error: "Algorithm not found"
    }
  }
  return algo;
}

export default async function Page(props: { params: Promise<{ cid: string }> }) {
  const params = await props.params;
  const pluginMeta = getPluginMeta();
  const algo = readAlgo(params);

  return (
    <DisplayAlgorithm algorithm={algo} pluginMeta={pluginMeta} algorithmSchema={algorithmSchema} />
  )
}
