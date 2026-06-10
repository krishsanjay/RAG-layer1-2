# README

## Overview

This folder contains two scripts that demonstrate different approaches to document extraction for a Retrieval-Augmented Generation (RAG) pipeline.

### 1. Naive Document Extraction

This script performs basic document content extraction without considering document structure.

### 2. Enhanced Document Extraction

This script performs more advanced document processing and extraction. It handles:

- Tables and tabular data
- Multi-column document layouts
- Section boundaries and structure
- Intelligent chunking based on section size and content organization

The enhanced approach produces higher-quality content for downstream RAG applications.

## Prerequisites

Before running the scripts, ensure that:

- All required Python dependencies are installed.
- The `.env` file is present and configured correctly.
- The `.env` file is **not committed** to version control.

## Running the Scripts

Execute a script using:

```bash
python <script_name>.py