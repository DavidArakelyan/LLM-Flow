"""Classify the query into simple / needs web search / needs doc / wants_code / wants_text."""
import re
def classify(state):
    q = state['query']
    lower = q.lower()
    state['is_simple'] = len(q.split()) < 20 and not any(k in lower for k in ['generate', 'create', 'write', 'code', 'document', 'pdf'])
    state['needs_web_search'] = 'latest' in lower or 'current' in lower or 'today' in lower
    state['needs_doc'] = 'attached' in lower or 'document' in lower
    state['wants_code'] = any(ext in lower for ext in ['.cpp', '.py', '.java', '.ts', 'c++', 'python', 'typescript', 'java'])
    state['wants_text'] = not state['wants_code']
    return state
