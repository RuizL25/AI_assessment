"""Interactive console chat with the RAG Support Agent."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from langchain_core.messages import HumanMessage, AIMessage
from agent.chat_agent import agent_executor


def main():
    chat_history = []
    print("=" * 60)
    print("  RAG Support Agent - Interactive Console Chat")
    print("  Type 'exit' or 'quit' to end the conversation.")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        result = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })

        answer = result["output"]
        print(f"\nAgent: {answer}\n")

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))

main()