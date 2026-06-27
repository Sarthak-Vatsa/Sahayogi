# Creator Insights AI Agent

Creator Insights is an AI-powered research and strategy agent that helps content creators consistently generate high-performing content by learning from successful creators in their niche.

Unlike traditional analytics tools that only display engagement metrics, Creator Insights monitors competitors, analyzes their content, identifies emerging trends, explains why reels perform well, and generates personalized recommendations tailored to a creator's own brand.

The long-term vision is to build an AI content strategist rather than another analytics dashboard.

---

## Motivation

Every content creator eventually asks the same questions:

* What should I create next?
* Which hooks are working this week?
* Which trends are worth adapting?
* Why did this reel outperform the creator's average?
* Would this idea fit my own content?

Answering these questions manually requires watching hundreds of reels every week.

Creator Insights automates this research process and converts raw analytics into actionable content strategy.

---

## Core Objective

Given:

* A list of competitor Instagram accounts
* A detailed description of a creator's brand, characters, style and goals

The agent answers:

> **What should I create next?**

---

## Features

### Competitor Monitoring

* Track competitor Instagram accounts
* Detect new reels
* Identify unusually high-performing content
* Maintain historical performance data

### Metadata Collection

Collects structured reel metadata including:

* Duration
* Views
* Likes
* Comments
* Caption
* Hashtags
* Audio
* Upload date

### AI Reel Analysis

Uses an LLM to analyze every reel and extract:

* Visual hook
* Written hook
* Spoken hook
* Story structure
* Camera movement
* Editing style
* Emotional triggers
* Audio style
* Psychological techniques

### Performance Reasoning

Instead of simply describing a reel, the agent explains:

* Why it performed well
* What retained viewers
* Which psychological triggers were used
* Which elements contributed most to engagement

### Trend Detection

Analyzes hundreds of reels to discover patterns such as:

* Most effective hook styles
* Best-performing durations
* Popular emotions
* Emerging content formats
* Camera trends
* Audio trends

### Personalized Recommendations

The agent understands a creator's brand and produces recommendations that maintain originality while adapting successful concepts.

---

## Project Structure

```text
creator-insights-agent/

├── config/
├── data/
├── agent/
├── prompts/
├── reel_schema.json
├── requirements.txt
└── README.md
```

---

## Architecture

```
Competitor Accounts
        │
        ▼
Collector
        │
        ▼
Metadata Extraction
        │
        ▼
LLM Analysis
        │
        ▼
Performance Reasoning
        │
        ▼
Trend Detection
        │
        ▼
Recommendation Engine
        │
        ▼
Weekly Report
```

---

## Technology Stack

### Language

* Python

### AI

* Gemini API

### Backend

* FastAPI (future)

### Database

* JSON (current)
* PostgreSQL via Supabase (future)

### Deployment

* Local development (current)
* Railway / Render (future)
* Vercel (future frontend)

---

## Development Roadmap

### Phase 1

Core intelligence

* Competitor monitoring
* Reel analysis
* Trend detection
* Personalized recommendations

### Phase 2

Automation

* Scheduled runs
* Historical tracking
* Weekly reports

### Phase 3

Dashboard

* Visual analytics
* Searchable insights
* Competitor comparisons

### Phase 4

SaaS

* User accounts
* Multiple creators
* Cloud deployment
* Subscription model

---

## Current Status

🚧 Under active development.

The current focus is validating the intelligence of the recommendation engine before investing in dashboards or frontend development.

---

## Long-Term Vision

The goal is not to build another Instagram analytics platform.

The goal is to build an AI-powered content strategist that continuously researches competitors, understands successful content, identifies trends, and recommends original ideas tailored to each creator's unique brand.

By automating research, creators can spend less time analyzing content and more time creating it.