const { defineConfig } = require('@vue/cli-service')
const CopyPlugin = require('copy-webpack-plugin');

module.exports = defineConfig({
  transpileDependencies: true,

  pages: {
    index: {
      entry: 'src/main.js',
    },
  },

  lintOnSave: false,

  devServer: {
    proxy: {
      '/sdapi': {
        target: 'http://127.0.0.1:7860',
        changeOrigin: true,
        // pathRewrite: { '^/sdapi': '' },
        ws: true
      },

      '/agapi': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true
      },

      '/static': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true
      },

      '/book/v1': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true
      }
    },

    // 设置正确的 Content-Type 头以提供 .wasm 文件
    headers: {
      // 'Content-Type': 'application/wasm',
      'Cross-Origin-Opener-Policy': 'same-origin',
      'Cross-Origin-Embedder-Policy': 'credentialless'
    },
  },

  configureWebpack: {
    plugins: [
      new CopyPlugin({
        patterns: [
          {
            from: 'node_modules/onnxruntime-web/dist/*.wasm',
            to: '[name]..[ext]',
            globOptions: {
              ignore: ['**/.*'], // 忽略隐藏文件
            },
          },
        ],
      }),
    ],
  },
})
