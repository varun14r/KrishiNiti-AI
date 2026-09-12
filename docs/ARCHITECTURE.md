# KrishiNiti AI Architecture

## Runtime flow

1. Farmer enters a natural-language question.
2. React sends the request to FastAPI.
3. ChatService embeds the query.
4. ChromaDB retrieves semantically relevant agricultural chunks.
5. Retrieved context is assembled into a grounded prompt.
6. IBM Granite (`ibm/granite-4-h-small`) generates the response.
7. The API returns the answer and retrieval metadata.
8. React presents the response and retrieved topics.

## Knowledge ingestion

Agricultural documents → loader → chunking → IBM `granite-embedding-278m-multilingual` → ChromaDB.

The same embedding model is used for document and query embeddings.

## Safety

The system is deliberately conservative about live information and uncertain diagnosis. It does not fabricate current weather or mandi prices and avoids unsupported pesticide dosing.
