import streamlit as st
import math
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------
# 앱 제목
# -----------------------------------
st.title("📐 멀티 기능 웹앱")

# -----------------------------------
# 사이드바 메뉴
# -----------------------------------
menu = st.sidebar.selectbox("메뉴 선택", ["계산기", "확률 시뮬레이터"])


# ============================================================
# 1) 계산기 기능
# ============================================================
if menu == "계산기":
    st.header("🧮 계산기")

    # 숫자 입력
    num1 = st.number_input("첫 번째 숫자:", value=0.0, format="%.10f")
    num2 = st.number_input("두 번째 숫자:", value=0.0, format="%.10f")

    # 연산 선택
    operation = st.selectbox(
        "연산 선택:",
        ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)",
        "모듈러 (%)", "지수연산 (x^y)", "로그 (log_x y)"]
    )

    # 계산하기
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
                    raise ValueError("로그의 밑은 0보다 크고 1이 아니어야 합니다.")
                if num2 <= 0:
                    raise ValueError("로그의 진수는 0보다 커야 합니다.")
                result = math.log(num2, num1)

            st.success(f"결과: {result}")

        except Exception as e:
            st.error(f"오류: {e}")

    # -----------------------------------
    # 다항함수 그래프
    # -----------------------------------
    st.subheader("📈 다항함수 그래프 그리기 (Plotly)")

    poly_input = st.text_input("다항식 입력 (例: 3x^2 - 2x + 1)", "x^2 - 2x + 1")
    x_min = st.number_input("x 최소값", value=-10)
    x_max = st.number_input("x 최대값", value=10)

    if st.button("그래프 그리기"):
        try:
            poly_expr = poly_input.replace("^", "**")
            x = np.linspace(x_min, x_max, 500)
            y = eval(poly_expr, {"x": x, "np": np, "math": math})

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f"f(x) = {poly_input}"))
            fig.update_layout(
                title="다항함수 그래프",
                xaxis_title="x",
                yaxis_title="f(x)",
                template="plotly_white"
            )
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"그래프 오류: {e}")


# ============================================================
# 2) 확률 시뮬레이터
# ============================================================
elif menu == "확률 시뮬레이터":

    st.header("🎲 확률 시뮬레이터")

    sim_type = st.selectbox("시뮬레이션 선택", ["동전", "주사위"])
    trials = st.number_input("시행 횟수", value=100, min_value=1, step=1)

    if st.button("시뮬레이션 실행"):
        if sim_type == "동전":
            outcomes = np.random.choice(["앞면", "뒷면"], size=trials)
        else:  # 주사위
            outcomes = np.random.randint(1, 7, size=trials)

        # 결과 집계
        unique, counts = np.unique(outcomes, return_counts=True)
        result = dict(zip(unique, counts))

        st.write("### 결과:", result)

        # Plotly 시각화
        fig = px.bar(
            x=list(result.keys()),
            y=list(result.values()),
            labels={"x": "결과", "y": "빈도"},
            title=f"{sim_type} 시뮬레이션 결과 ({trials}회)"
        )
        fig.update_layout(template="plotly_white")

        st.plotly_chart(fig)


st.caption("Made with Streamlit · Plotly")
import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.title("🧮 멀티 기능 계산기 + 다항함수 그래프")

# ----------------------------
# 숫자 입력 + 연산 기능
# ----------------------------
st.header("1️⃣ 기본 연산 계산기")

num1 = st.number_input("첫 번째 숫자:", value=0.0, format="%.10f")
num2 = st.number_input("두 번째 숫자:", value=0.0, format="%.10f")

operation = st.selectbox(
    "연산 선택:",
    ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)",
     "모듈러 (%)", "지수연산 (x^y)", "로그 (log_x y)"]
)

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
                raise ValueError("로그의 밑은 0보다 크고 1이 아니어야 합니다.")
            if num2 <= 0:
                raise ValueError("로그의 진수는 0보다 커야 합니다.")
            result = math.log(num2, num1)

        st.success(f"결과: {result}")

    except Exception as e:
        st.error(f"오류: {str(e)}")


# ----------------------------
# 다항함수 그래프 기능
# ----------------------------
st.header("2️⃣ 다항함수 그래프 그리기")

poly_input = st.text_input("다항식을 입력하세요 (예: 3x^2 - 2x + 5):", value="x^2 - 2x + 1")
x_min = st.number_input("x 최소값:", value=-10)
x_max = st.number_input("x 최대값:", value=10)

if st.button("그래프 그리기"):

    try:
        # 사용자가 입력한 문자열을 Python 식으로 변환
        poly_expr = poly_input.replace("^", "**")

        # x 범위 생성
        x = np.linspace(x_min, x_max, 400)

        # 식 계산
        y = eval(poly_expr, {"x": x, "np": np, "math": math})

        # 그래프 출력
        fig, ax = plt.subplots()
        ax.plot(x, y, label=f"f(x) = {poly_input}")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"다항식 처리 중 오류 발생: {e}")

st.caption("Made with Streamlit")
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
