import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Streamlit Secrets에서 자격 증명 정보 가져오기
credentials_info = dict(st.secrets["google_credentials"])  # 딕셔너리로 변환

# Google Spreadsheet와 연결하는 함수


def get_google_sheet_row_count(sheet_url, sheet_name):
    try:
        # 구글 스프레드시트에 접근할 수 있는 권한 부여
        print("Loading credentials...")
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_info, scope)
        client = gspread.authorize(creds)
        print("Credentials loaded successfully.")

        # 스프레드시트 열기
        print(f"Opening spreadsheet: {sheet_url}")
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.worksheet(sheet_name)
        print(f"Worksheet '{sheet_name}' opened successfully.")

        # 행의 수 가져오기
        rows = worksheet.get_all_values()
        return len(rows)
    except Exception as e:
        print(f"Error in get_google_sheet_row_count: {e}")
        print(f"Exception type: {type(e)}")
        print(f"Exception args: {e.args}")
        raise

# 특정 닉네임의 행을 찾고, 모든 값을 이어붙이는 함수


def find_and_concatenate_row(sheet_url, sheet_name, nickname):
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.worksheet(sheet_name)

        # A열에서 닉네임 찾기
        cell = worksheet.find(nickname)
        row_values = worksheet.row_values(cell.row)

        # 모든 값을 이어붙이기
        concatenated_values = ' / '.join(row_values)
        return concatenated_values
    except gspread.exceptions.CellNotFound:
        return "닉네임을 찾을 수 없습니다."
    except Exception as e:
        return f"An error occurred: {e}"


# Streamlit 앱 설정
st.markdown("<h1 style='text-align: center;'>은하수 소개팅 회원 현황</h1>",
            unsafe_allow_html=True)

# 사용자로부터 두 개의 스프레드시트 URL 입력 받기
male_sheet_url = st.secrets["sheet_urls"]["male"]
female_sheet_url = st.secrets["sheet_urls"]["female"]

# 남성 회원수 가져오기
male_sheet_name = "남성"
female_sheet_name = "여성"

if male_sheet_url and female_sheet_url:
    try:
        male_row_count = get_google_sheet_row_count(
            male_sheet_url, male_sheet_name)-1
        female_row_count = get_google_sheet_row_count(
            female_sheet_url, female_sheet_name)-1

        # 컬럼 레이아웃 사용
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"<div style='text-align: center; font-size: 24px;'><strong>남성 회원 수</strong><br><span style='font-size: 36px;'>{
                        male_row_count}</span></div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div style='text-align: center; font-size: 24px;'><strong>여성 회원 수</strong><br><span style='font-size: 36px;'>{
                        female_row_count}</span></div>", unsafe_allow_html=True)

    except gspread.exceptions.SpreadsheetNotFound:
        st.error("Spreadsheet not found. Please check the URL.")
    except gspread.exceptions.WorksheetNotFound:
        st.error("Worksheet not found. Please check the sheet name.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.error(f"Error details: {str(e)}")  # 예외 메시지 출력

# 사용자 입력 섹션 추가
st.markdown("<h2 style='text-align: center;'>보내는 사람 정보 입력</h2>",
            unsafe_allow_html=True)

# 상태 초기화
if "male_nickname" not in st.session_state:
    st.session_state.male_nickname = ""

if "female_nickname" not in st.session_state:
    st.session_state.female_nickname = ""

# 남성 닉네임 입력 및 버튼
male_nickname = st.text_input(
    "남성 닉네임을 입력하세요:", key="male_nickname", value=st.session_state.male_nickname)
if st.button("남성 닉네임 보내기"):
    if male_nickname:
        result = find_and_concatenate_row(
            male_sheet_url, male_sheet_name, male_nickname)
        st.markdown(f"<div style='text-align: center;'>보내는 사람: 남성, 닉네임: {
                    male_nickname}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align: center;'>결과: {result}</div>", unsafe_allow_html=True)
        st.session_state.male_nickname = ""  # 입력 폼 초기화
    else:
        st.error("닉네임을 입력하세요.")

# 여성 닉네임 입력 및 버튼
female_nickname = st.text_input(
    "여성 닉네임을 입력하세요:", key="female_nickname", value=st.session_state.female_nickname)
if st.button("여성 닉네임 보내기"):
    if female_nickname:
        result = find_and_concatenate_row(
            female_sheet_url, female_sheet_name, female_nickname)
        st.markdown(f"<div style='text-align: center;'>보내는 사람: 여성, 닉네임: {
                    female_nickname}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='text-align: center;'>결과: {result}</div>", unsafe_allow_html=True)
        st.session_state.female_nickname = ""  # 입력 폼 초기화
    else:
        st.error("닉네임을 입력하세요.")
