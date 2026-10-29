import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA WEB
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CYBER-CALC PRO // Suite Científica",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilo visual Cyberpunk Dark & Bloqueo de traducción automática
st.markdown(
    """
    <meta name="google" content="notranslate">
    <style>
    html, body, div, span, button {
        translate: no !important;
    }
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    div[data-baseweb="tab-list"] { gap: 10px; }
    button[data-baseweb="tab"] {
        background-color: #111827 !important;
        color: #06b6d4 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
    }
    button[aria-selected="true"] {
        background-color: #06b6d4 !important;
        color: #000000 !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f2937;
        color: #06b6d4;
        border: 1px solid #374151;
        border-radius: 6px;
        font-weight: bold;
        font-size: 15px;
        height: 48px;
    }
    .stButton>button:hover {
        background-color: #374151;
        color: #22d3ee;
        border-color: #06b6d4;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ CYBER-CALC PRO // Suite Científica & Analítica")
st.caption("Motor 100% interactivo alimentado por **NumPy**, **Pandas** y **Matplotlib**")

# -----------------------------------------------------------------------------
# ESTADO DE SESIÓN
# -----------------------------------------------------------------------------
if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Expresión", "Resultado"])

if "expr_input" not in st.session_state:
    st.session_state.expr_input = ""

if "memoria_val" not in st.session_state:
    st.session_state.memoria_val = 0.0

# -----------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🧮 CALCULADORA CIENTÍFICA",
    "📈 GRAFICADOR GEOMÉTRICO & 2D",
    "📐 ÁLGEBRA LINEAL & MATRICES",
    "📊 ANÁLISIS ESTADÍSTICO",
])

# =============================================================================
# 1. CALCULADORA CIENTÍFICA (NUMPY)
# =============================================================================
with tab1:
    col_left, col_right = st.columns([2, 1])

    with col_left:
        modo_angulo = st.radio(
            "Modo Angular:",
            ["Radianes (RAD)", "Grados (DEG)"],
            horizontal=True,
        )

        st.text_input(
            "ENTRADA DE EXPRESIÓN:",
            key="expr_input",
            placeholder="np.sin(np.pi/4) + np.sqrt(16)",
        )

        if "ultimo_resultado" in st.session_state:
            st.metric(
                label="RESULTADO CALCULADO:",
                value=st.session_state.ultimo_resultado,
            )

        def add_char(c):
            st.session_state.expr_input += c

        def clear_expr():
            st.session_state.expr_input = ""

        def del_char():
            st.session_state.expr_input = st.session_state.expr_input[:-1]

        def eval_expr():
            try:
                expr = st.session_state.expr_input
                if "DEG" in modo_angulo:
                    expr_proc = (
                        expr.replace("sin(", "sin(np.radians(")
                        .replace("cos(", "cos(np.radians(")
                        .replace("tan(", "tan(np.radians(")
                    )
                else:
                    expr_proc = expr

                contexto = {
                    "np": np,
                    "sin": np.sin,
                    "cos": np.cos,
                    "tan": np.tan,
                    "sqrt": np.sqrt,
                    "log": np.log10,
                    "ln": np.log,
                    "exp": np.exp,
                    "pi": np.pi,
                    "e": np.e,
                }
                res = eval(expr_proc, {"__builtins__": None}, contexto)

                res_str = f"{res:.8g}" if isinstance(res, (float, np.floating)) else str(res)
                st.session_state.ultimo_resultado = res_str

                nuevo = pd.DataFrame([{"Expresión": expr, "Resultado": res_str}])
                st.session_state.historial = pd.concat([st.session_state.historial, nuevo], ignore_index=True)
            except Exception:
                st.session_state.ultimo_resultado = "ERROR // SINTAXIS"

        def mem_clear():
            st.session_state.memoria_val = 0.0

        def mem_add():
            try:
                st.session_state.memoria_val += float(st.session_state.ultimo_resultado)
            except Exception:
                pass

        def mem_read():
            st.session_state.expr_input += str(st.session_state.memoria_val)

        # Panel Memoria
        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        c_m1.button("MC", on_click=mem_clear)
        c_m2.button("MR", on_click=mem_read)
        c_m3.button("M+", on_click=mem_add)
        c_m4.write(f"**Memoria:** `{st.session_state.memoria_val}`")

        # Botones Teclado
        botones = [
            [("sin", "np.sin("), ("cos", "np.cos("), ("tan", "np.tan("), ("log10", "np.log10("), ("ln", "np.log(")],
            [("sqrt", "np.sqrt("), ("exp", "np.exp("), ("π", "np.pi"), ("e", "np.e"), ("^", "**")],
            [("7", "7"), ("8", "8"), ("9", "9"), ("/", "/"), ("DEL", "DEL")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("*", "*"), ("AC", "AC")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("-", "-"), ("(", "(")],
            [("0", "0"), (".", "."), ("=", "="), ("+", "+"), (")", ")")],
        ]

        for fila in botones:
            cols = st.columns(5)
            for i, (txt, val) in enumerate(fila):
                if txt == "=":
                    cols[i].button(txt, on_click=eval_expr, type="primary")
                elif txt == "AC":
                    cols[i].button(txt, on_click=clear_expr)
                elif txt == "DEL":
                    cols[i].button(txt, on_click=del_char)
                else:
                    cols[i].button(txt, on_click=add_char, args=(val,), key=f"btn_{txt}_{i}")

    with col_right:
        st.subheader("📋 Historial (Pandas)")
        st.dataframe(st.session_state.historial, use_container_width=True, height=400)

# =============================================================================
# 2. GRAFICADOR GEOMÉTRICO Y FUNCIONAL (MATPLOTLIB)
# =============================================================================
with tab2:
    st.subheader("📈 Trazador Geométrico y Funcional 2D")

    tipo_grafico = st.selectbox(
        "Seleccione tipo de figura o función:",
        ["Función Libre f(x)", "Circunferencia", "Elipse", "Recta"],
    )

    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor("#0b0f19")
    ax.set_facecolor("#030712")

    if tipo_grafico == "Función Libre f(x)":
        c1, c2, c3 = st.columns([3, 1, 1])
        func_input = c1.text_input("f(x) = np.", value="sin(x) * np.exp(-0.1*x)")
        x_min = c2.number_input("X min", value=-10.0)
        x_max = c3.number_input("X max", value=10.0)

        try:
            x = np.linspace(x_min, x_max, 500)
            contexto = {"x": x, "np": np}
            y = eval(f"np.{func_input}" if not func_input.startswith("np.") else func_input, {"__builtins__": None}, contexto)

            df_plot = pd.DataFrame({"x": x, "y": y})
            ax.plot(df_plot["x"], df_plot["y"], color="#06b6d4", lw=2.5, label=f"f(x) = {func_input}")
            ax.fill_between(df_plot["x"], df_plot["y"], color="#06b6d4", alpha=0.15)
        except Exception as e:
            st.error(f"Error en la expresión: {e}")

    elif tipo_grafico == "Circunferencia":
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("Centro X (h)", value=0.0)
        k = c2.number_input("Centro Y (k)", value=0.0)
        r = c3.number_input("Radio (r)", value=5.0, min_value=0.1)

        theta = np.linspace(0, 2 * np.pi, 400)
        x = h + r * np.cos(theta)
        y = k + r * np.sin(theta)
        df_plot = pd.DataFrame({"x": x, "y": y})

        ax.plot(df_plot["x"], df_plot["y"], color="#ec4899", lw=2.5, label=f"(x-{h})² + (y-{k})² = {r}²")
        ax.plot(h, k, "ro", label=f"Centro ({h},{k})")
        ax.set_aspect("equal", "box")

    elif tipo_grafico == "Elipse":
        c1, c2, c3, c4, c5 = st.columns(5)
        h = c1.number_input("Centro X (h)", value=0.0)
        k = c2.number_input("Centro Y (k)", value=0.0)
        a = c3.number_input("Semieje a", value=6.0, min_value=0.1)
        b = c4.number_input("Semieje b", value=3.0, min_value=0.1)
        ang = c5.number_input("Ángulo (°)", value=0.0)

        theta = np.linspace(0, 2 * np.pi, 400)
        alpha = np.radians(ang)
        x_loc = a * np.cos(theta)
        y_loc = b * np.sin(theta)

        x = h + x_loc * np.cos(alpha) - y_loc * np.sin(alpha)
        y = k + x_loc * np.sin(alpha) + y_loc * np.cos(alpha)
        df_plot = pd.DataFrame({"x": x, "y": y})

        ax.plot(df_plot["x"], df_plot["y"], color="#10b981", lw=2.5, label=f"Elipse (a={a}, b={b})")
        ax.plot(h, k, "go", label=f"Centro ({h},{k})")
        ax.set_aspect("equal", "box")

    elif tipo_grafico == "Recta":
        c1, c2, c3, c4 = st.columns(4)
        m = c1.number_input("Pendiente (m)", value=1.5)
        b_val = c2.number_input("Corte Y (b)", value=-2.0)
        x_min = c3.number_input("X min", value=-10.0)
        x_max = c4.number_input("X max", value=10.0)

        x = np.linspace(x_min, x_max, 400)
        y = m * x + b_val
        df_plot = pd.DataFrame({"x": x, "y": y})

        ax.plot(df_plot["x"], df_plot["y"], color="#3b82f6", lw=2.5, label=f"y = {m}x + {b_val}")

    ax.grid(True, linestyle="--", alpha=0.2, color="#06b6d4")
    ax.axhline(0, color="#475569", lw=1)
    ax.axvline(0, color="#475569", lw=1)
    ax.tick_params(colors="#f3f4f6")
    ax.legend(facecolor="#111827", edgecolor="#06b6d4", labelcolor="white")
    st.pyplot(fig)

# =============================================================================
# 3. ÁLGEBRA LINEAL Y MATRICES (AUTOMÁTICO EN TIEMPO REAL)
# =============================================================================
with tab3:
    st.subheader("📐 Álgebra Lineal & Operaciones Matriciales")

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        raw_matA = st.text_area(
            "Matriz A (Filas separadas por ';' y columnas por ','):",
            value="4, 2, 1; 0, 3, -1; 1, 2, 5",
            height=90,
        )
    with col_m2:
        raw_matB = st.text_area(
            "Matriz / Vector B (Filas separadas por ';' y columnas por ','):",
            value="1, 0, 1; 2, 1, 0; 0, 0, 1",
            height=90,
        )

    try:
        A = np.array([[float(x.strip()) for x in f.split(",")] for f in raw_matA.strip().split(";") if f.strip()])
        B = np.array([[float(x.strip()) for x in f.split(",")] for f in raw_matB.strip().split(";") if f.strip()])

        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**Matriz A Ingresada:**")
            st.dataframe(pd.DataFrame(A), use_container_width=True)
        with col_b:
            st.write("**Matriz B Ingresada:**")
            st.dataframe(pd.DataFrame(B), use_container_width=True)

        st.markdown("---")
        op = st.selectbox(
            "Seleccione Operación Algebraica a Ejecutar:",
            [
                "Inversa de A",
                "Determinante de A",
                "Autovalores / Autovectores de A",
                "Transpuesta de A",
                "Multiplicación (A x B)",
                "Suma (A + B)",
                "Resolver Sistema (Ax = B)",
            ],
        )

        st.subheader(f"Resultado: {op}")
        if op == "Inversa de A":
            inv = np.linalg.inv(A)
            st.dataframe(pd.DataFrame(inv).round(4), use_container_width=True)
        elif op == "Determinante de A":
            det = np.linalg.det(A)
            st.metric("Determinante |A|", f"{det:.6f}")
        elif op == "Autovalores / Autovectores de A":
            val, vec = np.linalg.eig(A)
            c_e1, c_e2 = st.columns(2)
            with c_e1:
                st.write("**Autovalores (Eigenvalues):**")
                st.dataframe(pd.DataFrame({"Autovalor": np.round(val, 4)}), use_container_width=True)
            with c_e2:
                st.write("**Autovectores (Eigenvectors):**")
                st.dataframe(pd.DataFrame(np.round(vec, 4)), use_container_width=True)
        elif op == "Transpuesta de A":
            st.dataframe(pd.DataFrame(A.T), use_container_width=True)
        elif op == "Multiplicación (A x B)":
            res = np.matmul(A, B)
            st.dataframe(pd.DataFrame(res), use_container_width=True)
        elif op == "Suma (A + B)":
            res = A + B
            st.dataframe(pd.DataFrame(res), use_container_width=True)
        elif op == "Resolver Sistema (Ax = B)":
            sol = np.linalg.solve(A, B)
            st.write("**Matriz / Vector Solución x:**")
            st.dataframe(pd.DataFrame(sol).round(4), use_container_width=True)

    except Exception as e:
        st.error(f"Error procesando las matrices: {e}")

# =============================================================================
# 4. ANÁLISIS ESTADÍSTICO Y VISUALIZACIÓN (AUTOMÁTICO EN TIEMPO REAL)
# =============================================================================
with tab4:
    st.subheader("📊 Análisis Estadístico y Visualización de Datos")

    raw_data = st.text_area(
        "Ingrese conjunto de datos numéricos (separados por comas):",
        value="10.5, 12.3, 15.8, 14.1, 19.0, 22.4, 15.8, 17.2, 20.1, 18.5, 25.0, 11.2, 16.4, 19.8, 21.0",
        height=70,
    )

    try:
        datos = [float(x.strip()) for x in raw_data.split(",") if x.strip()]
        if len(datos) > 0:
            s = pd.Series(datos, name="Valores")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Promedio (Media)", f"{s.mean():.2f}")
            c2.metric("Mediana", f"{s.median():.2f}")
            c3.metric("Desviación Estándar", f"{s.std():.2f}")
            c4.metric("Varianza", f"{s.var():.2f}")

            col_tbl, col_plt = st.columns([1, 1.2])

            with col_tbl:
                st.write("**Estadísticas Descriptivas (Pandas):**")
                desc = s.describe().round(4)
                df_desc = pd.DataFrame({"Métrica": desc.index.str.upper(), "Valor": desc.values})

                extras = pd.DataFrame([
                    {"Métrica": "VARIANZA", "Valor": round(s.var(), 4)},
                    {"Métrica": "ASIMETRÍA", "Valor": round(s.skew(), 4)},
                    {"Métrica": "CURTOSIS", "Valor": round(s.kurt(), 4)},
                ])
                df_full = pd.concat([df_desc, extras], ignore_index=True)
                st.dataframe(df_full, use_container_width=True)

            with col_plt:
                st.write("**Distribución Visual (Matplotlib):**")
                fig_st, (ax_hist, ax_box) = plt.subplots(
                    2, 1, figsize=(6, 4.5), gridspec_kw={"height_ratios": [2, 1]}
                )
                fig_st.patch.set_facecolor("#0b0f19")
                ax_hist.set_facecolor("#030712")
                ax_box.set_facecolor("#030712")

                # Histograma
                ax_hist.hist(s, bins=7, color="#06b6d4", edgecolor="#111827", alpha=0.8)
                ax_hist.grid(True, linestyle="--", alpha=0.2, color="#06b6d4")
                ax_hist.tick_params(colors="#f3f4f6")
                ax_hist.set_title("Histograma de Frecuencias", color="#06b6d4", fontsize=10)

                # Boxplot (Diagrama de Caja)
                ax_box.boxplot(
                    s,
                    vert=False,
                    patch_artist=True,
                    boxprops=dict(facecolor="#06b6d4", color="#22d3ee"),
                    whiskerprops=dict(color="#06b6d4"),
                    capprops=dict(color="#06b6d4"),
                    medianprops=dict(color="#ec4899", linewidth=2),
                )
                ax_box.grid(True, linestyle="--", alpha=0.2, color="#06b6d4")
                ax_box.tick_params(colors="#f3f4f6")
                ax_box.set_title("Diagrama de Caja (Boxplot)", color="#06b6d4", fontsize=10)

                plt.tight_layout()
                st.pyplot(fig_st)
        else:
            st.warning("Por favor ingrese al menos un número válido.")
    except Exception as e:
        st.error(f"Error procesando datos numéricos: {e}")