## AI Coding Tools Used

### 1. GitHub Copilot

Usage:

- Accelerated writing boilerplate Python code
- Helped with function scaffolding
- Useful for repetitive code patterns

Worked well:

- Quick completions
- Autocomplete in LangChain pipelines
- Suggested fix patterns for common API errors

Did not work well:

- Sometimes suggested outdated LangChain APIs
- Occasionally hallucinated unavailable methods
- Needed supervision, especially with breaking LangChain changes

---

### 2. ChatGPT (GPT-5.1)

Usage:

- Designing system architecture
- Debugging authentication and API errors
- Refining retrieval logic
- Generating documentation (this file and design-and-evaluation.md)

Worked well:

- Reliable explanations for error messages
- Great at producing structured documentation
- Good for validating RAG pipeline architecture

Did not work well:

- Sometimes suggested legacy OpenAI client syntax
- Occasional confusion between "old" and "new" RAG patterns in LangChain

---

### 3. LangChain Debugging Tools

Usage:

- Document loaders
- Inspecting vector content
- Printing retrieved chunks during evaluation

Worked well:

- Easy to inspect retrieval output
- Good for debugging embeddings

Did not work well:

- Some debugging tools are poorly documented
- Occasional version mismatches

---

### 4. OpenAI Playground

Usage:

- Testing prompt strategies
- Comparing different models for synthesis

Worked well:

- Easy to test temperature, top_p, system prompts
- Great for creating final answer-generation prompt

Did not work well:

- Hard to test retrieval-only workflows without external code
