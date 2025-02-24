# Summarizzler

Summarizzler is a powerful web application that leverages AI to provide concise summaries from various sources including websites, text, PDF files, and YouTube videos.

🚀 **Try it now:** [https://summarizzler.web.app](https://summarizzler.web.app)

## Features

- **Multi-source summarization:** Easily summarize content from:
  - Websites (enter any URL)
  - Plain text (copy & paste)
  - PDF documents (file upload)
  - YouTube videos (paste video URL)
- **AI-powered:** Uses advanced LLM models to create accurate, coherent summaries
- **Clean, intuitive interface:** Simple to use with no technical knowledge required
- **Fast processing:** Get results quickly, even for longer content

## Getting Started

Follow these instructions to set up Summarizzler locally for development.

### Prerequisites

- Python 3.12+ 
- Node.js 16+
- npm or any other package manager

### Clone the repository:
   ```bash
   git clone https://github.com/JakubTuta/Summarizzler.git
   cd summarizzler
   ```

### Backend Setup (Django)
1. Navigate to the backend directory:
    ```bash
    cd backend
    ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Create a `.env` file in the backend directory with these variables:
        - SECRET_KEY: django app secret key
        - POSTGRES_URL: postgresql database url
        - GEMINI_API_KEY: api key with access to Gemini 2.0

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Start the backend server:
   ```bash
   python manage.py runserver
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000)

### Frontend Setup (Nuxt.js)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies (replace npm with your package manager):
   ```bash
   npm install
   ```

3. Create a `.env` file with the necessary environment variables:
   ```
   SERVER_URL=http://localhost:8000
   ```

4. Start the development server (replace npm with your package manager):
   ```bash
   npm run dev
   ```
   The frontend will be available at [http://localhost:3000](http://localhost:3000)
