# --*-- coding: utf-8 _*_
# @Author   :liyingkun
# @time     :2019/11/13 5:43 下午
# @File     :contactTool.py
# @Software :PyCharm

# -*- coding: utf-8 -*-
from itertools import groupby
import re


class extractor():
    def __init__(self):
        pass

    def extract_email(self, text):
        """
        extract all email addresses from texts<string>
        eg: extract_email('我的email是ifee@baidu.com和dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


        :param: raw_text
        :return: email_addresses_list<list>
        """
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        eng_texts = eng_texts.replace(' at ', '@').replace(' dot ', '.')
        sep = ',!?:; ，。！？《》、|\\/'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

        email_pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+$'

        emails = []
        for eng_text in eng_split_texts:
            result = re.match(email_pattern, eng_text, flags=0)
            if result:
                emails.append(result.string)
        return emails

    def extract_ids(self, text):
        """
        extract all ids from texts<string>
        eg: extract_ids('my ids is 150404198812011101 m and dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


        :param: raw_text
        :return: ids_list<list>
        """
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) == 18]

        id_pattern = r'^[1-9][0-7]\d{4}((19\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(19\d{2}(0[13578]|1[02])31)|(19\d{2}02(0[1-9]|1\d|2[0-8]))|(19([13579][26]|[2468][048]|0[48])0229))\d{3}(\d|X|x)?$'

        phones = []
        for eng_text in eng_split_texts_clean:
            result = re.match(id_pattern, eng_text, flags=0)
            if result:
                phones.append(result.string.replace('+86', '').replace('-', ''))
        return phones

    def replace_chinese(self, text):
        """
        remove all the chinese characters in text
        eg: replace_chinese('我的email是ifee@baidu.com和dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


        :param: raw_text
        :return: text_without_chinese<str>
        """
        if text == '':
            return []
        filtrate = re.compile(u'[\u4E00-\u9FA5]')
        text_without_chinese = filtrate.sub(r' ', text)
        return text_without_chinese

    def extract_cellphone(self, text, nation):
        """
        extract all cell phone numbers from texts<string>
        eg: extract_email('my email address is sldisd@baidu.com and dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')


        :param: raw_text
        :return: email_addresses_list<list>
        """
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) >= 7 and len(ele) < 17]
        if nation == 'CHN':
            phone_pattern = r'^((\+86)?([- ])?)?(|(13[0-9])|(14[0-9])|(15[0-9])|(17[0-9])|(18[0-9])|(19[0-9]))([- ])?\d{3}([- ])?\d{4}([- ])?\d{4}$'

        phones = []
        for eng_text in eng_split_texts_clean:
            result = re.match(phone_pattern, eng_text, flags=0)
            if result:
                phones.append(result.string.replace('+86', '').replace('-', ''))
        return phones

    def get_location(self, word_pos_list):
        """
        get location by the pos of the word, such as 'ns'
        eg: get_location('内蒙古赤峰市松山区')


        :param: word_pos_list<list>
        :return: location_list<list> eg: ['陕西省安康市汉滨区', '安康市汉滨区', '汉滨区']

        """
        location_list = []
        if word_pos_list == []:
            return []

        for i, t in enumerate(word_pos_list):
            word = t[0]
            nature = t[1]
            if nature == 'ns':
                loc_tmp = word
                count = i + 1
                while count < len(word_pos_list):
                    next_word_pos = word_pos_list[count]
                    next_pos = next_word_pos[1]
                    next_word = next_word_pos[0]
                    if next_pos == 'ns' or 'n' == next_pos[0]:
                        loc_tmp += next_word
                    else:
                        break
                    count += 1
                location_list.append(loc_tmp)

        return location_list  # max(location_list)

    def replace_cellphoneNum(self, text):
        """
        remove cellphone number from texts. If text contains cellphone No., the extract_time will report errors.
        hence, we remove it here.
        eg: extract_locations('我家住在陕西省安康市汉滨区，我的手机号是181-0006-5143。')


        :param: raw_text<string>
        :return: text_without_cellphone<string> eg: '我家住在陕西省安康市汉滨区，我的手机号是。'

        """
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) >= 7 and len(ele) < 17]
        for phone_num in eng_split_texts_clean:
            text = text.replace(phone_num, '')
        return text

    def replace_ids(self, text):
        """
        remove cellphone number from texts. If text contains cellphone No., the extract_time will report errors.
        hence, we remove it here.
        eg: extract_locations('我家住在陕西省安康市汉滨区，我的身份证号是150404198412011312。')


        :param: raw_text<string>
        :return: text_without_ids<string> eg: '我家住在陕西省安康市汉滨区，我的身份证号号是。'

        """
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) == 18]

        id_pattern = r'^[1-9][0-7]\d{4}((19\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(19\d{2}(0[13578]|1[02])31)|(19\d{2}02(0[1-9]|1\d|2[0-8]))|(19([13579][26]|[2468][048]|0[48])0229))\d{3}(\d|X|x)?$'
        ids = []
        for eng_text in eng_split_texts_clean:
            result = re.match(id_pattern, eng_text, flags=0)
            if result:
                ids.append(result.string)

        for phone_num in ids:
            text = text.replace(phone_num, '')
        return text

    def most_common(self, content_list):
        """
        return the most common element in a list
        eg: extract_time(['王龙'，'王龙'，'李二狗'])


        :param: content_list<list>
        :return: name<string> eg: '王龙'
        """
        if content_list == []:
            return None
        if len(content_list) == 0:
            return None
        return max(set(content_list), key=content_list.count)


"""
链接 https://github.com/fighting41love/funNLP
    https://github.com/fighting41love/cocoNLP
"""

"""
遇到的问题
jpype._jclass.UnsupportedClassVersionError: org/jpype/classloader/JPypeClassLoader : Unsupported major.minor version 52.0

解决时查看到的帮助：
https://github.com/hankcs/HanLP/issues/1275

jdk13:
https://www.oracle.com/technetwork/java/javase/downloads/jdk13-downloads-5672538.html


"""


####### 有他娘bug，文档与代码不符，需重写

class myextractor(extractor):
    def extract_email(self, text):
        """
        extract all email addresses from texts<string>
        eg: extract_email('我的email是ifee@baidu.com和dsdsd@dsdsd.com,李林的邮箱是eewewe@gmail.com哈哈哈')

        更新了email匹配的正则，之前为
        email_pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+$'

        现在：
        email_pattern = '^[*#\u4e00-\u9fa5 a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'

        :param: raw_text
        :return: email_addresses_list<list>
        """
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        eng_texts = eng_texts.replace(' at ', '@').replace(' dot ', '.')
        sep = '：,!?:; ，。！？《》()、|\\/'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

        email_pattern = '^[*#\u4e00-\u9fa5 a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'

        emails = []
        for eng_text in eng_split_texts:
            result = re.match(email_pattern, eng_text, flags=0)
            if result:
                emails.append(result.string)
        return emails

    def extract_wechat(self, text):
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = '+,!?:; ，。！？《》()（）、|\\/：'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

        wechat_pattern = r'^[a-zA-Z][-_a-zA-Z0-9]{5,19}$'

        wechat = []
        for eng_text in eng_split_texts:
            result = re.match(wechat_pattern, eng_text, flags=0)
            if result:
                wechat.append(result.string)
        return wechat

    def extract_qq(self, text):
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ，。！？《》、|\\/'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

        qq_pattern = r'^[1-9]([0-9]{5,11}$)'

        qq = []
        for eng_text in eng_split_texts:
            result = re.match(qq_pattern, eng_text, flags=0)
            if result:
                qq.append(result.string)
        return qq

    def get_contacts(self, text):
        Dict = {}
        Dict['email'] = self.extract_email(text)
        Dict['contactPhone'] = self.extract_cellphone(text, nation='CHN')
        # Dict['qq'] = self.extract_qq(text)
        # Dict['wechat'] = self.extract_wechat(text)
        return Dict


if __name__ == '__main__':
    text = '急寻特朗普，男孩，于2018年11月27号11时在陕西省安康市汉滨区走失。丢失发型短发，...如有线索，请迅速与警方联系：18100065143，132-6156-2938，baizhantang@sina.com.cn 和yangyangfuture at gmail dot com'

    mex = myextractor()

    text1 = "福景红图(北京)文化发展有限公司  工作邮箱：fotovision@vip.126.com"
    mex.extract_email(text1)

    text2 = "商务合作请联系QQ:3263428560"
    mex.extract_qq(text2)

    text3 = '重庆INS造型创办人，无痕接发导师，网红造型师，发型设计+vx18223754855'
    mex.extract_cellphone(text3, nation='CHN')
    mex.extract_wechat(text3)

    text4 = '关注我的友友记得看我置顶哦，别扒我身份啊，怕怕的，个人微信 a594254610'
    mex.extract_wechat(text4)

    text5="My name means God created the moon to brighten darkness for the world.  Ehh...no pressure right?\n\nInstagram: Youkeyy_\nFacebook: Youkeyy\n\nFor business and PR, please email: hello@youkeyy.com"
    mex.get_contacts(text1)
    mex.get_contacts(text2)
    mex.get_contacts(text3)
    mex.get_contacts(text4)
    mex.get_contacts(text5)
