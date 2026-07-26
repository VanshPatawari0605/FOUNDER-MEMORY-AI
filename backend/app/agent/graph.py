from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from app.config import settings
from app.agent.tools import search_memories, get_entity, get_promises, get_timeline
from sqlalchemy.orm import Session
from typing import TypedDict, Annotated
import operator
import json

llm = ChatGroq(api_key=settings.GROQ_API_KEY, model="llama-3.1-8b-instant")

class AgentState(TypedDict):
    question: str
    tenant_id: str
    company_context: str
    plan: str
    tool_calls: Annotated[list, operator.add]
    context: Annotated[list, operator.add]
    answer: str
    sources: list[str]

def planner(state: AgentState) -> AgentState:
    prompt = f"""You are a planning agent. Given a question, decide which tools to call.
Available tools: search_memories, get_entity, get_promises, get_timeline

Company context: {state.get("company_context", "")}
Question: {state["question"]}

Respond with JSON only:
{{"tools": ["tool1", "tool2"], "args": {{"search_memories": "query", "get_entity": "name", "get_promises": "person", "get_timeline": "topic"}}}}"""

    response = llm.invoke(prompt)
    raw = response.content.strip().replace("```json", "").replace("```", "").strip()
    state["plan"] = raw
    return state

def tool_caller(state: AgentState, db: Session) -> AgentState:
    try:
        plan = json.loads(state["plan"])
        tools = plan.get("tools", [])
        args = plan.get("args", {})
        tid = state["tenant_id"]
        calls = []
        context = []

        if "search_memories" in tools:
            results = search_memories(args.get("search_memories", state["question"]), tid, db)
            calls.append("search_memories")
            context.extend(results)

        if "get_entity" in tools:
            results = get_entity(args.get("get_entity", ""), tid, db)
            calls.append("get_entity")
            context.extend(results)

        if "get_promises" in tools:
            results = get_promises(args.get("get_promises", ""), tid, db)
            calls.append("get_promises")
            context.extend(results)

        if "get_timeline" in tools:
            results = get_timeline(args.get("get_timeline", state["question"]), tid, db)
            calls.append("get_timeline")
            context.extend(results)

        state["tool_calls"] = calls
        state["context"] = context

    except Exception as e:
        print(f"Tool caller error: {e}")
        state["context"] = []

    return state

def synthesizer(state: AgentState) -> AgentState:
    context_text = "\n\n".join(
        f"[{i+1}] {c.get('content') or c.get('commitment') or c.get('description', '')}"
        f" (source: {c.get('source') or c.get('name', 'unknown')})"
        for i, c in enumerate(state["context"])
    )

    prompt = f"""You are a founder's AI memory assistant. Answer the question using only the context below and company context.
Always cite sources. If you don't know, say so.

Company context: {state.get("company_context", "")}

Context:
{context_text}

Question: {state["question"]}"""

    response = llm.invoke(prompt)
    state["answer"] = response.content
    state["sources"] = list(set(
        c.get("source") or c.get("name", "")
        for c in state["context"]
        if c.get("source") or c.get("name")
    ))
    return state

def build_graph(db: Session):
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("tool_caller", lambda s: tool_caller(s, db))
    graph.add_node("synthesizer", synthesizer)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "tool_caller")
    graph.add_edge("tool_caller", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()

def run_agent(question: str, tenant_id: str, db: Session, company_context: str = "") -> dict:
    graph = build_graph(db)
    result = graph.invoke({
        "question": question,
        "tenant_id": tenant_id,
        "company_context": company_context,
        "plan": "",
        "tool_calls": [],
        "context": [],
        "answer": "",
        "sources": []
    })
    return {"answer": result["answer"], "sources": result["sources"]}