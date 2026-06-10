# Event-OCR
# AI Event Recognition App

An AI-powered application that extracts event details directly from posters or invitation images and generates a Google Calendar event link.

Instead of relying solely on traditional OCR, this project uses a Vision Language Model (VLM) to understand the content and structure of event posters, making it more effective for real-world invitation images shared through WhatsApp, Instagram, email, and digital flyers.

---

## Features

* Upload event posters or invitation images
* AI-powered event detail extraction
* Extracts:

  * Event Title
  * Date
  * Time
  * Location
* Generates Google Calendar event links
* Dockerized deployment
* FastAPI backend
* Lightweight web frontend

---

## Architecture

```text
Frontend (HTML/JS)
        │
        ▼
FastAPI Backend
        │
        ▼
Vision Language Model
        │
        ▼
Structured Event Data
        │
        ▼
Google Calendar Link Generator
        │
        ▼
Frontend Response
```

---

## Why Vision LLM Instead of OCR?

Traditional OCR works well for documents but struggles with event posters because of:

* Stylized fonts
* Complex layouts
* Decorative backgrounds
* Non-linear text placement

Vision Language Models understand both:

* Visual layout
* Textual content

This allows them to identify event details more accurately and return structured data instead of raw extracted text.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Transformers
* PyTorch

### Frontend

* HTML
* CSS
* JavaScript

### AI

* Vision Language Model (Moondream)

### Deployment

* Docker

---

## Project Structure

```text
event-ocr/
│
├── api/
│   ├── main.py
│   ├── model.py
│   ├── parser.py
│   └── calendar.py
│
├── templates/
│   └── index.html
│
├── requirements.txt
├── Dockerfile
├── README.md
└── __init__.py
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/<your-username>/event-ocr.git

cd event-ocr
```

---

## Create Virtual Environment

## Docker Setup

### Build Image

```bash
docker build -t ai-event-app .
```

### Run Container

```bash
docker run -p 8000:8000 ai-event-app
```

Open:

```text
http://localhost:8000
```

---

## API Endpoints

### Home Page

```http
GET /
```

Returns the upload interface.

---

### Upload Event Poster

```http
POST /upload
```

#### Request

Multipart form-data:

```text
file=<image>
```

#### Response

```json
{
  "event": {
    "title": "Tech Conference 2026",
    "date": "June 14, 2026",
    "time": "10:00 AM",
    "location": "Hyderabad"
  },
  "calendar_link": "https://calendar.google.com/..."
}
```

---

## Example Workflow

1. Upload an event poster.
2. AI analyzes the image.
3. Event details are extracted.
4. Google Calendar link is generated.
5. User clicks the link to add the event.

---

## Future Enhancements

* Multiple event extraction from a single poster
* ICS file generation
* Event database integration
* Authentication and user accounts
* Mobile application
* Kubernetes deployment
* CI/CD pipeline
* Monitoring and observability
* OCR + VLM hybrid extraction

---

## Learning Outcomes

This project explores:

* Vision Language Models
* Multimodal AI Applications
* FastAPI Development
* Docker Containerization
* Event Automation
* Calendar Integration
* AI-powered Information Extraction

---

## License

This project is released under the MIT License.
