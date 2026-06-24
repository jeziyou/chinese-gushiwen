import streamlit as st

st.set_page_config(page_title="测试", page_icon="🧪")

st.title("🧪 测试页面")
st.write("如果您看到这个页面，说明 Streamlit 基本功能正常！")

st.markdown("---")
st.subheader("检查数据文件")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.write(f"当前目录: {BASE_DIR}")

folders = ['guwen', 'sentence', 'writer']
for folder in folders:
    path = os.path.join(BASE_DIR, folder)
    if os.path.exists(path):
        files = [f for f in os.listdir(path) if f.endswith('.json')]
        st.success(f"✅ {folder}/ 存在，包含 {len(files)} 个 JSON 文件")
        for f in files[:3]:
            st.write(f"  - {f}")
    else:
        st.error(f"❌ {folder}/ 不存在")

st.markdown("---")
st.subheader("测试数据加载")

import json

for folder in folders:
    path = os.path.join(BASE_DIR, folder)
    if os.path.exists(path):
        try:
            count = 0
            files = [f for f in os.listdir(path) if f.endswith('.json')]
            for fname in files:
                fpath = os.path.join(path, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                json.loads(line)
                                count += 1
                            except:
                                pass
            st.success(f"✅ {folder}: 成功加载 {count} 条记录")
        except Exception as e:
            st.error(f"❌ {folder} 加载失败: {e}")

st.markdown("---")
st.success("🎉 所有测试完成！")
