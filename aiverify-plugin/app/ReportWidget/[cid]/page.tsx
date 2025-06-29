import { getMdxWidgetBundle } from 'src/bundler.mjs';
import { listWidgetCIDs, getComponent, getPluginMeta } from 'src/pluginManager.mjs';
import { reportWidgetSchema } from '../../../src/schemas.mjs'
import DisplayWidget from './displayWidget';

export const dynamicParams = false;

export async function generateStaticParams() {
  const paths = listWidgetCIDs().map(cid => ({
    cid
  }));
  // console.log("paths", paths);
  return paths;
}

async function getWidget(params) {
  const cid = params.cid;
  const widget = getComponent(cid);
  if (!widget) {
    return {
      error: "Widget not found"
    }
  }
  // const mdxPath = path.join(getWidgetFolder(), `${cid}.mdx`)
	const result = await getMdxWidgetBundle(widget.mdxPath);
  return {
    widget,
    result: result.result,
    error: result.error
  }
}

export default async function Page(props: { params: Promise<{ cid: string }> }) {
  const params = await props.params;
  const pluginMeta = getPluginMeta();
  const { widget, result, error } = await getWidget(params);
  if (!result) {
    return (
      <div>Invalid widget</div>
    )
  }

  // compute property values
  console.log("properties", widget.meta.properties)
  if (widget.meta.properties && widget.meta.properties.length > 0) {
    const initialValues = {};
    widget.meta.properties.forEach((prop) => {
      initialValues[prop.key] =
        prop.value !== undefined ? prop.value : prop.default;
    });
    widget.initialPropertyValues = initialValues
  } else {
    widget.initialPropertyValues = {}
  }
  
  
  const { code, frontmatter } = result;
  return (
    <DisplayWidget widget={widget} pluginMeta={pluginMeta} code={code} frontmatter={frontmatter} reportWidgetSchema={reportWidgetSchema} />
  )
}
