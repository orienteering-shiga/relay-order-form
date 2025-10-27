# Relay order form

全日本リレーオリエンテーリング大会のリレー走順表申請フォームアプリです。

## Streamlit Community Cloud app

Streamlit Community Cloud appを使うと、無料でStreamlitのホスティングが行えます。

Google フォームでは対話的にフォーム入力内容を記入してもらったり、大量のデータからマスタデータに応じた入力規制を設けることが困難です。

StreamlitではPythonおよびpandasデータフレームのみで効率的にWEBアプリケーションを構築できますので、比較的簡単に高度なWEBアプリケーションの記述が可能となります。

また、ここではデータベースとしてGoogle Spreadsheetと連携した対応ができるように構築していきたいと思います。

### Google Spread sheetへの接続設定

[https://console.cloud.google.com/apis/dashboard](https://console.cloud.google.com/apis/dashboard) にアクセスして、次の手順を実行してください。

* [秘密情報の管理](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
* [Google spreadsheetへアクセスする際のsecrets.tomlの書き方](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet#write-your-streamlit-app)
