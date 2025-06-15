import streamlit as st

# Karar motoru fonksiyonu
def doz_ayarla(
    tsh, mevcut_doz, yas, gebe_durumu, anti_tpo_pozitif,
    carpinti_var, cilt_kurulugu_var, adet_duzensizligi, psikiyatrik_hastalik_var,
    ilac_duzenli_kullanim
):
    notlar = []
    yeni_doz = mevcut_doz

    if yas < 15 or yas > 80:
        return mevcut_doz, "Bu sistem yalnızca 15-80 yaş arası için geçerlidir.", "Hekime başvurun."

    if gebe_durumu:
        if tsh > 12:
            yeni_doz += 75
        elif tsh > 8:
            yeni_doz += 50
        elif tsh > 4:
            yeni_doz += 25
        elif anti_tpo_pozitif and tsh > 2.5:
            if tsh > 12:
                yeni_doz += 75
            elif tsh > 8:
                yeni_doz += 50
            else:
                yeni_doz += 25
        kontrol = "Doz değiştiyse 4 hafta, değişmediyse 8 hafta sonra kontrol."
    else:
        if 1 <= tsh <= 2.5:
            kontrol = "3-6 ay sonra kontrole gelin."
        elif not ilac_duzenli_kullanim and tsh < 10:
            kontrol = "4-6 hafta sonra kontrole gelin."
        else:
            if tsh > 15:
                yeni_doz += 75
            elif tsh > 10:
                yeni_doz += 50
            elif tsh > 5:
                yeni_doz += 25
            elif tsh < 0.1:
                yeni_doz -= 50
            elif tsh < 0.5:
                yeni_doz -= 25
            elif 0.5 <= tsh <= 1 and carpinti_var:
                yeni_doz -= 25
            elif 0.5 <= tsh <= 1 and yas > 50:
                yeni_doz -= 25
            elif 2.5 < tsh <= 5 and yas < 45 and (
                cilt_kurulugu_var or anti_tpo_pozitif or adet_duzensizligi or psikiyatrik_hastalik_var
            ):
                yeni_doz += 25
            kontrol = "6-8 hafta sonra kontrole gelin." if yeni_doz != mevcut_doz else (
                "4-6 hafta sonra kontrole gelin." if not ilac_duzenli_kullanim else "3-6 ay sonra kontrole gelin."
            )

    notlar.append("Sabah aç karnına, kahvaltıdan 30-40 dk önce, ilaçlarla 3-4 saat aralık olacak şekilde alınız.")
    if yas > 50 and yeni_doz - mevcut_doz >= 50:
        notlar.append("Doz artışı haftalık 25 mcg şeklinde yavaş yavaş yapılmalı.")

    return round(yeni_doz, 1), kontrol, " ".join(notlar)


# Streamlit Arayüzü
st.title("📊 Primer Hipotiroidi Doz Ayarlama Aracı")

tsh = st.number_input("TSH (mIU/L)", 0.0, 100.0, step=0.1)
mevcut_doz = st.number_input("Mevcut Levotiroksin Dozu (mcg)", 0, 300, step=12)
yas = st.number_input("Yaş", 0, 120, step=1)
ilac_duzenli = st.checkbox("💊 İlacımı son dönemde düzenli kullandım", value=True)

gebe_durumu = st.checkbox("Gebe / Gebelik Planı Var")
anti_tpo = st.checkbox("Anti-TPO Pozitif")
carpinti = st.checkbox("Çarpıntı Var")
cilt = st.checkbox("Cilt Kuruluğu Var")
adet = st.checkbox("Adet Düzensizliği Var")
psikiyatrik = st.checkbox("Psikiyatrik Hastalık Var")

if st.button("💊 Doz Önerisi Hesapla"):
    doz, kontrol, bilgi = doz_ayarla(
        tsh, mevcut_doz, yas, gebe_durumu, anti_tpo,
        carpinti, cilt, adet, psikiyatrik, ilac_duzenli
    )
    st.success(f"Yeni Önerilen Doz: {doz} mcg")
    st.info(kontrol)
    st.warning(bilgi)
