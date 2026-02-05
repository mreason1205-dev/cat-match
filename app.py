import streamlit as st

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

    /* 4. 选项卡片样式 (关键修复：不再隐藏圆圈！) */
    div[role="radiogroup"] > label {
        background-color: #ffffff !important;
        padding: 15px 20px !important;
        border-radius: 12px !important;
        border: 1px solid #eee !important;
        margin-bottom: 12px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        display: flex !important; /* 保证圆圈和文字对齐 */
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
    
    /* 8. 强制清除列背景 (双重保险) */
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
        "tags": ["#粘人精", "#颜值天花板", "#玻璃心"],
        "desc": "你的灵魂柔软而细腻，像布偶猫一样，天生拥有极高的共情能力。你渴望被坚定地选择，愿意为了爱的人收起爪子。虽然偶尔会因为敏感而感到委屈，但你的温柔，是治愈这个世界最强大的力量。",
        "img": "images/buoumao.jpg"
    },
    "SilverShade": {
        "name": "银渐层 (Silver Shade)",
        "tags": ["#优雅贵族", "#有点小脾气", "#颜值正义"],
        "desc": "你自带一种与生俱来的优雅气质，像银渐层一样，既不刻意讨好，也不过分疏离。你心里有一杆秤，谁对你好你心里门儿清。虽然偶尔会耍点小性子，但那正是你可爱的个性所在。",
        "img": "images/yinjianceng.jpg"
    },
    "GoldenShade": {
        "name": "金渐层 (Golden Shade)",
        "tags": ["#人间富贵花", "#心态超稳", "#招财体质"],
        "desc": "你就是大家眼中的“小福星”！像金渐层一样，性格圆润，心态超稳。你很少为了不值得的小事内耗，懂得享受生活。你这种松弛感，总能给身边的人带来好运和快乐。",
        "img": "images/jinjianceng.jpg"
    },
    "MaineCoon":{
        "name": "缅因猫 (Maine Coon)",
        "tags": ["#温柔巨人", "#安全感爆棚", "#外冷内热"],
        "desc": "你的气场很强，像缅因猫一样给人十足的安全感。不熟悉的人觉得你高冷，但其实你内心住着一个小公主/小王子，对认定的人极度忠诚和温柔。你是那个能扛事儿的守护者。",
        "img": "images/mianyinmao.jpg"
    },
    "DragonLi": {
        "name": "狸花猫 (Dragon Li)",
        "tags": ["#智商天花板", "#独立酷飒", "#业务能力强"],
        "desc": "如果前世是猫，你一定是那只统领街头的狸花猫。你独立、聪明、执行力极强，不需要依附任何人。在工作中你往往是那个能解决棘手问题的大神，在这个复杂的世界里活得游刃有余。",
        "img": "images/lihuamao.jpg"
    },
    "Jianzhou": {
        "name": "简州猫 (Jianzhou)",
        "tags": ["#低调狩猎者", "#强悍实干", "#不服输"],
        "desc": "你像传说中的简州猫一样，低调而强悍。你平时不显山不露水，但关键时刻爆发力惊人。你非常务实，不喜欢花里胡哨的东西，是典型的实干家，认定的目标绝不轻易放弃。",
        "img": "images/jianzhoumao.jpg"
    },
    "BlueWhite": {
        "name": "英短蓝白 (Blue Bicolor)",
        "tags": ["#永远的少年", "#好奇宝宝", "#乐天派"],
        "desc": "你的灵魂里住着一个长不大的孩子，像蓝白一样，永远对世界充满好奇。你有点小淘气，但因为长得可爱、性格开朗，总能被大家原谅。你是朋友圈里的开心果，有你在就不会冷场。",
        "img": "images/yingduanlanbai.jpg"
    },
    "BlueCat": {
        "name": "英短蓝猫 (British Blue)",
        "tags": ["#憨厚老实", "#记仇本仇", "#稳重"],
        "desc": "你像蓝猫一样，给人一种憨厚老实、非常靠谱的感觉。你性格稳重，不容易生气（除非抢了你的吃的）。你比较慢热，不喜欢变动，喜欢安稳、有秩序的生活节奏。",
        "img": "images/yingduanlanmao.jpg"
    },
    "Orange": {
        "name": "橘猫 (Orange Tabby)",
        "tags": ["#以大橘为重", "#社交悍匪", "#心宽体胖"],
        "desc": "格局打开！你像大橘一样，心胸宽广，凡事不往心里去。你极具亲和力，朋友遍天下。虽然偶尔想躺平，但对生活的热爱从未减少。你是那种能吃得下饭、睡得着觉的有福之人。",
        "img": "images/jumao.jpg"
    },
    "Sphynx": {
        "name": "无毛猫 (Sphynx)",
        "tags": ["#极度粘人", "#特立独行", "#内心火热"],
        "desc": "你像无毛猫一样特立独行，不在乎世俗的眼光。虽然外表看起来很酷、很独特，但其实你内心非常火热，极度渴望亲密关系，对爱人有着毫无保留的依赖。",
        "img": "images/wumaomao.jpg"
    },
    "Calico": {
        "name": "三花猫 (Calico)",
        "tags": ["#傲娇御姐", "#双商在线", "#看心情"],
        "desc": "你像三花猫一样，多数时候聪明且独立。你非常有主见，不会随波逐流。你有点小傲娇，只有对你真正认可的人，才会展示柔软的一面。你的爱是稀缺资源，给谁谁珍惜。",
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
        "desc": "你是独一无二的奶牛猫！脑回路清奇，经常做一些让人意想不到的事。你精力旺盛，是大家的快乐源泉。有你在，生活永远不会无聊，你总能发现生活中的奇奇怪怪和可可爱爱。",
        "img": "images/nainiumao.jpg"
    },
    "DevonRex": {
        "name": "德文卷毛猫 (Devon Rex)",
        "tags": ["#机灵小狗", "#古灵精怪", "#反应快"],
        "desc": "你像德文卷毛猫一样，聪明机灵，反应极快。你性格像小狗一样热情，喜欢跟人互动，根本闲不下来。你古灵精怪，总能发现生活中的小乐趣，是大家的“小机灵鬼”。",
        "img": "images/dewenmao.jpg"
    },
    "Cheese": {
        "name": "起司猫 (Tabby & White)",
        "tags": ["#元气甜心", "#随和", "#适应力强"],
        "desc": "你像起司猫一样，元气满满，乐观向上。你适应能力很强，无论遇到什么困难都能笑着面对。你的笑容很有感染力，就像冬日里的暖阳，让人忍不住想靠近。",
        "img": "images/qisimao.jpg"
    }
}

QUESTIONS = [
    {
        "q": "如果你的前世是只猫，当家里突然来了陌生客人，你会？", 
        "options": [
            {"txt": "好奇凑过去闻闻，蹭蹭裤腿", "targets": ["Orange", "GoldenShade", "Cow", "DevonRex", "Cheese"]},
            {"txt": "远处高冷观察，敌不动我不动", "targets": ["DragonLi", "SilverShade", "Calico", "MaineCoon", "Jianzhou"]},
            {"txt": "吓得立刻钻进沙发底或床底", "targets": ["Ragdoll", "Sphynx", "BlueCat", "Chinchilla"]},
            {"txt": "完全无视，继续睡我的大觉", "targets": ["BlueWhite", "Orange", "BlueCat"]}
        ]
    },
    {
        "q": "当你看到窗外飞过一只小鸟，你的本能反应是？",
        "options": [
            {"txt": "发出咔咔声，激动地想抓", "targets": ["DragonLi", "Jianzhou", "Cow", "DevonRex", "MaineCoon"]},
            {"txt": "静静地欣赏，思考猫生", "targets": ["SilverShade", "Chinchilla", "Ragdoll", "BlueCat"]},
            {"txt": "没啥反应，不如罐头香", "targets": ["Orange", "GoldenShade", "BlueWhite"]},
            {"txt": "试图打开窗户跟它聊聊", "targets": ["Sphynx", "Cheese", "Calico"]}
        ]
    },
    {
        "q": "如果你要向主人表达爱意，你更倾向于？",
        "options": [
            {"txt": "直接一屁股坐脸上，贴贴！", "targets": ["Ragdoll", "Sphynx", "DevonRex", "Cheese"]},
            {"txt": "叼一只蟑螂/老鼠送给他", "targets": ["DragonLi", "Jianzhou", "Cow", "MaineCoon"]},
            {"txt": "在他工作时，默默趴旁边", "targets": ["GoldenShade", "BlueCat", "SilverShade", "BlueWhite"]},
            {"txt": "允许他摸两下，是恩赐", "targets": ["Calico", "Chinchilla", "SilverShade"]}
        ]
    },
    {
        "q": "在社交场合中，你通常是？",
        "options": [
            {"txt": "全场焦点，社牛本牛", "targets": ["Cow", "DevonRex", "Orange", "Cheese"]},
            {"txt": "只跟熟人聊，生人勿近", "targets": ["Calico", "DragonLi", "SilverShade"]},
            {"txt": "温和倾听者，微笑回应", "targets": ["GoldenShade", "BlueCat", "Ragdoll"]},
            {"txt": "游刃有余，照顾每个人", "targets": ["MaineCoon", "BlueWhite"]}
        ]
    },
    {
        "q": "遇到困难和压力时，你会？",
        "options": [
            {"txt": "找人撒娇求助，求抱抱", "targets": ["Ragdoll", "Sphynx", "Chinchilla"]},
            {"txt": "自己死磕，绝不认输", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "先吃顿好的，睡一觉再说", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "另辟蹊径，用奇怪招数", "targets": ["Cow", "DevonRex", "Cheese"]}
        ]
    },
    {
        "q": "对于“粘人”这件事，你怎么看？",
        "options": [
            {"txt": "我是粘人精，分开难受", "targets": ["Sphynx", "Ragdoll", "DevonRex"]},
            {"txt": "看心情，想理你才理你", "targets": ["Calico", "SilverShade", "BlueCat"]},
            {"txt": "不需要太粘，有各自空间", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "刚刚好，互相陪伴", "targets": ["GoldenShade", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "你的身材管理观念是？",
        "options": [
            {"txt": "心宽体胖，能吃是福", "targets": ["Orange", "GoldenShade", "BlueCat"]},
            {"txt": "天生丽质，无需刻意管理", "targets": ["Ragdoll", "Chinchilla", "BlueWhite"]},
            {"txt": "精壮结实，充满力量感", "targets": ["DragonLi", "Jianzhou", "MaineCoon"]},
            {"txt": "身材苗条/独特", "targets": ["Sphynx", "DevonRex", "Calico"]}
        ]
    },
    {
        "q": "你觉得自己像什么动物？",
        "options": [
            {"txt": "狗狗 (忠诚、热情)", "targets": ["MaineCoon", "DevonRex", "Sphynx"]},
            {"txt": "老虎/狮子 (霸气、独立)", "targets": ["DragonLi", "Jianzhou", "Calico"]},
            {"txt": "考拉/熊猫 (懒、可爱)", "targets": ["GoldenShade", "BlueCat", "Orange"]},
            {"txt": "猴子/哈士奇 (皮、活泼)", "targets": ["Cow", "Cheese", "BlueWhite"]}
        ]
    },
    {
        "q": "你对生活环境的要求？",
        "options": [
            {"txt": "必须干净整洁，有洁癖", "targets": ["Chinchilla", "SilverShade", "Calico"]},
            {"txt": "舒服就行，稍微乱点没事", "targets": ["Orange", "GoldenShade", "Cheese"]},
            {"txt": "只要有张床，哪里都能睡", "targets": ["BlueCat", "Cow", "BlueWhite"]},
            {"txt": "喜欢高处，视野要好", "targets": ["DragonLi", "MaineCoon", "Jianzhou"]}
        ]
    },
     {
        "q": "被人误解时，你会？",
        "options": [
            {"txt": "极力辩解，必须说清楚", "targets": ["DevonRex", "Sphynx", "Cow"]},
            {"txt": "懒得解释，爱咋咋地", "targets": ["DragonLi", "Calico", "SilverShade"]},
            {"txt": "委屈巴巴，自己生闷气", "targets": ["Ragdoll", "Chinchilla", "BlueCat"]},
            {"txt": "用行动证明自己", "targets": ["MaineCoon", "Jianzhou", "GoldenShade"]}
        ]
    },
    {
        "q": "你更喜欢哪种类型的伴侣？",
        "options": [
            {"txt": "能照顾我的，宠我的", "targets": ["Ragdoll", "Chinchilla", "Sphynx"]},
            {"txt": "势均力敌，能一起进步", "targets": ["DragonLi", "MaineCoon", "Jianzhou"]},
            {"txt": "有趣的，能玩到一起的", "targets": ["Cow", "DevonRex", "Cheese"]},
            {"txt": "情绪稳定，包容性强的", "targets": ["GoldenShade", "BlueCat", "SilverShade"]}
        ]
    },
    {
        "q": "最后一个问题，你最想要什么超能力？",
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
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# ================= 5. 页面逻辑 =================

# --- 0. 激活页 ---
if st.session_state.step == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔮 如果你的前世是一只小猫</h1>", unsafe_allow_html=True)
    st.caption("全网最火 · 灵魂品种测试 · 你的本能反应")
    
    st.image("https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=800&q=80", use_column_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<div style='text-align:center; color:#666; margin-bottom:10px;'>🔑 输入激活码解锁测试</div>", unsafe_allow_html=True)
        
        # 核心修改：placeholder 改为“请输入激活码”
        code_input = st.text_input("激活码", placeholder="请输入激活码", label_visibility="collapsed")
        
        # 去空格
        code_clean = code_input.strip()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("开始唤醒 ⚡", type="primary", use_container_width=True):
            # 核心修改：恢复 Secrets 验证逻辑
            try:
                if code_clean in st.secrets["valid_codes"]:
                    st.session_state.step = 1
                    st.rerun() 
                else:
                    st.error("激活码错误或已失效，请检查~")
            except FileNotFoundError:
                # 本地无Secrets时的后门
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
    
    # 底部按钮逻辑：第一题只有下一题
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
    
    final_scores = {k: 0 for k in CATS.keys()}
    for q_i, ans_i in st.session_state.answers.items():
        targets = QUESTIONS[q_i]['options'][ans_i]['targets']
        for cat_key in targets:
            if cat_key in final_scores:
                final_scores[cat_key] += 1

    sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    top1_key = sorted_scores[0][0]
    top1_score = sorted_scores[0][1]
    top1_cat = CATS[top1_key]
    
    match_percentage = min(99, 60 + top1_score * 4)
    
    with st.container(border=True):
        st.markdown("<center style='color:#888; font-size:14px; letter-spacing: 2px;'>你的前世灵魂是</center>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center; color:#2c3e50; margin-top:5px; margin-bottom: 5px;'>{top1_cat['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-score'>{match_percentage}%</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; color:#a1c4fd; font-weight:bold; margin-bottom:20px;'>灵 魂 契 合 度</div>", unsafe_allow_html=True)
        st.image(top1_cat['img'], use_column_width=True)
        st.markdown(f"""
        <div style='text-align:center; margin-top:15px; margin-bottom:15px'>
            {''.join([f'<span class="tag-span">{tag}</span>' for tag in top1_cat['tags']])}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<div style='line-height:1.6; color:#555; text-align:justify;'>{top1_cat['desc']}</div>", unsafe_allow_html=True)
    
    st.markdown("### 🧩 你的其他性格切片")
    
    for i in range(1, 4):
        key = sorted_scores[i][0]
        score = sorted_scores[i][1]
        cat = CATS[key]
        sub_match = min(90, 50 + score * 4)
        with st.container(border=True):
            col_img, col_txt = st.columns([1, 2.5])
            with col_img:
                st.image(cat['img'], use_column_width=True)
            with col_txt:
                st.markdown(f"**{cat['name']}**")
                st.markdown(f"<div style='font-size:12px; color:#999; margin-bottom:5px;'>潜在契合度: {sub_match}%</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:12px; color:#666;'>{cat['tags'][0]} {cat['tags'][1]}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 转世重修 (重测)", type="primary", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.q_index = 0
        st.rerun()