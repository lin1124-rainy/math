import streamlit as st
from sympy import simplify
# 引入 SymPy 的進階解析工具（加入了基礎字典 standard_transformations）
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

st.title("🧮 智慧型數學填充題系統 (親民版)")
st.write("現在你可以直接輸入一般的數學式了！例如：`2x^2`、`4x` 或 `(x+1)(x-1)`")

# 題目資料庫
questions = {
    "第一題": {"text": "請展開並化簡 $(x+1)(x-1)$", "ans": "x^2 - 1"},
    "第二題": {"text": "化簡 $2x + 3x - 1$", "ans": "5x - 1"},
}

# 【修正點】必須要把標準基礎字典加上去，AI 翻譯官才認得數字與變數
transformations = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

for q_id, q_info in questions.items():
    st.subheader(f"{q_id}：{q_info['text']}")

    student_ans = st.text_input(
        f"請輸入答案", key=q_id, placeholder="例如: x^2 - 1 或 5x - 1"
    )

    if st.button(f"送出{q_id}答案"):
        if student_ans == "":
            st.warning("你還沒有輸入答案喔！")
        else:
            try:
                # 使用修正後的翻譯官轉換答案
                parsed_standard = parse_expr(
                    q_info["ans"], transformations=transformations
                )
                parsed_student = parse_expr(
                    student_ans, transformations=transformations
                )

                # 進行數學等價對比
                is_correct = simplify(parsed_standard - parsed_student) == 0

                if is_correct:
                    st.success("🎉 AC")
                else:
                    st.error("❌ WA")

            except Exception as e:
                # 如果真的出錯，順便把錯誤印出來方便排錯
                st.warning(f"⚠️ 系統解析錯誤，請檢查輸入格式。")

    st.write("---")
