import { Tensor } from "onnxruntime-web";

export const modelScaleProps = {
    samScale: 0,
    height: 0,
    width: 0,
};

export const modelInputProps = {
    x: 0,
    y: 0,
    clickType: 0,
};

export const modeDataProps = {
    clicks: [],
    tensor: Tensor,
    modelScale: {},
};