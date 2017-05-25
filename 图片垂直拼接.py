from PIL import Image
import os


def get_img_lists():
    base_dir = 'C:\\Users\\ytpc\\Desktop\\python\\oldboy\\spider\\怪奇实录'
    for dir in os.listdir(base_dir):
        image = []
        length = len(os.listdir(base_dir+'\\'+dir))
        for i in range(1, length+1):
            image.append(base_dir + '\\'+dir + '\\'+str(i) + '.jpg')
        yield image


def image_merge(images, output_dir, output_name):
    max_width = 0
    total_height = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > max_width:
                max_width = width
            total_height += height

            # 产生一张空白图
    new_img = Image.new('RGB', (max_width, total_height), 255)
    # 合并
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            new_img.paste(img, (x, y))
            y += height
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path)
    return save_path

# image_merge(images,os.getcwd())

def main():
    for images in get_img_lists():
        print(images)
        image_merge(images,'jpg\\',images[0].split('\\')[-2]+'.jpg')


if __name__ == '__main__':
    main()



# 获取当前目录下文件的个数
# print(len(os.listdir(os.path.dirname(__file__))))
# 获取目录下的文件名
# print(os.listdir(r'C:\Users\ytpc\Desktop\python\oldboy\spider\怪奇实录'))