import streamlit as st

# ================= 1. 基础配置 =================
st.set_page_config(
    page_title="喵星人性格鉴定局",
    page_icon="🐱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= 2. 纯净版 UI 样式 =================
st.markdown("""
<style>
    /* 隐藏标头和页脚 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 隐藏 Streamlit 红色按钮 */
    .stDeployButton {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}

    /* 背景色 */
    .stApp {
        background-color: #f7f9fc;
    }

    /* 调整单选框样式，让它看起来更像卡片 */
    .stRadio > div {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 进度条颜色 */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff9a9e, #fad0c4);
    }
    
    /* 标签样式 */
    .tag-span {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 13px;
        margin-right: 5px;
        display: inline-block;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. 数据准备 =================
# ⚠️ 请确保 images 文件夹里的图片文件名全是小写！
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
    },
    
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
        "img": "images/lihuamao.jpg"
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
        "img": "images/wumaomao.jpg"
    },
    "Calico": {
        "name": "幸运女神·三花猫",
        "tags": ["#傲娇", "#聪明", "#猫中御姐"],
        "desc": "你像三花猫一样，多数时候聪明且独立。你非常有主见，不会随波逐流。你有点小傲娇，只有对你真正认可的人，才会展示柔软的一面。",
        "img": "images/sanhuamao.jpg"
    },
    "Chinchilla": {
        "name": "精致名媛·金吉拉",
        "tags": ["#精致", "#有洁癖", "#小公主"],
        "desc": "你像金吉拉一样，生活精致，注重细节。你对环境的要求比较高，受不了一点脏乱差。你举止优雅，是朋友圈里最有品味的那个人。",
        "img": "images/jinjila.jpg"
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
}

QUESTIONS = [
    {
        "q": " 周末早晨，你通常会？",
        "options": [
            {"txt": "睡到自然醒，赖床玩手机", "targets": ["GoldenShade", "Orange", "BlueCat", "SilverShade"]},
            {"txt": "早起运动/收拾屋子，精力充沛", "targets": ["DragonLi", "Jianzhou", "Cow", "DevonRex"]},
            {"txt": "必须找人贴贴/聊天才能起床", "targets": ["Ragdoll", "Sphynx", "Cheese", "DevonRex"]},
            {"txt": "按计划起床，做个精致早餐", "targets": ["Chinchilla", "MaineCoon", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": " 朋友突然放鸽子，你的反应是？",
        "options": [
            {"txt": "无所谓，刚好自己宅着", "targets": ["BlueCat", "Orange", "SilverShade"]},
            {"txt": "有点生气，需要哄", "targets": ["Calico", "Chinchilla", "Ragdoll"]},
            {"txt": "立刻改约别人，绝不浪费时间", "targets": ["DragonLi", "Jianzhou", "Cow"]},
            {"txt": "正好去做自己想做的事，很独立", "targets": ["MaineCoon", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": " 你更喜欢哪种穿衣风格？",
        "options": [
            {"txt": "舒适宽松，怎么舒服怎么来", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "精致优雅，注重搭配细节", "targets": ["Chinchilla", "SilverShade", "Ragdoll"]},
            {"txt": "个性潮牌，与众不同", "targets": ["Sphynx", "Cow", "DevonRex"]},
            {"txt": "简约干练，方便活动", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]}
        ]
    },
    {
        "q": " 在社交场合中，你是？",
        "options": [
            {"txt": "全场焦点，社牛本牛", "targets": ["Cow", "DevonRex", "Orange"]},
            {"txt": "只跟熟人聊，生人勿近", "targets": ["Calico", "DragonLi", "SilverShade"]},
            {"txt": "温和的倾听者，微笑回应", "targets": ["GoldenShade", "BlueCat", "Ragdoll"]},
            {"txt": "游刃有余，照顾每个人的感受", "targets": ["MaineCoon", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": " 遇到困难时，你会？",
        "options": [
            {"txt": "找人撒娇求助，抱大腿", "targets": ["Ragdoll", "Sphynx", "Chinchilla"]},
            {"txt": "自己死磕，绝不认输", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "先吃顿好的，明天再说", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "另辟蹊径，用奇怪的方法解决", "targets": ["Cow", "DevonRex", "Cheese"]}
        ]
    },
    {
        "q": " 对于“粘人”这件事，你怎么看？",
        "options": [
            {"txt": "我是粘人精，分开一秒都难受", "targets": ["Sphynx", "Ragdoll", "DevonRex"]},
            {"txt": "看心情，想理你才理你", "targets": ["Calico", "SilverShade", "BlueCat"]},
            {"txt": "不需要太粘，有各自空间最好", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "刚刚好，互相陪伴", "targets": ["GoldenShade", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": " 你的体型/身材管理观念是？",
        "options": [
            {"txt": "心宽体胖，能吃是福", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "天生丽质，无需刻意管理", "targets": ["Ragdoll", "Chinchilla", "BlueWhite"]},
            {"txt": "精壮结实，充满力量感", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "身材苗条/独特", "targets": ["Sphynx", "DevonRex", "Calico"]}
        ]
    },
    {
        "q": " 你觉得自己像什么动物？",
        "options": [
            {"txt": "狗狗 (忠诚、热情)", "targets": ["MaineCoon", "DevonRex", "Sphynx"]},
            {"txt": "老虎/狮子 (霸气、独立)", "targets": ["DragonLi", "Jianzhou", "Calico"]},
            {"txt": "考拉/熊猫 (懒、可爱)", "targets": ["GoldenShade", "BlueCat", "Orange"]},
            {"txt": "猴子/哈士奇 (皮、活泼)", "targets": ["Cow", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": " 你对生活环境的要求？",
        "options": [
            {"txt": "必须干净整洁，有洁癖", "targets": ["Chinchilla", "SilverShade", "Calico"]},
            {"txt": "舒服就行，稍微乱点也没事", "targets": ["Orange", "GoldenShade", "Cheese"]},
            {"txt": "只要有张床，哪里都能睡", "targets": ["BlueCat", "Cow", "BlueWhite"]},
            {"txt": "喜欢高处，视野要好", "targets": ["DragonLi", "MaineCoon", "Jianzhou"]}
        ]
    },
     {
        "q": " 被人误解时，你会？",
        "options": [
            {"txt": "极力辩解，必须说清楚", "targets": ["DevonRex", "Sphynx", "Cow"]},
            {"txt": "懒得解释，爱咋咋地", "targets": ["DragonLi", "Calico", "SilverShade"]},
            {"txt": "委屈巴巴，自己生闷气", "targets": ["Ragdoll", "Chinchilla", "BlueCat"]},
            {"txt": "用行动证明自己", "targets": ["MaineCoon", "Jianzhou", "GoldenShade"]}
        ]
    },
    {
        "q": " 你更喜欢哪种类型的伴侣？",
        "options": [
            {"txt": "能照顾我的，宠我的", "targets": ["Ragdoll", "Chinchilla", "Sphynx"]},
            {"txt": "势均力敌的，能一起进步的", "targets": ["DragonLi", "MaineCoon", "Jianzhou"]},
            {"txt": "有趣的，能玩到一起的", "targets": ["Cow", "DevonRex", "Cheese"]},
            {"txt": "情绪稳定的，包容性强的", "targets": ["GoldenShade", "BlueCat", "SilverShade"]}
        ]
    },
    {
        "q": " 最后一个问题，你最想要什么超能力？",
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
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
# 记录用户的选择： key=题号(0-11), value=选项索引(0-3)
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# ================= 5. 页面逻辑 =================

# --- 0. 激活页 ---
if st.session_state.step == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🐱 喵星人性格鉴定局")
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

# --- 1. 答题页 (支持上一题/下一题) ---
elif st.session_state.step == 1:
    idx = st.session_state.q_index
    q_data = QUESTIONS[idx]
    
    # 顶部进度条
    progress = (idx + 1) / len(QUESTIONS)
    st.progress(progress, text=f"灵魂扫描中... {idx + 1}/{len(QUESTIONS)}")
    
    # 题目
    st.markdown(f"### Q{idx+1}. {q_data['q']}")
    
    # 获取当前题目的选项文本列表
    options_list = [opt['txt'] for opt in q_data['options']]
    
    # 检查这一题之前是否选过，如果有，默认选中之前的答案
    default_index = st.session_state.answers.get(idx, 0)
    
    # 核心交互：单选框
    selected_option = st.radio(
        "请选择:", 
        options_list, 
        index=default_index,
        label_visibility="collapsed" # 隐藏"请选择"这几个字，更简洁
    )
    
    # 找到用户选的是第几个选项
    current_selection_index = options_list.index(selected_option)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 底部导航按钮
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        if idx > 0:
            if st.button("⬅️ 上一题"):
                st.session_state.q_index -= 1
                st.rerun()
                
    with c3:
        # 如果是最后一题，显示“查看结果”
        if idx == len(QUESTIONS) - 1:
            if st.button("查看结果 🚀", type="primary"):
                # 记录最后一题的答案
                st.session_state.answers[idx] = current_selection_index
                st.session_state.step = 2
                st.rerun()
        else:
            if st.button("下一题 ➡️", type="primary"):
                # 记录当前题答案
                st.session_state.answers[idx] = current_selection_index
                st.session_state.q_index += 1
                st.rerun()

# --- 2. 结果页 (原生组件渲染，解决图片不显示问题) ---
elif st.session_state.step == 2:
    st.balloons()
    
    # === 现场算分 ===
    # 初始化分数
    final_scores = {k: 0 for k in CATS.keys()}
    
    # 遍历每一道题的答案
    for q_i, ans_i in st.session_state.answers.items():
        # 找到这道题对应的 targets
        targets = QUESTIONS[q_i]['options'][ans_i]['targets']
        for cat_key in targets:
            if cat_key in final_scores:
                final_scores[cat_key] += 1

    # 排序
    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    top1_key = sorted_scores[0][0]
    top1_cat = CATS[top1_key]
    
    # === 核心结果 ===
    st.markdown("<center style='color:#888'>你的灵魂本命猫是</center>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center; color:#ff6b81; margin-top:-10px'>{top1_cat['name']}</h1>", unsafe_allow_html=True)
    
    # 主图 (使用 st.image 确保图片能显示)
    st.image(top1_cat['img'], use_column_width=True)
    
    # 标签
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:15px'>
        {''.join([f'<span class="tag-span">{tag}</span>' for tag in top1_cat['tags']])}
    </div>
    """, unsafe_allow_html=True)
    
    st.info(top1_cat['desc'])
    
    # === 备选契合 (第2-4名) ===
    st.markdown("### 🧩 你的其他性格切片")
    st.caption("虽然你是那个品种，但有时候你也像它们...")
    
    # 使用 Streamlit 原生布局替代 HTML img，解决图片不显示问题
    for i in range(1, 4):
        key = sorted_scores[i][0]
        score = sorted_scores[i][1]
        cat = CATS[key]
        match_rate = min(98, 70 + score * 3)
        
        # 容器卡片
        with st.container(border=True):
            col_img, col_txt = st.columns([1, 3])
            
            with col_img:
                # 这里使用 st.image，它能完美处理本地路径
                st.image(cat['img'], use_column_width=True)
            
            with col_txt:
                st.subheader(cat['name'])
                st.markdown(f"<span style='color:#666; font-size:14px'>潜在契合度: {match_rate}%</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 重测按钮
    if st.button("🔄 重测"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.q_index = 0
        st.rerun()