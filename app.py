import streamlit as st
import json
import random
import os
import sys

st.set_page_config(page_title="古诗词学习工具", page_icon="📜", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data(show_spinner=True, ttl=3600)
def load_poems():
    poems = []
    guwen_dir = os.path.join(BASE_DIR, 'guwen')
    if not os.path.exists(guwen_dir):
        return poems
    try:
        for file in sorted(os.listdir(guwen_dir)):
            if file.endswith('.json'):
                filepath = os.path.join(guwen_dir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                poems.append(json.loads(line))
                            except:
                                pass
    except Exception as e:
        st.sidebar.warning(f"加载诗词数据时出错: {e}")
    return poems

@st.cache_data(show_spinner=True, ttl=3600)
def load_sentences():
    sentences = []
    sentence_dir = os.path.join(BASE_DIR, 'sentence')
    if not os.path.exists(sentence_dir):
        return sentences
    try:
        for file in sorted(os.listdir(sentence_dir)):
            if file.endswith('.json'):
                filepath = os.path.join(sentence_dir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                sentences.append(json.loads(line))
                            except:
                                pass
    except Exception as e:
        st.sidebar.warning(f"加载名句数据时出错: {e}")
    return sentences

@st.cache_data(show_spinner=True, ttl=3600)
def load_writers():
    writers = []
    writer_dir = os.path.join(BASE_DIR, 'writer')
    if not os.path.exists(writer_dir):
        return writers
    try:
        for file in sorted(os.listdir(writer_dir)):
            if file.endswith('.json'):
                filepath = os.path.join(writer_dir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                writers.append(json.loads(line))
                            except:
                                pass
    except Exception as e:
        st.sidebar.warning(f"加载作者数据时出错: {e}")
    return writers

def main():
    st.sidebar.title("📜 古诗词学习工具")
    menu = ["诗词首页", "诗词浏览", "诗词搜索", "作者介绍", "每日推荐", "诗词测试"]
    choice = st.sidebar.selectbox("选择功能", menu)
    
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("❤️ 我的收藏")
        if st.session_state['favorites']:
            for fav in st.session_state['favorites'][:5]:
                st.write(f"- {fav.get('title', '')}")
            if len(st.session_state['favorites']) > 5:
                st.write(f"... 还有 {len(st.session_state['favorites']) - 5} 首")
        else:
            st.write("暂无收藏")
    
    if choice == "诗词首页":
        show_home()
    elif choice == "诗词浏览":
        show_browse()
    elif choice == "诗词搜索":
        show_search()
    elif choice == "作者介绍":
        show_writers()
    elif choice == "每日推荐":
        show_daily()
    elif choice == "诗词测试":
        show_quiz()

def show_home():
    st.title("📜 古诗词学习工具")
    st.markdown("""
    欢迎来到古诗词学习工具！这里汇集了数千首经典诗词，帮助您领略中华诗词之美。
    
    **功能特点：**
    - 📖 **诗词浏览** - 按朝代、作者、类型浏览诗词
    - 🔍 **诗词搜索** - 搜索诗词名句
    - 👤 **作者介绍** - 了解诗人生平
    - 🎯 **每日推荐** - 每日一首精选诗词
    - 📝 **诗词测试** - 检验学习成果
    
    让我们一起走进诗词的世界，感受中华文化的博大精深！
    """)
    
    st.subheader("🌟 今日诗词")
    poems = load_poems()
    if poems:
        today_poem = random.choice(poems)
        with st.expander(f"{today_poem.get('title', '')} - {today_poem.get('writer', '')}", expanded=True):
            st.write(f"朝代：{today_poem.get('dynasty', '')}")
            st.markdown(f"```\n{today_poem.get('content', '')}\n```")
            if 'remark' in today_poem and today_poem['remark']:
                with st.expander("📖 注释"):
                    st.write(today_poem['remark'])
    else:
        st.warning("暂无诗词数据，请检查数据文件是否存在。")

def show_browse():
    st.title("📖 诗词浏览")
    
    poems = load_poems()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    dynasties = sorted(list(set(p.get('dynasty', '') for p in poems if p.get('dynasty'))))
    writer_names = sorted(list(set(p.get('writer', '') for p in poems if p.get('writer'))))
    
    all_types = set()
    for p in poems:
        for t in p.get('type', []):
            all_types.add(t)
    poem_types = sorted(list(all_types))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        dynasty = st.selectbox("选择朝代", ["全部"] + dynasties)
    with col2:
        writer = st.selectbox("选择作者", ["全部"] + writer_names)
    with col3:
        poem_type = st.selectbox("选择类型", ["全部"] + poem_types)
    
    filtered = poems
    if dynasty != "全部":
        filtered = [p for p in filtered if p.get('dynasty') == dynasty]
    if writer != "全部":
        filtered = [p for p in filtered if p.get('writer') == writer]
    if poem_type != "全部":
        filtered = [p for p in filtered if poem_type in p.get('type', [])]
    
    st.write(f"共找到 {len(filtered)} 首诗词")
    
    display_count = min(50, len(filtered))
    for i, poem in enumerate(filtered[:display_count]):
        with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
            st.write(f"朝代：{poem.get('dynasty', '')}")
            st.write(f"类型：{', '.join(poem.get('type', []))}")
            st.markdown(f"```\n{poem.get('content', '')}\n```")
            
            col1, col2 = st.columns(2)
            with col1:
                if 'remark' in poem and poem['remark']:
                    with st.expander("📖 注释"):
                        st.write(poem['remark'])
            with col2:
                if 'shangxi' in poem and poem['shangxi']:
                    with st.expander("💡 赏析"):
                        shangxi = poem['shangxi']
                        if len(shangxi) > 1000:
                            st.write(shangxi[:1000] + "...")
                        else:
                            st.write(shangxi)
            
            is_fav = poem.get('title') in [f.get('title') for f in st.session_state['favorites']]
            if not is_fav:
                if st.button(f"❤️ 收藏", key=f"fav_browse_{i}"):
                    st.session_state['favorites'].append(poem)
                    st.success("已收藏！")
                    st.rerun()

def show_search():
    st.title("🔍 诗词搜索")
    
    search_type = st.radio("搜索类型", ["诗词", "名句", "作者"])
    keyword = st.text_input("输入关键词", "")
    
    if keyword:
        if search_type == "诗词":
            poems = load_poems()
            results = []
            kw = keyword.lower()
            for p in poems:
                title = p.get('title', '').lower()
                content = p.get('content', '').lower()
                writer = p.get('writer', '').lower()
                if kw in title or kw in content or kw in writer:
                    results.append(p)
            
            st.write(f"找到 {len(results)} 首诗词")
            for i, poem in enumerate(results[:20]):
                with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
                    st.write(f"朝代：{poem.get('dynasty', '')}")
                    st.markdown(f"```\n{poem.get('content', '')}\n```")
        
        elif search_type == "名句":
            sentences = load_sentences()
            results = []
            kw = keyword.lower()
            for s in sentences:
                name = s.get('name', '').lower()
                source = s.get('from', '').lower()
                if kw in name or kw in source:
                    results.append(s)
            
            st.write(f"找到 {len(results)} 条名句")
            for s in results[:30]:
                st.markdown(f"**{s.get('name', '')}**")
                st.write(f"—— {s.get('from', '')}")
                st.divider()
        
        elif search_type == "作者":
            writers = load_writers()
            results = []
            kw = keyword.lower()
            for w in writers:
                name = w.get('name', '').lower()
                intro = w.get('simpleIntro', '').lower()
                if kw in name or kw in intro:
                    results.append(w)
            
            st.write(f"找到 {len(results)} 位作者")
            for w in results[:10]:
                with st.expander(w.get('name', '')):
                    if 'headImageUrl' in w and w['headImageUrl']:
                        try:
                            st.image(w['headImageUrl'], width=100)
                        except:
                            pass
                    st.write(w.get('simpleIntro', ''))

def show_writers():
    st.title("👤 作者介绍")
    
    writers = load_writers()
    poems = load_poems()
    
    if not writers:
        st.warning("暂无作者数据")
        return
    
    writer_names = sorted([w['name'] for w in writers])
    selected = st.selectbox("选择作者", writer_names)
    
    writer = next((w for w in writers if w['name'] == selected), None)
    if writer:
        col1, col2 = st.columns([1, 3])
        with col1:
            if 'headImageUrl' in writer and writer['headImageUrl']:
                try:
                    st.image(writer['headImageUrl'], use_column_width=True)
                except:
                    pass
        with col2:
            st.subheader(writer['name'])
            st.write(writer.get('simpleIntro', ''))
        
        if 'detailIntro' in writer and writer['detailIntro']:
            detail = writer['detailIntro']
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
        
        st.subheader(f"{writer['name']} 的作品")
        writer_poems = [p for p in poems if p.get('writer') == writer['name']]
        if writer_poems:
            st.write(f"共 {len(writer_poems)} 首作品")
            for poem in writer_poems[:15]:
                with st.expander(poem.get('title', '')):
                    st.markdown(f"```\n{poem.get('content', '')}\n```")
        else:
            st.write("暂无作品记录")

def show_daily():
    st.title("🎯 每日推荐")
    
    poems = load_poems()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    if 'daily_poem' not in st.session_state or st.button("🔄 换一首"):
        st.session_state['daily_poem'] = random.choice(poems)
    
    poem = st.session_state['daily_poem']
    st.subheader(f"{poem.get('title', '')}")
    st.write(f"朝代：{poem.get('dynasty', '')} | 作者：{poem.get('writer', '')}")
    st.write(f"类型：{', '.join(poem.get('type', []))}")
    
    st.markdown("---")
    st.markdown(f"```\n{poem.get('content', '')}\n```")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📖 注释")
        if 'remark' in poem and poem['remark']:
            st.write(poem['remark'])
        else:
            st.write("暂无注释")
    with col2:
        st.subheader("💡 赏析")
        if 'shangxi' in poem and poem['shangxi']:
            st.write(poem['shangxi'])
        else:
            st.write("暂无赏析")
    
    is_fav = poem.get('title') in [f.get('title') for f in st.session_state['favorites']]
    if not is_fav:
        if st.button("❤️ 收藏这首诗"):
            st.session_state['favorites'].append(poem)
            st.success("已收藏！")
            st.rerun()
    else:
        st.info("已在收藏中")

def show_quiz():
    st.title("📝 诗词测试")
    
    poems = load_poems()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    if 'quiz' not in st.session_state or st.button("🎲 开始新测验"):
        poem = random.choice(poems)
        quiz = generate_quiz(poem)
        if quiz:
            st.session_state['quiz'] = quiz
            st.session_state['quiz_submitted'] = False
        else:
            st.warning("无法生成测验，请重试")
            return
    
    quiz = st.session_state.get('quiz')
    if not quiz:
        return
    
    st.write(f"根据诗词填空：")
    st.write(f"**{quiz['poem_title']}** - {quiz['poem_writer']}")
    st.markdown(f"```\n{quiz['question']}\n```")
    
    user_answers = []
    for i in range(len(quiz['answers'])):
        user_input = st.text_input(f"第 {i+1} 个空", key=f"quiz_ans_{i}")
        user_answers.append(user_input)
    
    if st.button("✅ 提交答案"):
        st.session_state['quiz_submitted'] = True
        
        all_correct = True
        for i, (user_ans, correct_ans) in enumerate(zip(user_answers, quiz['answers'])):
            if user_ans.strip() != correct_ans:
                all_correct = False
                st.error(f"第 {i+1} 个空答案错误！正确答案是：{correct_ans}")
            else:
                st.success(f"第 {i+1} 个空回答正确！")
        
        if all_correct:
            st.success("🎉 全部正确！太棒了！")
        else:
            st.info("继续努力，多练习几首诗吧！")
        
        st.write(f"完整诗句：**{quiz['full_line']}**")

def generate_quiz(poem):
    content = poem.get('content', '')
    lines = [l.strip() for l in content.split('\n') if l.strip() and len(l.strip()) >= 5]
    if not lines:
        return None
    
    selected_line = random.choice(lines)
    chars = list(selected_line)
    
    valid_positions = [i for i, c in enumerate(chars) if '\u4e00' <= c <= '\u9fff']
    if len(valid_positions) < 2:
        return None
    
    blank_count = min(2, len(valid_positions) // 3)
    blanks = random.sample(valid_positions, blank_count)
    blanks.sort()
    
    question = ''
    answers = []
    for i, c in enumerate(chars):
        if i in blanks:
            question += '＿'
            answers.append(c)
        else:
            question += c
    
    return {
        'question': question,
        'answers': answers,
        'full_line': selected_line,
        'poem_title': poem.get('title', ''),
        'poem_writer': poem.get('writer', '')
    }

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"应用运行出错: {e}")
        st.info("请刷新页面重试，或检查数据文件是否正确。")
