import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator emerytalny",
    page_icon="📈",
    layout="wide"
)

# Tytuł aplikacji
st.title("📈 Kalkulator emerytalny")
st.markdown("---")

# Sidebar z opcjami
st.sidebar.header("⚙️ Opcje")

# Wybór obecnego wieku
current_age = st.sidebar.selectbox(
    "Podaj swój obecny wiek:",
    options=list(range(18, 100)),
    index=14  # domyślnie 30 lat
)

# Wybór wieku planowego przejścia na emeryturę
retirement_age = st.sidebar.selectbox(
    "Podaj wiek, w którym planujesz przejść na emeryturę:",
    options=list(range(50, 80)),
    index=15  # domyślnie 65 lat
)

# Dodatkowe parametry w sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("💰 Parametry dochodowe")

current_savings = st.sidebar.number_input(
    "Obecne oszczędności (PLN):",
    min_value=0,
    value=71000,
    step=500,
    help="Kwota, którą już masz zaoszczędzoną"
)

monthly_income = st.sidebar.number_input(
    "Obecne miesięczne wynagrodzenie netto (PLN):",
    min_value=0,
    value=12833, #833 z PPE (200k brutto * 5% / 12)
    step=500,
    help="Miesięczne wynagrodzenie uwzględniające premie, zwroty podatku itp."
)

income_growth_rate = st.sidebar.slider(
    "Prognozowany wzrost wynagrodzenia (% rocznie):",
    min_value=0.0,
    max_value=10.0,
    value=6.5,
    step=0.1,
    help="Średni roczny wzrost wynagrodzenia (np. awanse, inflacja płac)"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🏠 Parametry wydatków")

monthly_expenses = st.sidebar.number_input(
    "Obecne miesięczne wydatki (PLN):",
    min_value=0,
    value=6500,
    step=500,
    help="Wszystkie miesięczne koszty życia"
)

st.sidebar.markdown("---")
st.sidebar.subheader("📈 Parametry inwestycyjne")

annual_return = st.sidebar.slider(
    "Oczekiwany roczny zwrot (%):",
    min_value=0.0,
    max_value=15.0,
    value=6.0,
    step=0.1,
    help="Średni roczny zwrot z inwestycji"
)

inflation_rate = st.sidebar.slider(
    "Stopa inflacji (%):",
    min_value=0.0,
    max_value=10.0,
    value=3.5,
    step=0.1,
    help="Oczekiwana średnia roczna inflacja (wzrost wydatków)"
)

# Obliczenia
years_to_retirement = retirement_age - current_age

if years_to_retirement <= 0:
    st.error("⚠️ Wiek przejścia na emeryturę musi być wyższy niż obecny wiek!")
else:
    # Kolumny dla głównej treści
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Prognoza wzrostu kapitału")
        
        # Sprawdzenie czy jest nadwyżka do oszczędzania
        current_monthly_surplus = monthly_income - monthly_expenses
        
        if current_monthly_surplus <= 0:
            st.error("⚠️ Obecne wydatki przewyższają dochody! Nie ma nadwyżki do oszczędzania.")
            st.stop()
        
        # Wyświetlenie obecnej nadwyżki
        st.info(f"💰 **Obecna miesięczna nadwyżka do oszczędzania:** {current_monthly_surplus:,.0f} PLN")
        
        # Obliczenia dla każdego roku
        years = []
        nominal_values = []
        real_values = []
        annual_contributions_list = []
        annual_income_list = []
        annual_expenses_list = []
        
        current_value = current_savings
        
        for year in range(years_to_retirement + 1):
            age = current_age + year
            years.append(age)
            
            # Obliczenie dochodów i wydatków dla danego roku
            annual_income = monthly_income * 12 * ((1 + income_growth_rate/100) ** year)
            annual_expenses = monthly_expenses * 12 * ((1 + inflation_rate/100) ** year)
            annual_contribution = annual_income - annual_expenses
            
            annual_income_list.append(annual_income)
            annual_expenses_list.append(annual_expenses)
            annual_contributions_list.append(annual_contribution)
            
            if year > 0 and annual_contribution > 0:
                # Zastosowanie zwrotu z inwestycji i dodanie rocznych wpłat
                current_value = (current_value + annual_contribution) * (1 + annual_return/100)
            elif year > 0:
                # Jeśli nie ma nadwyżki, tylko zwrot z inwestycji
                current_value = current_value * (1 + annual_return/100)
            
            nominal_values.append(current_value)
            # Wartość realna (skorygowana o inflację)
            real_value = current_value / ((1 + inflation_rate/100) ** year)
            real_values.append(real_value)
        
        # Tworzenie DataFrame
        df = pd.DataFrame({
            'Wiek': years,
            'Roczny dochód': annual_income_list,
            'Roczne wydatki': annual_expenses_list,
            'Roczna wpłata': annual_contributions_list,
            'Wartość nominalna': nominal_values,
            'Wartość realna': real_values
        })
        
        # Wykres Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Wiek'],
            y=df['Wartość nominalna'],
            mode='lines+markers',
            name='Wartość nominalna',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate='Wiek: %{x}<br>Wartość: %{y:,.0f} PLN<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Wiek'],
            y=df['Wartość realna'],
            mode='lines+markers',
            name='Wartość realna (po inflacji)',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=6),
            hovertemplate='Wiek: %{x}<br>Wartość realna: %{y:,.0f} PLN<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Wzrost kapitału emerytalnego ({years_to_retirement} lat)",
            xaxis_title="Wiek",
            yaxis_title="Wartość (PLN)",
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Formatowanie osi Y
        #fig.update_yaxis(tickformat=',.0f')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela z danymi
        st.subheader("📋 Szczegółowe dane")
        
        # Formatowanie wartości w tabeli
        df_display = df.copy()
        df_display['Roczny dochód'] = df_display['Roczny dochód'].apply(lambda x: f"{x:,.0f} PLN")
        df_display['Roczne wydatki'] = df_display['Roczne wydatki'].apply(lambda x: f"{x:,.0f} PLN")
        df_display['Roczna wpłata'] = df_display['Roczna wpłata'].apply(lambda x: f"{x:,.0f} PLN")
        df_display['Wartość nominalna'] = df_display['Wartość nominalna'].apply(lambda x: f"{x:,.0f} PLN")
        df_display['Wartość realna'] = df_display['Wartość realna'].apply(lambda x: f"{x:,.0f} PLN")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("📈 Podsumowanie")
        
        final_nominal = nominal_values[-1]
        final_real = real_values[-1]
        total_contributions = current_savings + sum(annual_contributions_list[1:])  # Pomijamy rok 0
        investment_gain = final_nominal - total_contributions
        
        # Średnia roczna wpłata (z lat, gdy była dodatnia)
        positive_contributions = [c for c in annual_contributions_list[1:] if c > 0]
        avg_annual_contribution = sum(positive_contributions) / len(positive_contributions) if positive_contributions else 0
        
        # Metryki
        st.metric(
            "Kapitał na emeryturze",
            f"{final_nominal:,.0f} PLN",
            help="Wartość nominalna kapitału"
        )
        
        st.metric(
            "Wartość realna",
            f"{final_real:,.0f} PLN",
            help="Wartość skorygowana o inflację"
        )
        
        st.metric(
            "Całkowite wpłaty",
            f"{total_contributions:,.0f} PLN",
            help="Suma wszystkich wpłat przez lata"
        )
        
        st.metric(
            "Średnia roczna wpłata",
            f"{avg_annual_contribution:,.0f} PLN",
            help="Średnia z lat z dodatnią nadwyżką"
        )
        
        st.metric(
            "Zysk z inwestycji",
            f"{investment_gain:,.0f} PLN",
            help="Różnica między kapitałem a wpłatami"
        )
        
        # Dodatkowe informacje
        st.markdown("---")
        st.subheader("💡 Dodatkowe informacje")
        
        # Ostatnia wpłata w roku emerytury
        final_contribution = annual_contributions_list[-1]
        final_income = annual_income_list[-1]
        final_expenses = annual_expenses_list[-1]
        
        st.info(f"**W roku emerytury ({retirement_age} lat):**\n"
                f"Dochód: {final_income:,.0f} PLN\n"
                f"Wydatki: {final_expenses:,.0f} PLN\n"
                f"Nadwyżka: {final_contribution:,.0f} PLN")
        
        # Miesięczna emerytura (4% reguła) - z wartości nominalnej
        monthly_pension_nominal = (final_nominal * 0.04) / 12
        # Miesięczna emerytura w wartości realnej (siła nabywcza dzisiejsza)
        monthly_pension_real = (final_real * 0.04) / 12
        
        st.info(f"**Miesięczna emerytura (4% reguła):**\n{monthly_pension_nominal:,.0f} PLN (w cenach z {current_age + years_to_retirement} roku)")
        
        # Porównanie z obecną siłą nabywczą - to jest właśnie zdyskontowana wartość
        st.info(f"**To odpowiada dzisiaj:**\n{monthly_pension_real:,.0f} PLN siły nabywczej")
        
        # Porównanie z obecnymi wydatkami
        pension_coverage = (monthly_pension_real / monthly_expenses) * 100
        st.info(f"**Pokrycie obecnych wydatków:**\n{pension_coverage:.1f}% ({monthly_pension_real:,.0f} PLN vs {monthly_expenses:,.0f} PLN)")
        
        # Czas podwojenia kapitału
        if annual_return > 0:
            doubling_time = 72 / annual_return
            st.info(f"**Czas podwojenia kapitału:**\n{doubling_time:.1f} lat")

# Dodatkowa sekcja z poradami
st.markdown("---")
st.subheader("💡 Porady emerytalne")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Zasada 4%**
    
    Bezpieczna roczna wypłata to 4% zgromadzonego kapitału. 
    To oznacza, że potrzebujesz 25x swoich rocznych wydatków.
    """)

with col2:
    st.markdown("""
    **📊 Dywersyfikacja**
    
    Rozłóż inwestycje między różne klasy aktywów: 
    akcje, obligacje, nieruchomości, surowce.
    """)

with col3:
    st.markdown("""
    **⏰ Czas to pieniądz**
    
    Im wcześniej zaczniesz, tym więcej skorzystasz 
    z procentu składanego. Każdy rok ma znaczenie!
    """)
