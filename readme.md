除源代码外，完整服务还需要安装Stable Diffusion WebUI，可以根据下载链接1进行安装，安装完成后开启服务即可。

同时，后端需要下载模型，地址如下载链接2，在下载完成后，将其放在 aigp source/aigp-back/backend/embeddings 里即可。

下面用到的5个文件在onnx-runtime-web依赖包里可以找到，将它们复制进public即可。

```vue
// Set the WebAssembly binary file path to jsdelivr CDN for a specific release version
ort.env.wasm.wasmPaths = {
    'ort-wasm.wasm': '/ort-wasm..wasm',
    'ort-wasm-simd.wasm': '/ort-wasm-simd..wasm',
    'ort-wasm-threaded.wasm': '/ort-wasm-threaded..wasm',
    'ort-wasm-simd-threaded.wasm': '/ort-wasm-simd-threaded..wasm',
};

const MODEL_DIR = '/sam_onnx_quantized_example.onnx';
```



[下载链接1: Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

[下载链接2: sam_vit_h_4b8939.pth](https://huggingface.co/spaces/abhishek/StableSAM/blob/main/sam_vit_h_4b8939.pth)
