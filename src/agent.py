import tiktoken
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class Agent:
    def __init__(self, system=""):
        """
        Initializes the Agent instance with a system message and configures the conversation context.

        Parameters:
        system (str): A system message that sets up the context for the conversation.
        """
        self.system = system
        self.messages = []  # List to store the conversation messages, including system messages and user queries.
        self.intermediate_messages = []  # Stores messages for multi-turn conversations temporarily.

        self.model_name = "gpt-4o"  # The OpenAI model to use for generating responses.
        self.chat_model = ChatOpenAI(model=self.model_name, temperature=0.5)  # Configures the AI model with a specified temperature for balanced responses.
        self.max_token_limit = 4000  # Token limit to ensure we stay within API constraints.

        self.encoding = tiktoken.encoding_for_model(self.model_name)  # Token encoding for token count estimation.

        # Add the system message to the messages list if provided.
        if self.system:
            self.messages.append(SystemMessage(content=system))

    def __call__(self, message, is_primary_query):
        """
        Handles user input by appending it to the conversation and executing the AI model to generate a response.

        Parameters:
        message (str): The user's input or query.
        is_primary_query (bool): Determines if the input is the user's main query (True) or a part of a multi-turn conversation (False).

        Returns:
        str: The generated AI response.
        """
        # Store the user query or intermediate conversation message.
        if is_primary_query:
            self.messages.append(HumanMessage(content=message))  # Append to main messages for primary queries.
        else:
            self.intermediate_messages.append(HumanMessage(content=message))  # Store intermediate conversation messages.

        result = self.execute()  # Generate a response using the AI model.
        self.intermediate_messages.append(AIMessage(content=result))  # Add AI's response to the intermediate messages.
        return result

    def execute(self):
        """
        Executes the AI model, chunking the conversation to manage token limits and aggregating responses.

        Returns:
        str: The concatenated AI responses for the full conversation.
        """
        # Combine all messages (primary + intermediate) for processing.
        all_messages = self.messages + self.intermediate_messages
        chunked_messages = self.chunk_messages(all_messages)  # Breaks long conversations into token-compliant chunks.

        full_response = ""
        for chunk in chunked_messages:
            response = self.chat_model.invoke(chunk)  # Fetch AI response for each message chunk.
            full_response += response.content  # Append the content to the full response.

        return full_response

    def chunk_messages(self, messages):
        """
        Divides the conversation messages into smaller chunks to avoid exceeding the token limit.

        Parameters:
        messages (list): List of conversation messages to be processed.

        Returns:
        list: A list of message chunks, each within the model's token limit.
        """
        chunks = []  # List to store the final message chunks.
        current_chunk = []
        current_token_count = 0

        # Loop through each message and calculate its token count.
        for message in messages:
            message_tokens = len(self.encoding.encode(message.content))  # Estimate token count of the message.

            # If adding the current message would exceed the token limit, finalize the current chunk.
            if current_token_count + message_tokens > self.max_token_limit - 1000: 
                chunks.append(current_chunk)
                # Start a new chunk with a system message indicating a continuation of the conversation.
                current_chunk = [SystemMessage(content="This is a continuation of a previous conversation.")]
                current_token_count = len(self.encoding.encode(current_chunk[0].content))

            # Add the message to the current chunk.
            current_chunk.append(message)
            current_token_count += message_tokens

        # Append any remaining messages as a final chunk.
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def finalize(self):
        """
        Resets the intermediate messages and prepares for a new conversation cycle by summarizing past questions.
        """
        self.intermediate_messages = []  # Clear intermediate conversation messages.

        # Retain the system message and append a summary of previous questions for the next interaction.
        self.messages = [
            self.messages[0],  # Keep the original system message.
            SystemMessage(content=f"previous contexts: {self.summarize_questions()}")  # Add a summary of prior questions.
        ]

    def summarize_questions(self) -> str:
        """
        Generates a summary of all questions asked during the conversation for future context.

        Returns:
        str: A concise summary of user queries, capturing key themes and topics.
        """
        questions = [msg.content for msg in self.messages[1:]]  # Extract the content of all user queries.

        # If no questions have been asked yet, return a default message.
        if not questions:
            return "No questions have been asked yet."

        # Prepare the prompt for summarizing the list of questions.
        questions_text = "\n".join([f"- {q}" for q in questions])
        summary_prompt = f"""You are an AI assistant tasked with summarizing the questions asked in a conversation. 
        Here are the questions that have been asked:

        {questions_text}

        Please provide a concise summary of these questions, capturing the main themes and topics of inquiry. 
        The summary should provide context for future interactions, but be brief enough to not exceed 2000 tokens. 
        Do not attempt to answer the questions, only summarize them."""

        # Generate the summary using the AI model.
        summary_message = [SystemMessage(content=summary_prompt)]
        response = self.chat_model.invoke(summary_message)
        return response.content  # Return the summarized context.
