import streamlit as st
import math

# 앱 제목
st.title("🧮 멀티 기능 계산기 (사칙연산 / 모듈러 / 지수 / 로그)")

# 사용자 입력
num1 = st.number_input("첫 번째 숫자를 입력하세요:", value=0.0, format="%.10f")
num2 = st.number_input("두 번째 숫자를 입력하세요:", value=0.0, format="%.10f")

# 선택 메뉴
operation = st.selectbox(
    "원하는 연산을 선택하세요:",
    ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)",
     "모듈러 (%)", "지수연산 (x^y)", "로그 (log_x y)"]
)

# 계산 실행
if st.button("계산하기"):
    try:
        if operation == "덧셈 (+)":
            result = num1 + num2

        elif operation == "뺄셈 (-)":
            result = num1 - num2

        elif operation == "곱셈 (×)":
            result = num1 * num2

        elif operation == "나눗셈 (÷)":
            if num2 == 0:
                raise ZeroDivisionError("0으로 나눌 수 없습니다.")
            result = num1 / num2

        elif operation == "모듈러 (%)":
            if num2 == 0:
                raise ZeroDivisionError("0으로 모듈러 연산 불가.")
            result = num1 % num2

        elif operation == "지수연산 (x^y)":
            result = num1 ** num2

        elif operation == "로그 (log_x y)":
            if num1 <= 0 or num1 == 1:
                raise ValueError("로그의 밑은 0보다 커야 하며 1이 될 수 없습니다.")
            if num2 <= 0:
                raise ValueError("로그의 진수는 0보다 커야 합니다.")
            result = math.log(num2, num1)

        st.success(f"결과: {result}")

    except Exception as e:
        st.error(f"오류: {str(e)}")

# 하단 정보
st.caption("Made with Streamlit")
