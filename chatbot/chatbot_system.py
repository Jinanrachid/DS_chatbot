from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrockConverse
import uuid

from connectdb import connect_to_chroma
from claude_config import bedrock_config
from dynamodb_creation import ensure_dynamodb_table
from prompt_creation import build_prompt_from_query

# DynamoDB Setup
table_name = ensure_dynamodb_table()
session_id = str(uuid.uuid4())

# Bedrock Model
model = ChatBedrockConverse(**bedrock_config)

# Chroma Retriever
vectordb = connect_to_chroma()
if vectordb is None:
    raise RuntimeError("Could not connect to ChromaDB. Ensure the server is running.")
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})


# Chat Setup
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "{system_prompt}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_prompt}"),
    ]
)


chain = prompt_template | model | StrOutputParser()
# Integrate with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: DynamoDBChatMessageHistory(
        table_name=table_name, session_id=session_id
    ),
    input_messages_key="user_prompt",
    history_messages_key="history",
)

# Chat Loop
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    try:
        digico_prompt = build_prompt_from_query(user_input, retriever)
        config = {"configurable": {"session_id": session_id}}
        response = chain_with_history.invoke(
            {"system_prompt": digico_prompt["system"], "user_prompt": digico_prompt["user"]},
            config=config,
        )
        print(f"Assistant: {response}")
    except Exception as e:
        print(f"Error generating response: {e}")
