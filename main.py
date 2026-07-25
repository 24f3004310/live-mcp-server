import hashlib
from fastapi import Request
from fastmcp import FastMCP, Context

NORMALIZED_EMAIL = "24f3004310@ds.study.iitm.ac.in"

# 1. Initialize FastMCP
mcp = FastMCP("Exam-Challenge-Server")

# 2. Define the tool required by the grader
@mcp.tool(
    name="solve_challenge",
    description="Solves the exam header challenge by calculating a SHA-256 slice."
)
async def solve_challenge(ctx: Context) -> str:
    # Retrieve request context
    request: Request = ctx.request_context.request
    
    # Read the custom header (Starlette/FastAPI headers are case-insensitive)
    challenge = request.headers.get("X-Exam-Challenge", "")
    
    if not challenge:
        return "error: missing X-Exam-Challenge header"

    # Compute SHA-256("${challenge}:${normalizedEmail}")
    raw_str = f"{challenge}:{NORMALIZED_EMAIL}"
    sha256_hash = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
    
    # Return the first 16 hex characters
    return sha256_hash[:16]

# 3. Create the HTTP ASGI application mapped explicitly to the root path "/"
app = mcp.http_app(path="/")