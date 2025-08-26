import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import os

# ページ設定
st.set_page_config(
    page_title="グリーンキーパー作業登録",
    page_icon="🌱",
    layout="centered",  # wideからcenteredに変更してモバイル最適化
    initial_sidebar_state="collapsed"
)

# カスタムCSSでモバイルフレンドリーなスタイルを適用
st.markdown("""
<style>
    .main {
        padding: 0.1rem;
        max-width: 100%;
    }
    
    /* モバイル最適化 */
    @media (max-width: 768px) {
        .main {
            padding: 0.05rem;
        }
        
        .stButton > button {
            width: 100%;
            height: 2.2rem;
            font-size: 1rem;
            border-radius: 6px;
            margin: 0.15rem 0;
        }
        
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            font-size: 1rem;
            padding: 0.4rem;
            border-radius: 6px;
            height: 2.2rem;
        }
        
        .stTextArea > div > div > textarea {
            font-size: 0.9rem;
            border-radius: 6px;
            padding: 0.3rem;
        }
        
        .stDateInput > div > div > input,
        .stTimeInput > div > div > input {
            font-size: 1rem;
            padding: 0.3rem;
            border-radius: 6px;
            height: 2.2rem;
        }
    }
    
    /* デスクトップ用 */
    .stButton > button {
        width: 100%;
        height: 2rem;
        font-size: 0.9rem;
        border-radius: 6px;
        margin: 0.15rem 0;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        font-size: 0.9rem;
        padding: 0.3rem;
        border-radius: 4px;
        height: 2rem;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 0.8rem;
        border-radius: 4px;
        padding: 0.25rem;
    }
    
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        font-size: 0.9rem;
        padding: 0.3rem;
        border-radius: 4px;
        height: 2rem;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 0.25rem;
        border-radius: 6px;
        margin: 0.15rem 0;
        text-align: center;
    }
    
    .header-section {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 0.25rem;
        border-radius: 6px;
        margin-bottom: 0.25rem;
        text-align: center;
    }
    
    .header-section h1 {
        margin: 0.15rem 0;
        font-size: 1.3rem;
    }
    
    .header-section p {
        margin: 0.15rem 0;
        font-size: 0.8rem;
    }
    
    /* タブのスタイル改善 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.15rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 2rem;
        border-radius: 4px;
    }
    
    /* フォームの間隔調整 */
    .stForm > div {
        margin-bottom: 0.25rem;
    }
    
    /* 作業タイトルのスタイル */
    .work-title {
        background: linear-gradient(90deg, #e8f4fd, #f0f8ff);
        padding: 0.25rem;
        border-radius: 4px;
        margin: 0.25rem 0 0.15rem 0;
        border-left: 2px solid #1f77b4;
    }
    
    /* 見出しのマージン調整 */
    h3 {
        margin: 0.25rem 0 0.15rem 0;
        font-size: 1rem;
    }
    
    /* 列の間隔調整 */
    .row-widget.stHorizontal {
        gap: 0.25rem;
    }
    
    /* 入力フィールド間の間隔調整 */
    .stTextInput, .stSelectbox, .stNumberInput, .stDateInput, .stTimeInput {
        margin-bottom: 0.15rem;
    }
    
    /* さらに縦方向を詰める */
    .stForm {
        padding: 0.25rem;
    }
    
    /* セクション間の間隔を最小限に */
    .stMarkdown {
        margin-bottom: 0.15rem;
    }
    
    /* 成功メッセージの間隔調整 */
    .stSuccess {
        margin: 0.15rem 0;
        padding: 0.25rem;
    }
    
    /* チェックボックスの間隔調整 */
    .stCheckbox {
        margin: 0.15rem 0;
    }
    
    /* 情報ボックスの間隔調整 */
    .stInfo {
        margin: 0.15rem 0;
        padding: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# データ保存用のファイル
DATA_FILE = "greens_data.json"

def load_data():
    """保存されたデータを読み込む"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """データを保存する"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    # ヘッダー
    st.markdown("""
    <div class="header-section">
        <h1>G&P Turf-Tools</h1>
        <p>ゴルフコース/スタジアム管理作業記録</p>
    </div>
    """, unsafe_allow_html=True)
    
    # タブを作成
    tab1, tab2, tab3 = st.tabs(["🌿 基本", "🚜 更新", "⚙️ 設定"])
    
    with tab1:
        # st.markdown("### 基本作業データ入力")
        
        # 入力フォーム
        with st.form("greens_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # エリアタイプ
                areaType_options = ["グリーン","フェアウェイ","ティー","ラフ"]
                areaType_name = st.selectbox("エリアタイプ", areaType_options)
                
                # エリア名
                area_options = ["全グリーン", "1Hグリーン", "2Hグリーン","3Hグリーン","4Hグリーン","5Hグリーン","6Hグリーン","7Hグリーン","8Hグリーン","9Hグリーン","10Hグリーン","12Hグリーン","13Hグリーン","14Hグリーン","15Hグリーン","16Hグリーン"]
                area_name = st.selectbox("エリア", area_options)
            

            with col2:
                # 日付
                input_date = st.date_input(
                    "日付",
                    value=date.today(),
                    format="YYYY/MM/DD"
                )

                # 時間
                input_time = st.time_input("時間", value=datetime.now().time())
            
            # 刈込データ
            col_title1, col_button1 = st.columns([3, 1])
            with col_title1:
                st.markdown("### 刈込作業")
            with col_button1:
                submitted1 = st.form_submit_button("💾 刈込保存", use_container_width=True)
            
            col3, col4, col5 = st.columns(3)
            with col3:
                # 刈高
                green_height = st.number_input(
                    "刈高 (mm)",
                    min_value=2.0,
                    max_value=10.0,
                    value=3.0,
                    step=0.1,
                    format="%.1f"
                )
                
                # 刈粕量
                rough_height = st.number_input(
                    "刈粕総量 (kg)",
                    min_value=10.0,
                    max_value=50.0,
                    value=25.0,
                    step=1.0,
                    format="%.0f"
                )

            with col4:
                # 散水タイトルとボタン
                col_title2, col_button2 = st.columns([3, 1])
                with col_title2:
                    st.markdown("### 散水作業")
                with col_button2:
                    submitted2 = st.form_submit_button("💾 散水保存", use_container_width=True)
                
                # 散水
                wateringType_options = ["スプリンクラー","スポット","手散水","シリンジング"]
                wateringType_name = st.selectbox("散水タイプ", wateringType_options)

                # 散水時間
                watering_duration = st.number_input("散水量 (ml/m2)",
                    min_value=8.0,
                    max_value=25.0,
                    value=12.0,
                    step=0.5,
                    format="%.1f"
                )
                
                # 雑草・病害虫タイトルとボタン
                col_title3, col_button3 = st.columns([3, 1])
                with col_title3:
                    st.markdown("### 雑草・病害虫")
                with col_button3:
                    submitted3 = st.form_submit_button("💾 病害保存", use_container_width=True)
                
                # 雑草
                weed_options = ["なし", "スズメノカタビラ", "メヒシバ", "クローバー","チガヤ","藻類","コケ","オオバコ","ススズメノヒエ","オヒシバ","ウラジロスズコグサ","ハマスゲ","ヒメクグ","ハヤズソウ","その他"]
                weed_status = st.selectbox("雑草", weed_options)
                
                # 病害
                disease_options = ["なし", "ダラースポット", "ピシウム病（寒涼期）", "立枯病（ゾイシアデクライン）","コケ","サマーパッチ","炭疽病","ドライスポット","デッドスポット","フェアリーリング","疑似葉腐病","ヘルミントスポリウム","かさ枯病"]
                disease_status = st.selectbox("病害", disease_options)
                
                # 害虫・害獣
                pest_options = ["なし", "シバツトガ", "ケラ", "コガネムシ","シバオサゾウムシ","スジキリヨトウ","タマナヤガ","アワヨトウ","チガヤシロオカイガラムシ","サル","シカ","イノシシ"]
                pest_status = st.selectbox("害虫・害獣", pest_options)
                
                # その他タイトルとボタン
                col_title4, col_button4 = st.columns([3, 1])
                with col_title4:
                    st.markdown("### その他")
                with col_button4:
                    submitted4 = st.form_submit_button("💾 その他保存", use_container_width=True)
                
                # その他
                other_notes = st.text_input("その他", placeholder="その他の作業名を入力してください...")
            
            with col5:
                pass
            
            if submitted1 or submitted2 or submitted3 or submitted4:
                # データを保存
                data = {
                    "date": input_date.strftime("%Y-%m-%d"),
                    "time": input_time.strftime("%H:%M"),
                    "areaType": areaType_name,
                    "area_name": area_name,
                    "green_height": green_height,
                    "rough_height": rough_height,
                    "wateringType": wateringType_name,
                    "watering_duration": watering_duration,
                    "weed_status": weed_status,
                    "disease_status": disease_status,
                    "pest_status": pest_status,
                    "other_notes": other_notes,
                    "timestamp": datetime.now().isoformat()
                }
                
                # 既存データを読み込み
                existing_data = load_data()
                existing_data.append(data)
                save_data(existing_data)
                
                st.success("✅ データが正常に保存されました！")
                st.balloons()
    
    with tab2:
        st.markdown("### 更新作業入力")
        
        # 入力フォーム
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # エリアタイプ
                areaType_options = ["グリーン","フェアウェイ","ティー","ラフ"]
                areaType_name = st.selectbox("エリアタイプ", areaType_options)
                
                # エリア名
                area_options = ["全グリーン", "1Hグリーン", "2Hグリーン","3Hグリーン","4Hグリーン","5Hグリーン","6Hグリーン","7Hグリーン","8Hグリーン","9Hグリーン","10Hグリーン","12Hグリーン","13Hグリーン","14Hグリーン","15Hグリーン","16Hグリーン"]
                area_name = st.selectbox("エリア", area_options)
            
            with col2:
                # 日付
                input_date = st.date_input(
                    "日付",
                    value=date.today(),
                    format="YYYY/MM/DD"
                )

                # 時間
                input_time = st.time_input("時間", value=datetime.now().time())
            
            # コアリング
            st.markdown("### コアリング")
            # コアリング保存ボタンをタイトルの下に移動
            submitted_coring = st.form_submit_button("💾 コアリング保存", use_container_width=True)
            
            col_coring1, col_coring2 = st.columns(2)
            
            with col_coring1:
                coring_depth = st.number_input("コアリング深さ (cm)",
                    min_value=5.0,
                    max_value=15.0,
                    value=8.0,
                    step=0.5,
                    format="%.1f"
                )
            
            with col_coring2:
                coring_spacing = st.number_input("コアリング間隔 (cm)",
                    min_value=5.0,
                    max_value=20.0,
                    value=10.0,
                    step=0.5,
                    format="%.1f"
                )
            
            # バーチカルカット
            st.markdown("### バーチカルカット")
            # バーチカル保存ボタンをタイトルの下に移動
            submitted_vertical = st.form_submit_button("💾 バーチカル保存", use_container_width=True)
            
            vertical_depth = st.number_input("バーチカル深さ (cm)",
                min_value=1.0,
                max_value=5.0,
                value=2.0,
                step=0.1,
                format="%.1f"
            )
            
            # 目砂
            st.markdown("### 目砂")
            # 目砂保存ボタンをタイトルの下に移動
            submitted_sand = st.form_submit_button("💾 目砂保存", use_container_width=True)
            
            sand_amount = st.number_input("目砂量 (kg)",
                min_value=10.0,
                max_value=100.0,
                value=30.0,
                step=1.0,
                format="%.0f"
            )
            
            # その他更新作業
            st.markdown("### その他更新作業")
            # その他更新保存ボタンをタイトルの下に移動
            submitted_other_update = st.form_submit_button("💾 その他更新保存", use_container_width=True)
            
            other_update_notes = st.text_input("その他更新作業", placeholder="その他の更新作業名を入力してください...")
            
            if submitted_vertical or submitted_sand or submitted_coring or submitted_other_update:
                # 更新データを保存
                update_data = {
                    "date": input_date.strftime("%Y-%m-%d"),
                    "time": input_time.strftime("%H:%M"),
                    "areaType": areaType_name,
                    "area_name": area_name,
                    "vertical_depth": vertical_depth if submitted_vertical else None,
                    "sand_amount": sand_amount if submitted_sand else None,
                    "coring_depth": coring_depth if submitted_coring else None,
                    "coring_spacing": coring_spacing if submitted_coring else None,
                    "other_update_notes": other_update_notes if submitted_other_update else "",
                    "timestamp": datetime.now().isoformat()
                }
                
                # 既存データを読み込み
                existing_data = load_data()
                existing_data.append(update_data)
                save_data(existing_data)
                
                st.success("✅ 更新作業データが正常に保存されました！")
                st.balloons()
    
    with tab3:
        st.markdown("### 設定")
        
        # データ削除機能
        st.markdown("#### データ管理")
        
        if st.button("🗑️ 全データを削除", type="secondary"):
            if st.checkbox("本当に削除しますか？"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.success("データが削除されました。")
                    st.rerun()
        
        # アプリ情報
        st.markdown("#### アプリ情報")
        st.info("""
        **eTURF基本作業登録アプリ**
        
        - グリーン、フェアウェイ、ティーの刈込作業を記録
        - 散水作業（スプリンクラー、スポット、手散水）を記録
        - 刈粕総量の記録
        - 天気、気温、湿度などの環境データも記録
        - モバイルフレンドリーなインターフェース
        - データのCSVエクスポート機能
        
        **使用方法:**
        1. 「基本作業入力」タブでデータを入力
        2. 「更新作業入力」タブで保存されたデータを確認
        3. 必要に応じてCSVでダウンロード
        """)

if __name__ == "__main__":
    main()
