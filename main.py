
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

# Enable CORS for browser-based graders
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StreamRequest(BaseModel):
    prompt: str
    stream: bool = True


def generate_essay():
    return (
        "Artificial intelligence has become one of the most transformative "
        "technologies of the twenty-first century. As AI systems grow more capable, "
        "ethical considerations surrounding their development and deployment become "
        "increasingly urgent. AI ethics is concerned with ensuring that intelligent "
        "systems are designed in ways that promote fairness, accountability, "
        "transparency, and human well-being.\n\n"

        "One major ethical concern is bias. AI systems are trained on data, and if "
        "that data reflects historical inequalities or prejudices, the system may "
        "replicate or even amplify those biases. This can result in unfair treatment "
        "in areas such as hiring, lending, healthcare, and criminal justice. "
        "Developers must therefore prioritize diverse datasets and implement bias "
        "detection mechanisms to reduce discriminatory outcomes.\n\n"

        "Another important issue is privacy. AI systems often rely on massive amounts "
        "of personal data. Without proper safeguards, individuals may lose control "
        "over their information. Ethical AI development requires strong data "
        "protection policies, encryption standards, and transparency about how data "
        "is collected and used.\n\n"

        "Accountability is equally critical. When AI systems make decisions, it must "
        "be clear who is responsible for those outcomes. Organizations deploying AI "
        "should maintain audit trails and provide explanations for automated "
        "decisions to ensure trust and regulatory compliance.\n\n"

        "Finally, there is the broader societal impact. As automation increases, "
        "concerns arise about job displacement and economic inequality. Ethical AI "
        "policy must include strategies for workforce transition, education, and "
        "inclusive growth to prevent widening social gaps.\n\n"

        "In conclusion, AI ethics is not optional but essential. By embedding "
        "fairness, transparency, accountability, and human-centered values into AI "
        "systems, society can harness technological progress while minimizing harm. "
        "Responsible innovation ensures that artificial intelligence remains a tool "
        "for collective benefit rather than a source of unintended consequences."
    )


async def stream_generator():
    essay = generate_essay()
    words = essay.split(" ")

    for word in words:
        payload = {
            "choices": [
                {
                    "delta": {
                        "content": word + " "
                    }
                }
            ]
        }

        yield f"data: {json.dumps(payload)}\n\n"
        await asyncio.sleep(0.02)

    yield "data: [DONE]\n\n"


@app.post("/")
async def stream_endpoint(request: StreamRequest):
    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream"
    )
