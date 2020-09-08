# -*- coding:utf-8 -*-
import pathlib
import imageio
import logger
from os import makedirs, listdir, remove
from os.path import exists, join
from enum import Enum
from PIL import Image, ImageFont, ImageDraw

root_path = pathlib.Path(__file__).parent.absolute()


class Chars(Enum):
    # ASCII 字符列表，效果会有一些差别，根据自己喜好选择
    CHARS_17 = """#8XOHLTI)i=+;:,. """
    CHARS_19 = """MNHQ$OC67)oa+>!:+. """
    CHARS_71 = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`''. """


class AsciiImage:
    def __init__(self, ascii_chars=Chars.CHARS_71):
        self.ascii_chars = ascii_chars.value
        self.input_path = join(root_path, "input_images")
        self.output_path = join(root_path, "output_images")
        self.temp_output_path = join(root_path, "temp_output")
        self.init()

    def init(self):
        if not exists(self.input_path):
            makedirs(self.input_path)

        if not exists(self.output_path):
            makedirs(self.output_path)

        if not exists(self.temp_output_path):
            makedirs(self.temp_output_path)

    def get_ascii_char(self, r, g, b, alpha=256):
        """
        根据颜色值及alpha通道，选择并返回合适的ascii字符
        :param r: 红色分量
        :param g: 绿色分量
        :param b: 蓝色分量
        :param alpha: alpha通道值
        :return: ascii 字符
        """
        if alpha == 0:
            return " "
        length = len(self.ascii_chars)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 灰度公式
        unit = (256.0 + 1) / length

        return self.ascii_chars[int(gray / unit)]

    def create_ascii_picture(self, file_name: str, zoom=1, colorful=True, save_txt=False):
        """
        创建彩色、黑白字符画图片和文本字符画
        :param src: 需要处理的图像文件名
        :param des: 输出文件名
        :param zoom: 缩放倍数，可以是小数
        :param colorful: 是否是彩色，默认是彩色，设成False则为黑白
        :param save_txt: 是否保存文本
        :return:
        """
        input_image_path = join(self.input_path, file_name)
        # image = Image.open(input_image_path)

        # 强制转换成彩色图
        image = Image.open(input_image_path).convert('RGB')
        image_txt, txt = self.create_ascii_image(image, zoom=zoom, colorful=colorful)

        output_image_path = join(self.output_path, file_name)
        image_txt.save(output_image_path)

        if save_txt:
            txt_file_name = file_name.split(".")[0] + '.txt'
            with open(join(self.output_path, txt_file_name), 'w') as f:
                f.write(txt)

    def create_ascii_image(self, src: Image, zoom=1, colorful=True):
        """
        创建彩色、黑白字符画图片和文本字符画
        :param src: 需要处理的图片文件对象
        :param zoom: 缩放倍数，可以是小数
        :param colorful: 是否是彩色，默认是彩色，设成False则为黑白
        :return: tuple 对象，第一个值是处理后的图像文件对象
        """
        width = int((src.width / 6) * zoom)  # 宽度比例为原图的1/6较好，字体宽度的原因
        height = int((src.height / 15) * zoom)  # 高度比例为原图1/15较好，字体宽度的原因

        des_image = Image.new("RGB", (int(src.width * zoom), int(src.height * zoom)), (255, 255, 255))

        # RGBA 模式
        # image_txt = Image.new("RGBA", (int(src.width * zoom), int(src.height * zoom)), (255, 255, 255, 0))

        im = src.resize((width, height), Image.ANTIALIAS)
        txt = ""
        colors = []
        for i in range(height):
            for j in range(width):
                pixel = im.getpixel((j, i))
                colors.append((pixel[0], pixel[1], pixel[2]))  # 记录像素颜色信息
                if len(pixel) == 4:
                    txt += self.get_ascii_char(pixel[0], pixel[1], pixel[2], pixel[3])
                else:
                    txt += self.get_ascii_char(pixel[0], pixel[1], pixel[2])
            txt += "\n"
            colors.append((100, 100, 100))
        dr = ImageDraw.Draw(des_image)
        font = ImageFont.load_default().font  # 获取字体
        x = y = 0
        font_w, font_h = font.getsize(txt[0])  # 获取字体高和宽
        font_h *= 1.37
        # ImageDraw为每个ascii码上色
        for i in range(len(txt)):
            if txt[i] == "\n":
                x += font_h
                y = font_w
            if colorful:
                dr.text([y, x], txt[i], colors[i])
            else:
                dr.text([y, x], txt[i], (0, 0, 0))  # 黑白
            y += font_w

        return des_image, txt

    def del_files(self, path):
        ls = listdir(path)
        for i in ls:
            c_path = join(path, i)
            remove(c_path)

    def create_frames(self, file_name, zoom, colorful, ascii_pic=True):
        """
        按帧拆分gif图，分别处理成单独的静态字符画
        :param file_name: 需要处理的动态gif图文件名
        :param zoom: 缩放倍数
        :param colorful: 是否处理成彩色，False为黑白
        :param ascii_pic: 是否处理成ASCII字符图
        :return:
        """
        input_image_path = join(self.input_path, file_name)
        gif_img = Image.open(input_image_path)

        # 保存播放时间间隔
        duration = gif_img.info.get("duration", 0)
        with open(join(self.temp_output_path, "duration.txt"), 'w') as f:
            f.write(str(duration))

        # 保存帧数信息
        frames = gif_img.n_frames
        with open(join(self.temp_output_path, "frames.txt"), 'w') as f:
            f.write(str(frames))

        for i in range(frames):
            # lx = gif_img.tell()
            gif_img.seek(i)
            logger.info("处理第{0}帧".format(i + 1))
            frame = gif_img.convert("RGB")

            if ascii_pic:
                image, txt = self.create_ascii_image(frame, zoom=zoom, colorful=colorful)
                image.save(join(self.temp_output_path, str(i) + ".png"))
            else:
                frame.save(join(self.temp_output_path, str(i) + ".png"))

        logger.info("所有帧均处理完成")

    def merge_frames(self, output_file_name: str):
        """
        将中间输出文件全部合，生成动态gif图
        :param output_file_name: 最终输出的gif文件名
        :return:
        """
        logger.info("合并生成gif图")
        with open(join(self.temp_output_path, "frames.txt"), 'r') as f:
            frames_amount = int(f.read())

        frames = []
        for i in range(frames_amount):
            frames.append(imageio.imread(join(self.temp_output_path, str(i) + ".png")))

        duration = 0.015
        with open(join(self.temp_output_path, "duration.txt"), 'r') as f:
            duration = float(f.read()) / 1000

        imageio.mimsave(join(self.output_path, output_file_name), frames, 'GIF', duration=duration)

        logger.info(f"动态字符图片{output_file_name}生成完毕")

    def create_ascii_gif(self, src_file_name, zoom=1, colorful=True):
        """
        创建gif动态字符画
        :param src_file_name: 需要处理的原始gif图文件名
        :param zoom: 缩放倍数
        :param colorful: 是否生成彩色图
        :return:
        """
        # 清空文件夹
        self.del_files(self.temp_output_path)

        # 拆分gif，每帧创建一张字符画
        self.create_frames(src_file_name, zoom=zoom, colorful=colorful, ascii_pic=True)

        # 合并所有帧，生成gif图
        self.merge_frames(src_file_name)

    def run_samples(self):
        # self.create_ascii_picture("Sheeta.jpeg", zoom=4, colorful=True)
        #self.create_ascii_picture("Sheeta.jpeg", zoom=10, colorful=False)
        # self.create_ascii_picture("GongXiFaCai.png", zoom=1, save_txt=True, colorful=False)
        self.create_ascii_gif("Agnes.gif", zoom=10)
        # self.create_ascii_gif("Cat.gif", zoom=10)


if __name__ == "__main__":
    ai = AsciiImage()
    ai.run_samples()
