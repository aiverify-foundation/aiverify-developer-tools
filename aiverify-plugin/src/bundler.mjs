import {bundleMDX} from 'mdx-bundler';
import remarkMdxImages from 'remark-mdx-images';
import remarkGfm from 'remark-gfm';
import { getPluginDir } from './pluginManager.mjs';

export async function getMdxWidgetBundle (mdxPath) {
	try {
		const result = await bundleMDX({
			cwd: getPluginDir(),
			file: mdxPath,
			mdxOptions: options => {
				options.remarkPlugins = [...(options.remarkPlugins ?? []), remarkMdxImages, remarkGfm]
				return options
			},
			esbuildOptions: options => {
				options.loader = {
					...options.loader,
					'.png': 'dataurl',
				}
				return options
			},
		})
		return {
			result
		};	
	} catch (e) {
		console.error("Error loading MDX", mdxPath, e);
		return {
			error: e,
		};
	}
}