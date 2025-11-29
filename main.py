import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# -----------------------------------
# 앱 제목
# -----------------------------------
st.title("📐 멀티 기능 웹앱 (계산기 + 그래프 + 시뮬레이터 + 인구 분석 + 세계 지도)")


# -----------------------------------
# 사이드바 메뉴
# -----------------------------------
menu = st.sidebar.selectbox(
    "메뉴 선택",
    [
        "계산기",
        "다항함수 그래프",
        "확률 시뮬레이터",
        "연도별 세계인구 분석",
        "세계 인구 지도 (Choropleth)"     # 🌍 새 기능 추가
    ]
)


# ============================================================
# 1) 계산기
# ============================================================
if menu == "계산기":
    st.header("🧮 계산기")

    num1 = st.number_input("첫 번째 숫자:", value=0.0, format="%.10f", key="calc_num1")
    num2 = st.number_input("두 번째 숫자:", value=0.0, format="%.10f", key="calc_num2")

    operation = st.selectbox(
        "연산 선택:",
        ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)",
         "모듈러 (%)", "지수연산 (x^y)", "로그 (log_x y)"],
        key="calc_operation"
    )

    if st.button("계산하기", key="calc_button"):
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
                    raise ValueError("로그 밑 오류")
                if num2 <= 0:
                    raise ValueError("로그 진수 오류")
                result = math.log(num2, num1)

            st.success(f"결과: {result}")

        except Exception as e:
            st.error(f"오류: {e}")


# ============================================================
# 2) 다항함수 그래프
# ============================================================
elif menu == "다항함수 그래프":

    st.header("📈 다항함수 그래프")

    poly_input = st.text_input("다항식 입력", "x^2 - 2x + 1", key="poly_input")
    x_min = st.number_input("x 최소값", value=-10.0, key="poly_xmin")
    x_max = st.number_input("x 최대값", value=10.0, key="poly_xmax")

    if st.button("그래프 그리기", key="poly_button"):
        try:
            poly_expr = poly_input.replace("^", "**")
            x = np.linspace(x_min, x_max, 500)
            y = eval(poly_expr, {"x": x, "np": np, "math": math})

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
            fig.update_layout(
                title=f"f(x) = {poly_input}",
                xaxis_title="x",
                yaxis_title="f(x)",
                template="plotly_white"
            )
            st.plotly_chart(fig)
        except:
            st.error("다항식 오류")


# ============================================================
# 3) 확률 시뮬레이터
# ============================================================
elif menu == "확률 시뮬레이터":

    st.header("🎲 확률 시뮬레이터")

    sim_type = st.selectbox("시뮬레이션 선택", ["동전", "주사위"], key="sim_type")
    trials = st.number_input("시행 횟수", value=100, min_value=1, key="sim_trials")

    if st.button("시뮬레이션 실행", key="sim_button"):
        if sim_type == "동전":
            outcomes = np.random.choice(["앞면", "뒷면"], size=trials)
        else:
            outcomes = np.random.randint(1, 7, size=trials)

        unique, counts = np.unique(outcomes, return_counts=True)
        result = dict(zip(unique, counts))

        st.write("### 📊 결과:", result)

        fig = px.bar(
            x=list(result.keys()),
            y=list(result.values()),
            labels={"x": "결과", "y": "빈도"},
            title="시뮬레이션 결과",
            template="plotly_white"
        )
        st.plotly_chart(fig)


# ============================================================
# 4) 연도별 세계인구 분석
# ============================================================
elif menu == "연도별 세계인구 분석":

    st.header("🌍 연도별 세계 인구 분석")

    uploaded_file = st.file_uploader("CSV 또는 Excel 업로드", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.dataframe(df)

            year_col = st.selectbox("연도 컬럼 선택", df.columns)
            pop_col = st.selectbox("인구 컬럼 선택", df.columns)

            fig = px.line(
                df, x=year_col, y=pop_col,
                title="연도별 인구 변화",
                markers=True,
                template="plotly_white"
            )
            st.plotly_chart(fig)

        except:
            st.error("파일 형식 오류 또는 컬럼 분석 불가")


# ============================================================
# 5) 🌍 세계 인구 지도 (Choropleth Map) — 새 기능
# ============================================================
elif menu == "세계 인구 지도 (Choropleth)":

    st.header("🗺️ 세계 인구 지도로 보기")

    st.write("1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022년 세계 인구를 색으로 보여줍니다.")

    # 연도 선택 드롭다운
    selected_year = st.selectbox(
        "연도 선택",
        [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022],
        key="map_year"
    )

    # 예시 데이터 URL (UN Population Data 형식 가정)
    st.info("업로드한 세계 인구 데이터를 기반으로 지도를 생성합니다.")

    file = st.file_uploader("세계 인구 데이터 업로드 (CSV/XLSX)", type=["csv", "xlsx"])

    if file:
        # 파일 읽기
        if file.name.endswith(".csv"):
            data = pd.read_csv(file)
        else:
            data = pd.read_excel(file)

        st.subheader("📄 데이터 미리보기")
        st.dataframe(data)

        # 국가 및 선택된 연도 컬럼 추출
        country_col = st.selectbox("국가 컬럼 선택", data.columns)
        pop_col = st.selectbox("인구 컬럼 선택", data.columns)

        st.subheader(f"🌍 {selected_year}년 세계 인구 지도")

        # Choropleth Map 생성
        fig = px.choropleth(
            data,
            locations=country_col,
            locationmode="country names",
            color=pop_col,
            color_continuous_scale="Viridis",
            title=f"{selected_year}년 세계 인구 지도",
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 기본 통계")
        st.write(f"최대 인구: {data[pop_col].max():,}")
        st.write(f"최소 인구: {data[pop_col].min():,}")
        st.write(f"평균 인구: {data[pop_col].mean():,.2f}")


# -----------------------------------
# 하단
# -----------------------------------
st.caption("Made with Streamlit · Plotly · NumPy · Pandas")
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
menu = st.sidebar.selectbox(
    "메뉴 선택",
    ["계산기", "다항함수 그래프", "확률 시뮬레이터"]
)

# ============================================================
# 1) 계산기 기능
# ============================================================
if menu == "계산기":

    st.header("🧮 계산기")

    # 숫자 입력 (고유 key 필요)
    num1 = st.number_input("첫 번째 숫자:", value=0.0, format="%.10f", key="calc_num1")
    num2 = st.number_input("두 번째 숫자:", value=0.0, format="%.10f", key="calc_num2")

    # 연산 선택
    operation = st.selectbox(
        "연산 선택:",
        ["덧셈 (+)", "뺄셈 (-)", "곱셈 (×)", "나눗셈 (÷)",
        "모듈러 (%)", "지수연산 (x^y)", "로그 (log_x y)"],
        key="calc_operation"
    )

    # 계산하기
    if st.button("계산하기", key="calc_button"):
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


# ============================================================
# 2) 다항함수 그래프 기능
# ============================================================
elif menu == "다항함수 그래프":

    st.header("📈 다항함수 그래프 그리기")

    poly_input = st.text_input(
        "다항식 입력 (例: 3x^2 - 2x + 1)",
        "x^2 - 2x + 1",
        key="poly_input"
    )
    x_min = st.number_input("x 최소값", value=-10, key="poly_xmin")
    x_max = st.number_input("x 최대값", value=10, key="poly_xmax")

    if st.button("그래프 그리기", key="poly_button"):
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
# 3) 확률 시뮬레이터
# ============================================================
elif menu == "확률 시뮬레이터":

    st.header("🎲 확률 시뮬레이터")

    sim_type = st.selectbox("시뮬레이션 선택", ["동전", "주사위"], key="sim_type")
    trials = st.number_input("시행 횟수", value=100, min_value=1, step=1, key="sim_trials")

    if st.button("시뮬레이션 실행", key="sim_button"):
        if sim_type == "동전":
            outcomes = np.random.choice(["앞면", "뒷면"], size=trials)
        else:
            outcomes = np.random.randint(1, 7, size=trials)

        unique, counts = np.unique(outcomes, return_counts=True)
        result = dict(zip(unique, counts))

        st.write("### 결과:", result)

        fig = px.bar(
            x=list(result.keys()),
            y=list(result.values()),
            labels={"x": "결과", "y": "빈도"},
            title=f"{sim_type} 시뮬레이션 결과 ({trials}회)"
        )
        fig.update_layout(template="plotly_white")

        st.plotly_chart(fig)

# Footer
st.caption("Made with Streamlit · Plotly")
