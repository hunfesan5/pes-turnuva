# turnuva.py

import streamlit as st
import pandas as pd

# Sayfa yapılandırmasını ayarla (geniş mod ve başlık)
st.set_page_config(layout="wide", page_title="PES Turnuva Paneli")

# Oyuncu ve Fikstür Bilgileri
PLAYERS = ["İsmail", "Mücahit", "Ozan", "Özkan", "Tuncay", "Vedat"]

# Session state'i kullanarak fikstür verilerini başlat
# Bu sayede skorlar sayfa yenilense bile kaybolmaz
if 'fixture' not in st.session_state:
    st.session_state.fixture = [
        {"match_id": 1,  "home_team": ("İsmail", "Vedat"),   "away_team": ("Mücahit", "Tuncay"), "home_score": None, "away_score": None, "played": False},
        {"match_id": 2,  "home_team": ("İsmail", "Tuncay"),  "away_team": ("Vedat", "Özkan"),   "home_score": None, "away_score": None, "played": False},
        {"match_id": 3,  "home_team": ("İsmail", "Özkan"),   "away_team": ("Tuncay", "Ozan"),    "home_score": None, "away_score": None, "played": False},
        {"match_id": 4,  "home_team": ("İsmail", "Ozan"),    "away_team": ("Özkan", "Mücahit"),  "home_score": None, "away_score": None, "played": False},
        {"match_id": 5,  "home_team": ("İsmail", "Mücahit"), "away_team": ("Ozan", "Vedat"),     "home_score": None, "away_score": None, "played": False},
        {"match_id": 6,  "home_team": ("Ozan", "Özkan"),     "away_team": ("İsmail", "Vedat"),   "home_score": None, "away_score": None, "played": False},
        {"match_id": 7,  "home_team": ("Mücahit", "Ozan"),   "away_team": ("İsmail", "Tuncay"),  "home_score": None, "away_score": None, "played": False},
        {"match_id": 8,  "home_team": ("Vedat", "Mücahit"),  "away_team": ("İsmail", "Özkan"),   "home_score": None, "away_score": None, "played": False},
        {"match_id": 9,  "home_team": ("Tuncay", "Vedat"),   "away_team": ("İsmail", "Ozan"),    "home_score": None, "away_score": None, "played": False},
        {"match_id": 10, "home_team": ("Özkan", "Tuncay"),   "away_team": ("İsmail", "Mücahit"), "home_score": None, "away_score": None, "played": False},
        {"match_id": 11, "home_team": ("Mücahit", "Tuncay"), "away_team": ("Ozan", "Özkan"),     "home_score": None, "away_score": None, "played": False},
        {"match_id": 12, "home_team": ("Vedat", "Özkan"),    "away_team": ("Mücahit", "Ozan"),   "home_score": None, "away_score": None, "played": False},
        {"match_id": 13, "home_team": ("Tuncay", "Ozan"),    "away_team": ("Vedat", "Mücahit"),  "home_score": None, "away_score": None, "played": False},
        {"match_id": 14, "home_team": ("Özkan", "Mücahit"),  "away_team": ("Tuncay", "Vedat"),   "home_score": None, "away_score": None, "played": False},
        {"match_id": 15, "home_team": ("Ozan", "Vedat"),     "away_team": ("Özkan", "Tuncay"),   "home_score": None, "away_score": None, "played": False},
    ]

def calculate_stats():
    """Fikstürdeki skorlara göre oyuncu istatistiklerini hesaplar."""
    stats = {player: {'OM': 0, 'G': 0, 'B': 0, 'M': 0, 'AG': 0, 'YG': 0, 'AV': 0, 'P': 0} for player in PLAYERS}
    
    for match in st.session_state.fixture:
        if match['played']:
            home_players = match['home_team']
            away_players = match['away_team']
            hs = match['home_score']
            aws = match['away_score']

            # İlgili 4 oyuncu için OM (Oynanan Maç) artır
            for p in home_players + away_players:
                stats[p]['OM'] += 1

            # Golleri ve puanları işle
            for p in home_players:
                stats[p]['AG'] += hs
                stats[p]['YG'] += aws
            for p in away_players:
                stats[p]['AG'] += aws
                stats[p]['YG'] += hs
            
            # Galibiyet/Beraberlik/Mağlubiyet durumunu işle
            if hs > aws: # Ev sahibi kazandı
                for p in home_players:
                    stats[p]['G'] += 1
                    stats[p]['P'] += 3
                for p in away_players:
                    stats[p]['M'] += 1
            elif aws > hs: # Deplasman kazandı
                for p in away_players:
                    stats[p]['G'] += 1
                    stats[p]['P'] += 3
                for p in home_players:
                    stats[p]['M'] += 1
            else: # Beraberlik
                for p in home_players + away_players:
                    stats[p]['B'] += 1
                    stats[p]['P'] += 1

    # Averajları hesapla ve DataFrame'e dönüştür
    for player in stats:
        stats[player]['AV'] = stats[player]['AG'] - stats[player]['YG']
    
    df = pd.DataFrame.from_dict(stats, orient='index')
    df.index.name = "Oyuncu"
    df = df.sort_values(by=['P', 'AV', 'AG'], ascending=[False, False, False])
    
    return df

# --- ARAYÜZ KISMI ---

st.title("🏆 PES 2v2 Turnuva Paneli 🏆")
st.markdown("---")

# İki ana sütun oluştur: Fikstür ve Puan Durumu
col1, col2 = st.columns((1.5, 1))

with col1:
    st.header("📋 Maç Sonuçları")
    st.markdown("Maç sonuçlarını girin ve **'Kaydet'** butonuna tıklayın. Puan durumu anında güncellenecektir.")

    # Fikstürü göster ve skor giriş alanlarını oluştur
    for i, match in enumerate(st.session_state.fixture):
        st.markdown(f"**Maç {match['match_id']}**")
        row = st.columns((2, 1, 0.5, 1, 2, 1.5))
        
        home_team_str = f" & ".join(match['home_team'])
        away_team_str = f" & ".join(match['away_team'])

        row[0].text(home_team_str)
        
        # Her bir skor girişi için benzersiz bir anahtar (key) oluştur
        home_score = row[1].number_input("Skor", min_value=0, max_value=30, key=f"h_score_{i}", value=match['home_score'] or 0, label_visibility="collapsed")
        row[2].text("-")
        away_score = row[3].number_input("Skor", min_value=0, max_value=30, key=f"a_score_{i}", value=match['away_score'] or 0, label_visibility="collapsed")
        row[4].text(away_team_str)

        # Kaydet butonu
        if row[5].button("Kaydet", key=f"save_{i}"):
            st.session_state.fixture[i]['home_score'] = home_score
            st.session_state.fixture[i]['away_score'] = away_score
            st.session_state.fixture[i]['played'] = True
            st.rerun() # Sayfayı yeniden çalıştırarak puan durumunu anında güncelle
        
        st.markdown("---")

with col2:
    st.header("📈 Puan Durumu")
    
    # Hesaplanan istatistikleri göster
    stats_df = calculate_stats()
    
    # Sütun isimlerini Türkçeleştir
    stats_df.columns = ["OM", "G", "B", "M", "AG", "YG", "AV", "Puan"]
    
    st.dataframe(stats_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # Turnuva geneli istatistikler
    st.header("📊 Turnuva İstatistikleri")
    played_matches = sum(1 for m in st.session_state.fixture if m['played'])
    total_goals = sum(m['home_score'] + m['away_score'] for m in st.session_state.fixture if m['played'])
    
    st.metric(label="Oynanan Toplam Maç", value=f"{played_matches} / 15")
    st.metric(label="Atılan Toplam Gol", value=total_goals)
    if played_matches > 0:
        st.metric(label="Maç Başına Gol Ortalaması", value=f"{total_goals / played_matches:.2f}")

