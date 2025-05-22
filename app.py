from dotenv import load_dotenv
# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain.prompts import PromptTemplate
import sqlite3

load_dotenv()

# llm = HuggingFaceEndpoint(
#     repo_id="HuggingFaceH4/zephyr-7b-beta",
#     # repo_id="meta-llama/Meta-Llama-3-8B",
#     # repo_id="meta-llama/Llama-3.1-8B-Instruct",
#     task="text-generation",
#     max_new_tokens=512,
#     do_sample=False,
#     repetition_penalty=1.03,
# )

# chat_model = ChatHuggingFace(llm=llm)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)



st.header('Talk to Inventory db')

user_question = st.text_input('Enter your query')

prompt_template = """
You are an expert in converting English questions into SQL queries. Given the following table and examples, you will convert English language questions into the corresponding SQL queries.

Table structure:
The table is called `inventory` and it has the following columns:
- `product_id`: Unique identifier for each product (INTEGER).
- `product_name`: Name of the product (VARCHAR).
- `category`: The category of the product (VARCHAR).
- `supplier_name`: Name of the supplier (VARCHAR).
- `stock_quantity`: Quantity of the product in stock (INTEGER).
- `purchase_price`: The price at which the store buys the product (DECIMAL).

Example 1:
Question: "What are the names of all products in the supply chain?"
SQL Query: SELECT product_name FROM inventory;

Example 2:
Question: "How many units of 'Rice' are currently in stock?"
SQL Query: SELECT stock_quantity FROM inventory WHERE product_name = 'Rice';

Example 3:
Question: "What is the purchase price of the product with product_id 5?"
SQL Query: SELECT purchase_price FROM inventory WHERE product_id = 5;

Now, based on the table structure and the examples above, please convert the following English question into an SQL query:

Question: {question}

ONLY RETURN THE SQL QUERY AND NOTHING ELSE SHOULD BE WRITTEN EXCEPT THE SQL QUERY.DONT WRITE 'POSSIBLE SOLUTION:' Just return the sql query. DONT WRITE 'SQL QUERY' BEFORE THE ACTUAL SQL QUERY.

Note: Do not include ''' at the beginning or end of your response.
"""


prompt = PromptTemplate(input_variables=["question"], template=prompt_template)


final_prompt = prompt.format(question=user_question)


def fxn():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    result = llm.invoke(final_prompt)
    print(result.content)

    sql_query = result.content
    cursor.execute(sql_query)
    data = cursor.fetchall()
    for row in data:
        st.write(row)
    conn.close()
   


if st.button('Generate Result'):
    fxn()

    