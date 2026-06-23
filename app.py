import streamlit as st
import json
import random
import os

st.set_page_config(page_title="古诗词学习工具", page_icon="📜", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_files(folder_name):
    data = []
    folder_path = os.path.join(BASE_DIR, folder_name)
    if not os.path.exists(folder_path):
        return data
    try:
        files = sorted([f for f in os.listdir(folder_path) if f.endswith('.json')])
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data.append(json.loads(line))
                        except Exception:
                            continue
    except Exception as e:
        st.error(f"加载数据出错 ({folder_name}): {e}")
    return data

@st.cache_data(show_spinner=False)
def get_poems():
    return load_json_files('guwen')

@st.cache_data(show_spinner=False)
def get_sentences():
    return load_json_files('sentence')

@st.cache_data(show_spinner=False)
def get_writers():
    return load_json_files('writer')

def main():
    st.sidebar.title("📜 古诗词学习工具")
    
    page = st.sidebar.radio("功能菜单", [
        "🏠 诗词首页",
        "📖 诗词浏览", 
        "🔍 诗词搜索",
        "👤 作者介绍",
        "🎯 每日推荐",
        "📝 诗词测试"
    ])
    
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ❤️ 我的收藏")
        if st.session_state.favorites:
            for i, fav in enumerate(st.session_state.favorites[:5]):
                st.write(f"{i+1}. {fav.get('title', '')}")
            if len(st.session_state.favorites) > 5:
                st.write(f"... 还有 {len(st.session_state.favorites) - 5} 首")
        else:
            st.caption("暂无收藏")
    
    try:
        if page == "🏠 诗词首页":
            page_home()
        elif page == "📖 诗词浏览":
            page_browse()
        elif page == "🔍 诗词搜索":
            page_search()
        elif page == "👤 作者介绍":
            page_writers()
        elif page == "🎯 每日推荐":
            page_daily()
        elif page == "📝 诗词测试":
            page_quiz()
    except Exception as e:
        st.error(f"页面加载出错: {e}")
        st.info("请刷新页面重试")

def page_home():
    st.title("📜 古诗词学习工具")
    st.markdown("""
    欢迎来到古诗词学习工具！这里汇集了数千首经典诗词，帮助您领略中华诗词之美。
    
    **功能特点：**
    - 📖 **诗词浏览** - 按朝代、作者、类型浏览诗词
    - 🔍 **诗词搜索** - 搜索诗词名句
    - 👤 **作者介绍** - 了解诗人生平
    - 🎯 **每日推荐** - 每日一首精选诗词
    - 📝 **诗词测试** - 检验学习成果
    """)
    
    st.markdown("---")
    st.subheader("🌟 今日诗词")
    
    poems = get_poems()
    if poems:
        today_poem = random.choice(poems)
        st.markdown(f"### {today_poem.get('title', '')}")
        st.caption(f"{today_poem.get('dynasty', '')} · {today_poem.get('writer', '')}")
        st.markdown(f"```\n{today_poem.get('content', '')}\n```")
        
        with st.expander("📖 注释"):
            st.write(today_poem.get('remark', '暂无注释'))
    else:
        st.warning("暂无诗词数据")

def page_browse():
    st.title("📖 诗词浏览")
    
    poems = get_poems()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    dynasties = sorted(set(p.get('dynasty', '') for p in poems if p.get('dynasty')))
    writers_list = sorted(set(p.get('writer', '') for p in poems if p.get('writer')))
    
    all_types = set()
    for p in poems:
        for t in p.get('type', []):
            all_types.add(t)
    types_list = sorted(all_types)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sel_dynasty = st.selectbox("朝代", ["全部"] + dynasties)
    with col2:
        sel_writer = st.selectbox("作者", ["全部"] + writers_list)
    with col3:
        sel_type = st.selectbox("类型", ["全部"] + types_list)
    
    filtered = poems
    if sel_dynasty != "全部":
        filtered = [p for p in filtered if p.get('dynasty') == sel_dynasty]
    if sel_writer != "全部":
        filtered = [p for p in filtered if p.get('writer') == sel_writer]
    if sel_type != "全部":
        filtered = [p for p in filtered if sel_type in p.get('type', [])]
    
    st.info(f"共找到 {len(filtered)} 首诗词，显示前 30 首")
    
    for i, poem in enumerate(filtered[:30]):
        with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
            st.write(f"**朝代**：{poem.get('dynasty', '')}")
            st.write(f"**类型**：{', '.join(poem.get('type', []))}")
            st.markdown(f"```\n{poem.get('content', '')}\n```")
            
            col_a, col_b = st.columns(2)
            with col_a:
                with st.expander("📖 注释"):
                    st.write(poem.get('remark', '暂无注释'))
            with col_b:
                with st.expander("💡 赏析"):
                    shangxi = poem.get('shangxi', '暂无赏析')
                    if len(shangxi) > 500:
                        st.write(shangxi[:500] + "...")
                    else:
                        st.write(shangxi)

def page_search():
    st.title("🔍 诗词搜索")
    
    search_type = st.radio("搜索类型", ["诗词", "名句", "作者"], horizontal=True)
    keyword = st.text_input("输入关键词", placeholder="请输入搜索关键词...")
    
    if not keyword:
        st.info("请输入关键词开始搜索")
        return
    
    if search_type == "诗词":
        poems = get_poems()
        kw = keyword.lower()
        results = [p for p in poems if 
                  kw in p.get('title', '').lower() or 
                  kw in p.get('content', '').lower() or
                  kw in p.get('writer', '').lower()]
        
        st.success(f"找到 {len(results)} 首诗词")
        for poem in results[:20]:
            with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
                st.write(f"朝代：{poem.get('dynasty', '')}")
                st.markdown(f"```\n{poem.get('content', '')}\n```")
    
    elif search_type == "名句":
        sentences = get_sentences()
        kw = keyword.lower()
        results = [s for s in sentences if 
                  kw in s.get('name', '').lower() or 
                  kw in s.get('from', '').lower()]
        
        st.success(f"找到 {len(results)} 条名句")
        for s in results[:30]:
            st.markdown(f"> **{s.get('name', '')}**")
            st.caption(f"—— {s.get('from', '')}")
            st.markdown("---")
    
    elif search_type == "作者":
        writers = get_writers()
        kw = keyword.lower()
        results = [w for w in writers if 
                  kw in w.get('name', '').lower() or 
                  kw in w.get('simpleIntro', '').lower()]
        
        st.success(f"找到 {len(results)} 位作者")
        for w in results[:10]:
            with st.expander(w.get('name', '')):
                if w.get('headImageUrl'):
                    try:
                        st.image(w['headImageUrl'], width=120)
                    except:
                        pass
                st.write(w.get('simpleIntro', ''))

def page_writers():
    st.title("👤 作者介绍")
    
    writers = get_writers()
    poems = get_poems()
    
    if not writers:
        st.warning("暂无作者数据")
        return
    
    writer_names = sorted([w['name'] for w in writers])
    selected = st.selectbox("选择作者", writer_names)
    
    writer = next((w for w in writers if w['name'] == selected), None)
    if not writer:
        return
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if writer.get('headImageUrl'):
            try:
                st.image(writer['headImageUrl'], use_column_width=True)
            except:
                pass
    with col2:
        st.subheader(writer['name'])
        st.write(writer.get('simpleIntro', ''))
    
    st.markdown("---")
    
    detail = writer.get('detailIntro', '')
    if detail:
        if isinstance(detail, str):
            try:
                detail = json.loads(detail)
            except:
                pass
        
        if isinstance(detail, dict):
            for key, value in detail.items():
                with st.expander(key):
                    st.write(value)
        else:
            with st.expander("详细介绍"):
                st.write(detail)
    
    st.subheader(f"📚 {writer['name']} 的作品")
    writer_poems = [p for p in poems if p.get('writer') == writer['name']]
    if writer_poems:
        st.caption(f"共 {len(writer_poems)} 首作品")
        for poem in writer_poems[:10]:
            with st.expander(poem.get('title', '')):
                st.markdown(f"```\n{poem.get('content', '')}\n```")
    else:
        st.info("暂无作品记录")

def page_daily():
    st.title("🎯 每日推荐")
    
    poems = get_poems()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    if st.button("🔄 换一首"):
        st.session_state.daily_poem = random.choice(poems)
    
    if 'daily_poem' not in st.session_state:
        st.session_state.daily_poem = random.choice(poems)
    
    poem = st.session_state.daily_poem
    
    st.markdown(f"## {poem.get('title', '')}")
    st.caption(f"{poem.get('dynasty', '')} · {poem.get('writer', '')}")
    st.write(f"**类型**：{', '.join(poem.get('type', []))}")
    
    st.markdown("---")
    st.markdown(f"```\n{poem.get('content', '')}\n```")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📖 注释")
        st.write(poem.get('remark', '暂无注释'))
    with col2:
        st.subheader("💡 赏析")
        st.write(poem.get('shangxi', '暂无赏析'))

def page_quiz():
    st.title("📝 诗词测试")
    
    poems = get_poems()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    if st.button("🎲 开始新测验"):
        poem = random.choice(poems)
        quiz = make_quiz(poem)
        if quiz:
            st.session_state.current_quiz = quiz
            st.session_state.quiz_done = False
        else:
            st.info("请再试一次")
            return
    
    if 'current_quiz' not in st.session_state:
        poem = random.choice(poems)
        quiz = make_quiz(poem)
        if quiz:
            st.session_state.current_quiz = quiz
            st.session_state.quiz_done = False
        else:
            st.warning("暂时无法生成测验，请刷新页面重试")
            return
    
    quiz = st.session_state.current_quiz
    
    st.info(f"出自：**{quiz['title']}** - {quiz['writer']}")
    st.markdown(f"### {quiz['question']}")
    
    answers = []
    for i in range(len(quiz['answers'])):
        ans = st.text_input(f"第 {i+1} 空", key=f"q_{i}")
        answers.append(ans)
    
    if st.button("✅ 提交答案"):
        st.session_state.quiz_done = True
        correct_count = 0
        
        for i, (user_ans, correct_ans) in enumerate(zip(answers, quiz['answers'])):
            if user_ans.strip() == correct_ans:
                st.success(f"第 {i+1} 空 ✓ 正确！")
                correct_count += 1
            else:
                st.error(f"第 {i+1} 空 ✗ 错误，正确答案是：{correct_ans}")
        
        st.markdown("---")
        if correct_count == len(quiz['answers']):
            st.success("🎉 太棒了！全部正确！")
        else:
            st.info(f"答对了 {correct_count}/{len(quiz['answers'])} 题，继续加油！")
        
        st.write(f"**完整诗句**：{quiz['full_line']}")

def make_quiz(poem):
    content = poem.get('content', '')
    lines = [l.strip() for l in content.split('\n') if l.strip() and len(l.strip()) >= 4]
    if not lines:
        return None
    
    selected_line = random.choice(lines)
    chars = list(selected_line)
    
    hanzi_pos = [i for i, c in enumerate(chars) if '\u4e00' <= c <= '\u9fff']
    if len(hanzi_pos) < 2:
        return None
    
    num_blanks = min(2, max(1, len(hanzi_pos) // 4))
    blank_positions = sorted(random.sample(hanzi_pos, num_blanks))
    
    question_chars = []
    answers = []
    for i, c in enumerate(chars):
        if i in blank_positions:
            question_chars.append('＿')
            answers.append(c)
        else:
            question_chars.append(c)
    
    return {
        'question': ''.join(question_chars),
        'answers': answers,
        'full_line': selected_line,
        'title': poem.get('title', ''),
        'writer': poem.get('writer', '')
    }

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"应用运行出错: {e}")
        st.info("请刷新页面重试")
