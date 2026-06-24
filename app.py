import streamlit as st
import json
import os

st.set_page_config(page_title="古诗词学习工具", page_icon="📜", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data(show_spinner=False)
def load_guwen():
    data = []
    folder = os.path.join(BASE_DIR, 'guwen')
    if not os.path.exists(folder):
        return data
    try:
        for fname in sorted(os.listdir(folder)):
            if fname.endswith('.json'):
                fpath = os.path.join(folder, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                data.append(json.loads(line))
                            except:
                                pass
    except Exception as e:
        st.error(f"加载诗词数据错误: {e}")
    return data

@st.cache_data(show_spinner=False)
def load_sentence():
    data = []
    folder = os.path.join(BASE_DIR, 'sentence')
    if not os.path.exists(folder):
        return data
    try:
        for fname in sorted(os.listdir(folder)):
            if fname.endswith('.json'):
                fpath = os.path.join(folder, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                data.append(json.loads(line))
                            except:
                                pass
    except Exception as e:
        st.error(f"加载名句数据错误: {e}")
    return data

@st.cache_data(show_spinner=False)
def load_writer():
    data = []
    folder = os.path.join(BASE_DIR, 'writer')
    if not os.path.exists(folder):
        return data
    try:
        for fname in sorted(os.listdir(folder)):
            if fname.endswith('.json'):
                fpath = os.path.join(folder, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                data.append(json.loads(line))
                            except:
                                pass
    except Exception as e:
        st.error(f"加载作者数据错误: {e}")
    return data

def main():
    st.sidebar.title("📜 古诗词学习工具")
    
    page = st.sidebar.selectbox("功能菜单", [
        "首页",
        "诗词浏览", 
        "诗词搜索",
        "作者介绍",
        "名句欣赏"
    ])
    
    if page == "首页":
        show_home()
    elif page == "诗词浏览":
        show_browse()
    elif page == "诗词搜索":
        show_search()
    elif page == "作者介绍":
        show_writers()
    elif page == "名句欣赏":
        show_sentences()

def show_home():
    st.title("📜 古诗词学习工具")
    st.write("欢迎来到古诗词学习工具！")
    
    poems = load_guwen()
    sentences = load_sentence()
    writers = load_writer()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("诗词数量", len(poems))
    col2.metric("名句数量", len(sentences))
    col3.metric("作者数量", len(writers))
    
    st.markdown("---")
    st.subheader("今日推荐")
    
    if poems:
        import random
        poem = random.choice(poems)
        st.markdown(f"### {poem.get('title', '')}")
        st.caption(f"{poem.get('dynasty', '')} · {poem.get('writer', '')}")
        st.markdown(f"```\n{poem.get('content', '')}\n```")
    else:
        st.warning("暂无诗词数据")

def show_browse():
    st.title("📖 诗词浏览")
    
    poems = load_guwen()
    if not poems:
        st.warning("暂无诗词数据")
        return
    
    dynasties = []
    for p in poems:
        d = p.get('dynasty', '')
        if d and d not in dynasties:
            dynasties.append(d)
    dynasties.sort()
    
    sel_dynasty = st.selectbox("选择朝代", ["全部"] + dynasties)
    
    filtered = poems
    if sel_dynasty != "全部":
        filtered = [p for p in poems if p.get('dynasty') == sel_dynasty]
    
    st.info(f"共 {len(filtered)} 首，显示前 20 首")
    
    for poem in filtered[:20]:
        with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
            st.write(f"朝代：{poem.get('dynasty', '')}")
            st.markdown(f"```\n{poem.get('content', '')}\n```")
            remark = poem.get('remark', '')
            if remark:
                st.write("**注释：**", remark)

def show_search():
    st.title("🔍 诗词搜索")
    
    keyword = st.text_input("输入关键词搜索")
    
    if keyword:
        poems = load_guwen()
        kw = keyword.lower()
        results = []
        for p in poems:
            title = p.get('title', '').lower()
            content = p.get('content', '').lower()
            writer = p.get('writer', '').lower()
            if kw in title or kw in content or kw in writer:
                results.append(p)
        
        st.success(f"找到 {len(results)} 首诗词")
        for poem in results[:15]:
            with st.expander(f"{poem.get('title', '')} - {poem.get('writer', '')}"):
                st.markdown(f"```\n{poem.get('content', '')}\n```")

def show_writers():
    st.title("👤 作者介绍")
    
    writers = load_writer()
    poems = load_guwen()
    
    if not writers:
        st.warning("暂无作者数据")
        return
    
    names = [w.get('name', '') for w in writers]
    names.sort()
    
    selected = st.selectbox("选择作者", names)
    
    writer = None
    for w in writers:
        if w.get('name') == selected:
            writer = w
            break
    
    if writer:
        st.subheader(writer.get('name', ''))
        st.write(writer.get('simpleIntro', ''))
        
        st.subheader("作品")
        writer_poems = [p for p in poems if p.get('writer') == selected]
        st.write(f"共 {len(writer_poems)} 首作品")
        for poem in writer_poems[:10]:
            with st.expander(poem.get('title', '')):
                st.markdown(f"```\n{poem.get('content', '')}\n```")

def show_sentences():
    st.title("💬 名句欣赏")
    
    sentences = load_sentence()
    if not sentences:
        st.warning("暂无名句数据")
        return
    
    st.info(f"共 {len(sentences)} 条名句，显示前 50 条")
    
    for s in sentences[:50]:
        st.markdown(f"> **{s.get('name', '')}**")
        st.caption(f"—— {s.get('from', '')}")
        st.markdown("---")

if __name__ == "__main__":
    main()
