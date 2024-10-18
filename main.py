import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Google Spreadsheet와 연결하는 함수


def get_google_sheet_row_count(sheet_url, sheet_name):
    try:
        # 구글 스프레드시트에 접근할 수 있는 권한 부여
        print("Loading credentials...")
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "galaxyselfblinddate-3165e8484c88.json", scope)
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


# Streamlit 앱 설정
st.markdown("<h1 style='text-align: center;'>은하수 소개팅 회원 현황</h1>",
            unsafe_allow_html=True)

# 사용자로부터 두 개의 스프레드시트 URL 입력 받기
male_sheet_url = "https://docs.google.com/spreadsheets/d/10qhSG6BNsxb89JiNHo1OL95YUS8MjB6PICzVB_wXaso/edit?gid=1277522226#gid=1277522226"
female_sheet_url = "https://docs.google.com/spreadsheets/d/1hkEnvCfXePw3Ng2QO6Pd-mOJaxha6CBGGvS32TVs03E/edit?gid=716709069#gid=716709069"

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

        # # 추가적인 스타일링
        # st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)
        # st.markdown("<h3 style='text-align: center;'>회원 수 통계</h3>", unsafe_allow_html=True)
        # st.markdown(f"<div style='text-align: center;'><strong>남성 회원 수</strong>: {male_row_count}명</div>", unsafe_allow_html=True)
        # st.markdown(f"<div style='text-align: center;'><strong>여성 회원 수</strong>: {female_row_count}명</div>", unsafe_allow_html=True)

    except gspread.exceptions.SpreadsheetNotFound:
        st.error("Spreadsheet not found. Please check the URL.")
    except gspread.exceptions.WorksheetNotFound:
        st.error("Worksheet not found. Please check the sheet name.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.error(f"Error details: {str(e)}")  # 예외 메시지 출력
