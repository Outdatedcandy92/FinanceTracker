import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
from streamlit_option_menu import option_menu
import database as db
import plotly.express as px
import pandas as pd

# Setting

incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent","Stuff","Etc"]
currency = "CAD"
page_title = "Income And Expense Tracker"
page_icon = "💸"
layout = "centered"

# -----
st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)
st.title(page_title + " "  + page_icon )

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Drop down

years = [datetime.today().year , datetime.today().year + 1]
months = list(calendar.month_name[1:])

def income_plot():
    income_figure = px.bar(x=incomesrc, y=incomes, height=400, width=400,labels={"x": "Sources Of Income","y": "Amount",},title="Income")
    st.plotly_chart(income_figure, use_container_width=True)
def expense_plot():
    expense_figure = px.bar(x=expenserc, y=expenses, height=400, width=400,labels={"x": "Sources Of Expense","y": "Amount",},title="Expense")
    st.plotly_chart(expense_figure, use_container_width=True)
def income_pie():
    IncomePie = go.Figure(go.Pie(labels= incomesrc, values=incomeamt,textinfo='value',textfont_size=20,))
    st.plotly_chart(IncomePie, use_container_width=True)  
def expense_pie():
    expensePie = go.Figure(go.Pie(labels= expenserc, values= expenseamt,textinfo='value',textfont_size=20,  ))
    st.plotly_chart(expensePie, use_container_width=True)  
def bar():
    bar = px.line( y=[incomeamt , expenseamt], markers=True)
    st.plotly_chart(bar,use_container_width=True )


def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods







selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill","bar-chart-fill"],
    orientation="horizontal",
)

# Input
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form",clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("select month:", months,key="month")
        col2.selectbox("select year:", years, key="year")

        "---"

        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0,format="%d",step=10,key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0,format="%d",step=10,key=expense)

            valin , numin = st.columns(2)

            with valin:
                newitem = st.text_area("",placeholder="Enter The Name")  

            with numin:
                newitemval  = st.number_input(f"Price", min_value=0,format="%d",step=10,key=newitem)


        with st.expander("comment"):
            comment = st.text_area("",placeholder="enter a comment here")     

        "---"    

        submitted = st.form_submit_button("Save Data")   

        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income:st.session_state[income] for income in incomes}
            nxs = {newitem: st.session_state[newitem]}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            db.insert_period(period,incomes,expenses , comment, nxs)
            st.success("Data saved")



# plot
if selected == "Data Visualization":
    st.header("Data visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot period")
        if submitted:
            period_data = db.get_period(period)
            comment = period_data.get("comment")
            expenses = period_data.get("expenses")
            
            incomes = period_data.get("incomes")
            newexpense = period_data.get("nxs")
            print(comment, expenses, incomes, newexpense)
  

            total_income = sum(incomes.values())

            incomesrc = list(incomes.keys())
            incomeamt = list(incomes.values())

            total_expense = sum(expenses.values())

            expenserc = list(expenses.keys())
            expenseamt = list(expenses.values())

            remaning_buget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income",f"{total_income}{currency}")
            col2.metric("Total Expense", f"{total_expense}{currency}")
            col3.metric("remaning budget",f"{remaning_buget}{currency}" )
            st.text(f"comment: {comment}")

            "---"
            incol, excol, = st.columns(2)

            with incol:
                incol.header="income"
                income_plot()

            with excol:
                excol.header="expense"                  
                expense_plot()

            "---"
            st.markdown("""
                        <style>
                        .income-heading{
                            font-size:40px !important;
                        }            
                        </style>


                        """, unsafe_allow_html=True)
            st.markdown('<p class="income-heading">Income Breakdown</p>', unsafe_allow_html=True)
            
            highincome = list(dict(sorted(incomes.items(), key = lambda x: x[1])))[-1]
            st.write("The Highest Source Of Income Was", f"{highincome}")
            income_pie()

            st.markdown('<p class="income-heading">Expense Breakdown</p>', unsafe_allow_html=True)
            highexpense = list(dict(sorted(expenses.items(), key = lambda x: x[1])))[-1]
            st.write("The Highest Source Of Expense Was", f"{highexpense}")
            expense_pie()
            
            "---"

            st.markdown('<p class="income-heading">Comparison</p>', unsafe_allow_html=True)
            bar()





            




            
            


           
            
            
            
            
        

            