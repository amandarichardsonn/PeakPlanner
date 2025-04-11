RoadMap
=======

**Step 1**: Create basic chat interface
Set up a frontend interface with streamlit

- [x] Task 1: Build frontend using streamlit
- [x] Task 2: Connect to a LLM (narrowed down to Claude 3 or GPT-4)

-----------------------------------------------------------

**Step 2**: Setup vector search with embeddings
Pull mountaineering trip reports from forums like Mountain Project, process the text, generate embeddings, store in vector db for semantic search

- [x] Task 1: Scrape trip reports and store in json or csv file
- [ ] Task 2: Process the scraped text data into a format for vector embeddings
- [ ] Task 3: Store the generated embeddings in a vector db for future semantic search

-----------------------------------------------------------

**Step 3**: Build the RAG pipeline (using LangChain or LlamaIndex)
Combine retrieval from vector db and generation of response from the LLM

- [ ] Task 1: convert user queries into embedding, search the vector db using similarity search and return the text content of the documents
- [ ] Task 2: send the users query and returned trip reports to the LLM and display response
- [ ] Task 3: possibly fine tune the RAG pipeline?

-----------------------------------------------------------

**Step 4**: Document Summarization
Summarize long trip reports to mitigate context window limit

- [ ] Task 1. Write a function that breaks long text into smaller chunks of tokens
- [ ] Task 2. fine tune the prompt and summarization process
- [ ] Task 3. connect summarization capability to flow / make accessible to user

-----------------------------------------------------------

**Step 5**: Weather Integration
Add weather data

- [ ] Task 1. Write a function to accept location, query weather api, parse temperature, wind speed, etc, format the output for return
