import base64

def handle_jpg_to_py(picture_name):
    """
    将jpg图像文件转换为py文件
    :param picture_name:
    :return:
    """
    open_jpg = open('%s.jpg' % picture_name, 'rb')
    b64str = base64.b64encode(open_jpg.read())
    open_jpg.close()
    # 注意这边b64str一定要加上.decode()
    write_data = 'img = "%s"' % b64str.decode()
    f = open('%s.py' % picture_name, 'w+')
    f.write(write_data)
    f.close()

if __name__ == '__main__':
    pictrue = "crane"
    handle_jpg_to_py(pictrue)