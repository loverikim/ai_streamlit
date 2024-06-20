import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO # 이미지, 엑셀파일 텍스트 파일을 제외한 데이터는 바이너리 형식으로 저장 컨버트해서 보내야함.

def ex_rate(): ##다른화면에 불러오기 위해서 파일의 내용이 class function으로 되어 있어야 불러올 수 있음
# 함수로 만들어서 사용하기
    def get_exchange(currency_code):
        # currency_code = 'USD'
        # page_no = 1
        last_page_num = 10
        df = pd.DataFrame()

        for page_no in range(1,last_page_num+1): #1~3page
            url=f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_no}"
            dfs = pd.read_html(url,header=1,encoding='cp949') #header=1 -> 0번은 안가져오겠다.

            # 크롤링시 예외처리 해주는것이 좋음.
            if dfs[0].empty:
                if(page_no == 1):
                    print(f"통화코드({currency_code})가 잘 못 지정되었습니다.")
                else:
                    print(f"{page_no}마지막 페이지 입니다.")
                break

            # print(dfs[0])    
            df = pd.concat([df,dfs[0]]) # 1개씩 들어감.# 밑으로 합치기 concat

        return df

    # print(df)
    currency_name_dict = {'미국 달러' :'USD','유럽연합 유로':'EUR','일본 엔':'JPY'}
    #### 사이드바 ####
    # currency_name = st.sidebar.selectbox('통화선택',currency_name_dict.keys()) #사용자가 선택한 key값
    # clicked = st.sidebar.button("환율 데이터 가져오기") # 버튼 선택
    currency_name = st.selectbox('통화선택',currency_name_dict.keys()) #사용자가 선택한 key값
    clicked = st.button("환율 데이터 가져오기") # 버튼 선택

    if clicked:
        currency_code = currency_name_dict[currency_name] # 값을 가져와서 
        df_exchange = get_exchange(currency_code)
        # print(df_exchange)

        #원하는 열만 선택
        df_exchange_rate = df_exchange[['날짜','매매기준율','사실 때','파실 때','보내실 때','받으실 때']]
        df_exchange_rate2 = df_exchange_rate.set_index('날짜')

        #날짜열의 데이터 변경
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index, format='%Y-%m-%d', errors="ignore")

        #환율 데이터 표시
        st.subheader(f"{currency_name} 환율 데이터")
        st.dataframe(df_exchange_rate2)

        # df_exchange_rate2.info()

        #한글코드넣기
        matplotlib.rcParams['font.family'] ='Malgun Gothic'


        #차트(선 그래프) 그리기
        ax = df_exchange_rate2['매매기준율'].plot(figsize=(15,5), grid=True) #차트크기 조정시
        ax.set_title("환율(매매기준율) 그래프", fontsize=15)
        ax.set_xlabel("기간", fontsize=10)
        ax.set_ylabel(f"원화/{currency_name}", fontsize=10)
        plt.xticks(fontsize=10) #x축 눈금값의 폰트크기
        plt.yticks(fontsize=10) 
        fig = ax.get_figure() # fig객체 가져오기
        st.pyplot(fig)

        #파일 다운로드 -> 가상 공간에 생성 -> 버튼을 눌렀을 때 로컬에 저장이 되도록 하기 위해.
        st.text("** 환율 데이터 파일 다운로드 **")
        #dataframe 데이터를 csv 데이터로 변환 
        csv_data = df_exchange_rate.to_csv()

        #dataframe 데이터를 xlsx 데이터로 변환 
        #주의!) 저장하는 방법이 다름 바이너리파일로 넣었다가 컨버트가 되어서 변환 
        excel_data = BytesIO() #메모리 버퍼(임시장소)에 바이너리 객체 생성
        df_exchange_rate.to_excel(excel_data) # 엑셀 형식으로 버퍼에 쓰기

        col = st.columns(2) #2개의 새로단 생성
        with col[0]:
            st.download_button("csv파일 다운로드", csv_data,file_name='exchange_rate_data.csv')
        with col[1]:
            st.download_button("엑셀파일 다운로드", excel_data,file_name='exchange_rate_data.xlsx')


# else:
#     pass

