# -*- coding: utf-8 -*-
"""
@Time : 2022/7/7 17:52
@Author : name
@File : generator.py
"""
from faker import Factory

fake = Factory().create('zh_CN')


def random_python_data():
    """
    随机生成不同类型的内容
    :return:
    """
    return fake.pystr(), \
           fake.pyint(), \
           fake.pybool(), \
           fake.pyfloat(), \
           fake.pytuple(nb_elements=2), \
           fake.pylist(nb_elements=2), \
           fake.pydict(nb_elements=2)


def random_uuid():
    """
    随机生成不同的uuid
    :return:
    """
    return fake.uuid4()


def random_text(length: int = 200):
    """
    随机生成文本
    :param length:字符个数，最低为5
    :return:
    """
    return fake.text(length)


def random_word(nb: int = 3):
    """
    随机生成词语
    :param nb:词语列表的长度
    :return:
        - fake.word() 2个字的词语
        - fake.words() 词语列表，默认长度为3
    """
    return fake.word(), fake.words(nb)


def random_image_url():
    """
    随机生成url地址，例如：https://placeimg.com/606/228/any
    :return:
    """
    return fake.image_url()


def random_file_path():
    """
    随机生成文件路径，例如：/完成/全国.wav
    :return:
    """
    return fake.file_path()


def random_os_info(os_type: str = 'win'):
    """
    生成不同系统的信息
    :param os_type: 系统类型：win、linux、mac、ios、android
    :return:
    """
    if os_type == 'win':
        return fake.windows_platform_token() + ' ' + fake.linux_processor()
    if os_type == 'linux':
        return fake.linux_processor()
    if os_type == 'mac':
        return fake.mac_platform_token()
    if os_type == 'ios':
        return fake.ios_platform_token()
    if os_type == 'android':
        return fake.android_platform_token()
    return None


def random_name():
    """
    随机生成姓名
    :return:
    """
    return fake.name()


def random_address():
    """
    随机生成地址
    :return:
    """
    return fake.address()


def random_phone_number():
    """
    随机生成移动电话号码
    :return:
    """
    return fake.phone_number()


def random_job():
    """
    随机生成职位
    :return:
    """
    return fake.job()


def random_ssn(min_age: int = 18, max_age: int = 20):
    """
    随机生成一定年龄段区间的身份证号码
    :param min_age:最小年龄
    :param max_age:最大年龄
    :return:
    """
    return fake.ssn(min_age, max_age)


def random_credit_card():
    """
    随机生成银行卡信息：姓名 银行卡
    :return:
    """
    return fake.credit_card_full(), fake.credit_card_number()


def random_company():
    """
    随机生成公司名
    :return:
    """
    return fake.company()


def random_email(domain: dict):
    """
    随机生成邮箱
    :param domain: dict；example：{"domain": "163.com"}
    :return:
    """
    return fake.email(**domain)


def random_birth(minimum_age=18, maximum_age=25):
    """
    随机生成出生日期，explame：2002-08-04
    :param minimum_age:最小年龄
    :param maximum_age:最大年龄
    :return:
    """
    return fake.date_of_birth(minimum_age=minimum_age, maximum_age=maximum_age)


def random_profile():
    """
    随机生成个人信息：explame：{'job': '促销经理', 'company': '雨林木风计算机传媒有限公司', 'ssn': '370214200401072347', 'residence': '甘肃省利县山亭杜路c座 663082', 'current_location': (Decimal('47.3299625'), Decimal('-139.117372')), 'blood_group': 'O+', 'website': ['https://www.rw.cn/', 'http://fangpan.cn/', 'http://www.xiuyingtao.cn/'], 'username': 'yangwen', 'name': '刘慧', 'sex': 'M', 'address': '海南省秀芳市永川杨街Q座 763069', 'mail': 'yan31@yahoo.com', 'birthdate': datetime.date(1966, 3, 12)}
    :return:
    """
    return fake.profile()


def random_ip4(private=False, public=False):
    """
    随机生成ip4
    :param private: 私有
    :param public: 公有
    :return:
    """
    if private:
        return fake.ipv4_private()
    if public:
        return fake.ipv4_public()
    return fake.ipv4()


def random_ip6():
    """
    随机生成ipv6地址
    :return:
    """
    return fake.ipv6()


def random_mac_address():
    """
    随机生成mac地址
    :return:
    """
    return fake.mac_address()


def random_user_agent():
    """
    随机生成浏览器用户代理地址
    :return:
    """
    return fake.user_agent()


def random_mime_type(mime_type: str = 'application'):
    """
    随机生成mime type
    :param mime_type:默认为application
    :return:
    """
    return fake.mime_type(mime_type)





