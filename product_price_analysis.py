import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# =========================
# 自动选择可用中文字体
# =========================
def get_chinese_font():
    for font in font_manager.findSystemFonts():
        if any(name in font for name in ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]):
            return font
    return None

chinese_font = get_chinese_font()
if chinese_font:
    plt.rcParams['font.sans-serif'] = [chinese_font]
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# =========================
# Streamlit 页面设置
# =========================
st.set_page_config(page_title="产品价格差额可视化", layout="wide")
st.title("🛒 产品价格比较与动态差额可视化")

# =========================
# 上传 Excel
# =========================
uploaded_file = st.file_uploader("📁 上传 Excel 文件", type=['xlsx', 'xls'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    required_cols = {'产品名', '数量'}
    if not required_cols.issubset(df.columns):
        st.error("Excel 必须包含 '产品名' 和 '数量' 列")
    else:
        dealer_cols = [col for col in df.columns if col not in ['产品名', '数量']]
        if len(dealer_cols) < 2:
            st.error("至少需要两个经销商价格列")
        else:
            dealer1, dealer2 = dealer_cols[:2]
            df[dealer1] = pd.to_numeric(df[dealer1], errors='coerce')
            df[dealer2] = pd.to_numeric(df[dealer2], errors='coerce')
            df['数量'] = pd.to_numeric(df['数量'], errors='coerce')
            df['差额'] = df[dealer1] - df[dealer2]

            st.subheader("📊 Excel 数据")
            st.dataframe(df)

            products = df['产品名'].tolist()
            n_products = len(products)
            x = np.arange(n_products)
            width = 0.25

            # =========================
            # 静态柱状图
            # =========================
            fig1, ax1 = plt.subplots(figsize=(max(12, n_products*0.6), 6))
            ax1.bar(x - width, df[dealer1], width, label=dealer1, color='#1f77b4', alpha=0.8, edgecolor='k')
            ax1.bar(x, df[dealer2], width, label=dealer2, color='#ff7f0e', alpha=0.8, edgecolor='k')
            colors = ['#e74c3c' if val > 0 else '#2ecc71' for val in df['差额']]
            ax1.bar(x + width, df['差额'].abs(), width, color=colors, alpha=0.9, edgecolor='k', label='差额(A-B)')

            for i in range(n_products):
                ax1.text(x[i]+width,
                         df['差额'].abs()[i]+max(df[dealer1].max(), df[dealer2].max())*0.02,
                         f"{df['差额'][i]:+.0f}", ha='center', va='bottom', fontsize=10, color=colors[i])

            ax1.set_xticks(x)
            ax1.set_xticklabels(products, rotation=0, ha='center', fontsize=10)
            ax1.set_ylabel('价格 / 差额', fontsize=11)
            ax1.set_title('静态产品价格和差额', fontsize=14)
            ax1.legend(fontsize=10)
            ax1.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.subheader("📈 静态柱状图")
            st.pyplot(fig1)

            # =========================
            # 动态总差额柱状图
            # =========================
            st.subheader("⚡ 动态总差额柱状图")
            quantities = {}
            for product in products:
                default_qty = int(df.loc[df['产品名']==product, '数量'].values[0])
                quantities[product] = st.slider(
                    f"{product} 数量",
                    min_value=0,
                    max_value=10000,
                    value=default_qty,
                    step=1
                )

            df['数量'] = df['产品名'].map(quantities)
            df['总差额'] = df['差额'] * df['数量']
            total_diff = df['总差额'].sum()
            st.write(f"所有产品总差额: {total_diff:.0f}")

            fig2, ax2 = plt.subplots(figsize=(max(12, n_products*0.6), 6))
            colors = ['#e74c3c' if val > 0 else '#2ecc71' for val in df['差额']]
            ax2.bar(x, df['总差额'].abs(), width, color=colors, alpha=0.9, edgecolor='k')

            # 动态总差额右上角显示
            diff_text = "\n".join([f"{products[i]}: {df['总差额'][i]:+.0f}" for i in range(n_products)])
            ax2.text(
                1.02, 0.95, diff_text, transform=ax2.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='left',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
            )

            ax2.set_xticks(x)
            ax2.set_xticklabels(products, rotation=0, ha='center', fontsize=10)
            ax2.set_ylabel('总差额', fontsize=11)
            ax2.set_title(f'动态总差额 (总合={total_diff:.0f})', fontsize=14)
            ax2.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
