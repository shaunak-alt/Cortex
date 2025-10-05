# Cortex: An Autonomous AI Tutor Orchestrator

**A submission for the YoLearn.ai Yophoria Innovation Challenge by Team OOPS, I DID IT AGAIN**

---

## 📖 Project Overview

[cite_start]Cortex is an intelligent middleware orchestrator designed to act as the "brain" for an AI tutoring system. [cite: 14] [cite_start]It autonomously connects a conversational AI tutor to a vast library of educational tools by understanding the context of a student's conversation and dynamically extracting the necessary information to call the right tool. [cite: 13]

[cite_start]This project directly addresses the hackathon's core challenge of creating a scalable system that can handle diverse tool schemas and automate complex interactions without manual configuration. [cite: 13, 24] [cite_start]The focus is purely on the intelligent orchestration layer, not the UI or the tools themselves. [cite: 22]

## ✨ Key Features

* [cite_start]**Intelligent Tool Routing:** Automatically analyzes user intent to select the appropriate tool(s) from a predefined library. [cite: 16]
* **Multi-Tool Orchestration:** A powerful LangGraph-based state machine that can handle complex, multi-step requests requiring several tools in a sequence.
* [cite_start]**Dynamic Parameter Extraction:** Intelligently extracts and infers parameters required by various tools directly from natural conversation, a key success criterion worth 40% of the evaluation. [cite: 17, 636]
* [cite_start]**Scalable Architecture:** Built using a modular "Hybrid Agent System" approach, allowing for easy integration of new tools. [cite: 78, 646]
* **Innovative Tool Integration:** The system has been extended beyond the core requirements to include a custom **Sign Language Tutor**, showcasing its flexibility and potential for creating inclusive learning experiences.

## 🏗️ System Architecture

Cortex is built on a Hybrid Agent System architecture, coordinated by LangGraph. The flow is as follows:

`User Request → FastAPI → LangGraph Workflow → Router Agent → Parameter Extractor Agent → Final JSON Payload(s)`

[cite_start]This design provides a clean separation of concerns and a robust, scalable foundation for orchestrating a large number of educational tools. [cite: 647]

*(You can insert the architecture diagram image here)*

## 🛠️ Technology Stack

* [cite_start]**Backend Framework:** Python with FastAPI [cite: 39]
* [cite_start]**AI / Agent Framework:** LangChain & LangGraph [cite: 40]
* **LLM Engine:** Google Gemini
* **Data Validation:** Pydantic

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.9+
* An active Google AI API Key with the Gemini API enabled.

### 1. Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/cortex-ai-orchestrator.git](https://github.com/your-username/cortex-ai-orchestrator.git)
    cd cortex-ai-orchestrator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    * Rename the `.env.example` file to `.env`.
    * Open the `.env` file and add your Google API key:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

### 2. How to Run the Server

With your virtual environment activated, start the FastAPI server using Uvicorn:

```bash
uvicorn orchestrator.app:app --reload
```
The application will be running at http://127.0.0.1:8000

### 3. How to Test the Application
You can test the application by sending a POST request to the /invoke endpoint.

Using PowerShell (Windows)
Open a new terminal and use the Invoke-WebRequest command:

```bash
Invoke-WebRequest -Uri "[http://127.0.0.1:8000/invoke](http://127.0.0.1:8000/invoke)" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"user_message": "Make me 5 easy flashcards on the water cycle for my science class."}'
```
Using cURL (macOS/Linux/WSL)
Open a new terminal and use the curl command:

```Bash
curl -X POST "[http://127.0.0.1:8000/invoke](http://127.0.0.1:8000/invoke)" \
-H "Content-Type: application/json" \
-d '{"user_message": "Make me 5 easy flashcards on the water cycle for my science class."}'
```
You will see the step-by-step execution logged in the terminal where the server is running, and the final JSON payload will be returned as the API response.
