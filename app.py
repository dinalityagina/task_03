import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_URL = "http://127.0.0.1:8000"
RECORDS_URL = f"{API_URL}/records"

def load_all_records():
    try:
        response = requests.get(RECORDS_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Ошибка при загрузке данных: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
        return []

def add_record(timestep, cons_eur, cons_sib, price_eur, price_sib):
    new_record = {
        "timestep": timestep,
        "consumption_eur": cons_eur,
        "consumption_sib": cons_sib,
        "price_eur": price_eur,
        "price_sib": price_sib
    }
    try:
        response = requests.post(RECORDS_URL, json=new_record)
        if response.status_code == 201:
            st.success("Запись успешно добавлена!")
            return True
        else:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            st.error(f"Ошибка при добавлении: {error_detail}")
            return False
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
        return False

def delete_record(record_id):
    try:
        response = requests.delete(f"{RECORDS_URL}/{record_id}")
        if response.status_code == 200:
            st.success(f"Запись с ID {record_id} успешно удалена!")
            return True
        elif response.status_code == 404:
            st.error(f"Запись с ID {record_id} не найдена")
            return False
        else:
            st.error(f"Ошибка при удалении: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
        return False

def main():
    st.set_page_config(
        page_title="Потребление энергии",
        layout="wide"
    )
    st.title("Дашборд потребления электроэнергии")
    st.markdown("---")

    # with st.spinner("Загрузка данных..."):
    #     records = load_all_records()
    records = load_all_records()
    if not records:
        st.warning("Нет данных для отображения.")
        return
    df = pd.DataFrame(records)
    df['timestep'] = pd.to_datetime(df['timestep'], format='mixed', errors='coerce')
    df = df.sort_values('timestep')
    st.subheader("Таблица данных")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": "ID",
            "timestep": st.column_config.DatetimeColumn("Время"),
            "consumption_eur": st.column_config.NumberColumn("Потребление (Европ.)", format="%.0f"),
            "consumption_sib": st.column_config.NumberColumn("Потребление (Азиат.)", format="%.0f"),
            "price_eur": st.column_config.NumberColumn("Цена (Евр.)", format="%.2f"),
            "price_sib": st.column_config.NumberColumn("Цена (Аз.)", format="%.2f")
        }
    )
    st.markdown("---")

    st.subheader("Графики")
    fig = px.line(
        df,
        x='timestep',
        y=['price_eur', 'price_sib'],
        title='Сравнение цен',
        labels={'timestep': 'Дата', 'value': 'Цена, руб/МВт·ч', 'variable': 'Регион'}
    )
    # Переименовываем для легенды
    fig.data[0].name = 'Европейский'
    fig.data[1].name = 'Азиатский'
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        df,
        x='timestep',
        y=['consumption_eur', 'consumption_sib'],
        title='Сравнение потребления',
        labels={'timestep': 'Дата', 'value': 'Потребление, МВт·ч', 'variable': 'Регион'}
    )
    fig.data[0].name = 'Европейский'
    fig.data[1].name = 'Азиатский'
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Добавить новую запись")
    with st.form("add_record_form"):
        timestep = st.text_input(
            "Время (ГГГГ-ММ-ДД ЧЧ:ММ)",
            value=datetime.now().strftime("%Y-%m-%d %H:00")
        )
        consumption_eur = st.number_input(
            "Потребление (Европейский)",
            min_value=0.0,
            value=80000.0,
            step=1000.0,
            format="%.0f"
        )
        consumption_sib = st.number_input(
            "Потребление (Азиатский)",
            min_value=0.0,
            value=20000.0,
            step=1000.0,
            format="%.0f"
        )
        price_eur = st.number_input(
            "Цена (Европейский)",
            min_value=0.0,
            value=1000.0,
            step=10.0,
            format="%.2f"
        )
        price_sib = st.number_input(
            "Цена (Азиатский)",
            min_value=0.0,
            value=500.0,
            step=10.0,
            format="%.2f"
        )
        submitted = st.form_submit_button("Добавить запись")
        if submitted:
            try:
                pd.to_datetime(timestep, format='%Y-%m-%d %H:%M')
            except:
                st.error("Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ")
            else:
                success = add_record(timestep, consumption_eur, consumption_sib, price_eur, price_sib)
                if success:
                    st.rerun()

    st.markdown("---")

    st.subheader("Удалить запись")
    delete_id = st.number_input(
        "Введите ID записи для удаления",
        min_value=1,
        step=1,
        value=1
    )
    if st.button("Удалить", type="primary"):
        success = delete_record(delete_id)
        if success:
            st.rerun()
    st.markdown("---")

 # Запускаем приложение
if __name__ == "__main__":
    main()


