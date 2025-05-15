# RAGHunter TODO List

## Epic 1: Data Cleansing and Completion

**Goal**: Ensure the quality and consistency of the input knowledge sources to reduce downstream errors.

1. **User Stories**:

   * As a data engineer, I want to automatically validate and complete missing fields in structured tables to minimize manual intervention.
   * As a document processor, I want to extract and correct OCR recognition errors to ensure a full-text accuracy rate of ≥ 95%.

2. **Tasks**:

   * [ ] Design and review "field-level data quality standards" (referencing *Great Expectations*)
   * [ ] Implement an automatic completion module for missing values in structured data (using Pandas + Pydantic)
   * [ ] Integrate PDF/Word document parsing
   * [ ] Introduce an OCR detection and correction pipeline
   * [ ] Write unit tests with coverage ≥ 80%
   * [ ] Deploy to the development environment, run a smoke test: input sample data → output validated and completed data

## Epic 2: Intelligent Chunking and Deduplication

**Goal**: Generate high-quality, low-redundancy text chunks that are ready for vectorization.

1. **User Stories**:

   * As a retrieval developer, I want to intelligently split text based on chapters/paragraphs to preserve contextual coherence.
   * As a system administrator, I want to automatically eliminate duplicate or highly similar chunks to save storage and retrieval costs.

2. **Tasks**:

   * [ ] Define metadata structure for chunks (ID, source document, hierarchy level, character count, etc.)
   * [ ] Implement a “structure-based” splitting strategy (headings + paragraph boundaries)
   * [ ] Supplement with a “length-based” strategy (e.g., max token limits)
   * [ ] Integrate approximate deduplication algorithms (MinHash + Cosine Similarity)
   * [ ] Develop a batch deduplication pipeline with threshold parameterization
   * [ ] Write performance tests (e.g., deduplicate 10,000 chunks in under XX seconds)
   * [ ] Release an Alpha version and invite internal users for usability feedback

## Epic 3: Retrieval Evaluation and Weight Optimization

**Goal**: Continuously validate retrieval quality and automate parameter tuning to meet recall and precision standards in production.

1. **User Stories**:

   * As a product manager, I need an automated evaluation metric suite (Recall, Precision, MRR) to quantify retrieval performance.
   * As a search engineer, I want a one-click workflow to test different index configurations and get optimal parameter recommendations.

2. **Tasks**:

   * [ ] Design an evaluation case set (including representative business queries + annotated answers)
   * [ ] Develop an evaluation framework supporting batch tests (various embedding models + index types)
   * [ ] Generate automated reports (in HTML/Markdown with visualized metrics)
   * [ ] Integrate a parameter tuner (Grid Search / Bayesian Optimization)
   * [ ] Output recommended parameter configurations and push to the indexing module
   * [ ] Set up a “model performance monitoring dashboard” (Grafana + Prometheus)

## Cross-Cutting: Pipeline Orchestration and Release

**Goal**: Link all modules into a CI/CD pipeline that can be triggered with one click.

* [ ] Define the overall API specification and data contract documentation
* [ ] Use Airflow/Prefect to orchestrate module execution order
* [ ] Configure CI pipeline: code linting → unit testing → deployment tests
* [ ] Write user operation manuals & deployment guides
* [ ] Conduct cross-team reviews to confirm MVP release milestones