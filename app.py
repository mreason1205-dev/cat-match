import streamlit as st
import random

# ================= 1. 基础配置 =================
st.set_page_config(
    page_title="如果你的前世是一只小猫",
    page_icon="🐾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= 2. 交互级 UI 修复 =================
st.markdown("""
<style>
    /* 1. 全局净化 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* 2. 背景设置 (灰蓝渐变) */
    .stApp {
        background-color: #f0f4f8;
        background-image: linear-gradient(180deg, #f0f4f8 0%, #eef2f6 100%);
        background-attachment: fixed;
    }

    /* 3. 进度条 */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%);
        height: 10px;
        border-radius: 5px;
    }

    /* 4. 选项卡片样式 */
    div[role="radiogroup"] > label {
        background-color: #ffffff !important;
        padding: 15px 20px !important;
        border-radius: 12px !important;
        border: 1px solid #eee !important;
        margin-bottom: 12px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        display: flex !important; 
    }
    
    /* 悬停效果 */
    div[role="radiogroup"] > label:hover {
        border-color: #8ec5fc !important;
        background-color: #f8fbff !important;
    }

    /* 5. 题目大卡片容器 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
        border: none !important;
    }

    /* 6. 字体优化 */
    h1, h2, h3, p, div, span, button {
        font-family: "PingFang SC", "Microsoft YaHei", sans-serif !important;
    }
    
    .question-header {
        font-size: 20px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    
    .q-num {
        color: #8ec5fc;
        font-size: 22px;
        margin-right: 10px;
    }

    /* 7. 结果页大数字 */
    .big-score {
        font-size: 60px;
        font-weight: 900;
        color: #8fd3f4;
        text-align: center;
        margin: 5px 0;
        text-shadow: 2px 2px 0px #fff;
    }
    
    /* 8. 强制清除列背景 */
    [data-testid="column"] {
        background: transparent !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. 数据准备 =================
CATS = {
    "Ragdoll": {
        "name": "布偶猫 (Ragdoll)",
        "tags": ["#黏人精", "#颜值天花板", "#贴心小棉袄"],
        "desc": "你的前世一定是只布偶猫。你性格温柔软萌，极度重感情，比起独立闯荡，你更喜欢黏在在意的人身边。你拥有极高的共情能力，是大家公认的“治愈系”存在。",
        "img": "images/buoumao.jpg"
    },
    "SilverShade": {
        "name": "银渐层 (Silver Shade)",
        "tags": ["#优雅贵族", "#有原则", "#高冷范"],
        "desc": "你自带一种与生俱来的优雅气质，像银渐层一样。你既不刻意讨好，也不过分疏离，非常有原则。在陌生环境里你会保持矜持，只有对认可的人才会展示柔软的一面。",
        "img": "images/yinjianceng.jpg"
    },
    "GoldenShade": {
        "name": "金渐层 (Golden Shade)",
        "tags": ["#人间富贵花", "#心态超稳", "#摆烂大爷"],
        "desc": "你就是大家眼中的“小福星”！像金渐层一样，性格圆润，心态超稳。你很少为了不值得的小事内耗，懂得享受生活。做一只快乐的摆烂小猫，是你的人生哲学。",
        "img": "images/jinjianceng.jpg"
    },
    "MaineCoon":{
        "name": "缅因猫 (Maine Coon)",
        "tags": ["#温柔巨人", "#高冷王者", "#安全感"],
        "desc": "你的气场很强，像缅因猫一样给人十足的安全感。不熟悉的人觉得你高冷，但其实你内心住着一个小公主，对认定的人极度忠诚。你是那种能扛事儿的守护者。",
        "img": "images/mianyinmao.jpg"
    },
    "DragonLi": {
        "name": "狸花猫 (Dragon Li)",
        "tags": ["#智商天花板", "#独立酷飒", "#独行侠"],
        "desc": "如果前世是猫，你一定是那只统领街头的狸花猫。你独立、聪明、执行力极强，不需要依附任何人。你享受独处的时光，在工作中往往是那个能解决棘手问题的大神。",
        "img": "images/lihuamao.jpg"
    },
    "Jianzhou": {
        "name": "简州猫 (Jianzhou)",
        "tags": ["#狩猎者", "#强悍实干", "#人狠话不多"],
        "desc": "你像传说中的简州猫一样，低调而强悍。你平时不显山不露水，但关键时刻爆发力惊人。你非常务实，不喜欢花里胡哨的东西，是典型的实干家。",
        "img": "images/jianzhoumao.jpg"
    },
    "BlueWhite": {
        "name": "英短蓝白 (Blue Bicolor)",
        "tags": ["#好奇宝宝", "#永远的少年", "#探险家"],
        "desc": "你的灵魂里住着一个长不大的孩子，像蓝白一样，永远对世界充满好奇。你有点小淘气，喜欢探索新事物。你是朋友圈里的开心果，有你在就不会冷场。",
        "img": "images/yingduanlanbai.jpg"
    },
    "BlueCat": {
        "name": "英短蓝猫 (British Blue)",
        "tags": ["#憨厚老实", "#佛系躺平", "#稳重"],
        "desc": "你像蓝猫一样，给人一种憨厚老实、非常靠谱的感觉。你性格稳重，不容易生气。你比较慢热，不喜欢变动，喜欢安稳、有秩序的慢生活。",
        "img": "images/yingduanlanmao.jpg"
    },
    "Orange": {
        "name": "橘猫 (Orange Tabby)",
        "tags": ["#以大橘为重", "#社交悍匪", "#吃货"],
        "desc": "格局打开！你像大橘一样，心胸宽广，凡事不往心里去。你极具亲和力，朋友遍天下。虽然偶尔想躺平，但对生活的热爱从未减少。你是那种能吃得下饭、睡得着觉的有福之人。",
        "img": "images/jumao.jpg"
    },
    "Sphynx": {
        "name": "无毛猫 (Sphynx)",
        "tags": ["#极度粘人", "#特立独行", "#内心火热"],
        "desc": "你像无毛猫一样特立独行，不在乎世俗的眼光。虽然外表看起来很酷，但其实你内心非常火热，极度渴望亲密关系，对爱人有着毫无保留的依赖。",
        "img": "images/wumaomao.jpg"
    },
    "Calico": {
        "name": "三花猫 (Calico)",
        "tags": ["#傲娇御姐", "#双商在线", "#看心情"],
        "desc": "你像三花猫一样，多数时候聪明且独立。你非常有主见，不会随波逐流。你有点小傲娇，只有对你真正认可的人，才会展示柔软的一面。你的爱是稀缺资源。",
        "img": "images/sanhuamao.jpg"
    },
    "Chinchilla": {
        "name": "金吉拉 (Chinchilla)",
        "tags": ["#精致名媛", "#有洁癖", "#小公主"],
        "desc": "你像金吉拉一样，生活精致，注重细节和仪式感。你对环境的要求比较高，受不了一点脏乱差。你举止优雅，审美在线，是朋友圈里最有品味的那个人。",
        "img": "images/jinjila.jpg"
    },
    "Cow": {
        "name": "奶牛猫 (Tuxedo)",
        "tags": ["#猫中二哈", "#精力过剩", "#脑回路清奇"],
        "desc": "你是独一无二的奶牛猫！脑回路清奇，经常做一些让人意想不到的事。你精力旺盛，是大家的快乐源泉。有你在，生活永远不会无聊，你总能发现生活中的奇奇怪怪。",
        "img": "images/nainiumao.jpg"
    },
    "DevonRex": {
        "name": "德文卷毛猫 (Devon Rex)",
        "tags": ["#机灵小狗", "#古灵精怪", "#反应快"],
        "desc": "你像德文卷毛猫一样，聪明机灵，反应极快。你性格像小狗一样热情，喜欢跟人互动，根本闲不下来。你古灵精怪，总能发现生活中的小乐趣。",
        "img": "images/dewenmao.jpg"
    },
    "Cheese": {
        "name": "起司猫 (Tabby & White)",
        "tags": ["#元气甜心", "#随和", "#适应力强"],
        "desc": "你像起司猫一样，元气满满，乐观向上。你适应能力很强，无论遇到什么困难都能笑着面对。你的笑容很有感染力，就像冬日里的暖阳。",
        "img": "images/qisimao.jpg"
    }
}

# A -> 高冷王者 (Group A)
# B -> 贴心黏人 (Group B)
# C -> 好奇探险 (Group C)
# D -> 摆烂大爷 (Group D)

GROUP_A = ["DragonLi", "MaineCoon", "Jianzhou", "Calico", "SilverShade"]
GROUP_B = ["Ragdoll", "Sphynx", "DevonRex"]
GROUP_C = ["Cow", "BlueWhite", "Cheese"]
GROUP_D = ["Orange", "GoldenShade", "BlueCat", "Chinchilla"]

QUESTIONS = [
    {
        "q": "你最常处于的状态是？", 
        "options": [
            {"txt": "晒太阳发呆，谁叫都纹丝不动", "targets": GROUP_D},
            {"txt": "巡视周边，对风吹草动超敏感", "targets": GROUP_A},
            {"txt": "黏着在意的人求贴贴，离开就不安", "targets": GROUP_B},
            {"txt": "自己玩自己的，偶尔给个眼神已是恩赐", "targets": GROUP_A} 
        ]
    },
    {
        "q": "遇到陌生环境，你的第一反应是？",
        "options": [
            {"txt": "立刻躲起来，观察半小时再试探", "targets": GROUP_B}, 
            {"txt": "竖起耳朵谨慎探索，好奇大于胆怯", "targets": GROUP_C},
            {"txt": "直接找看起来最温柔的人蹭腿求安全感", "targets": GROUP_B},
            {"txt": "无所谓，在哪都能躺，适应力拉满", "targets": GROUP_D}
        ]
    },
    {
        "q": "被人突然抱住，你会？",
        "options": [
            {"txt": "挣扎逃跑，甚至下意识哈气警告", "targets": GROUP_A},
            {"txt": "僵硬 3 秒，确认无危险后慢慢放松", "targets": GROUP_A},
            {"txt": "顺势躺平，还会主动蹭对方求抚摸", "targets": GROUP_B},
            {"txt": "用爪子轻轻推开，保持体面且有距离", "targets": GROUP_D} 
        ]
    },
    {
        "q": "你最喜欢的 “专属小窝” 是？",
        "options": [
            {"txt": "高处（书架顶、窗台、衣柜上）", "targets": GROUP_A},
            {"txt": "封闭空间（纸箱、被窝、小角落）", "targets": GROUP_B},
            {"txt": "人的腿上 / 身边，必须有体温陪伴", "targets": GROUP_B},
            {"txt": "随机切换，哪里舒服躺哪里", "targets": GROUP_D}
        ]
    },
    {
        "q": "玩耍时，你更偏爱哪种类型的玩具？",
        "options": [
            {"txt": "会动的小玩意儿（逗猫棒、激光笔、小飞虫）", "targets": GROUP_C},
            {"txt": "能咬能抓的（猫抓板、磨牙棒、毛线球）", "targets": GROUP_A},
            {"txt": "能抱着睡的（毛绒玩具、小毯子、软抱枕）", "targets": GROUP_B},
            {"txt": "对玩具没兴趣，只喜欢跟 “人” 互动", "targets": GROUP_D}
        ]
    },
    {
        "q": "你的吃饭风格是？",
        "options": [
            {"txt": "细嚼慢咽，每一口都慢慢品，不着急", "targets": GROUP_D},
            {"txt": "狼吞虎咽，吃完还会盯着别人的碗", "targets": GROUP_D},
            {"txt": "必须有人陪才吃，独自吃饭没胃口", "targets": GROUP_B},
            {"txt": "重度挑食，只吃合口味的，不合口直接走", "targets": GROUP_A}
        ]
    },
    {
        "q": "你觉得自己的 “猫毛” 更像哪种质感？",
        "options": [
            {"txt": "短而密，摸起来顺滑像绸缎", "targets": GROUP_A},
            {"txt": "长而软，容易炸毛也容易打结", "targets": GROUP_B},
            {"txt": "卷卷的 / 蓬蓬的，像个小绒球", "targets": GROUP_C},
            {"txt": "薄而短，几乎不用打理，省心型", "targets": GROUP_D}
        ]
    },
    {
        "q": "你的 “猫眼睛” 给人的第一感觉是？",
        "options": [
            {"txt": "圆溜溜的，无辜又天真，惹人疼", "targets": GROUP_B},
            {"txt": "细长的，高冷又神秘，有距离感", "targets": GROUP_A},
            {"txt": "大大的，时刻充满好奇，亮晶晶", "targets": GROUP_C},
            {"txt": "眯眯的，看起来永远没睡醒，佛系感拉满", "targets": GROUP_D}
        ]
    },
    {
        "q": "给自己的 “猫界运动能力” 打个分，更贴近？",
        "options": [
            {"txt": "飞檐走壁，跳高跳远小能手，精力爆棚", "targets": GROUP_C},
            {"txt": "灵活但不爱动，擅长蹲点 “伏击” 小目标", "targets": GROUP_A},
            {"txt": "四肢短萌，跑不快但蹦跶起来超可爱", "targets": GROUP_D},
            {"txt": "佛系躺平，能不动就不动，运动全靠本能", "targets": GROUP_D}
        ]
    },
    {
        "q": "面对陌生的 “同类（陌生人）”，你会？",
        "options": [
            {"txt": "完全无视，自顾自玩，懒得搭理", "targets": GROUP_D},
            {"txt": "先哈气警告，保持距离，再判断是否友好", "targets": GROUP_A},
            {"txt": "主动贴贴示好，想跟所有同类做朋友", "targets": GROUP_C},
            {"txt": "看心情，心情好就凑上去，不好就扭头走", "targets": GROUP_A}
        ]
    },
    {
        "q": "如果 “主人（重要的人）” 出门，你会？",
        "options": [
            {"txt": "在家疯狂拆家，发泄被丢下的不满", "targets": GROUP_C},
            {"txt": "守在门口乖乖等，直到对方回来", "targets": GROUP_B},
            {"txt": "该吃吃该睡睡，完全不在意，自己玩得开心", "targets": GROUP_D},
            {"txt": "到处找对方，发出委屈的叫声，黏人感拉满", "targets": GROUP_B}
        ]
    },
    {
        "q": "你觉得自己的 “猫生使命” 是？",
        "options": [
            {"txt": "做高冷王者，被仰望、被细心伺候", "targets": GROUP_A},
            {"txt": "做贴心小棉袄，被宠爱、陪在主人身边", "targets": GROUP_B},
            {"txt": "做聪明探险家，闯世界、搞点小乐趣", "targets": GROUP_C},
            {"txt": "做摆烂大爷，被投喂、吃睡无忧就够了", "targets": GROUP_D}
        ]
    },
    {
        "q": "面前有一碗小鱼干和一个超舒服的纸箱，你选？",
        "options": [
            {"txt": "先吃光小鱼干，再蜷进纸箱睡大觉", "targets": GROUP_D},
            {"txt": "先蜷进纸箱，小鱼干什么时候吃都一样", "targets": GROUP_D},
            {"txt": "把小鱼干叼进纸箱，边吃边睡，两不误", "targets": GROUP_C},
            {"txt": "对两者都没兴趣，扭头去找主人求贴贴", "targets": GROUP_B}
        ]
    },
    {
        "q": "外面突然下大雨，你在户外，会躲在哪里？",
        "options": [
            {"txt": "车底下，隐蔽又挡风，安全感拉满", "targets": GROUP_A},
            {"txt": "楼道口，既能躲雨，又能观察外面的雨景", "targets": GROUP_A},
            {"txt": "直接冒雨跑回家，找主人求安慰、擦毛毛", "targets": GROUP_B},
            {"txt": "随便找个小水坑踩踩，觉得下雨超好玩", "targets": GROUP_C}
        ]
    },
    {
        "q": "主人给你买了新的猫爬架，你会？",
        "options": [
            {"txt": "立刻爬上去占最高位，宣布这是自己的领地", "targets": GROUP_A},
            {"txt": "小心翼翼绕着看一圈，确认安全再慢慢爬", "targets": GROUP_A},
            {"txt": "拉着主人一起玩，让对方扶着自己爬", "targets": GROUP_B},
            {"txt": "看了一眼，觉得不如沙发舒服，扭头躺平", "targets": GROUP_D}
        ]
    },
    {
        "q": "家里来了一只新的小奶猫，你会？",
        "options": [
            {"txt": "懒得搭理，离得远远的，不跟小屁孩玩", "targets": GROUP_A},
            {"txt": "主动凑上去闻一闻，偶尔还会护着它", "targets": GROUP_B},
            {"txt": "跟小奶猫疯玩，追着跑跳，一起拆家", "targets": GROUP_C},
            {"txt": "觉得它抢了主人的关注，偷偷躲起来生闷气", "targets": GROUP_B}
        ]
    },
    {
        "q": "主人拿着逗猫棒跟你玩，你会？",
        "options": [
            {"txt": "高冷观望，偶尔抬抬爪子，不主动出击", "targets": GROUP_A},
            {"txt": "蹲点伏击，找准时机一跃而起，精准扑抓", "targets": GROUP_A},
            {"txt": "蹦蹦跳跳追着跑，玩到气喘吁吁还不停", "targets": GROUP_C},
            {"txt": "玩了两下就腻了，扭头去吃零食，懒得配合", "targets": GROUP_D}
        ]
    },
    {
        "q": "你不小心把主人的水杯碰倒了，会？",
        "options": [
            {"txt": "立刻溜之大吉，躲起来直到主人消气", "targets": GROUP_C},
            {"txt": "蹲在旁边低头认错，一副可怜兮兮的样子", "targets": GROUP_B},
            {"txt": "用爪子扒拉水杯，觉得洒出来的水超好玩", "targets": GROUP_C},
            {"txt": "无所谓，扭头躺平，反正主人会收拾", "targets": GROUP_D}
        ]
    }
]

# ================= 4. 状态管理 =================
if 'step' not in st.session_state:
    st.session_state.step = 0 
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# ================= 5. 页面逻辑 =================

# --- 0. 激活页 ---
if st.session_state.step == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔮 如果你的前世是一只小猫</h1>", unsafe_allow_html=True)
    st.caption("全网最火 · 灵魂品种测试 · 你的本能反应")
    
    st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800&q=80", use_column_width=True)
    st.markdown("<div style='text-align:center; color:#888; margin-top:10px; font-size:14px'>每只猫的前世，都藏着你的性格底色与生存策略。<br>回答越凭直觉，结果越准，犹豫就会败北～</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<div style='text-align:center; color:#666; margin-bottom:10px;'>🔑 输入激活码解锁测试</div>", unsafe_allow_html=True)
        
        # 激活码输入框
        code_input = st.text_input("激活码", placeholder="请输入激活码", label_visibility="collapsed")
        
        code_clean = code_input.strip()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("开始唤醒 ⚡", type="primary", use_container_width=True):
            try:
                if code_clean in st.secrets["valid_codes"]:
                    st.session_state.step = 1
                    st.rerun() 
                else:
                    st.error("激活码错误或已失效，请检查~")
            except FileNotFoundError:
                if code_clean == "CAT666":
                    st.session_state.step = 1
                    st.rerun()
                else:
                    st.error("激活码错误 (请配置Secrets)")

# --- 1. 答题页 ---
elif st.session_state.step == 1:
    idx = st.session_state.q_index
    q_data = QUESTIONS[idx]
    
    progress = (idx + 1) / len(QUESTIONS)
    st.progress(progress, text=f"灵魂扫描中... {idx + 1}/{len(QUESTIONS)}")
    
    with st.container(border=True):
        st.markdown(f'''
            <div class="question-header">
                <span class="q-num">问题{idx+1}</span> {q_data["q"]}
            </div>
        ''', unsafe_allow_html=True)
        
        options_list = [opt['txt'] for opt in q_data['options']]
        default_index = st.session_state.answers.get(idx, None)
        
        selected_option = st.radio(
            "请选择:", 
            options_list, 
            index=default_index, 
            label_visibility="collapsed"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    current_selection_index = options_list.index(selected_option) if selected_option else None
    
    # 底部按钮逻辑
    if idx == 0:
        if st.button("下一题 ➡️", type="primary", use_container_width=True):
            if current_selection_index is not None:
                st.session_state.answers[idx] = current_selection_index
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.toast('👻 请先选择一个选项哦！', icon="🐾")
    
    else:
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("⬅️ 上一题", type="secondary", use_container_width=True):
                st.session_state.q_index -= 1
                st.rerun()
        
        with c2:
            if idx == len(QUESTIONS) - 1:
                if st.button("查看结果 🚀", type="primary", use_container_width=True):
                    if current_selection_index is not None:
                        st.session_state.answers[idx] = current_selection_index
                        st.session_state.step = 2
                        st.rerun()
                    else:
                        st.toast('👻 请先选择一个选项哦！', icon="🐾")
            else:
                if st.button("下一题 ➡️", type="primary", use_container_width=True):
                    if current_selection_index is not None:
                        st.session_state.answers[idx] = current_selection_index
                        st.session_state.q_index += 1
                        st.rerun()
                    else:
                        st.toast('👻 请先选择一个选项哦！', icon="🐾")

# --- 2. 结果页 ---
elif st.session_state.step == 2:
    st.balloons()
    
    # 1. 统计得分
    final_scores = {k: 0 for k in CATS.keys()}
    for q_i, ans_i in st.session_state.answers.items():
        targets = QUESTIONS[q_i]['options'][ans_i]['targets']
        for cat_key in targets:
            if cat_key in final_scores:
                final_scores[cat_key] += 1

    # 2. 排序
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    top1_key = sorted_scores[0][0]
    top1_score = sorted_scores[0][1]
    top1_cat = CATS[top1_key]
    
    # ================= 核心算法升级 V13.0 =================
    
    # A. 计算“性格纯度” (Dominance Rate)
    # 你的选择中，命中该猫咪的比例是多少？
    # 例如：18题里有12题都指向了这只猫，dominance = 12/18 = 0.66
    dominance_rate = top1_score / 18.0
    
    # B. 基础契合度 (Base Match)
    # 60分起步，每多一点纯度，分数越高。
    # 满分(18/18) -> 60 + 50 = 110 (会被截断到99)
    # 刚及格(5/18) -> 60 + 13.8 = 73.8% (合理的低分)
    # 高分(12/18) -> 60 + 33.3 = 93.3% (合理的高分)
    raw_percentage = 60 + (dominance_rate * 50)
    
    # C. 引入“微扰动” (Micro-Variance)
    # 哪怕得分一样，根据你具体选了哪几个选项，产生一个微小的波动(-1.5% 到 +1.5%)
    # 这样用户觉得“哇，我是93.5%，你是94.2%，好精确！”
    answer_sum = sum(st.session_state.answers.values()) # 选项索引之和
    variance = (answer_sum % 30) / 10.0 - 1.5 # 产生 -1.5 到 1.5 的随机数
    
    final_percentage = min(99.9, max(65.0, raw_percentage + variance))

    # =======================================================

    with st.container(border=True):
        st.markdown("<center style='color:#888; font-size:14px; letter-spacing: 2px;'>你的前世灵魂是</center>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#2c3e50; margin-top:5px; margin-bottom: 5px;'>{top1_cat['name']}</h2>", unsafe_allow_html=True)
        
        # 显示带一位小数的百分比，显得更专业
        st.markdown(f"<div class='big-score'>{final_percentage:.1f}%</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='text-align:center; color:#a1c4fd; font-weight:bold; margin-bottom:20px;'>灵 魂 契 合 度</div>", unsafe_allow_html=True)
        st.image(top1_cat['img'], use_column_width=True)
        st.markdown(f"""
        <div style='text-align:center; margin-top:15px; margin-bottom:15px'>
            {''.join([f'<span class="tag-span">{tag}</span>' for tag in top1_cat['tags']])}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='line-height:1.6; color:#555; text-align:justify;'>{top1_cat['desc']}</div>", unsafe_allow_html=True)
    
    st.markdown("### 🧩 你的其他性格切片")
    
    # 显示第2-4名，分数也动态计算
    for i in range(1, 4):
        key = sorted_scores[i][0]
        score = sorted_scores[i][1]
        cat = CATS[key]
        
        # 次要性格的算法：基于得分比例，但也加一点波动
        sub_dominance = score / 18.0
        sub_match = 40 + (sub_dominance * 50) + variance
        sub_match = min(90, max(20, sub_match)) # 限制在20%-90%之间
        
        with st.container(border=True):
            col_img, col_txt = st.columns([1, 2.5])
            with col_img:
                st.image(cat['img'], use_column_width=True)
            with col_txt:
                st.markdown(f"**{cat['name']}**")
                st.markdown(f"<div style='font-size:12px; color:#999; margin-bottom:5px;'>潜在契合度: {sub_match:.1f}%</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:12px; color:#666;'>{cat['tags'][0]} {cat['tags'][1]}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 转世重修 (重测)", type="primary", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.q_index = 0
        st.rerun()