import openai
import time
import streamlit as st

def main():
    # Initialize the client if not already done
    if 'client' not in st.session_state:
        st.session_state.client = openai.OpenAI(api_key=st.secrets["openai_secret_key"] )

        # Create and upload the file
        st.session_state.file = st.session_state.client.files.create(
            file=open("chronicles_of_light.txt", "rb"),
            purpose='assistants'
        )

        # Create an Assistant
        st.session_state.assistant = st.session_state.client.beta.assistants.create(
            name="Story Assistant",
            instructions="You are a role-playing game referee and storytelling assistant. You guide the creation of interesting stories through conversation.",
            model="gpt-3.5-turbo-1106",
            file_ids=[st.session_state.file.id],
            tools=[{"type": "retrieval"}]
        )

    # Create a Thread if not already done
    if 'thread' not in st.session_state:
        st.session_state.thread = st.session_state.client.beta.threads.create()

    user_query = st.text_input("You are running for your life.")

    if st.button('Submit'):
        # Add a Message to a Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_query
        )

        # Run the Assistant
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
            instructions="Please address the user as John Light"
        )

        while True:
            time.sleep(5)  # Wait for 5 seconds

            # Retrieve the run status
            run_status = st.session_state.client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=run.id
            )

            if run_status.status == 'completed':
                messages = st.session_state.client.beta.threads.messages.list(
                    thread_id=st.session_state.thread.id
                )

                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    st.write(f"{role.capitalize()}: {content}")
                break
            else:
                st.write("Thinking about the story...")
                time.sleep(5)

if __name__ == "__main__":
    main()

