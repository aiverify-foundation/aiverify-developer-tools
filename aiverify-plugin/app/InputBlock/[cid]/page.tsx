import { getMdxWidgetBundle } from 'src/bundler.mjs';
import { listInputBlockCIDs, getComponent, getPluginMeta } from 'src/pluginManager.mjs';
import DisplayInputBlock from './displayInputBlock';
import { inputBlockSchema } from '../../../src/schemas.mjs'

export const dynamicParams = false;

export async function generateStaticParams() {
  const paths = listInputBlockCIDs().map(cid => ({
    cid
  }));
  // console.log("paths", paths);
  return paths;
}

async function getInputBlock(params) {
  const cid = params.cid;
  const inputBlock = getComponent(cid);
  if (!inputBlock) {
    return {
      error: "Input Block not found"
    }
  }
  // const mdxPath = path.join(getWidgetFolder(), `${cid}.mdx`)
	const result = await getMdxWidgetBundle(inputBlock.mdxPath);
  return {
    inputBlock,
    result: result.result,
    error: result.error
  }
}

export default async function Page(props: { params: Promise<{ cid: string }> }) {
  const params = await props.params;
  const pluginMeta = getPluginMeta();
  const { inputBlock, result, error } = await getInputBlock(params);
  if (!result) {
    return (
      <div>Invalid inputBlock</div>
    )
  }

  const { code, frontmatter } = result;
  return (
    <DisplayInputBlock inputBlock={inputBlock} pluginMeta={pluginMeta} code={code} frontmatter={frontmatter} inputBlockSchema={inputBlockSchema} />
  )
}
