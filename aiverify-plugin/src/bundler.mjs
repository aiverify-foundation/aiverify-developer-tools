import { bundleMDX } from "mdx-bundler";
import rehypeMdxImportMedia from "rehype-mdx-import-media";
import remarkGfm from "remark-gfm";
import { getPluginDir } from "./pluginManager.mjs";
import path from "path";

export async function getMdxWidgetBundle(mdxPath) {
  try {
	const pluginDir = getPluginDir()
    const result = await bundleMDX({
      cwd: pluginDir,
      file: mdxPath,
      mdxOptions: (options) => {
        options.remarkPlugins = [...(options.remarkPlugins ?? []), remarkGfm];
        options.rehypePlugins = [
          ...(options.rehypePlugins ?? []),
          rehypeMdxImportMedia,
        ];
        return options;
      },
      esbuildOptions: (options) => {
        options.loader = {
          ...options.loader,
          ".png": "dataurl",
        };
		options.nodePaths = [path.resolve(pluginDir, "node_modules")];
        return options;
      },
    });
    return {
      result,
    };
  } catch (e) {
    console.error("Error loading MDX", mdxPath, e);
    return {
      error: e,
    };
  }
}
