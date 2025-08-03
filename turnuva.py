# turnuva.py (Son Fikstür Düzenlemesi ve Kalıcı Kayıt)

import streamlit as st
import pandas as pd
import json
import os

# --- VERİ YÖNETİMİ FONKSİYONLARI ---

DATA_FILE = "kayitli_skorlar.json"

def get_initial_fixture():
    """Turnuvanın başlangıç fikstürünü istenen yeni sıralama ile döndürür."""
    return [
        # Hafta 1-4 (Aynı)
        {"match_id": 1,  "home_team": ("İsmail", "Vedat"),   "away_team": ("Mücahit", "Tuncay"), "home_score": None, "away_score": None, "played": False},
        {"match_id": 2,  "home_team": ("İsmail", "Tuncay"),  "away_team": ("Vedat", "Özkan"),   "home_score": None, "away_score": None, "played": False},
        {"match_id": 3,  "home_team": ("İsmail", "Özkan"),   "away_team": ("Tuncay", "Ozan"),    "home_score": None, "away_score": None, "played": False},
        {"match_id": 4,  "home_team": ("İsmail", "Ozan"),    "away_team": ("Özkan", "Mücahit"),  "home_score": None, "away_score": None, "played": False},
        
        # Hafta 5 (Eski 15. Hafta)
        {"match_id": 15, "home_team": ("Ozan", "Vedat"),     "away_team": ("Özkan", "Tuncay"),   "home_score": None, "away_score": None, "played": False},
        
        # Hafta 6 (Aynı)
        {"match_id": 6,  "home_team": ("Ozan", "Özkan"),     "away_team": ("İsmail", "Vedat"),   "home_score": None, "away_score": None, "played": False},
        
        # Hafta 7 (Eski 13. Hafta)
        {"match_id": 13, "home_team": ("Tuncay", "Ozan"),    "away_team": ("Vedat", "Mücahit"),  "home_score": None, "away_score": None, "played": False},
        
        # Hafta 8 (Aynı)
        {"match_id": 8,  "home_team": ("Vedat", "Mücahit"),  "away_team": ("İsmail", "Özkan"),   "home_score": None, "away_score": None, "played": False},
        
        # Hafta 9 (Eski 11. Hafta)
        {"match_id": 11, "home_team": ("Mücahit", "Tuncay"), "away_team": ("Ozan", "Özkan"),     "home_score": None, "away_score": None, "played": False},
        
        # Hafta 10 (Aynı)
        {"match_id": 10, "home_team": ("Özkan", "Tuncay"),   "away_team": ("İsmail", "Mücahit"), "home_score": None, "away_score": None, "played": False},
        
        # Hafta 11 (Eski 9. Hafta)
        {"match_id": 9,  "home_team": ("Tuncay", "Vedat"),   "away_team": ("İsmail", "Ozan"),    "home_score": None, "away_score": None, "played": False},
        
        # Hafta 12 (Aynı)
        {"match_id": 12, "home_team": ("Vedat", "Özkan"),    "away_team": ("Mücahit", "Ozan"),   "home_score": None, "away_score": None, "played": False},
        
        # Hafta 13 (Eski 7. Hafta)
        {"match_id": 7,  "home_team": ("Mücahit", "Ozan"),   "away_team": ("İsmail", "Tuncay"),  "home_score": None, "away_score": None, "played": False},
        
        # Hafta 14 (Aynı)
        {"match_id": 14, "home_team": ("Özkan", "Mücahit"),  "away_team": ("Tuncay", "Vedat"),   "home_score": None, "away_score": None, "played": False},
        
        # Hafta 15 (Eski 5. Hafta)
        {"match_id": 5,  "home_team": ("İsmail", "Mücahit"), "away_team": ("Ozan", "Vedat"),     "home_score": None, "away_score": None, "played": False},
    ]

def load_data():
    """JSON dosyasından verileri yükler. Dosya yoksa başlangıç verilerini kullanır."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return get_initial_fixture()

def save_data(data):
    """Verileri JSON dosyasına kaydeder."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- UYGULAMA MANTIĞI ---

st.set_page_config(layout="wide", page_title="PES Turnuva Paneli")

PLAYERS = ["İsmail", "Mücahit", "Ozan", "Özkan", "Tuncay", "Vedat"]

if 'fixture' not in st.session_state:
    st.session_state.fixture = load_data()

def calculate_stats():
    """Fikstürdeki skorlara göre oyuncu istatistiklerini hesaplar."""
    stats = {player: {'OM': 0, 'G': 0, 'B': 0, 'M': 0, 'AG': 0, 'YG': 0, 'AV': 0, 'P': 0} for player in PLAYERS}
    
    for match in st.session_state.fixture:
        if match.get('played', False):
            home_players = tuple(match['home_team'])
            away_players = tuple(match['away_team'])
            hs = match['home_score']
            aws = match['away_score']

            for p in home_players + away_players:
                stats[p]['OM'] += 1

            for p in home_players:
                stats[p]['AG'] += hs
                stats[p]['YG'] += aws
            for p in away_players:
                stats[p]['AG'] += aws
                stats[p]['YG'] += hs
            
            if hs > aws:
                for p in home_players:
                    stats[p]['G'] += 1
                    stats[p]['P'] += 3
                for p in away_players:
                    stats[p]['M'] += 1
            elif aws > hs:
                for p in away_players:
                    stats[p]['G'] += 1
                    stats[p]['P'] += 3
                for p in home_players:
                    stats[p]['M'] += 1
            else:
                for p in home_players + away_players:
                    stats[p]['B'] += 1
                    stats[p]['P'] += 1

    for player in stats:
        stats[player]['AV'] = stats[player]['AG'] - stats[player]['YG']
    
    df = pd.DataFrame.from_dict(stats, orient='index')
    df.index.name = "Oyuncu"
    df = df.sort_values(by=['P', 'AV', 'AG'], ascending=[False, False, False])
    
    return df

# --- ARAYÜZ KISMI ---

st.title("🏆 PES 2v2 Turnuva Paneli 🏆")
st.markdown("---")

# Eğer turnuva sıfırlanmak istenirse diye bir buton ekleyelim
if st.sidebar.button("TURNUVAYI SIFIRLA (TÜM SKORLARI SİL)"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.session_state.fixture = get_initial_fixture()
    st.rerun()

col1, col2 = st.columns((1.5, 1))

with col1:
    st.header("📋 Maç Sonuçları")
    st.markdown("Maç sonuçlarını girin ve **'Kaydet'** butonuna tıklayın. Skorlar bilgisayarınıza kaydedilecektir.")

    for i, match in enumerate(st.session_state.fixture):
        # Arayüzde gösterilecek hafta numarasını 1'den başlat
        hafta_no = i + 1
        st.markdown(f"**{hafta_no}. Hafta** (Maç ID: {match['match_id']})")
        
        row = st.columns((2, 1, 0.5, 1, 2, 1.5))
        
        home_team_str = f" & ".join(match['home_team'])
        away_team_str = f" & ".join(match['away_team'])
        
        home_score_val = match['home_score'] if match['home_score'] is not None else 0
        away_score_val = match['away_score'] if match['away_score'] is not None else 0

        row[0].text(home_team_str)
        home_score = row[1].number_input("Skor", min_value=0, max_value=30, key=f"h_score_{i}", value=home_score_val, label_visibility="collapsed")
        row[2].text("-")
        away_score = row[3].number_input("Skor", min_value=0, max_value=30, key=f"a_score_{i}", value=away_score_val, label_visibility="collapsed")
        row[4].text(away_team_str)

        if row[5].button("Kaydet", key=f"save_{i}"):
            st.session_state.fixture[i]['home_score'] = home_score
            st.session_state.fixture[i]['away_score'] = away_score
            st.session_state.fixture[i]['played'] = True
            save_data(st.session_state.fixture)
            st.rerun()

        st.markdown("---")

with col2:
    st.header("📈 Puan Durumu")
    stats_df = calculate_stats()
    stats_df.columns = ["OM", "G", "B", "M", "AG", "YG", "AV", "Puan"]
    st.dataframe(stats_df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.header("📊 Turnuva İstatistikleri")
    played_matches = sum(1 for m in st.session_state.fixture if m.get('played', False))
    total_goals = sum(m['home_score'] + m['away_score'] for m in st.session_state.fixture if m.get('played', False) and m['home_score'] is not None)
    
    st.metric(label="Oynanan Toplam Maç", value=f"{played_matches} / 15")
    st.metric(label="Atılan Toplam Gol", value=total_goals)
    if played_matches > 0:
        st.metric(label="Maç Başına Gol Ortalaması", value=f"{total_goals / played_matches:.2f}")

