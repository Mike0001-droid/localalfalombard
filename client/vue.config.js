const webpack = require('webpack');

module.exports = {
    assetsDir: 'assets',
    css: {
        requireModuleExtension: true,
        sourceMap: true
    },
    pluginOptions: {
        lintStyleOnBuild: false,
        stylelint: {
            fix: true,
            files: ['./src/**/*.vue', './src/assets/css/**/*.pcss']
        }
    },
    configureWebpack: config => {
        return {
            node: {
                __filename: true,
                __dirname: true
            },
            plugins: [
                new webpack.NormalModuleReplacementPlugin(/settings$/, function(resource) {
                    resource.request = resource.request.replace(/settings$/, `settings/${process.env.NODE_ENV}`);
                })
            ],
            output: {
                libraryExport: 'default'
            }
        };
    },
    chainWebpack: config => {
      const svgRule = config.module.rule('svg')
  
      // clear all existing loaders.
      // if you don't do this, the loader below will be appended to
      // existing loaders of the rule.
      svgRule.uses.clear()
  
      // add replacement loader(s)
      svgRule
        .use('url-loader')
          .loader('url-loader')
    }
}
