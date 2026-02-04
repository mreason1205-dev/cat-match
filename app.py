import streamlit as st
import random

# ================= 1. 基础配置 =================
st.set_page_config(
    page_title="喵星人性格鉴定局 V4.0",
    page_icon="🐱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= 2. 商业级 UI 样式 (保持清新风) =================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #f7f9fc;
    }

    /* 进度条 */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff9a9e, #fad0c4);
    }

    /* 选项按钮 */
    .stButton > button {
        background-color: white;
        color: #4a4a4a;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px 20px;
        font-size: 16px;
        width: 100%;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #fff0f5;
        border-color: #ff9a9e;
        color: #ff6b81;
        transform: scale(1.01);
    }
    
    /* 结果页标签 */
    .tag {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 13px;
        margin-right: 5px;
        display: inline-block;
        margin-bottom: 5px;
    }

    /* 次要结果卡片 */
    .sub-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .sub-card img {
        border-radius: 8px;
        width: 60px;
        height: 60px;
        object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. 核心数据 (15种猫) =================

CATS = {
    # --- 热门组 ---
    "Ragdoll": {
        "name": "仙女本仙·布偶猫",
        "tags": ["#粘人精", "#颜值天花板", "#玻璃心"],
        "desc": "你像布偶猫一样，拥有极高的共情能力和温柔的内心。你非常重感情，愿意为了喜欢的人付出一切。虽然偶尔会因为敏感而感到委屈，但你的温柔是治愈世界的良药。",
        "img": "images/buoumao.jpg"
    },
    "SilverShade": {
        "name": "优雅贵族·银渐层",
        "tags": ["#优雅", "#小脾气", "#颜值正义"],
        "desc": "你像银渐层一样，自带一种优雅的贵族气质。你性格温和但有原则，不会随意对人敞开心扉，但一旦接纳了对方，就会变得非常可爱。",
        "img": "images/yinjianceng.jpg"
    },
    "GoldenShade": {
        "name": "人间富贵花·金渐层",
        "tags": ["#圆润", "#好脾气", "#招财体质"],
        "desc": "你就是人见人爱的金渐层！性格圆润（无论是身材还是脾气），非常讨喜。你心态超好，很少内耗，总能给身边的人带来福气和快乐。",
        "img": "images/jinjianceng.jpg"
    }, # <--- 修复点：帮你加上了逗号，关好了门
    
    # --- 霸气/独立组 ---
    "MaineCoon":{
        "name": "温柔巨人·缅因猫",
        "tags": ["#安全感", "#外冷内热", "#忠诚"],
        "desc": "你拥有强大的气场，像缅因猫一样给人十足的安全感。外表可能看起来有点高冷或霸气，但内心其实住着一个小公举，对认定的人极度温柔忠诚。",
        "img": "images/mianyinmao.jpg"
    },
    "DragonLi": {
        "name": "中华战神·狸花猫",
        "tags": ["#智商超群", "#独立", "#业务能力强"],
        "desc": "你像狸花猫一样，独立、聪明、执行力极强。你不需要依附任何人，有极强的生存能力。在工作中你往往是那个能解决棘手问题的大神。",
        "img": "images/lihuamao.jpg" # <--- 修复点：删掉了多余的 "img":
    },
    "Jianzhou": {
        "name": "四耳神喵·简州猫",
        "tags": ["#狩猎者", "#低调", "#强悍"],
        "desc": "你像传说中的简州猫一样，低调而强悍。你平时不显山不露水，但关键时刻爆发力惊人。你非常务实，不喜欢花里胡哨的东西，是典型的实干家。",
        "img": "images/jianzhoumao.jpg"
    },

    # --- 英短家族 ---
    "BlueWhite": {
        "name": "甜美正太·英短蓝白",
        "tags": ["#好奇宝宝", "#尴尬期尴尬", "#活泼"],
        "desc": "你像蓝白一样，性格活泼开朗，总是对世界充满好奇。你有点小淘气，但因为长得可爱，总能被原谅。你是大家眼中的开心果。",
        "img": "images/yingduanlanbai.jpg"
    },
    "BlueCat": {
        "name": "蓝胖子·英短蓝猫",
        "tags": ["#憨厚", "#记仇", "#尤其是吃"],
        "desc": "你像蓝猫一样，给人一种憨厚老实的感觉。你性格稳重，不容易生气（除非抢你的吃的）。你比较慢热，喜欢安稳的生活节奏。",
        "img": "images/yingduanlanmao.jpg"
    },

    # --- 特色组 ---
    "Orange": {
        "name": "以大橘为重·橘猫",
        "tags": ["#干饭王", "#心宽体胖", "#社交牛逼症"],
        "desc": "格局打开！你像大橘一样，心胸宽广，凡事不往心里去。你极具亲和力，朋友遍天下。虽然偶尔想躺平，但对生活的热爱从未减少。",
        "img": "images/jumao.jpg"
    },
    "Sphynx": {
        "name": "外星来客·无毛猫",
        "tags": ["#极度粘人", "#特立独行", "#体温高"],
        "desc": "你像无毛猫一样特立独行，不在乎世俗的眼光。虽然外表看起来很酷，但其实你内心非常火热，极度渴望亲密关系，是真正的“粘人精”。",
        "img": "images/wumaomao.jpg" # <--- 修复点：修正了图片路径格式
    },
    "Calico": {
        "name": "幸运女神·三花猫",
        "tags": ["#傲娇", "#聪明", "#猫中御姐"],
        "desc": "你像三花猫一样，多数时候聪明且独立。你非常有主见，不会随波逐流。你有点小傲娇，只有对你真正认可的人，才会展示柔软的一面。",
        "img": "images/sanhuamao.jpg" # <--- 修复点：修正了图片路径格式
    },
    "Chinchilla": {
        "name": "精致名媛·金吉拉",
        "tags": ["#精致", "#有洁癖", "#小公主"],
        "desc": "你像金吉拉一样，生活精致，注重细节。你对环境的要求比较高，受不了一点脏乱差。你举止优雅，是朋友圈里最有品味的那个人。",
        "img": "images/jinjila.jpg" # <--- 修复点：修正了图片路径格式
    },
    "Cow": {
        "name": "猫中二哈·奶牛猫",
        "tags": ["#神经质", "#精力过剩", "#搞笑女/男"],
        "desc": "你是独一无二的奶牛猫！脑回路清奇，经常做一些让人意想不到的事。你精力旺盛，是大家的快乐源泉。有你在，生活永远不会无聊。",
        "img": "images/nainiumao.jpg"
    },
    "DevonRex": {
        "name": "落入凡间的小精灵·德文",
        "tags": ["#机灵", "#像狗一样", "#古灵精怪"],
        "desc": "你像德文卷毛猫一样，聪明机灵，反应极快。你性格像小狗一样热情，喜欢跟人互动。你古灵精怪，总能发现生活中的小乐趣。",
        "img": "images/dewenmao.jpg"
    },
    "Cheese": {
        "name": "甜心宝贝·起司猫",
        "tags": ["#元气", "#随和", "#乐天派"],
        "desc": "你像美短加白（起司猫）一样，元气满满，乐观向上。你适应能力很强，无论遇到什么困难都能笑着面对。你的笑容很有感染力。",
        "img": "images/qisimao.jpg"
    }
} # <--- 修复点：这里原来是大括号没对齐，现在帮你关好了！

# 4. 题库 (12道精准题，覆盖15种猫)
QUESTIONS = [
    {
        "q": "1. 周末早晨，你通常会？",
        "options": [
            {"txt": "睡到自然醒，赖床玩手机", "targets": ["GoldenShade", "Orange", "BlueCat", "SilverShade"]},
            {"txt": "早起运动/收拾屋子，精力充沛", "targets": ["DragonLi", "Jianzhou", "Cow", "DevonRex"]},
            {"txt": "必须找人贴贴/聊天才能起床", "targets": ["Ragdoll", "Sphynx", "Siamese", "DevonRex"]},
            {"txt": "按计划起床，做个精致早餐", "targets": ["Chinchilla", "MaineCoon", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "2. 朋友突然放鸽子，你的反应是？",
        "options": [
            {"txt": "无所谓，刚好自己宅着", "targets": ["BlueCat", "Orange", "SilverShade"]},
            {"txt": "有点生气，需要哄", "targets": ["Calico", "Chinchilla", "Ragdoll"]},
            {"txt": "立刻改约别人，绝不浪费时间", "targets": ["DragonLi", "Jianzhou", "Cow"]},
            {"txt": "正好去做自己想做的事，很独立", "targets": ["MaineCoon", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "3. 你更喜欢哪种穿衣风格？",
        "options": [
            {"txt": "舒适宽松，怎么舒服怎么来", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "精致优雅，注重搭配细节", "targets": ["Chinchilla", "SilverShade", "Ragdoll"]},
            {"txt": "个性潮牌，与众不同", "targets": ["Sphynx", "Cow", "DevonRex"]},
            {"txt": "简约干练，方便活动", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]}
        ]
    },
    {
        "q": "4. 在社交场合中，你是？",
        "options": [
            {"txt": "全场焦点，社牛本牛", "targets": ["Cow", "DevonRex", "Orange"]},
            {"txt": "只跟熟人聊，生人勿近", "targets": ["Calico", "DragonLi", "SilverShade"]},
            {"txt": "温和的倾听者，微笑回应", "targets": ["GoldenShade", "BlueCat", "Ragdoll"]},
            {"txt": "游刃有余，照顾每个人的感受", "targets": ["MaineCoon", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "5. 遇到困难时，你会？",
        "options": [
            {"txt": "找人撒娇求助，抱大腿", "targets": ["Ragdoll", "Sphynx", "Chinchilla"]},
            {"txt": "自己死磕，绝不认输", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "先吃顿好的，明天再说", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "另辟蹊径，用奇怪的方法解决", "targets": ["Cow", "DevonRex", "Cheese"]}
        ]
    },
    {
        "q": "6. 对于“粘人”这件事，你怎么看？",
        "options": [
            {"txt": "我是粘人精，分开一秒都难受", "targets": ["Sphynx", "Ragdoll", "DevonRex"]},
            {"txt": "看心情，想理你才理你", "targets": ["Calico", "SilverShade", "BlueCat"]},
            {"txt": "不需要太粘，有各自空间最好", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "刚刚好，互相陪伴", "targets": ["GoldenShade", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "7. 你的体型/身材管理观念是？",
        "options": [
            {"txt": "心宽体胖，能吃是福", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "天生丽质，无需刻意管理", "targets": ["Ragdoll", "Chinchilla", "BlueWhite"]},
            {"txt": "精壮结实，充满力量感", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "身材苗条/独特", "targets": ["Sphynx", "DevonRex", "Calico"]}
        ]
    },
    {
        "q": "8. 你觉得自己像什么动物？",
        "options": [
            {"txt": "狗狗 (忠诚、热情)", "targets": ["MaineCoon", "DevonRex", "Sphynx"]},
            {"txt": "老虎/狮子 (霸气、独立)", "targets": ["DragonLi", "Jianzhou", "Calico"]},
            {"txt": "考拉/熊猫 (懒、可爱)", "targets": ["GoldenShade", "BlueCat", "Orange"]},
            {"txt": "猴子/哈士奇 (皮、活泼)", "targets": ["Cow", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "9. 你对生活环境的要求？",
        "options": [
            {"txt": "必须干净整洁，有洁癖", "targets": ["Chinchilla", "SilverShade", "Calico"]},
            {"txt": "舒服就行，稍微乱点也没事", "targets": ["Orange", "GoldenShade", "Cheese"]},
            {"txt": "只要有张床，哪里都能睡", "targets": ["BlueCat", "Cow", "BlueWhite"]},
            {"txt": "喜欢高处，视野要好", "targets": ["DragonLi", "MaineCoon", "Jianzhou"]}
        ]
    },
     {
        "q": "10. 被人误解时，你会？",
        "options": [
            {"txt": "极力辩解，必须说清楚", "targets": ["DevonRex", "Sphynx", "Cow"]},
            {"txt": "懒得解释，爱咋咋地", "targets": ["DragonLi", "Calico", "SilverShade"]},
            {"txt": "委屈巴巴，自己生闷气", "targets": ["Ragdoll", "Chinchilla", "BlueCat"]},
            {"txt": "用行动证明自己", "targets": ["MaineCoon", "Jianzhou", "GoldenShade"]}
        ]
    },
    {
        "q": "11. 你更喜欢哪种类型的伴侣？",
        "options": [
            {"txt": "能照顾我的，宠我的", "targets": ["Ragdoll", "Chinchilla", "Sphynx"]},
            {"txt": "势均力敌的，能一起进步的", "targets": ["DragonLi", "MaineCoon", "Jianzhou"]},
            {"txt": "有趣的，能玩到一起的", "targets": ["Cow", "DevonRex", "Cheese"]},
            {"txt": "情绪稳定的，包容性强的", "targets": ["GoldenShade", "BlueCat", "SilverShade"]}
        ]
    },
    {
        "q": "12. 最后一个问题，你最想要什么超能力？",
        "options": [
            {"txt": "读心术 (懂人心)", "targets": ["Ragdoll", "Calico", "SilverShade"]},
            {"txt": "瞬间移动 (自由)", "targets": ["DragonLi", "Jianzhou", "Cow"]},
            {"txt": "力大无穷/守护 (力量)", "targets": ["MaineCoon", "BlueCat"]},
            {"txt": "吃不胖/无限金钱 (享受)", "targets": ["Orange", "GoldenShade", "Chinchilla"]}
        ]
    }
]

# ================= 4. 状态管理 =================
if 'step' not in st.session_state:
    st.session_state.step = 0 
if 'scores' not in st.session_state:
    st.session_state.scores = {k: 0 for k in CATS.keys()}
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0

# ================= 5. 页面逻辑 =================

# --- 0. 激活页 ---
if st.session_state.step == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🐱 喵星人性格鉴定局 V4.0")
    st.caption("全网最全 · 15大品种 · 精准画像")
    
    st.image("https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=800&q=80", use_column_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        code = st.text_input("激活码", placeholder="CAT666", label_visibility="collapsed")
    with col2:
        start_btn = st.button("🚀 开始")
    
    if start_btn:
        if code == "CAT666":
            st.session_state.step = 1
            st.rerun() 
        else:
            st.error("激活码是 CAT666 哦~")

# --- 1. 答题页 ---
elif st.session_state.step == 1:
    current_q = st.session_state.q_index
    q_data = QUESTIONS[current_q]
    
    progress = (current_q + 1) / len(QUESTIONS)
    st.progress(progress, text=f"正在扫描灵魂... {current_q + 1}/{len(QUESTIONS)}")
    
    st.markdown(f"### {q_data['q']}")
    
    for opt in q_data['options']:
        if st.button(opt['txt']):
            for cat_key in opt['targets']:
                st.session_state.scores[cat_key] += 1
            
            if st.session_state.q_index < len(QUESTIONS) - 1:
                st.session_state.q_index += 1
            else:
                st.session_state.step = 2
            st.rerun()

# --- 2. 结果页 (Top 4 展示) ---
elif st.session_state.step == 2:
    st.balloons()
    
    # 排序：按分数从高到低，拿出前 4 名
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    top1_key = sorted_scores[0][0]
    top1_cat = CATS[top1_key]
    
    # === 核心结果 ===
    st.markdown("<center style='color:#888'>你的灵魂本命猫是</center>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center; color:#ff6b81; margin-top:-10px'>{top1_cat['name']}</h1>", unsafe_allow_html=True)
    
    # ⚠️ 确保你的 images 文件夹里有这些图片，且名字完全一致！
    st.image(top1_cat['img'], use_column_width=True)
    
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:15px'>
        {''.join([f'<span class="tag">{tag}</span>' for tag in top1_cat['tags']])}
    </div>
    """, unsafe_allow_html=True)
    
    st.info(top1_cat['desc'])
    
    # === 备选契合 (第2-4名) ===
    st.markdown("### 🧩 你的其他性格切片")
    st.markdown("虽然你是那个品种，但有时候你也像它们...")
    
    for i in range(1, 4): # 取第2,3,4名
        key = sorted_scores[i][0]
        score = sorted_scores[i][1]
        cat = CATS[key]
        
        # 简单计算一个匹配度百分比
        match_rate = min(98, 70 + score * 3)
        
        st.markdown(f"""
        <div class="sub-card">
            <img src="{cat['img']}">
            <div style="flex:1">
                <div style="font-weight:bold; font-size:16px">{cat['name']}</div>
                <div style="font-size:12px; color:#666">潜在契合度: {match_rate}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔄 重测"):
        st.session_state.step = 0
        st.session_state.scores = {k: 0 for k in CATS.keys()}
        st.session_state.q_index = 0
        st.rerun()