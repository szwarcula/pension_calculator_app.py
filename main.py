import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Translations dictionary
translations = {
    'en': {
        'page_title': 'Retirement Calculator',
        'page_icon': '📈',
        'main_title': '📈 Retirement Calculator',
        'sidebar_options': '⚙️ Options',
        'language_select': 'Select Language:',
        'current_age': 'Enter your current age:',
        'retirement_age': 'Enter the age you plan to retire:',
        'income_params': '💰 Income Parameters',
        'current_savings': 'Current savings (USD):',
        'current_savings_help': 'Amount you already have saved',
        'monthly_income': 'Current monthly net income (USD):',
        'monthly_income_help': 'Monthly income including bonuses, tax refunds, etc.',
        'income_growth': 'Expected income growth (% annually):',
        'income_growth_help': 'Average annual income growth (e.g., promotions, wage inflation)',
        'expense_params': '🏠 Expense Parameters',
        'monthly_expenses': 'Current monthly expenses (USD):',
        'monthly_expenses_help': 'All monthly living costs',
        'investment_params': '📈 Investment Parameters',
        'annual_return': 'Expected annual return (%):',
        'annual_return_help': 'Average annual return on investments',
        'inflation_rate': 'Inflation rate (%):',
        'inflation_help': 'Expected average annual inflation (expense growth)',
        'capital_forecast': '📊 Capital Growth Forecast',
        'monthly_surplus': '💰 **Current monthly surplus for savings:**',
        'age_col': 'Age',
        'annual_income_col': 'Annual Income',
        'annual_expenses_col': 'Annual Expenses',
        'annual_contribution_col': 'Annual Contribution',
        'nominal_value_col': 'Nominal Value',
        'real_value_col': 'Real Value',
        'detailed_data': '📋 Detailed Data',
        'summary': '📈 Summary',
        'retirement_capital': 'Retirement Capital',
        'real_value': 'Real Value',
        'total_contributions': 'Total Contributions',
        'avg_annual_contribution': 'Average Annual Contribution',
        'investment_gain': 'Investment Gain',
        'additional_info': '💡 Additional Information',
        'retirement_year_info': '**In retirement year ({} years old):**',
        'income_label': 'Income',
        'expenses_label': 'Expenses',
        'surplus_label': 'Surplus',
        'monthly_pension_4pct': '**Monthly pension (4% rule):**',
        'current_purchasing_power': '**This equals today:**',
        'expense_coverage': '**Coverage of current expenses:**',
        'doubling_time': '**Capital doubling time:**',
        'retirement_tips': '💡 Retirement Tips',
        'rule_4pct_title': '🎯 4% Rule',
        'rule_4pct_desc': 'Safe annual withdrawal is 4% of accumulated capital. This means you need 25x your annual expenses.',
        'diversification_title': '📊 Diversification',
        'diversification_desc': 'Spread investments across different asset classes: stocks, bonds, real estate, commodities.',
        'time_money_title': '⏰ Time is Money',
        'time_money_desc': 'The earlier you start, the more you benefit from compound interest. Every year matters!',
        'error_age': '⚠️ Retirement age must be higher than current age!',
        'error_no_surplus': '⚠️ Current expenses exceed income! No surplus for savings.',
        'nominal_value_chart': 'Nominal Value',
        'real_value_chart': 'Real Value (after inflation)',
        'chart_title': 'Retirement Capital Growth ({} years)',
        'chart_age': 'Age',
        'chart_value': 'Value (USD)',
        'chart_hover_age': 'Age',
        'chart_hover_value': 'Value',
        'chart_hover_real_value': 'Real Value',
        'currency': 'USD',
        'years_suffix': 'years',
        'purchasing_power': 'purchasing power'
    },
    'pl': {
        'page_title': 'Kalkulator emerytalny',
        'page_icon': '📈',
        'main_title': '📈 Kalkulator emerytalny',
        'sidebar_options': '⚙️ Opcje',
        'language_select': 'Wybierz język:',
        'current_age': 'Podaj swój obecny wiek:',
        'retirement_age': 'Podaj wiek, w którym planujesz przejść na emeryturę:',
        'income_params': '💰 Parametry dochodowe',
        'current_savings': 'Obecne oszczędności (PLN):',
        'current_savings_help': 'Kwota, którą już masz zaoszczędzoną',
        'monthly_income': 'Obecne miesięczne wynagrodzenie netto (PLN):',
        'monthly_income_help': 'Miesięczne wynagrodzenie uwzględniające premie, zwroty podatku itp.',
        'income_growth': 'Prognozowany wzrost wynagrodzenia (% rocznie):',
        'income_growth_help': 'Średni roczny wzrost wynagrodzenia (np. awanse, inflacja płac)',
        'expense_params': '🏠 Parametry wydatków',
        'monthly_expenses': 'Obecne miesięczne wydatki (PLN):',
        'monthly_expenses_help': 'Wszystkie miesięczne koszty życia',
        'investment_params': '📈 Parametry inwestycyjne',
        'annual_return': 'Oczekiwany roczny zwrot (%):',
        'annual_return_help': 'Średni roczny zwrot z inwestycji',
        'inflation_rate': 'Stopa inflacji (%):',
        'inflation_help': 'Oczekiwana średnia roczna inflacja (wzrost wydatków)',
        'capital_forecast': '📊 Prognoza wzrostu kapitału',
        'monthly_surplus': '💰 **Obecna miesięczna nadwyżka do oszczędzania:**',
        'age_col': 'Wiek',
        'annual_income_col': 'Roczny dochód',
        'annual_expenses_col': 'Roczne wydatki',
        'annual_contribution_col': 'Roczna wpłata',
        'nominal_value_col': 'Wartość nominalna',
        'real_value_col': 'Wartość realna',
        'detailed_data': '📋 Szczegółowe dane',
        'summary': '📈 Podsumowanie',
        'retirement_capital': 'Kapitał na emeryturze',
        'real_value': 'Wartość realna',
        'total_contributions': 'Całkowite wpłaty',
        'avg_annual_contribution': 'Średnia roczna wpłata',
        'investment_gain': 'Zysk z inwestycji',
        'additional_info': '💡 Dodatkowe informacje',
        'retirement_year_info': '**W roku emerytury ({} lat):**',
        'income_label': 'Dochód',
        'expenses_label': 'Wydatki',
        'surplus_label': 'Nadwyżka',
        'monthly_pension_4pct': '**Miesięczna emerytura (4% reguła):**',
        'current_purchasing_power': '**To odpowiada dzisiaj:**',
        'expense_coverage': '**Pokrycie obecnych wydatków:**',
        'doubling_time': '**Czas podwojenia kapitału:**',
        'retirement_tips': '💡 Porady emerytalne',
        'rule_4pct_title': '🎯 Zasada 4%',
        'rule_4pct_desc': 'Bezpieczna roczna wypłata to 4% zgromadzonego kapitału. To oznacza, że potrzebujesz 25x swoich rocznych wydatków.',
        'diversification_title': '📊 Dywersyfikacja',
        'diversification_desc': 'Rozłóż inwestycje między różne klasy aktywów: akcje, obligacje, nieruchomości, surowce.',
        'time_money_title': '⏰ Czas to pieniądz',
        'time_money_desc': 'Im wcześniej zaczniesz, tym więcej skorzystasz z procentu składanego. Każdy rok ma znaczenie!',
        'error_age': '⚠️ Wiek przejścia na emeryturę musi być wyższy niż obecny wiek!',
        'error_no_surplus': '⚠️ Obecne wydatki przewyższają dochody! Nie ma nadwyżki do oszczędzania.',
        'nominal_value_chart': 'Wartość nominalna',
        'real_value_chart': 'Wartość realna (po inflacji)',
        'chart_title': 'Wzrost kapitału emerytalnego ({} lat)',
        'chart_age': 'Wiek',
        'chart_value': 'Wartość (PLN)',
        'chart_hover_age': 'Wiek',
        'chart_hover_value': 'Wartość',
        'chart_hover_real_value': 'Wartość realna',
        'currency': 'PLN',
        'years_suffix': 'lat',
        'purchasing_power': 'siły nabywczej'
    },
    'zh': {
        'page_title': '退休计算器',
        'page_icon': '📈',
        'main_title': '📈 退休计算器',
        'sidebar_options': '⚙️ 选项',
        'language_select': '选择语言:',
        'current_age': '请输入您的当前年龄:',
        'retirement_age': '请输入您计划退休的年龄:',
        'income_params': '💰 收入参数',
        'current_savings': '当前储蓄 (CNY):',
        'current_savings_help': '您已经储蓄的金额',
        'monthly_income': '当前月净收入 (CNY):',
        'monthly_income_help': '月收入包括奖金、退税等',
        'income_growth': '预期收入增长率 (% 每年):',
        'income_growth_help': '平均年收入增长率（如升职、工资通胀）',
        'expense_params': '🏠 支出参数',
        'monthly_expenses': '当前月支出 (CNY):',
        'monthly_expenses_help': '所有月生活费用',
        'investment_params': '📈 投资参数',
        'annual_return': '预期年回报率 (%):',
        'annual_return_help': '投资的平均年回报率',
        'inflation_rate': '通胀率 (%):',
        'inflation_help': '预期平均年通胀率（支出增长）',
        'capital_forecast': '📊 资本增长预测',
        'monthly_surplus': '💰 **当前月储蓄余额:**',
        'age_col': '年龄',
        'annual_income_col': '年收入',
        'annual_expenses_col': '年支出',
        'annual_contribution_col': '年投入',
        'nominal_value_col': '名义价值',
        'real_value_col': '实际价值',
        'detailed_data': '📋 详细数据',
        'summary': '📈 摘要',
        'retirement_capital': '退休资本',
        'real_value': '实际价值',
        'total_contributions': '总投入',
        'avg_annual_contribution': '平均年投入',
        'investment_gain': '投资收益',
        'additional_info': '💡 附加信息',
        'retirement_year_info': '**在退休年份（{}岁）:**',
        'income_label': '收入',
        'expenses_label': '支出',
        'surplus_label': '余额',
        'monthly_pension_4pct': '**月退休金（4%规则）:**',
        'current_purchasing_power': '**相当于今天:**',
        'expense_coverage': '**当前支出覆盖率:**',
        'doubling_time': '**资本翻倍时间:**',
        'retirement_tips': '💡 退休建议',
        'rule_4pct_title': '🎯 4%规则',
        'rule_4pct_desc': '安全的年提取率是累积资本的4%。这意味着您需要25倍的年支出。',
        'diversification_title': '📊 多元化',
        'diversification_desc': '将投资分散到不同的资产类别：股票、债券、房地产、大宗商品。',
        'time_money_title': '⏰ 时间就是金钱',
        'time_money_desc': '越早开始，就越能从复利中受益。每一年都很重要！',
        'error_age': '⚠️ 退休年龄必须高于当前年龄！',
        'error_no_surplus': '⚠️ 当前支出超过收入！没有储蓄余额。',
        'nominal_value_chart': '名义价值',
        'real_value_chart': '实际价值（扣除通胀）',
        'chart_title': '退休资本增长（{}年）',
        'chart_age': '年龄',
        'chart_value': '价值 (CNY)',
        'chart_hover_age': '年龄',
        'chart_hover_value': '价值',
        'chart_hover_real_value': '实际价值',
        'currency': 'CNY',
        'years_suffix': '年',
        'purchasing_power': '购买力'
    }
}

# Language selection
language = st.selectbox(
    'Select Language / Wybierz język / 选择语言:',
    options=['en', 'pl', 'zh'],
    format_func=lambda x: {'en': 'English', 'pl': 'Polski', 'zh': '中文'}[x],
    index=0
)

# Get current language translations
t = translations[language]

# Default values based on language/region
default_values = {
    'en': {
        'current_savings': 71000,
        'monthly_income': 12833,
        'monthly_expenses': 6500,
        'income_growth': 6.5,
        'annual_return': 6.0,
        'inflation_rate': 3.5
    },
    'pl': {
        'current_savings': 71000,
        'monthly_income': 12833,
        'monthly_expenses': 6500,
        'income_growth': 6.5,
        'annual_return': 6.0,
        'inflation_rate': 3.5
    },
    'zh': {
        'current_savings': 71000,
        'monthly_income': 12833,
        'monthly_expenses': 6500,
        'income_growth': 6.5,
        'annual_return': 6.0,
        'inflation_rate': 3.5
    }
}

defaults = default_values[language]

# Page configuration
st.set_page_config(
    page_title=t['page_title'],
    page_icon=t['page_icon'],
    layout="wide"
)

# Main title
st.title(t['main_title'])
st.markdown("---")

# Sidebar with options
st.sidebar.header(t['sidebar_options'])

# Current age selection
current_age = st.sidebar.selectbox(
    t['current_age'],
    options=list(range(18, 100)),
    index=14  # default 32 years old
)

# Retirement age selection
retirement_age = st.sidebar.selectbox(
    t['retirement_age'],
    options=list(range(50, 80)),
    index=10  # default 65 years old
)

# Additional parameters in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader(t['income_params'])

current_savings = st.sidebar.number_input(
    t['current_savings'],
    min_value=0,
    value=defaults['current_savings'],
    step=500,
    help=t['current_savings_help']
)

monthly_income = st.sidebar.number_input(
    t['monthly_income'],
    min_value=0,
    value=defaults['monthly_income'],
    step=500,
    help=t['monthly_income_help']
)

income_growth_rate = st.sidebar.slider(
    t['income_growth'],
    min_value=0.0,
    max_value=10.0,
    value=defaults['income_growth'],
    step=0.1,
    help=t['income_growth_help']
)

st.sidebar.markdown("---")
st.sidebar.subheader(t['expense_params'])

monthly_expenses = st.sidebar.number_input(
    t['monthly_expenses'],
    min_value=0,
    value=defaults['monthly_expenses'],
    step=500,
    help=t['monthly_expenses_help']
)

st.sidebar.markdown("---")
st.sidebar.subheader(t['investment_params'])

annual_return = st.sidebar.slider(
    t['annual_return'],
    min_value=0.0,
    max_value=15.0,
    value=defaults['annual_return'],
    step=0.1,
    help=t['annual_return_help']
)

inflation_rate = st.sidebar.slider(
    t['inflation_rate'],
    min_value=0.0,
    max_value=10.0,
    value=defaults['inflation_rate'],
    step=0.1,
    help=t['inflation_help']
)

# Calculations
years_to_retirement = retirement_age - current_age

if years_to_retirement <= 0:
    st.error(t['error_age'])
else:
    # Columns for main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(t['capital_forecast'])
        
        # Check if there's surplus for savings
        current_monthly_surplus = monthly_income - monthly_expenses
        
        if current_monthly_surplus <= 0:
            st.error(t['error_no_surplus'])
            st.stop()
        
        # Display current surplus
        st.info(f"{t['monthly_surplus']} {current_monthly_surplus:,.0f} {t['currency']}")
        
        # Calculations for each year
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
            
            # Calculate income and expenses for given year
            annual_income = monthly_income * 12 * ((1 + income_growth_rate/100) ** year)
            annual_expenses = monthly_expenses * 12 * ((1 + inflation_rate/100) ** year)
            annual_contribution = annual_income - annual_expenses
            
            annual_income_list.append(annual_income)
            annual_expenses_list.append(annual_expenses)
            annual_contributions_list.append(annual_contribution)
            
            if year > 0 and annual_contribution > 0:
                # Apply investment return and add annual contributions
                current_value = (current_value + annual_contribution) * (1 + annual_return/100)
            elif year > 0:
                # If no surplus, only investment return
                current_value = current_value * (1 + annual_return/100)
            
            nominal_values.append(current_value)
            # Real value (adjusted for inflation)
            real_value = current_value / ((1 + inflation_rate/100) ** year)
            real_values.append(real_value)
        
        # Create DataFrame
        df = pd.DataFrame({
            t['age_col']: years,
            t['annual_income_col']: annual_income_list,
            t['annual_expenses_col']: annual_expenses_list,
            t['annual_contribution_col']: annual_contributions_list,
            t['nominal_value_col']: nominal_values,
            t['real_value_col']: real_values
        })
        
        # Plotly chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[t['age_col']],
            y=df[t['nominal_value_col']],
            mode='lines+markers',
            name=t['nominal_value_chart'],
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate=f'{t["chart_hover_age"]}: %{{x}}<br>{t["chart_hover_value"]}: %{{y:,.0f}} {t["currency"]}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df[t['age_col']],
            y=df[t['real_value_col']],
            mode='lines+markers',
            name=t['real_value_chart'],
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=6),
            hovertemplate=f'{t["chart_hover_age"]}: %{{x}}<br>{t["chart_hover_real_value"]}: %{{y:,.0f}} {t["currency"]}<extra></extra>'
        ))
        
        fig.update_layout(
            title=t['chart_title'].format(years_to_retirement),
            xaxis_title=t['chart_age'],
            yaxis_title=t['chart_value'],
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
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader(t['detailed_data'])
        
        # Format values in table
        df_display = df.copy()
        df_display[t['annual_income_col']] = df_display[t['annual_income_col']].apply(lambda x: f"{x:,.0f} {t['currency']}")
        df_display[t['annual_expenses_col']] = df_display[t['annual_expenses_col']].apply(lambda x: f"{x:,.0f} {t['currency']}")
        df_display[t['annual_contribution_col']] = df_display[t['annual_contribution_col']].apply(lambda x: f"{x:,.0f} {t['currency']}")
        df_display[t['nominal_value_col']] = df_display[t['nominal_value_col']].apply(lambda x: f"{x:,.0f} {t['currency']}")
        df_display[t['real_value_col']] = df_display[t['real_value_col']].apply(lambda x: f"{x:,.0f} {t['currency']}")
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader(t['summary'])
        
        final_nominal = nominal_values[-1]
        final_real = real_values[-1]
        total_contributions = current_savings + sum(annual_contributions_list[1:])  # Skip year 0
        investment_gain = final_nominal - total_contributions
        
        # Average annual contribution (from years with positive contribution)
        positive_contributions = [c for c in annual_contributions_list[1:] if c > 0]
        avg_annual_contribution = sum(positive_contributions) / len(positive_contributions) if positive_contributions else 0
        
        # Metrics
        st.metric(
            t['retirement_capital'],
            f"{final_nominal:,.0f} {t['currency']}",
            help="Wartość nominalna kapitału" if language == 'pl' else "Nominal capital value" if language == 'en' else "名义资本价值"
        )
        
        st.metric(
            t['real_value'],
            f"{final_real:,.0f} {t['currency']}",
            help="Wartość skorygowana o inflację" if language == 'pl' else "Value adjusted for inflation" if language == 'en' else "通胀调整后的价值"
        )
        
        st.metric(
            t['total_contributions'],
            f"{total_contributions:,.0f} {t['currency']}",
            help="Suma wszystkich wpłat przez lata" if language == 'pl' else "Sum of all contributions over the years" if language == 'en' else "多年来所有投入的总和"
        )
        
        st.metric(
            t['avg_annual_contribution'],
            f"{avg_annual_contribution:,.0f} {t['currency']}",
            help="Średnia z lat z dodatnią nadwyżką" if language == 'pl' else "Average from years with positive surplus" if language == 'en' else "有正余额年份的平均值"
        )
        
        st.metric(
            t['investment_gain'],
            f"{investment_gain:,.0f} {t['currency']}",
            help="Różnica między kapitałem a wpłatami" if language == 'pl' else "Difference between capital and contributions" if language == 'en' else "资本与投入之间的差额"
        )
        
        # Additional information
        st.markdown("---")
        st.subheader(t['additional_info'])
        
        # Last contribution in retirement year
        final_contribution = annual_contributions_list[-1]
        final_income = annual_income_list[-1]
        final_expenses = annual_expenses_list[-1]
        
        st.info(f"{t['retirement_year_info'].format(retirement_age)}\n"
                f"{t['income_label']}: {final_income:,.0f} {t['currency']}\n"
                f"{t['expenses_label']}: {final_expenses:,.0f} {t['currency']}\n"
                f"{t['surplus_label']}: {final_contribution:,.0f} {t['currency']}")
        
        # Monthly pension (4% rule) - from nominal value
        monthly_pension_nominal = (final_nominal * 0.04) / 12
        # Monthly pension in real value (today's purchasing power)
        monthly_pension_real = (final_real * 0.04) / 12
        
        st.info(f"{t['monthly_pension_4pct']}\n{monthly_pension_nominal:,.0f} {t['currency']} (w cenach z {current_age + years_to_retirement} roku)" if language == 'pl' 
                else f"{t['monthly_pension_4pct']}\n{monthly_pension_nominal:,.0f} {t['currency']} (in {current_age + years_to_retirement} year prices)" if language == 'en'
                else f"{t['monthly_pension_4pct']}\n{monthly_pension_nominal:,.0f} {t['currency']} (以{current_age + years_to_retirement}年价格计算)")
        
        # Comparison with today's purchasing power
        st.info(f"{t['current_purchasing_power']}\n{monthly_pension_real:,.0f} {t['currency']} {t['purchasing_power']}")
        
        # Comparison with current expenses
        pension_coverage = (monthly_pension_real / monthly_expenses) * 100
        st.info(f"{t['expense_coverage']}\n{pension_coverage:.1f}% ({monthly_pension_real:,.0f} {t['currency']} vs {monthly_expenses:,.0f} {t['currency']})")
        
        # Capital doubling time
        if annual_return > 0:
            doubling_time = 72 / annual_return
            st.info(f"{t['doubling_time']}\n{doubling_time:.1f} {t['years_suffix']}")

# Additional section with tips
st.markdown("---")
st.subheader(t['retirement_tips'])

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    **{t['rule_4pct_title']}**
    
    {t['rule_4pct_desc']}
    """)

with col2:
    st.markdown(f"""
    **{t['diversification_title']}**
    
    {t['diversification_desc']}
    """)

with col3:
    st.markdown(f"""
    **{t['time_money_title']}**
    
    {t['time_money_desc']}
    """)
