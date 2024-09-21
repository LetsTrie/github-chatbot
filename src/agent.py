import tiktoken
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class Agent:
    def __init__(self, system=""):
        self.system = system
        
        self.messages = []
        self.intermediate_messages = []

        self.model_name = "gpt-4o"
        self.chat_model = ChatOpenAI(model=self.model_name, temperature=0.5)
        self.max_token_limit = 4000

        self.encoding = tiktoken.encoding_for_model(self.model_name)
        
        if self.system:
            self.messages.append(SystemMessage(content=system))

    def __call__(self, message, is_primary_query):
        if is_primary_query:
            self.messages.append(HumanMessage(content=message))
        else: 
            self.intermediate_messages.append(HumanMessage(content=message))
            
        result = self.execute()
        self.intermediate_messages.append(AIMessage(content=result))
        return result

    def execute(self):
        all_messages = self.messages + self.intermediate_messages
        chunked_messages = self.chunk_messages(all_messages)
        
        full_response = ""
        for chunk in chunked_messages:
            response = self.chat_model.invoke(chunk)
            full_response += response.content

        return full_response

    def chunk_messages(self, messages):
        chunks = []
        current_chunk = []
        current_token_count = 0

        for message in messages:
            message_tokens = len(self.encoding.encode(message.content))
            
            if current_token_count + message_tokens > self.max_token_limit - 1000: 
                chunks.append(current_chunk)
                current_chunk = [SystemMessage(content="This is a continuation of a previous conversation.")]
                current_token_count = len(self.encoding.encode(current_chunk[0].content))

            current_chunk.append(message)
            current_token_count += message_tokens

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def finalize(self):
        self.intermediate_messages = []
        self.messages = [
            self.messages[0],
            SystemMessage(content=f"previous contexts: {self.summarize_questions()}")
        ]

    def summarize_questions(self) -> str:
        questions = [msg.content for msg in self.messages[1:]]
        
        if not questions:
            return "No questions have been asked yet."

        questions_text = "\n".join([f"- {q}" for q in questions])
        
        summary_prompt = f"""You are an AI assistant tasked with summarizing the questions asked in a conversation. 
        Here are the questions that have been asked:

        {questions_text}

        Please provide a concise summary of these questions, capturing the main themes and topics of inquiry. 
        The summary should provide context for future interactions, but be brief enough to not exceed 2000 tokens. 
        Do not attempt to answer the questions, only summarize them."""

        summary_message = [SystemMessage(content=summary_prompt)]
        response = self.chat_model.invoke(summary_message)
        return response.content