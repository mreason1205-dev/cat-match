import random
import string

def generate_codes(count=50, length=6):
    codes = []
    for _ in range(count):
        # 生成由大写字母和数字组成的随机码
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        codes.append(code)
    return codes

my_codes = generate_codes(50) # 生成50个
print("请复制下面这些码放到 Streamlit Secrets 里：")
print(my_codes)