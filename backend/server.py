from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://mongo:27017')
client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
db = client[os.environ.get('DB_NAME', 'portfolio')]

# DB readiness flag
DB_READY: bool = False


async def wait_for_db(timeout: int = 30, interval: float = 1.0) -> bool:
    """Wait up to `timeout` seconds for MongoDB to be responsive.

    Returns True if the DB responded to a ping, False otherwise.
    """
    global DB_READY
    deadline = asyncio.get_event_loop().time() + timeout
    while True:
        try:
            # motor exposes the same admin command
            await client.admin.command("ping")
            DB_READY = True
            return True
        except Exception:
            if asyncio.get_event_loop().time() >= deadline:
                DB_READY = False
                return False
            await asyncio.sleep(interval)

# -------------------- Models --------------------

class Stat(BaseModel):
    label: str
    value: str

class Social(BaseModel):
    name: str
    url: str
    icon: str

class Profile(BaseModel):
    name: str
    handle: str
    role: str
    location: str
    email: str
    tagline: str
    bio: str
    avatar: str
    resumeUrl: str = "#"
    stats: List[Stat]
    socials: List[Social]

class Experience(BaseModel):
    role: str
    company: str
    period: str
    description: str

class Education(BaseModel):
    school: str
    degree: str
    period: str

class SkillItem(BaseModel):
    name: str
    level: int

class SkillGroup(BaseModel):
    category: str
    items: List[SkillItem]

class Project(BaseModel):
    id: str
    title: str
    category: str
    description: str
    tech: List[str]
    image: str
    github: str
    demo: str
    featured: bool = False

class PortfolioPayload(BaseModel):
    profile: Profile
    experience: List[Experience]
    education: List[Education]
    skillGroups: List[SkillGroup]
    projects: List[Project]

class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    message: str = Field(min_length=10, max_length=5000)

class ContactMessage(BaseModel):
    id: str
    name: str
    email: str
    message: str
    ts: datetime

class ContactResponse(BaseModel):
    id: str
    status: str
    ts: datetime

# Legacy status check (kept for compatibility)
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str


# -------------------- Seed Data --------------------

SEED_PROFILE: Dict[str, Any] = {
    "name": "Chinmay Gurav",
    "handle": "@chinmay.gurav",
    "role": "Full-Stack Engineer",
    "location": "Mumbai, India",
    "email": "tech.chinmayg@gmail.com",
    "tagline": "I build fast, accessible, and delightful web experiences.",
    "bio": (
        "Full-stack engineer with a passion for shipping production software "
        "across fintech, dev-tools, and SaaS. I care deeply about clean architecture, "
        "thoughtful UX, and performance budgets. Currently exploring distributed systems "
        "and LLM tooling."
    ),
    "avatar": "https://images.unsplash.com/photo-1672685667592-0392f458f46f",
    "resumeUrl": "#",
    "stats": [
        {"label": "Years Exp.", "value": "5+"},
        {"label": "Projects", "value": "40+"},
        {"label": "Commits / yr", "value": "2.1k"},
        {"label": "Coffee / day", "value": "\u221e"},
    ],
    "socials": [
        {"name": "GitHub", "url": "https://github.com/Chinmayg366", "icon": "Github"},
        {"name": "LinkedIn", "url": "https://www.linkedin.com/in/chinmay-gurav-55a38426a/", "icon": "Linkedin"},
        {"name": "X", "url": "https://x.com/chinmaygurav", "icon": "Twitter"},
        {"name": "Email", "url": "tech.chinmayg@gmail.com", "icon": "Mail"},
    ],
}

SEED_EXPERIENCE = [
    {
        "role": "Senior Software Engineer",
        "company": "Northbeam Labs",
        "period": "2023 \u2014 Present",
        "description": "Leading platform team building observability tools for distributed systems. Shipped a real-time tracing pipeline handling 40k rps.",
    },
    {
        "role": "Full-Stack Engineer",
        "company": "Finch Pay",
        "period": "2021 \u2014 2023",
        "description": "Built core ledger UI and onboarding flows in React + Node. Improved conversion by 18% via performance and UX refinements.",
    },
    {
        "role": "Software Engineer",
        "company": "Canvas Studio",
        "period": "2019 \u2014 2021",
        "description": "Developed collaborative design tools using WebSockets, Canvas API, and Postgres. First engineering hire.",
    },
]

SEED_EDUCATION = [
    {"school": "IIIT Hyderabad", "degree": "B.Tech, Computer Science", "period": "2015 \u2014 2019"}
]

SEED_SKILL_GROUPS = [
    {
        "category": "Frontend",
        "items": [
            {"name": "React / Next.js", "level": 95},
            {"name": "TypeScript", "level": 92},
            {"name": "TailwindCSS", "level": 90},
            {"name": "Framer Motion", "level": 75},
        ],
    },
    {
        "category": "Backend",
        "items": [
            {"name": "Node.js", "level": 90},
            {"name": "Python / FastAPI", "level": 85},
            {"name": "PostgreSQL", "level": 82},
            {"name": "MongoDB", "level": 78},
        ],
    },
    {
        "category": "DevOps & Tools",
        "items": [
            {"name": "Docker", "level": 85},
            {"name": "AWS", "level": 78},
            {"name": "GitHub Actions", "level": 82},
            {"name": "Kubernetes", "level": 65},
        ],
    },
]

SEED_PROJECTS = [
    {
        "id": "p1",
        "title": "Helios Observability",
        "category": "Platform",
        "description": "Real-time tracing and metrics dashboard for distributed services with sub-second query latency.",
        "tech": ["React", "TypeScript", "Go", "ClickHouse"],
        "image": "https://images.unsplash.com/photo-1664854953181-b12e6dda8b7c",
        "github": "https://github.com/Chinmayg366",
        "demo": "https://example.com",
        "featured": True,
    },
    {
        "id": "p2",
        "title": "Ledger Studio",
        "category": "Fintech",
        "description": "Double-entry accounting UI with keyboard-first navigation and diff-based reconciliation.",
        "tech": ["Next.js", "tRPC", "PostgreSQL"],
        "image": "https://images.pexels.com/photos/10020092/pexels-photo-10020092.jpeg",
        "github": "https://github.com/Chinmayg366",
        "demo": "https://example.com",
        "featured": True,
    },
    {
        "id": "p3",
        "title": "Quill CMS",
        "category": "SaaS",
        "description": "Headless CMS with visual content modeling, versioning, and role-based collaboration.",
        "tech": ["React", "Node.js", "MongoDB"],
        "image": "https://images.unsplash.com/photo-1590935216109-8d3318de2c1c",
        "github": "https://github.com/Chinmayg366",
        "demo": "https://example.com",
        "featured": False,
    },
    {
        "id": "p4",
        "title": "Pocket Budget",
        "category": "Mobile",
        "description": "Zero-based budgeting app with offline-first sync and envelope categorization.",
        "tech": ["React Native", "SQLite", "FastAPI"],
        "image": "https://images.unsplash.com/photo-1611120227195-91674b693491",
        "github": "https://github.com/Chinmayg366",
        "demo": "https://example.com",
        "featured": False,
    },
    {
        "id": "p5",
        "title": "Graphline",
        "category": "Data",
        "description": "Interactive data-viz library for time-series analytics, used at 3 fintech companies.",
        "tech": ["TypeScript", "D3.js", "Canvas"],
        "image": "https://images.unsplash.com/photo-1529078155058-5d716f45d604",
        "github": "https://github.com/Chinmayg366",
        "demo": "https://example.com",
        "featured": True,
    },
    {
        "id": "p6",
        "title": "Devbench",
        "category": "Dev-tools",
        "description": "Benchmark harness for comparing serverless platforms across cold-start and throughput.",
        "tech": ["Python", "FastAPI", "Docker"],
        "image": "https://images.unsplash.com/photo-1549818771-cb569f554ac7",
        "github": "https://github.com/Chinmayg366",
        "demo": "https://example.com",
        "featured": False,
    },
]


async def seed_if_empty():
    """Seed portfolio collections if profile is not present."""
    # If DB is not ready, don't try to run DB operations here.
    if not DB_READY:
        logger.warning("seed_if_empty skipped because DB is not ready")
        return

    existing = await db.portfolio_profile.find_one({"_key": "singleton"})
    if existing:
        return
    await db.portfolio_profile.insert_one({"_key": "singleton", **SEED_PROFILE})
    if SEED_EXPERIENCE:
        await db.portfolio_experience.insert_many([{**e} for e in SEED_EXPERIENCE])
    if SEED_EDUCATION:
        await db.portfolio_education.insert_many([{**e} for e in SEED_EDUCATION])
    if SEED_SKILL_GROUPS:
        await db.portfolio_skill_groups.insert_many([{**g} for g in SEED_SKILL_GROUPS])
    if SEED_PROJECTS:
        await db.portfolio_projects.insert_many([{**p} for p in SEED_PROJECTS])
    logger.info("Portfolio collections seeded with initial data.")


def clean(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    doc.pop("_id", None)
    doc.pop("_key", None)
    return doc


# -------------------- Lifespan Context --------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ok = await wait_for_db(timeout=30)
    if not ok:
        logger.error("Database did not become ready within timeout; continuing without DB")
    else:
        try:
            await seed_if_empty()
        except Exception as e:
            logger.error(f"Startup seed failed: {e}")
    yield
    # Shutdown
    client.close()


# -------------------- FastAPI App --------------------

app = FastAPI(title="Portfolio API", lifespan=lifespan)
api_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- Routes --------------------

@api_router.get("/")
async def root():
    return {"message": "Portfolio API"}


# Health endpoint returning service + DB readiness
@api_router.get("/health")
async def health():
    return {"status": "ok", "db_ready": DB_READY}


@api_router.get("/portfolio", response_model=PortfolioPayload)
async def get_portfolio():
    # If DB is not known-ready, fall back to returning the seeded payload
    # This allows the frontend to function in development without a running DB.
    if not DB_READY:
        logger.warning("Database not available — returning seeded portfolio payload")
        return {
            "profile": clean({**{"_key": "singleton"}, **SEED_PROFILE}),
            "experience": [clean(e) for e in SEED_EXPERIENCE],
            "education": [clean(e) for e in SEED_EDUCATION],
            "skillGroups": [clean(g) for g in SEED_SKILL_GROUPS],
            "projects": [clean(p) for p in SEED_PROJECTS],
        }

    try:
        await seed_if_empty()
        profile_doc = await db.portfolio_profile.find_one({"_key": "singleton"})
    except Exception as e:
        # If any DB error occurs at runtime, return 503 with Retry-After header
        logger.exception("Error accessing database for /api/portfolio")
        return JSONResponse(
            status_code=503,
            content={"detail": "Database unavailable, try again later"},
            headers={"Retry-After": "30"},
        )
    if not profile_doc:
        raise HTTPException(status_code=500, detail="Profile not seeded")

    experience = [clean(d) for d in await db.portfolio_experience.find().to_list(100)]
    education = [clean(d) for d in await db.portfolio_education.find().to_list(50)]
    skill_groups = [clean(d) for d in await db.portfolio_skill_groups.find().to_list(50)]
    projects = [clean(d) for d in await db.portfolio_projects.find().to_list(200)]

    return {
        "profile": clean(profile_doc),
        "experience": experience,
        "education": education,
        "skillGroups": skill_groups,
        "projects": projects,
    }


@api_router.post("/contact", response_model=ContactResponse)
async def create_contact(payload: ContactCreate):
    msg_id = str(uuid.uuid4())
    ts = datetime.now(timezone.utc)
    doc = {
        "id": msg_id,
        "name": payload.name.strip(),
        "email": str(payload.email).strip(),
        "message": payload.message.strip(),
        "ts": ts,
    }
    await db.contact_messages.insert_one(doc)
    return {"id": msg_id, "status": "received", "ts": ts}


@api_router.get("/contact", response_model=List[ContactMessage])
async def list_contacts():
    docs = await db.contact_messages.find().sort("ts", -1).to_list(500)
    return [ContactMessage(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


# Legacy endpoints (kept)
@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(payload: StatusCheckCreate):
    status_obj = StatusCheck(**payload.dict())
    await db.status_checks.insert_one(status_obj.dict())
    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    docs = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]


# Include router
app.include_router(api_router)
