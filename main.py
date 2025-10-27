import streamlit as st
import pandas as pd
import re
from streamlit_gsheets import GSheetsConnection

def check_email_format(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def load_editor_window(df : pd.DataFrame, selected_class: str, selected_team: str):
    class_filterd_df = df.loc[df["クラス"] == selected_class]
    filterd_df = class_filterd_df.loc[class_filterd_df["チーム"] == selected_team]
    return filterd_df

def main():
    # Google Sheets Authentication
    conn = st.connection("gsheets", type=GSheetsConnection)

    df = conn.read(
        worksheet="走順シート申請",
        ttl=10,
        dtype=object
    )

    selected_class = st.sidebar.selectbox(
        "クラス",
        df["クラス"].unique(),
        index=None
    )


    selected_team = st.sidebar.selectbox(
            "チーム",
            df.loc[df["クラス"] == selected_class]["チーム"].unique(),
            index=None
    )

    filterd_df = load_editor_window(df,selected_class, selected_team)
    filterd_df = filterd_df.sort_values("走順")
    #df_pivot = filterd_df.set_index(["クラス","チーム","走順"]).unstack("走順").swaplevel(axis=1).stack()
    st.dataframe(filterd_df)
    backup = filterd_df[["ナンバー","走順"]].reset_index(drop=True).values.tolist()

    if len(filterd_df) > 0:
        indexes = filterd_df.index.values.tolist()
        editet_runners = ["", "", ""]
        with st.form("order_form"):
            st.write("走順申請")
            init_name = filterd_df.at[indexes[0], "申請者氏名"]
            if init_name == "nan":
                init_name = ""
            init_mail = filterd_df.at[indexes[0], "申請者email"]
            if init_mail == "nan":
                init_mail = ""
            name = st.text_input("申請者氏名",init_name)
            mail = st.text_input("email",init_mail)
            editet_runners[0] = st.selectbox("1走", filterd_df["氏名"], index=0)
            editet_runners[1] = st.selectbox("2走", filterd_df["氏名"], index=1)
            editet_runners[2] = st.selectbox("3走", filterd_df["氏名"], index=2)
            st.form_submit_button("確認")

        if name in ("", "nan") or mail in ("", "nan"):
            st.error("申請者の氏名とメールアドレスを入力してください。")
        elif not check_email_format(mail):
            st.error("申請者のメールアドレスの書式が不正です。")
        elif len(editet_runners) != len(set(editet_runners)):
            st.error("競技者に重複があります。")
        else:
            filterd_df["走順"] = None
            filterd_df.loc[filterd_df["氏名"] == editet_runners[0],["走順"]] = 1
            filterd_df.loc[filterd_df["氏名"] == editet_runners[1],["走順"]] = 2
            filterd_df.loc[filterd_df["氏名"] == editet_runners[2],["走順"]] = 3
            filterd_df["申請者氏名"] = name
            filterd_df["申請者email"] = mail
            filterd_df = filterd_df.sort_values("走順")
            filterd_df[["ナンバー","走順"]] = backup
            st.write(filterd_df)


            if st.button("登録"):
                df = conn.read(
                            worksheet="走順シート申請",
                            ttl=10,
                            dtype=object

                        )
                df = df.set_index("ナンバー")
                filterd_df = filterd_df.set_index("ナンバー")
                edit_target_df = load_editor_window(df,selected_class, selected_team)
                df.loc[edit_target_df.index] = filterd_df
                df = df[~df.index.duplicated(keep='first')]
                conn.update(
                    worksheet="走順シート申請",
                    data=df.reset_index()
                )

# Print results.

if __name__ == "__main__":
    main()
