# 通用OCR服务

## 原理

基于Flask+PaddleOCR实现

服务支持Swagger接口文档

## 配置

configs/dev 为开发配置。

因为代码中的日志系统会将日志存入MongoDB中，所以你需要配置MongoDB的账号密码。

## 运行

```shell
python main.py
```

## 使用

进入tests目录下：

- test_img_ocr.py: 提供了2种使用方法
- test_ocr_model.py: 提供了PaddleOCR的基本使用方式

你可以运行IMGOCR服务，然后执行：

```shell
python test_img_ocr.py
```
