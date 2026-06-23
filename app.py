import streamlit as st
import json
import random
import os
import re

st.set_page_config(page_title="古诗词学习工具", page_icon="📜", layout="wide")

@st.cache_data
def load_data():
    sentences = []
    for file in os.listdir('/workspace/sentence'):
        if file.endswith('.json'):
            with open(f'/workspace/sentence/{file}', 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        sentences.append(json.loads(line))
                    except:
                        pass
    
    poems = []
    for file in os.listdir('/workspace/guwen'):
        if file.endswith('.json'):
            with open(f'/workspace/guwen/{file}', 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        poems.append(json.loads(line))
                    except:
                        pass
    
    writers = []
    for file in os.listdir('/workspace/writer'):
        if file.endswith('.json'):
            with open(f'/workspace/writer/{file}', 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        writers.append(json.loads(line))
                    except:
                        pass
    
    return sentences, poems, writers

sentences, poems, writers = load_data()

def get_dynasties():
    dynasties = set()
    for poem in poems:
        if 'dynasty' in poem:
            dynasties.add(poem['dynasty'])
    return sorted(list(dynasties))

def get_writer_names():
    return sorted([w['name'] for w in writers])

def get_poem_types():
    types = set()
    for poem in poems:
        if 'type' in poem:
            for t in poem['type']:
                types.add(t)
    return sorted(list(types))

def search_poems(keyword):
    results = []
    keyword = keyword.lower()
    for poem in poems:
        title = poem.get('title', '').lower()
        content = poem.get('content', '').lower()
        writer = poem.get('writer', '').lower()
        if keyword in title or keyword in content or keyword in writer:
            results.append(poem)
    return results

def search_sentences(keyword):
    results = []
    keyword = keyword.lower()
    for s in sentences:
        name = s.get('name', '').lower()
        source = s.get('from', '').lower()
        if keyword in name or keyword in source:
            results.append(s)
    return results

def search_writers(keyword):
    results = []
    keyword = keyword.lower()
    for w in writers:
        name = w.get('name', '').lower()
        intro = w.get('simpleIntro', '').lower()
        if keyword in name or keyword in intro:
            results.append(w)
    return results

def random_poem():
    return random.choice(poems)

def generate_quiz(poem):
    content = poem.get('content', '')
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    if len(lines) < 2:
        return None
    
    selected_line = random.choice(lines)
    chars = list(selected_line)
    if len(chars) < 3:
        return None
    
    blank_count = min(2, len(chars) // 3)
    blanks = random.sample(range(len(chars)), blank_count)
    blanks.sort()
    
    question = ''
    answers = []
    for i, c in enumerate(chars):
        if i in blanks:
            question += '____'
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

def main():
    st.sidebar.title("📜 古诗词学习工具")
    menu = ["诗词首页", "诗词浏览", "诗词搜索", "作者介绍", "每日推荐", "诗词测试"]
    choice = st.sidebar.selectbox("选择功能", menu)
    
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []
    
    if choice == "诗词首页":
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
        today_poem = random_poem()
        with st.expander(f"{today_poem.get('title', '')} - {today_poem.get('writer', '')}", expanded=True):
            st.write(f"朝代：{today_poem.get('dynasty', '')}")
            st.markdown(f"```\n{today_poem.get('content', '')}\n```")
            if 'remark' in today_poem:
                with st.expander("📖 注释"):
                    st.write(today_poem['remark'])
    
    elif choice == "诗词浏览":
        st.title("📖 诗词浏览")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dynasty = st.selectbox("选择朝代", ["全部"] + get_dynasties())
        with col2:
            writer = st.selectbox("选择作者", ["全部"] + get_writer_names())
        with col3:
            poem_type = st.selectbox("选择类型", ["全部"] + get_poem_types())
        
        filtered_poems = poems
        if dynasty != "全部":
            filtered_poems = [p for p in filtered_poems if p.get('dynasty') == dynasty]
        if writer != "全部":
            filtered_poems = [p for p in filtered_poems if p.get('writer') == writer]
        if poem_type != "全部":
            filtered_poems = [p for p in filtered_poems if poem_type in p.get('type', [])]
        
        st.write(f"共找到 {len(filtered_poems)} 首诗词")
        
        for poem in filtered_poems[:50]:
            with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
                st.write(f"朝代：{poem.get('dynasty', '')}")
                st.write(f"类型：{', '.join(poem.get('type', []))}")
                st.markdown(f"```\n{poem.get('content', '')}\n```")
                
                col1, col2 = st.columns(2)
                with col1:
                    if 'remark' in poem:
                        with st.expander("📖 注释"):
                            st.write(poem['remark'])
                with col2:
                    if 'shangxi' in poem:
                        with st.expander("💡 赏析"):
                            st.write(poem['shangxi'][:500] + "..." if len(poem['shangxi']) > 500 else poem['shangxi'])
                
                if poem.get('title') not in [f.get('title') for f in st.session_state['favorites']]:
                    if st.button(f"❤️ 收藏 {poem.get('title', '')}", key=f"fav_{poem.get('title')}"):
                        st.session_state['favorites'].append(poem)
                        st.success("已收藏！")
    
    elif choice == "诗词搜索":
        st.title("🔍 诗词搜索")
        
        search_type = st.radio("搜索类型", ["诗词", "名句", "作者"])
        keyword = st.text_input("输入关键词")
        
        if keyword:
            if search_type == "诗词":
                results = search_poems(keyword)
                st.write(f"找到 {len(results)} 首诗词")
                for poem in results[:20]:
                    with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
                        st.write(f"朝代：{poem.get('dynasty', '')}")
                        st.markdown(f"```\n{poem.get('content', '')}\n```")
            
            elif search_type == "名句":
                results = search_sentences(keyword)
                st.write(f"找到 {len(results)} 条名句")
                for s in results[:20]:
                    st.markdown(f"**{s.get('name', '')}**")
                    st.write(f"—— {s.get('from', '')}")
                    st.divider()
            
            elif search_type == "作者":
                results = search_writers(keyword)
                st.write(f"找到 {len(results)} 位作者")
                for w in results[:10]:
                    with st.expander(w.get('name', '')):
                        if 'headImageUrl' in w:
                            st.image(w['headImageUrl'], width=100)
                        st.write(w.get('simpleIntro', ''))
    
    elif choice == "作者介绍":
        st.title("👤 作者介绍")
        
        selected_writer = st.selectbox("选择作者", get_writer_names())
        
        writer = next((w for w in writers if w['name'] == selected_writer), None)
        if writer:
            if 'headImageUrl' in writer:
                st.image(writer['headImageUrl'], width=150)
            st.subheader(writer['name'])
            st.write(writer.get('simpleIntro', ''))
            
            if 'detailIntro' in writer:
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
                    st.write(detail)
            
            st.subheader(f"{writer['name']} 的作品")
            writer_poems = [p for p in poems if p.get('writer') == writer['name']]
            for poem in writer_poems[:10]:
                st.markdown(f"- [{poem.get('title', '')}]({poem.get('title', '')})")
    
    elif choice == "每日推荐":
        st.title("🎯 每日推荐")
        
        if 'daily_poem' not in st.session_state or st.button("获取今日推荐"):
            st.session_state['daily_poem'] = random_poem()
        
        poem = st.session_state['daily_poem']
        st.subheader(f"{poem.get('title', '')}")
        st.write(f"朝代：{poem.get('dynasty', '')} | 作者：{poem.get('writer', '')}")
        st.write(f"类型：{', '.join(poem.get('type', []))}")
        
        st.markdown("---")
        st.markdown(f"```\n{poem.get('content', '')}\n```")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📖 注释")
            if 'remark' in poem:
                st.write(poem['remark'])
        with col2:
            st.subheader("💡 赏析")
            if 'shangxi' in poem:
                st.write(poem['shangxi'])
        
        if poem.get('title') not in [f.get('title') for f in st.session_state['favorites']]:
            if st.button("❤️ 收藏这首诗"):
                st.session_state['favorites'].append(poem)
                st.success("已收藏！")
    
    elif choice == "诗词测试":
        st.title("📝 诗词测试")
        
        if 'quiz' not in st.session_state or st.button("开始新测验"):
            poem = random_poem()
            st.session_state['quiz'] = generate_quiz(poem)
            st.session_state['user_answers'] = []
            st.session_state['submitted'] = False
        
        quiz = st.session_state.get('quiz')
        if not quiz:
            st.warning("无法生成测验，请点击重新开始")
            return
        
        st.write(f"根据诗词填空：")
        st.write(f"**{quiz['poem_title']}** - {quiz['poem_writer']}")
        st.markdown(f"```\n{quiz['question']}\n```")
        
        for i, answer in enumerate(quiz['answers']):
            user_input = st.text_input(f"请输入第 {i+1} 个空的答案", key=f"answer_{i}")
            st.session_state['user_answers'].append(user_input)
        
        if st.button("提交答案"):
            st.session_state['submitted'] = True
            
            correct = True
            for i, (user_ans, correct_ans) in enumerate(zip(st.session_state['user_answers'], quiz['answers'])):
                if user_ans != correct_ans:
                    correct = False
                    st.error(f"第 {i+1} 个空答案错误！正确答案是：{correct_ans}")
                else:
                    st.success(f"第 {i+1} 个空回答正确！")
            
            if correct:
                st.success("🎉 全部正确！太棒了！")
            
            st.write(f"完整诗句：**{quiz['full_line']}**")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("❤️ 我的收藏")
    if st.session_state['favorites']:
        for fav in st.session_state['favorites'][:5]:
            st.sidebar.write(f"- {fav.get('title', '')}")
        if len(st.session_state['favorites']) > 5:
            st.sidebar.write(f"... 还有 {len(st.session_state['favorites']) - 5} 首")
    else:
        st.sidebar.write("暂无收藏")

if __name__ == "__main__":
    main()