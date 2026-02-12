"""
BillEasy RAG Chatbot — Streamlit Interface
============================================
Professional chat UI with document upload, source display,
confidence indicators, and conversation management.
"""

import streamlit as st
from pathlib import Path

# ─── Must be the first Streamlit command ─────────────────
st.set_page_config(
    page_title="BillEasy — Soporte Técnico AI",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.chatbot import RAGChatbot, ChatResponse
from src.utils import Config, DATA_DIR


# ─── Custom CSS ──────────────────────────────────────────
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }

    /* Header */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .header-container h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .header-container p {
        margin: 0.3rem 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }

    /* Source cards */
    .source-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 0.6rem 1rem;
        margin: 0.3rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.85rem;
    }

    /* Confidence indicator */
    .confidence-high { color: #28a745; font-weight: 600; }
    .confidence-medium { color: #ffc107; font-weight: 600; }
    .confidence-low { color: #dc3545; font-weight: 600; }

    /* Stats cards */
    .stats-card {
        background: #f1f3f5;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.3rem 0;
    }
    .stats-card .number {
        font-size: 1.4rem;
        font-weight: 700;
        color: #667eea;
    }
    .stats-card .label {
        font-size: 0.75rem;
        color: #6c757d;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #adb5bd;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ────────────────────────
def init_session_state():
    """Initialize all Streamlit session state variables."""
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = RAGChatbot()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "docs_loaded" not in st.session_state:
        st.session_state.docs_loaded = False
    if "uploaded_files_list" not in st.session_state:
        st.session_state.uploaded_files_list = []

init_session_state()
chatbot: RAGChatbot = st.session_state.chatbot


# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📁 Documentos")

    # Load sample documents
    if not st.session_state.docs_loaded:
        if st.button("📥 Cargar Documentos de Demo", use_container_width=True):
            with st.spinner("Cargando documentos de BillEasy..."):
                count = chatbot.load_sample_documents()
                st.session_state.docs_loaded = True
                # Populate uploaded files list with sample docs
                if DATA_DIR.exists():
                    for f in sorted(DATA_DIR.iterdir()):
                        if f.is_file() and f.suffix in {".md", ".pdf", ".txt", ".docx"}:
                            st.session_state.uploaded_files_list.append(f.name)
            st.success(f"✅ {count} fragmentos cargados")
            st.rerun()
    else:
        st.success(f"✅ {chatbot.em.document_count} fragmentos en memoria")

    st.markdown("---")

    # File upload
    st.markdown("### ➕ Subir Documentos")
    uploaded_files = st.file_uploader(
        "Arrastra tus archivos aquí",
        type=["pdf", "txt", "docx", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_files_list:
                with st.spinner(f"Procesando {uploaded_file.name}..."):
                    count = chatbot.load_uploaded_file(
                        uploaded_file.getvalue(),
                        uploaded_file.name,
                    )
                    st.session_state.uploaded_files_list.append(uploaded_file.name)
                st.success(f"✅ {uploaded_file.name} — {count} fragmentos")

    # Show loaded documents
    if st.session_state.uploaded_files_list:
        st.markdown("### 📄 Documentos Cargados")
        for doc_name in st.session_state.uploaded_files_list:
            st.markdown(f"- 📎 `{doc_name}`")

    st.markdown("---")

    # Actions
    st.markdown("### ⚙️ Acciones")

    if st.button("🗑️ Limpiar Historial", use_container_width=True):
        st.session_state.messages = []
        chatbot.clear_memory()
        st.rerun()

    if st.button("🔄 Reiniciar Todo", use_container_width=True):
        st.session_state.messages = []
        st.session_state.docs_loaded = False
        st.session_state.uploaded_files_list = []
        chatbot.clear_all()
        st.rerun()

    st.markdown("---")

    # Metrics
    st.markdown("### 📊 Métricas")
    metrics = chatbot.metrics.summary()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="number">{metrics['total_queries']}</div>
            <div class="label">Consultas</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        avg_time = round(metrics.get('avg_response_time_ms', 0))
        st.markdown(f"""
        <div class="stats-card">
            <div class="number">{avg_time}ms</div>
            <div class="label">Tiempo Promedio</div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        avg_conf = round(metrics.get('avg_confidence', 0) * 100)
        st.markdown(f"""
        <div class="stats-card">
            <div class="number">{avg_conf}%</div>
            <div class="label">Confianza</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stats-card">
            <div class="number">{chatbot.em.document_count}</div>
            <div class="label">Fragmentos</div>
        </div>
        """, unsafe_allow_html=True)

    # Configuration
    st.markdown("---")
    st.markdown("### 🎛️ Configuración")
    with st.expander("Parámetros del modelo"):
        new_temp = st.slider("Temperature", 0.0, 1.0, chatbot.config.temperature, 0.1)
        new_top_k = st.slider("Top K (documentos)", 1, 10, chatbot.config.top_k)
        new_threshold = st.slider("Umbral de confianza", 0.0, 1.0, chatbot.config.confidence_threshold, 0.05)

        if new_temp != chatbot.config.temperature:
            chatbot.config.temperature = new_temp
        if new_top_k != chatbot.config.top_k:
            chatbot.config.top_k = new_top_k
        if new_threshold != chatbot.config.confidence_threshold:
            chatbot.config.confidence_threshold = new_threshold


# ─── Main Chat Area ──────────────────────────────────────

# Header
st.markdown("""
<div class="header-container">
    <h1>🧾 BillEasy — Soporte Técnico AI</h1>
    <p>Asistente inteligente basado en la documentación oficial de BillEasy</p>
</div>
""", unsafe_allow_html=True)

# Check if documents are loaded
if not st.session_state.docs_loaded and chatbot.em.document_count == 0:
    st.info("👈 Comienza cargando los documentos de demo desde el sidebar, o sube tus propios documentos.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🧾"):
        st.markdown(msg["content"])

        # Show sources for assistant messages
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander(f"📄 Fuentes consultadas ({len(msg['sources'])})"):
                for src in msg["sources"]:
                    st.markdown(
                        f'<div class="source-card">'
                        f'📎 <strong>{src["source"]}</strong> — '
                        f'Fragmento {src["chunk"]} — '
                        f'Relevancia: {src["relevance"]:.0%}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            # Confidence badge
            confidence = msg.get("confidence", 0)
            if confidence >= 0.7:
                css_class = "confidence-high"
                label = "Alta"
            elif confidence >= 0.4:
                css_class = "confidence-medium"
                label = "Media"
            else:
                css_class = "confidence-low"
                label = "Baja"

            col_conf, col_time, col_fb = st.columns([2, 2, 3])
            with col_conf:
                st.markdown(
                    f'Confianza: <span class="{css_class}">{confidence:.0%} ({label})</span>',
                    unsafe_allow_html=True,
                )
            with col_time:
                rt = msg.get("response_time", 0)
                st.caption(f"⏱️ {rt*1000:.0f}ms")

            # Feedback buttons
            with col_fb:
                msg_idx = msg.get("idx", 0)
                c1, c2, _ = st.columns([1, 1, 4])
                with c1:
                    if st.button("👍", key=f"up_{msg_idx}"):
                        st.toast("¡Gracias por tu feedback! 👍")
                with c2:
                    if st.button("👎", key=f"down_{msg_idx}"):
                        st.toast("Gracias, mejoraremos esta respuesta 📝")


# Chat input
if prompt := st.chat_input("Escribe tu pregunta sobre BillEasy..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="🧾"):
        with st.spinner("Buscando en la documentación..."):
            response: ChatResponse = chatbot.chat(prompt)

        st.markdown(response.answer)

        # Sources
        if response.sources:
            with st.expander(f"📄 Fuentes consultadas ({len(response.sources)})"):
                for src in response.sources:
                    st.markdown(
                        f'<div class="source-card">'
                        f'📎 <strong>{src["source"]}</strong> — '
                        f'Fragmento {src["chunk"]} — '
                        f'Relevancia: {src["relevance"]:.0%}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

        # Confidence
        if response.confidence >= 0.7:
            css_class = "confidence-high"
            label = "Alta"
        elif response.confidence >= 0.4:
            css_class = "confidence-medium"
            label = "Media"
        else:
            css_class = "confidence-low"
            label = "Baja"

        col_conf, col_time, col_fb = st.columns([2, 2, 3])
        with col_conf:
            st.markdown(
                f'Confianza: <span class="{css_class}">{response.confidence:.0%} ({label})</span>',
                unsafe_allow_html=True,
            )
        with col_time:
            st.caption(f"⏱️ {response.response_time*1000:.0f}ms")

        # Feedback
        msg_idx = len(st.session_state.messages)
        with col_fb:
            c1, c2, _ = st.columns([1, 1, 4])
            with c1:
                if st.button("👍", key=f"up_{msg_idx}"):
                    chatbot.record_feedback(response, "positive")
                    st.toast("¡Gracias por tu feedback! 👍")
            with c2:
                if st.button("👎", key=f"down_{msg_idx}"):
                    chatbot.record_feedback(response, "negative")
                    st.toast("Gracias, mejoraremos esta respuesta 📝")

    # Save to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
        "response_time": response.response_time,
        "idx": msg_idx,
    })

# Footer
st.markdown("""
<div class="footer">
    BillEasy RAG Chatbot — Powered by OpenAI + LangChain + ChromaDB<br>
    Los documentos son propiedad de BillEasy (empresa ficticia con fines demostrativos)
</div>
""", unsafe_allow_html=True)
