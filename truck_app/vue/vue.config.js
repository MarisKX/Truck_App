const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    entry: "./src/main.js",
    devServer: {
      hot: true,
      port: 8095,
      host: '0.0.0.0',
    },
    watchOptions: {
      ignored: /node_modules/,
      poll: 1000,
    }
  }
})