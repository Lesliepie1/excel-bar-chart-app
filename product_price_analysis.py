# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib import font_manager as fm
# import os

# # =========================
# # 加载本地字体
# # =========================
# font_path = os.path.join(os.path.dirname(__file__), "Ubuntu_18.04_SimHei.ttf")  # 放在同目录
# if os.path.exists(font_path):
#     my_font = fm.FontProperties(fname=font_path)
#     plt.rcParams['font.family'] = my_font.get_name()
# else:
#     my_font = None
#     st.warning("未找到字体文件，中文可能无法显示")
# plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# # =========================
# # Streamlit 页面设置
# # =========================
# st.set_page_config(page_title="产品价格差额可视化", layout="wide")
# st.title("🛒 产品价格比较与动态差额可视化")

# # =========================
# # 上传 Excel
# # =========================
# uploaded_file = st.file_uploader("📁 上传 Excel 文件", type=['xlsx', 'xls'])
# if uploaded_file is not None:
#     df = pd.read_excel(uploaded_file)

#     # 检查列
#     required_cols = {'产品名', '数量'}
#     if not required_cols.issubset(df.columns):
#         st.error("Excel 必须包含 '产品名' 和 '数量' 列")
#     else:
#         # 自动获取经销商列
#         dealer_cols = [col for col in df.columns if col not in ['产品名', '数量']]
#         if len(dealer_cols) < 2:
#             st.error("至少需要两个经销商价格列")
#         else:
#             dealer1, dealer2 = dealer_cols[:2]

#             # 转为数值
#             df[dealer1] = pd.to_numeric(df[dealer1], errors='coerce')
#             df[dealer2] = pd.to_numeric(df[dealer2], errors='coerce')
#             df['数量'] = pd.to_numeric(df['数量'], errors='coerce')

#             # 计算差额
#             df['差额'] = df[dealer1] - df[dealer2]

#             # =========================
#             # 显示表格
#             # =========================
#             st.subheader("📊 Excel 数据")
#             st.dataframe(df)

#             products = df['产品名'].tolist()
#             n_products = len(products)
#             x = np.arange(n_products)
#             width = 0.25

#             # =========================
#             # 静态柱状图
#             # =========================
#             fig1, ax1 = plt.subplots(figsize=(max(12, n_products*0.6), 6))
#             ax1.bar(x - width, df[dealer1], width, label=dealer1, color='#1f77b4', alpha=0.8, edgecolor='k')
#             ax1.bar(x, df[dealer2], width, label=dealer2, color='#ff7f0e', alpha=0.8, edgecolor='k')
#             colors = ['#e74c3c' if val > 0 else '#2ecc71' for val in df['差额']]
#             ax1.bar(x + width, df['差额'].abs(), width, color=colors, alpha=0.9, edgecolor='k', label='差额(A-B)')

#             # 添加差额顶部标签
#             for i in range(n_products):
#                 ax1.text(
#                     x[i] + width,
#                     df['差额'].abs()[i] + max(df[dealer1].max(), df[dealer2].max())*0.02,
#                     f"{df['差额'][i]:+.0f}",
#                     ha='center', va='bottom',
#                     fontsize=10, color=colors[i],
#                     fontproperties=my_font
#                 )

#             ax1.set_xticks(x)
#             ax1.set_xticklabels(products, rotation=0, ha='center', fontsize=10, fontproperties=my_font)
#             ax1.set_ylabel('价格 / 差额', fontsize=11, fontproperties=my_font)
#             ax1.set_title('静态产品价格和差额', fontsize=14, fontproperties=my_font)
#             ax1.legend(fontsize=10, prop=my_font)
#             ax1.grid(axis='y', linestyle='--', alpha=0.3)
#             plt.tight_layout()
#             st.subheader("📈 静态柱状图")
#             st.pyplot(fig1)

#             # =========================
#             # 动态总差额柱状图
#             # =========================
#             st.subheader("⚡ 动态总差额柱状图")

#             # 创建滑块调整数量（0-10000）
#             quantities = {}
#             for product in products:
#                 default_qty = int(df.loc[df['产品名']==product, '数量'].values[0])
#                 quantities[product] = st.slider(
#                     f"{product} 数量",
#                     min_value=0,
#                     max_value=10000,
#                     value=default_qty,
#                     step=1
#                 )

#             df['数量'] = df['产品名'].map(quantities)
#             df['总差额'] = df['差额'] * df['数量']
#             total_diff = df['总差额'].sum()
#             st.write(f"所有产品总差额: {total_diff:.0f}")

#             # 绘制动态总差额柱状图
#             fig2, ax2 = plt.subplots(figsize=(max(12, n_products*0.6), 6))
#             colors = ['#e74c3c' if val > 0 else '#2ecc71' for val in df['差额']]
#             ax2.bar(x, df['总差额'].abs(), width, color=colors, alpha=0.9, edgecolor='k')

#             # 右上角显示每个产品动态总差额
#             diff_text = "\n".join([f"{products[i]}: {df['总差额'][i]:+.0f}" for i in range(n_products)])
#             ax2.text(
#                 1.02, 0.95, diff_text, transform=ax2.transAxes, fontsize=10,
#                 verticalalignment='top', horizontalalignment='left',
#                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'),
#                 fontproperties=my_font
#             )

#             ax2.set_xticks(x)
#             ax2.set_xticklabels(products, rotation=0, ha='center', fontsize=10, fontproperties=my_font)
#             ax2.set_ylabel('总差额', fontsize=11, fontproperties=my_font)
#             ax2.set_title(f'动态总差额 (总合={total_diff:.0f})', fontsize=14, fontproperties=my_font)
#             ax2.grid(axis='y', linestyle='--', alpha=0.3)
#             plt.tight_layout()
#             st.pyplot(fig2)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import os


# =========================
# 加载本地字体
# =========================

# 当前项目目录下的字体文件
font_path = os.path.join(os.getcwd(), "Ubuntu_18.04_SimHei.ttf")
my_font = font_manager.FontProperties(fname=font_path)

# 设置 matplotlib 使用这个字体
plt.rcParams['font.family'] = my_font.get_name()  # 注意这里不要写 'SimHei'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="产品价格差额可视化", layout="wide")
st.title("🛒 产品价格比较与动态差额可视化")

# =========================
# 上传 Excel
# =========================
uploaded_file = st.file_uploader("📁 上传 Excel 文件", type=['xlsx', 'xls'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # 检查列
    required_cols = {'产品名', '数量'}
    if not required_cols.issubset(df.columns):
        st.error("Excel 必须包含 '产品名' 和 '数量' 列")
    else:
        # 动态识别所有经销商列
        dealer_cols = [col for col in df.columns if col not in ['产品名', '数量']]
        if len(dealer_cols) < 2:
            st.error("至少需要两个经销商价格列")
        else:
            # 转数值
            for col in dealer_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df['数量'] = pd.to_numeric(df['数量'], errors='coerce')

            # =========================
            # 显示表格
            # =========================
            st.subheader("📊 Excel 数据")
            st.dataframe(df)

            products = df['产品名'].tolist()
            n_products = len(products)
            x = np.arange(n_products)

            # =========================
            # 静态柱状图（所有供应商）
            # =========================
            st.subheader("📈 所有供应商价格对比")
            fig1, ax1 = plt.subplots(figsize=(max(12, n_products * 0.6), 6))
            width = 0.8 / len(dealer_cols)  # 动态调整柱宽

            for i, dealer in enumerate(dealer_cols):
                ax1.bar(x + i * width, df[dealer], width,
                        label=dealer, alpha=0.8, edgecolor='k')

            ax1.set_xticks(x + width * (len(dealer_cols) - 1) / 2)
            ax1.set_xticklabels(products, rotation=0, ha='center', fontsize=10)
            ax1.set_ylabel('价格', fontsize=11)
            ax1.set_title('多供应商价格对比', fontsize=14)
            ax1.legend(fontsize=10)
            ax1.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig1)

            # =========================
            # 差额分析（选择两个供应商）
            # =========================
            st.subheader("⚡ 差额分析")
            dealer1 = st.selectbox("选择经销商 A", dealer_cols, index=0)
            dealer2 = st.selectbox("选择经销商 B", dealer_cols, index=1)

            # 计算差额
            df['差额'] = df[dealer1] - df[dealer2]
            df['差额绝对'] = df['差额'].abs()
            colors = ['#e74c3c' if val > 0 else '#2ecc71' for val in df['差额']]

            fig2, ax2 = plt.subplots(figsize=(max(12, n_products * 0.6), 6))
            ax2.bar(x, df['差额绝对'], 0.6, color=colors, alpha=0.9, edgecolor='k')

            # 添加差额标签（显示原始差额符号）
            for i in range(n_products):
                ax2.text(x[i],
                         df['差额绝对'][i] + df['差额绝对'].max()*0.02,
                         f"{df['差额'][i]:+.0f}",
                         ha='center', va='bottom', fontsize=10, color=colors[i])

            ax2.set_xticks(x)
            ax2.set_xticklabels(products, rotation=0, ha='center', fontsize=10)
            ax2.set_ylabel('差额 (绝对值)', fontsize=11)
            ax2.set_title(f'差额对比 ({dealer1} - {dealer2})', fontsize=14)
            ax2.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)

            # =========================
            # 动态总差额柱状图
            # =========================
            st.subheader("🎛 动态总差额柱状图")

            # 创建滑块调整数量
            quantities = {}
            for product in products:
                default_qty = int(df.loc[df['产品名'] == product, '数量'].values[0])
                quantities[product] = st.slider(
                    f"{product} 数量",
                    min_value=0,
                    max_value=10000,
                    value=default_qty,
                    step=1
                )

            # 更新数量和总差额
            df['数量'] = df['产品名'].map(quantities)
            df['总差额'] = df['差额'] * df['数量']
            df['总差额绝对'] = df['总差额'].abs()
            total_diff = df['总差额'].sum()

            st.write(f"所有产品总差额: {total_diff:.0f}")

            # 绘制动态总差额柱状图
            fig3, ax3 = plt.subplots(figsize=(max(12, n_products * 0.6), 6))
            colors = ['#e74c3c' if val > 0 else '#2ecc71' for val in df['差额']]
            ax3.bar(x, df['总差额绝对'], 0.6, color=colors, alpha=0.9, edgecolor='k')

            # 右上角显示每个产品动态总差额
            diff_text = "\n".join([f"{products[i]}: {df['总差额'][i]:+.0f}" for i in range(n_products)])
            ax3.text(
                1.02, 0.95, diff_text, transform=ax3.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='left',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
            )

            ax3.set_xticks(x)
            ax3.set_xticklabels(products, rotation=0, ha='center', fontsize=10)
            ax3.set_ylabel('动态总差额 (绝对值)', fontsize=11)
            ax3.set_title(f'动态总差额 (总合={total_diff:.0f})', fontsize=14)
            ax3.grid(axis='y', linestyle='--', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig3)









