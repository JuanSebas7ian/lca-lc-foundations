from langchain.agents import create_agent
from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="us.meta.llama4-maverick-17b-instruct-v1:0",  # Nota el prefijo "us."
    region_name="us-east-1",
    model_kwargs={
        "temperature": 0.5,
        "max_tokens": 2048,
        "top_p": 0.9,
    }
)

from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents import AgentState, create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_model_call, dynamic_prompt, HumanInTheLoopMiddleware
from langchain.agents.middleware import ModelRequest, ModelResponse
from typing import Callable

load_dotenv()


@dataclass
class EmailContext:
    """
    Define el contexto estático del agente. 
    Contiene información que no cambia durante la ejecución pero que el 
    agente necesita consultar (como credenciales de una base de datos simulada).
    """
    email_address: str = "julie@example.com"
    password: str = "password123"


class AuthenticatedState(AgentState):
    """
    Define el esquema de memoria persistente del agente.
    Al heredar de AgentState, mantiene el historial de mensajes y añade
    la variable 'authenticated' para rastrear si el usuario ha iniciado sesión.
    """
    authenticated: bool


@tool
def check_inbox() -> str:
    """
    Herramienta para consultar los correos pendientes.
    Solo será accesible para el agente si el estado 'authenticated' es True.
    """
    return """
    Hi Julie, 
    I'm going to be in town next week and was wondering if we could grab a coffee?
    - best, Jane (jane@example.com)
    """


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    Herramienta para enviar correos electrónicos.
    Está configurada con un interruptor de 'Human in the Loop', lo que significa
    que el sistema pausará la ejecución para pedir aprobación humana antes de enviar.
    """
    return f"Email sent to {to} with subject {subject} and body {body}"


@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
    """
    Realiza la validación de credenciales comparando los datos del usuario con EmailContext.
    
    Argumentos:
        email: Correo proporcionado por el usuario.
        password: Clave proporcionada por el usuario.
        runtime: Objeto que permite acceder al contexto y modificar el estado del agente.
        
    Retorna:
        Un objeto Command que actualiza la variable 'authenticated' en el mapa de estado.
    """
    if email == runtime.context.email_address and password == runtime.context.password:
        return Command(
            update={
                "authenticated": True,
                "messages": [
                    ToolMessage("Successfully authenticated", tool_call_id=runtime.tool_call_id)
                ],
            }
        )
    else:
        return Command(
            update={
                "authenticated": False,
                "messages": [
                    ToolMessage("Authentication failed", tool_call_id=runtime.tool_call_id)
                ],
            }
        )


@wrap_model_call
async def dynamic_tool_call(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """
    MIDDLEWARE DE HERRAMIENTAS DINÁMICAS: 
    Este método intercepta la llamada al modelo antes de que ocurra. 
    Revisa si el usuario está autenticado en el 'state'. 
    - Si SI: Le da acceso a las herramientas de email.
    - Si NO: Solo le permite usar la herramienta de autenticación.
    """

    authenticated = request.state.get("authenticated", False)

    if authenticated:
        tools = [check_inbox, send_email]
    else:
        tools = [authenticate]

    request = request.override(tools=tools)
    return await handler(request)


authenticated_prompt = "You are a helpful assistant that can check the inbox and send emails."
unauthenticated_prompt = "You are a helpful assistant that can authenticate users."


@dynamic_prompt
def dynamic_prompt_func(request: ModelRequest) -> str:
    """
    MIDDLEWARE DE PROMPT DINÁMICO:
    Cambia las instrucciones del sistema (System Prompt) dependiendo del estado.
    Esto asegura que el agente sepa qué rol tomar (Seguridad vs Asistente de Email).
    """
    authenticated = request.state.get("authenticated", False)

    if authenticated:
        return authenticated_prompt
    else:
        return unauthenticated_prompt


# CREACIÓN DEL AGENTE:
# Aquí se orquestan todos los componentes: 
# El LLM, las herramientas, el esquema de estado, el contexto y los middlewares.
agent = create_agent(
        llm,
        tools=[authenticate, check_inbox, send_email],
        state_schema=AuthenticatedState,
        context_schema=EmailContext,
        middleware=[
            dynamic_tool_call,
            dynamic_prompt_func,
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "authenticate": False,
                    "check_inbox": False,
                    "send_email": True, # Pausa para aprobación humana en esta herramienta
                }
            ),
        ],
    )
