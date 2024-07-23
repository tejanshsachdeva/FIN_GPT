# FIN_GPT: Indian Budget 2024 Q&A 🇮🇳

FIN_GPT is an AI-powered application that allows users to ask questions and get insights about the Indian Budget 2024, presented by Nirmala Sitharaman. The application uses natural language processing and machine learning techniques to provide accurate and relevant information from official press releases and budget documents.

## Features

- **Question-answering system**: Get answers about the Indian Budget 2024.
- **Budget comparison**: Compare the 2023 and 2024 budgets.
- **Official datasets**: Utilizes official press releases and budget documents (in PDF form).
- **Interactive chat interface**: Powered by Streamlit.
- **OpenAI models**: Leverages advanced language models for intelligent responses.

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/tejanshsachdeva/fin-gpt.git
   cd fin-gpt
   ```
2. **Install the required dependencies**:

   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your OpenAI API key**:

   - Create a `.env` file in the project root.
   - Add your OpenAI API key:
     ```sh
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the Streamlit app**:

   ```sh
   streamlit run app.py
   ```
2. **Open your web browser** and navigate to the provided local URL (usually `http://localhost:8501`).
3. **Start asking questions** about the Indian Budget 2024 in the chat interface.

## Data Sources

The application uses official press releases and budget documents for the years 2023 and 2024. These documents should be placed in the `pdfs` directory in PDF format.

## How It Works

1. The application loads and processes the PDF documents containing budget information.
2. It creates vector and summary indices for efficient querying.
3. An AI agent is initialized with specialized tools for answering budget-related questions.
4. Users can input questions through the Streamlit chat interface.
5. The AI agent processes the questions and provides relevant answers using the prepared indices.

## Customization

You can customize the following aspects of the application:

- **OpenAI models**: Adjust the models used for summary, Q&A, and embeddings (modify the constants at the beginning of the script).
- **System prompt**: Change the `system_prompt` in the `load_agent` function to modify how the AI agent responds.
- **Tools**: Add more tools or modify existing ones to enhance the agent's capabilities.

## Contributing

Contributions are welcome! Please feel free to submit a pull request to improve the application.

---
