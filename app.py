import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import streamlit as st
from main import run_content_creation

# Configuração da página
st.set_page_config(
    page_title="Assistente de Criação de Conteúdo",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração da sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 400px;
        max-width: 600px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título da aplicação
st.title("📝 Assistente de Criação de Conteúdo")
st.write("Seu assistente para criar conteúdo envolvente e estratégico")

# Inicializa o estado da sessão
if 'resultado' not in st.session_state:
    st.session_state.resultado = None

# Sidebar com informações
with st.sidebar:
    st.header("📋 Informações do Projeto")
    
    topic = st.text_input(
        "Tópico Principal",
        help="Digite o tema principal do conteúdo que você deseja criar"
    )
    
    target_audience = st.text_area(
        "Público-Alvo",
        help="Descreva o perfil do público que você deseja alcançar com este conteúdo"
    )
    
    content_goals = st.multiselect(
        "Objetivos do Conteúdo",
        ["Educar", "Entreter", "Converter", "Engajar", "Informar", "Inspirar"],
        help="Selecione os principais objetivos do seu conteúdo"
    )
    
    platforms = st.multiselect(
        "Plataformas",
        ["Blog", "Instagram", "LinkedIn", "Facebook", "Twitter", "TikTok"],
        help="Selecione as plataformas onde o conteúdo será publicado"
    )
    
    st.header("🎯 Diretrizes de Conteúdo")
    tone = st.select_slider(
        "Tom da Comunicação",
        options=["Formal", "Profissional", "Neutro", "Casual", "Descontraído"],
        value="Profissional"
    )
    
    additional_instructions = st.text_area(
        "Instruções Adicionais",
        help="Adicione quaisquer instruções específicas ou preferências para a criação do conteúdo"
    )

# Botão de ação principal
if st.button("🚀 Gerar Conteúdo", key="main_button"):
    if not all([topic, target_audience, content_goals, platforms]):
        st.warning("⚠️ Por favor, preencha todos os campos obrigatórios antes de executar.")
    else:
        with st.spinner("Criando seu conteúdo... Aguarde, por favor."):
            inputs = {
                "target_audience": target_audience,
                "content_goals": content_goals,
                "platforms": platforms,
                "tone": tone,
                "additional_instructions": additional_instructions
            }
            st.session_state.resultado = run_content_creation(topic=topic, inputs=inputs)

# Lista de nomes das tarefas em ordem
task_names = [
    "Pesquisa de Conteúdo",
    "Criação do Post",
    "Conteúdo Visual",
    "Estratégia de Redes Sociais",
    "Revisão Final"
]

# Exibe o resultado se existir
if st.session_state.resultado:
    if not st.session_state.resultado.success:
        st.error(st.session_state.resultado.error_message)
    else:
        # Exibe os resultados de cada tarefa separadamente
        for i, task_output in enumerate(st.session_state.resultado.tasks_output):
            task_name = task_names[i]
            st.subheader(f"📌 {task_name}")
            
            # Formata o resultado em markdown com borda sólida
            resultado_formatado = f"""
            <div style="font-family: Roboto, sans-serif; font-size: 16px; line-height: 1.6; border: 2px solid #e0e0e0; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            {task_output.raw}
            </div>
            """
            st.markdown(resultado_formatado, unsafe_allow_html=True)
            
            # Adiciona um botão para copiar o conteúdo
            st.code(task_output.raw, language="text", line_numbers=False)
