
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root",
    database="student_db"
)
cursor = conn.cursor()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Performance System", layout="wide")
st.title("Student Performance Management System")
menu = st.sidebar.selectbox(
    "Select Action",
    ["Add Student","View Students","Update Marks","Delete Student","Analytics"]
)

#add
if menu == "Add Student":
    st.header("Add Student")

    with st.form("add_student"):
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 100)
        subject = st.text_input("Subject")
        marks = st.number_input("Marks", 0, 100)
        submit = st.form_submit_button("Add")

    if submit:
        if name == "" or subject == "":
            st.warning("All fields are required")
        else:
            cursor.execute(
                "INSERT INTO student_performance (name, age, subject, marks) VALUES (%s,%s,%s,%s)",
                (name, age, subject, marks)
            )
            conn.commit()
            st.success("Student added successfully")

#view
if menu == "View Students":
    st.header("Student Records")

    df = pd.read_sql("SELECT * FROM student_performance", conn)
    st.dataframe(df)

#update
if menu == "Update Marks":
    st.header("Update Marks")

    student_id = st.number_input("Student ID", 1)
    new_marks = st.number_input("New Marks", 0, 100)

    if st.button("Update"):
        cursor.execute(
            "UPDATE student_performance SET marks=%s WHERE id=%s",
            (new_marks, student_id)
        )
        conn.commit()
        st.success("Marks updated successfully")

#delete
if menu == "Delete Student":
    st.header("Delete Student")

    student_id = st.number_input("Student ID to delete", 1)

    if st.button("Delete"):
        cursor.execute(
            "DELETE FROM student_performance WHERE id=%s",
            (student_id,)
        )
        conn.commit()
        st.success("Student deleted successfully")

#options
if menu == "Analytics":
    st.header("Performance Analytics")

    df = pd.read_sql("SELECT * FROM student_performance", conn)

    if df.empty:
        st.warning("No data available")
    else:
        df["Result"] = df["marks"].apply(
            lambda x: "Pass" if x >= 40 else "Fail"
        )

        st.metric("Average Marks", round(df["marks"].mean(), 2))
        st.metric(
            "Pass Percentage",
            round((df["Result"] == "Pass").mean() * 100, 2)
        )

        top = df.loc[df["marks"].idxmax()]
        st.write("Top Scorer:", top["name"], "-", top["marks"])

        # Bar chart: Subject vs Avg Marks
        subject_avg = df.groupby("subject")["marks"].mean()
        fig, ax = plt.subplots()
        subject_avg.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        # Pie chart: Pass/Fail
        result_count = df["Result"].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(result_count, labels=result_count.index, autopct="%1.1f%%")
        st.pyplot(fig2)