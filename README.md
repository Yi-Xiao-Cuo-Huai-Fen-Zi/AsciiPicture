# AsciiPicture
基于 [Pillow](https://github.com/python-pillow/Pillow) 和 [imageio](https://github.com/imageio/imageio) 实现的将图片处理成字符图的脚本。

下面是样例，原始图片存在于 [input_images](https://github.com/Yi-Xiao-Cuo-Huai-Fen-Zi/AsciiPicture/tree/master/input_images) 目录下。
### 处理静态图
原始图片：

![Sheeta.jpeg](https://github.com/Yi-Xiao-Cuo-Huai-Fen-Zi/AsciiPicture/blob/master/input_images/Sheeta.jpeg)
##### 彩色：

处理代码：
```python
ai = AsciiImage()
ai.create_ascii_picture("Sheeta.jpeg", zoom=4, colorful=True)
``` 
处理后：

![Sheeta_colorful.jpeg](https://github.com/Yi-Xiao-Cuo-Huai-Fen-Zi/AsciiPicture/blob/master/output_images/Sheeta_colorful.jpeg)
##### 黑白：
处理代码：
```python
ai = AsciiImage()
ai.create_ascii_picture("Sheeta.jpeg", zoom=4, colorful=False)
```
处理后：

![Sheeta_gray.jpeg](https://github.com/Yi-Xiao-Cuo-Huai-Fen-Zi/AsciiPicture/blob/master/output_images/Sheeta_gray.jpeg)
### 处理动态图：
原始图片：

![Agnes.gif](https://github.com/Yi-Xiao-Cuo-Huai-Fen-Zi/AsciiPicture/blob/master/input_images/Agnes.gif)

处理代码：
```python
ai = AsciiImage()
ai.create_ascii_gif("Agnes.gif", zoom=5)
```

处理后：
![Agnes.gif](https://github.com/Yi-Xiao-Cuo-Huai-Fen-Zi/AsciiPicture/blob/master/output_images/Agnes.gif)