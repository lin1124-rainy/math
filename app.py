import streamlit as st
# 引入 SymPy 的進階解析工具
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
)

st.title("智慧型數學答題系統")
st.write("現在你可以直接輸入一般的數學式了！例如：`2x^2`、`4x` 或 `(x+1)(x-1)`")

# 題目資料庫
questions = {
    "第一題": {"text": "請展開並化簡 $(x+1)(x-1)$", "ans": "x^2 - 1"},
    "第二題": {"text": "化簡 $2x + 3x - 1$", "ans": "5x - 1"},
}

# 設定魔法翻譯官：自動處理「省略的乘號」與「^ 次方符號」
transformations = (implicit_multiplication_application, convert_xor)

for q_id, q_info in questions.items():
    st.subheader(f"{q_id}：{q_info['text']}")

    # 提示學生可以用一般數學打法
    student_ans = st.text_input(
        f"請輸入答案", key=q_id, placeholder="例如: x^2 - 1 或 5x - 1"
    )

    if st.button(f"送出{q_id}答案"):
        if student_ans == "":
            st.warning("你還沒有輸入答案喔！")
        else:
            try:
                # 【核心改進】使用 parse_expr 搭配自動轉換，把學生的直覺輸入轉成 Python 數學物件
                parsed_standard = parse_expr(
                    q_info["ans"], transformations=transformations
                )
                parsed_student = parse_expr(
                    student_ans, transformations=transformations
                )

                # 進行數學等價對比 (標準答案 - 學生答案 == 0)
                from sympy import simplify

                is_correct = simplify(parsed_standard - parsed_student) == 0

                if is_correct:
                    st.success("🎉 AC (Correct Answer)! 答對了！")
                else:
                    st.error("❌ WA (Wrong Answer)... 再試試看！")

            except Exception:
                st.warning(
                    "⚠️ 語法錯誤！雖然支援一般輸入，但請不要輸入奇怪的文字喔！"
                )

    st.write("---")
