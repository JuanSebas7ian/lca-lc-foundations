
import json
import os

def document_notebook_with_diagram():
    # Usamos el archivo fuente original para leer los datos limpios
    source_path = "/home/juansebas7ian/lca-lc-foundations/notebooks/module-3/3.5_email_agent.ipynb"
    # Y escribimos en el nuevo archivo documentado
    output_path = "/home/juansebas7ian/lca-lc-foundations/notebooks/module-3/3.5_email_agent_documented.ipynb"
    
    if not os.path.exists(source_path):
        print(f"Error: No se encontró el archivo fuente en {source_path}")
        return

    with open(source_path, 'r', encoding='utf-8') as f:
        nb_data = json.load(f)

    # Definición del Diagrama (Versión Código Python para garantizar renderizado)
    # Usamos mermaid.ink para generar la imagen dinámicamente
    mermaid_code_source = [
        "# Visualización: Flujo y Patrón de Diseño\n",
        "import base64\n",
        "import textwrap\n",
        "from IPython.display import Image, display\n",
        "\n",
        "def render_mermaid(graph_code):\n",
        "    \"\"\"Helper to render ASCII mermaid graphs\"\"\"\n",
        "    graphbytes = graph_code.encode(\"utf8\")\n",
        "    base64_bytes = base64.urlsafe_b64encode(graphbytes)\n",
        "    base64_string = base64_bytes.decode(\"ascii\")\n",
        "    url = \"https://mermaid.ink/img/\" + base64_string\n",
        "    display(Image(url=url))\n",
        "\n",
        "def visualize_flow():\n",
        "    print('--- 1. Flujo de Ejecución (Logic Flow) ---')\n",
        "    # Diagrama de decisión lógica\n",
        "    graph = textwrap.dedent(\"\"\"\n",
        "    graph TD\n",
        "        A[Start: Message] --> B{Authenticated?}\n",
        "        B -- No --> C(Role: Security)\n",
        "        C --> D[Only Tool: authenticate]\n",
        "        D --> E{Credentials OK?}\n",
        "        E -- Yes --> F[State: Authenticated]\n",
        "        E -- No --> G[Error]\n",
        "        B -- Yes --> H(Role: Assistant)\n",
        "        H --> I[Tools: inbox, send_email]\n",
        "        I --> J{Send Email?}\n",
        "        J -- Yes --> K[PAUSE: Human-in-the-Loop]\n",
        "        K --> L[Wait Approval]\n",
        "        L --> M[Execute]\n",
        "        J -- No --> M\n",
        "    \"\"\")\n",
        "    render_mermaid(graph)\n",
        "\n",
        "def visualize_pattern():\n",
        "    print('\\n--- 2. Patrón de Diseño de Arquitectura (Agent Pattern) ---')\n",
        "    # Diagrama de componentes y capas\n",
        "    graph = textwrap.dedent(\"\"\"\n",
        "    graph TD\n",
        "        subgraph State_Memory\n",
        "            ST[State: Authenticated]\n",
        "        end\n",
        "\n",
        "        subgraph Middleware_Layer\n",
        "            DP[Dynamic Prompt]\n",
        "            DT[Tool Filter]\n",
        "        end\n",
        "\n",
        "        subgraph Agent_Core\n",
        "            LLM[LLM Brain]\n",
        "        end\n",
        "\n",
        "        subgraph Tools\n",
        "            T1[Auth Tool]\n",
        "            T2[Inbox Tool]\n",
        "            HITL{Human Check}\n",
        "            T3[Send Email]\n",
        "        end\n",
        "\n",
        "        User((User)) --> DP\n",
        "        User --> DT\n",
        "        \n",
        "        ST -.->|Read Status| DP\n",
        "        ST -.->|Read Status| DT\n",
        "        \n",
        "        DP -->|Context| LLM\n",
        "        DT -->|Allowed Tools| LLM\n",
        "        \n",
        "        LLM -->|Call| T1\n",
        "        T1 -->|Update| ST\n",
        "        \n",
        "        LLM -->|Call| T2\n",
        "        LLM -->|Call| HITL\n",
        "        HITL -.->|Approve| T3\n",
        "    \"\"\")\n",
        "    render_mermaid(graph)\n",
        "\n",
        "visualize_flow()\n",
        "visualize_pattern()"
    ]

    mermaid_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": mermaid_code_source
    }

    # Reutilizamos las explicaciones profundas, pero las acortamos un poco para el script
    # (Para no hacer este script de Python demasiado largo en la respuesta, asumo las mismas explicaciones)
    deep_explanations = [
        # 1. Configuración
        """# 1. Configuración del Entorno y Librerías

### 🛠️ Desglose de Funciones
- **`load_dotenv()`**:
  - **Propósito**: Lee el archivo `.env` del directorio raíz y carga las variables (como `AWS_ACCESS_KEY_ID`) en `os.environ`.
  - **Por qué usarla**: Evita escribir credenciales en el código fuente (hardcoding), lo cual es una grave falla de seguridad.
""",

        # 2. Contexto
        """# 2. Definición del Contexto Estático (`EmailContext`)

### 🔍 Análisis de Decoradores
- **`@dataclass`**: 
  - Proveniente de la librería estándar `dataclasses`.
  - **Qué hace**: Genera automáticamente métodos especiales como `__init__()` (constructor), `__repr__()` (representación en texto) y `__eq__()` (comparación).
  - **Beneficio**: Nos ahorra escribir un constructor manual `def __init__(self, email, password): ...`.

### 🛠️ Desglose de Clases
- **`EmailContext`**:
  - Actúa como un contenedor inmutable de configuración.
  - Se inyectará en el agente para que las herramientas puedan validar credenciales sin acceder a variables globales.
""",

        # 3. Estado
        """# 3. Diseño del Estado Persistente (`AuthenticatedState`)

### 🧩 Concepto: AgentState
En LangGraph/LangChain, el estado es un `TypedDict` o clase que define **qué datos sobreviven** entre interacciones.

### 🛠️ Desglose de Clases
- **`AuthenticatedState(AgentState)`**:
  - **Herencia**: Al heredar de `AgentState`, obtienes gratis el campo `messages` (historial de chat).
  - **Campo `authenticated: bool`**:
    - Variable personalizada. 
    - Actúa como "bandera de sesión". Si es `True`, el usuario tiene permiso de administrador.
""",

        # 4. Tools
        """# 4. Definición de Herramientas (Tools)

### 🔍 Análisis de Decoradores
- **`@tool`**:
  - Convierte una función Python normal en una "Herramienta LangChain".
  - **Magia interna**: Lee el *type hinting* (ej: `to: str`) y el *docstring* para generar automáticamente un esquema JSON que el LLM puede entender.

### 🛠️ Desglose de Funciones
1. **`check_inbox` / `send_email`**:
   - Funciones simples que retornan strings. El LLM las usa para "leer" y "actuar".

2. **`authenticate(email, password, runtime)`**:
   - **Parámetro Especial `runtime`**: 
     - Tipo: `ToolRuntime`.
     - Permite acceder a recursos del sistema (`runtime.context`) y metadatos (`runtime.tool_call_id`).
   - **Retorno `Command`**:
     - No devuelve texto simple. Devuelve una **instrucción de control**.
     - `update={"authenticated": True}`: Modifica directamente la memoria del agente.
""",

        # 5. Middleware Tools
        """# 5. Middleware: `dynamic_tool_call`

### 🔍 Análisis de Decoradores
- **`@wrap_model_call`**:
  - Convierte la función en un interceptor.
  - Permite ejecutar código **antes** y **después** de que el LLM genere texto.

### 🛠️ Desglose de Funciones
- **`dynamic_tool_call(request, handler)`**:
  - **`request`**: Contiene el estado actual (`request.state`), los mensajes y las herramientas disponibles.
  - **`handler`**: La función que llama al siguiente paso (el LLM real).
  - **Lógica Crítica**:
    ```python
    tools = [check_inbox...] if authenticated else [authenticate]
    request.override(tools=tools)
    ```
    Esto **borra** físicamente las herramientas sensibles de la petición si el usuario no es admin. Es la capa de seguridad más fuerte.

### 🧠 Deep Dive: ¿Por qué `handler: Callable[[ModelRequest], ModelResponse]`?

Esta firma de tipo es el núcleo del patrón **Middleware (Interceptor)**.

- **`Callable`**: Indica que `handler` es una función ejecutable.
- **`[ModelRequest]`**: Recibe como entrada la "petición" actual (que incluye el historial de mensajes, las herramientas disponibles y el estado).
- **`ModelResponse`**: Promete devolver la respuesta generada por el LLM.

**¿Por qué es necesario?**
El middleware se sitúa *en medio* del agente y el modelo (LLM).
1.  **Intercepta**: Recibe el `request` original.
2.  **Modifica**: En este caso, filtra la lista de `tools` disponibles según la seguridad.
3.  **Delega**: Llama a `handler(request)` para pasarle la pelota al verdadero LLM (o al siguiente middleware de la cadena).
4.  **Retorna**: Devuelve la respuesta del modelo hacia atrás.

Sin llamar a `handler`, el agente se quedaría mudo; nunca llegaría a invocar al modelo.
""",

        # 6. Middleware Prompt
        """# 6. Middleware: Prompt Dinámico

### 🔍 Análisis de Decoradores
- **`@dynamic_prompt`**:
  - Indica que esta función generará el *System Message* (instrucción principal) dinámicamente en cada turno.

### 🛠️ Desglose de Funciones
- **`get_custom_prompt(request)`**:
  - Lee `request.state.get("authenticated")`.
  - Retorna un string diferente según el estado.
  - **Efecto Psicológico en el LLM**: Cambia la "personalidad" del modelo de "Portero de Seguridad" a "Asistente Servicial".
""",

        # 7. LLM
        """# 7. Configuración del Modelo (LLM)

### ⚙️ Parámetros
- **`model_id`**: Identificador del modelo en AWS Bedrock (ej. Nova Lite, Llama 3).
- **`temperature=0.5`**: Balance entre creatividad y precisión. Para uso de herramientas, valores bajos (0-0.5) suelen ser mejores para evitar alucinaciones en los argumentos JSON.
""",

        # 8. Agente
        """# 8. Ensamblaje Final con `create_agent`

### 🛠️ Desglose de Argumentos del Agente

Esta función orquesta todos los componentes definidos anteriormente:

1.  **`llm`**:
    - El objeto `ChatBedrock` ya configurado. Es el "motor de inferencia".

2.  **`tools=[authenticate, check_inbox, send_email]`**:
    - Lista maestra de capacidades.
    - *Nota*: Aunque las listamos todas aquí, el middleware `dynamic_tool_call` las filtrará en tiempo de ejecución según la seguridad.

3.  **`state_schema=AuthenticatedState`**:
    - Define la "memoria" del grafo. Asegura que el campo `authenticated` exista y se persista entre mensajes.

4.  **`context_schema=EmailContext`**:
    - Define los datos estáticos (read-only) que se inyectarán en las herramientas mediante `runtime.context`.

5.  **`middleware=[...]`**:
    - La tubería de procesamiento. El orden es vital:
        1. **`dynamic_tool_call`**: Filtra herramientas (Seguridad).
        2. **`dynamic_prompt`**: Ajusta la personalidad (Adaptabilidad).
        3. **`HumanInTheLoopMiddleware`**:
            - **`interrupt_on={"send_email": True}`**:
            - Intercepta específicamente la herramienta de envío.
            - **Efecto**: El agente generará el JSON para enviar el correo, pero el sistema PAUSARÁ la ejecución antes de enviarlo realmente, esperando confirmación.
""",

        # 9. Ejecución
        """# 9. Ejecución: Prueba de Seguridad (Acceso Denegado)

### 🛠️ Desglose del Código de Ejecución
Esta celda es donde "encendemos" el motor.

1.  **`HumanMessage(content="draft 1")`**:
    - Empaquetamos el texto del usuario en un objeto mensaje estándar de LangChain.
    - "draft 1" es una solicitud ambigua intencional para ver cómo reacciona el agente sin contexto.

2.  **`config={"configurable": {"thread_id": "1"}}`**:
    - **CRÍTICO**: LangGraph usa este `thread_id` para persistir la memoria (`checkpoint`).
    - Todo lo que pase en este `thread_id="1"` se guardará. Si luego llamamos de nuevo con el mismo ID, el agente recordará lo anterior.

3.  **`context=EmailContext()`**:
    - Aquí ocurre la **Inyección de Dependencias**.
    - Pasamos la base de datos de usuarios (simulada) al `ToolRuntime`. Las herramientas (`authenticate`) accederán a esto para validar la contraseña.

4.  **`agent.invoke(...)`**:
    - Ejecuta el grafo paso a paso hasta que termina o se detiene.
    - Como **NO** estamos autenticados (`authenticated=False` por defecto en el estado inicial), el middleware ocultará las herramientas de email.
    - El LLM, al verse restringido, debería responder que necesita autenticación.
""",

        # 10. Inspección
        """# 10. Inspección de Interrupciones

Aquí accedemos al interior del objeto `response`.
- **`response['__interrupt__']`**: Contiene los detalles de la acción pausada.
- Podemos leer qué argumentos (`to`, `subject`, `body`) intentó usar el modelo para enviarlos a revisión humana.
""",

        # 11. Resume
        """# 11. Aprobar y Reanudar (`Command`)

### 🛠️ Desglose de Funciones
- **`Command(resume=...)`**:
  - Es el mecanismo para reanudar un grafo pausado.
  - `resume={"decisions": ...}`: Pasamos datos de vuelta al nodo que se pausó. En este caso, confirmamos que la acción puede proceder.
""",

        # 12. Debug
        """# 12. Depuración Final

Usamos `print` o `pprint` para ver la respuesta cruda y verificar que el flujo de mensajes (`AIMessage`, `ToolMessage`) es correcto y que el estado final es `authenticated: True`.
"""
    ]

    new_cells = []

    # 1. Título
    new_cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# 📘 Documentación Maestra: Agente de Email Dinámico\n", "Tutorial completo sobre arquitectura de agentes seguros."]
    })

    # 2. DIAGRAMA MERMAID (Insertado aquí)
    new_cells.append(mermaid_cell)

    exp_idx = 0
    code_cells = [c for c in nb_data.get('cells', []) if c['cell_type'] == 'code']
    
    for i, cell in enumerate(code_cells):
        if exp_idx < len(deep_explanations):
            markdown_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [deep_explanations[exp_idx] + "\n"]
            }
            new_cells.append(markdown_cell)
            exp_idx += 1
        new_cells.append(cell)

    # Completar si sobran explicaciones
    while exp_idx < len(deep_explanations):
        new_cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [deep_explanations[exp_idx] + "\n"]
        })
        exp_idx += 1

    nb_data['cells'] = new_cells

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb_data, f, indent=1, ensure_ascii=False)
    
    print(f"Éxito: Diagrama Mermaid agregado en {output_path}")

if __name__ == "__main__":
    document_notebook_with_diagram()
