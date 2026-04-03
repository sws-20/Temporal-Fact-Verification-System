# Temporal-Fact-Verification-System
An NLP-based system that extracts timeline information from Wikipedia biographies and detects chronological inconsistencies using rule-based temporal reasoning.

This project focuses on verifying temporal facts from Wikipedia biography pages. The system uses Natural Language Processing (NLP) to extract dates, ages, and event-related information from unstructured text and then checks whether the timeline of events is logically consistent.
The goal of this project is to go beyond traditional fact-checking by verifying whether information is chronologically possible and consistent, not just whether it exists.

**Objectives**
Extract temporal information (dates, ages, years, events) from biography text
Build a timeline of events for an individual
Apply rule-based logic to verify timeline consistency
Detect logically impossible or inconsistent temporal claims

### **Tech Stack**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Wikipedia](https://img.shields.io/badge/Wikipedia-000000?style=for-the-badge&logo=wikipedia&logoColor=white)

**Project Status (Currently Under Development)**

This project is currently in development. The following components are in progress:

Extracting dates and age information from text using spaCy
Creating custom Named Entity Recognition (NER) patterns for biographical data
Building event timeline from extracted information
Developing rule-based logic to compare events and detect inconsistencies
Designing the “Quantity Evolution” logic to track how values like age and years change across events
Testing the system on Wikipedia biography pages
