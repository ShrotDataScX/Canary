# Week 2: Data Ingestion & Processing

> **Status: outline.** Detailed resources and tasks will be added at the end of Week 1, informed by what the team learned.

## Goal
Turn the exploration scripts from Week 1 into **robust, repeatable ingestion pipelines** that produce a clean, chunked, metadata-rich corpus ready for indexing.

## Planned topics
- Production-quality loaders for **CISA KEV**, **NVD** (pagination, rate limiting, retries, disk caching), **SEC EDGAR** (10-K, 8-K; CIK mapping; amendments) and **market data**
- Parsing 10-K HTML: extracting **Item 1A, 1C, 7**; handling tables and inline XBRL
- **Chunking strategies**: structure-aware vs fixed-size, overlap, token counting
- A shared **metadata schema** (`source`, `cik`, `ticker`, `form`, `item`, `filing_date`, `url`, …)
- Data validation (`pydantic`/schemas), logging, and reproducible **corpus snapshots**
- Choosing a bounded **company universe** (~30 companies)

## Expected deliverables
- `src/canary/ingest/` modules with unit tests
- A documented corpus format (JSONL/Parquet) + snapshot date
- A data-quality report (counts, missing fields, chunk-length distribution)

## Prerequisite
Complete [Week 1](../week-1/README.md), especially exercises 1–3 and 7.
