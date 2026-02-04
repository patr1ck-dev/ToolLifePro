import flet as ft
import os
from datetime import datetime
from fpdf import FPDF
import json

class ToolLifePro:
    """Aplicação principal de controle de vida útil de ferramentas"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.configurar_pagina()
        
        # Arquivos de dados
        self.ARQUIVO_DADOS = "ferramental.json"
        self.ARQUIVO_HISTORICO = "historico_trocas.json"
        
        # Carregar dados
        self.dados = self.carregar_dados()
        self.historico = self.carregar_historico()
        
        # Inicializar componentes
        self.criar_componentes()
        self.construir_interface()
    
    def configurar_pagina(self):
        """Configura as propriedades da página"""
        self.page.title = "ToolLife Pro v13.0"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 550
        self.page.window_height = 950
        self.page.scroll = "adaptive"
        self.page.padding = 20
    
    def carregar_dados(self):
        """Carrega dados do arquivo JSON"""
        if os.path.exists(self.ARQUIVO_DADOS):
            try:
                with open(self.ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        
        # Dados padrão
        return {
            "maquinas": ["301", "302", "303", "304", "305", "306", "307"],
            "ferramentas": ["Broca Ø6mm", "Broca Ø8mm", "Macho M6", "Macho M8", 
                           "Inserto CNMG", "Inserto DNMG", "Bedame 12mm", "Fresa Ø16mm"],
            "vida_padrao": {
                "Broca Ø6mm": 1500,
                "Broca Ø8mm": 1200,
                "Macho M6": 800,
                "Macho M8": 600,
                "Inserto CNMG": 2000,
                "Inserto DNMG": 1800,
                "Bedame 12mm": 1000,
                "Fresa Ø16mm": 900
            }
        }
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        try:
            with open(self.ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def carregar_historico(self):
        """Carrega histórico de trocas"""
        if os.path.exists(self.ARQUIVO_HISTORICO):
            try:
                with open(self.ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def salvar_historico(self):
        """Salva histórico de trocas"""
        try:
            with open(self.ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def criar_componentes(self):
        """Cria todos os componentes da interface"""
        
        # === CABEÇALHO ===
        self.txt_operador = ft.TextField(
            label="👤 Seu Nome",
            border_radius=10,
            hint_text="Ex: João Silva"
        )
        
        self.txt_lote = ft.TextField(
            label="📋 Lote ou OP",
            border_radius=10,
            hint_text="Ex: OP-2024-001"
        )
        
        self.sel_maq = ft.Dropdown(
            label="🏭 Máquina",
            options=[ft.dropdown.Option(m) for m in self.dados["maquinas"]],
            border_radius=10
        )
        
        self.sel_fer = ft.Dropdown(
            label="🔧 Ferramenta",
            options=[ft.dropdown.Option(f) for f in self.dados["ferramentas"]],
            border_radius=10
        )
        
        # === ABA 1: CALCULADORA UNIVERSAL ===
        self.in_num1 = ft.TextField(
            label="Primeiro Número",
            border_radius=10,
            keyboard_type="number",
            hint_text="0"
        )
        
        self.sel_operacao = ft.Dropdown(
            label="Operação",
            options=[
                ft.dropdown.Option("➕ Somar (+)"),
                ft.dropdown.Option("➖ Subtrair (-)"),
                ft.dropdown.Option("✖️ Multiplicar (×)"),
                ft.dropdown.Option("➗ Dividir (÷)")
            ],
            value="➕ Somar (+)",
            border_radius=10
        )
        
        self.in_num2 = ft.TextField(
            label="Segundo Número",
            border_radius=10,
            keyboard_type="number",
            hint_text="0"
        )
        
        self.res_calc = ft.Container(
            content=ft.Column([
                ft.Text("RESULTADO", size=16, color="blue200"),
                ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color="blue400")
            ]),
            padding=20,
            border_radius=15,
            bgcolor="blue900"
        )
        
        self.btn_calcular = ft.ElevatedButton(
            "🧮 CALCULAR",
            on_click=self.calcular,
            width=500,
            height=50,
            bgcolor="blue700",
            color="white"
        )
        
        self.btn_limpar_calc = ft.TextButton(
            "Limpar",
            on_click=self.limpar_calculadora
        )
        
        # === ABA 2: REGISTRO DE TROCA ===
        self.in_pecas_feitas = ft.TextField(
            label="Quantas Peças Você Fez com Esta Ferramenta?",
            border_radius=10,
            keyboard_type="number",
            hint_text="Ex: 1250"
        )
        
        self.txt_vida_esperada = ft.TextField(
            label="Vida Esperada (peças)",
            border_radius=10,
            keyboard_type="number",
            hint_text="Preenche sozinho",
            read_only=True,
            bgcolor="grey900"
        )
        
        self.motivo = ft.Dropdown(
            label="Por Que Trocou?",
            options=[
                ft.dropdown.Option("✅ Completou a Vida Útil"),
                ft.dropdown.Option("💥 Ferramenta Quebrou"),
                ft.dropdown.Option("⚠️ Acabamento Ruim"),
                ft.dropdown.Option("🔧 Manutenção Preventiva"),
                ft.dropdown.Option("🔄 Troca de Setup/Produto")
            ],
            value="✅ Completou a Vida Útil",
            border_radius=10
        )
        
        self.txt_obs = ft.TextField(
            label="Observações (opcional)",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=10,
            hint_text="Adicione comentários se quiser..."
        )
        
        self.res_vida = ft.Container(
            content=ft.Column([
                ft.Text("DESEMPENHO DA FERRAMENTA", size=16, color="orange200"),
                ft.Text("0 peças", size=40, weight=ft.FontWeight.BOLD, color="orange400"),
                ft.Text("", size=14, color="orange100")
            ]),
            padding=20,
            border_radius=15,
            bgcolor="orange900",
            visible=False
        )
        
        self.btn_gerar_pdf = ft.ElevatedButton(
            "📄 GERAR RELATÓRIO",
            on_click=self.gerar_relatorio,
            width=500,
            height=50,
            bgcolor="orange700",
            color="white"
        )
        
        self.btn_limpar_troca = ft.TextButton(
            "Limpar",
            on_click=self.limpar_troca
        )
        
        self.status_pdf = ft.Text("", color="green400", weight=ft.FontWeight.BOLD, size=14)
        
        # === ABA 3: HISTÓRICO ===
        self.lista_historico = ft.ListView(
            spacing=10,
            padding=10,
            height=600
        )
        
        self.btn_atualizar_historico = ft.ElevatedButton(
            "🔄 Atualizar",
            on_click=self.atualizar_historico,
            bgcolor="purple700",
            color="white"
        )
        
        # === ABA 4: CONFIGURAÇÃO ===
        self.txt_novo_item = ft.TextField(
            label="Nome do Novo Item",
            border_radius=10,
            hint_text="Digite o nome..."
        )
        
        self.txt_vida_nova_ferramenta = ft.TextField(
            label="Vida Esperada (só para ferramentas)",
            border_radius=10,
            keyboard_type="number",
            hint_text="Ex: 1500"
        )
        
        self.lista_maquinas = ft.ListView(spacing=5, height=200)
        self.lista_ferramentas = ft.ListView(spacing=5, height=200)
        
        self.atualizar_listas_config()
        
        # === NAVEGAÇÃO ===
        self.layout_calc = ft.Column([
            ft.Container(
                content=ft.Text("🧮 Calculadora", 
                               size=20, weight=ft.FontWeight.BOLD, color="blue300"),
                padding=ft.padding.only(bottom=10)
            ),
            self.in_num1,
            self.sel_operacao,
            self.in_num2,
            self.btn_calcular,
            self.res_calc,
            self.btn_limpar_calc
        ], visible=True)
        
        self.layout_troca = ft.Column([
            ft.Container(
                content=ft.Text("🔧 Registro de Troca", 
                               size=20, weight=ft.FontWeight.BOLD, color="orange300"),
                padding=ft.padding.only(bottom=10)
            ),
            self.in_pecas_feitas,
            self.txt_vida_esperada,
            self.motivo,
            self.txt_obs,
            self.btn_gerar_pdf,
            self.res_vida,
            self.status_pdf,
            self.btn_limpar_troca
        ], visible=False)
        
        self.layout_historico = ft.Column([
            ft.Container(
                content=ft.Text("📜 Histórico de Trocas", 
                               size=20, weight=ft.FontWeight.BOLD, color="purple300"),
                padding=ft.padding.only(bottom=10)
            ),
            self.btn_atualizar_historico,
            self.lista_historico
        ], visible=False)
        
        self.layout_config = ft.Column([
            ft.Container(
                content=ft.Text("⚙️ Configurações", 
                               size=20, weight=ft.FontWeight.BOLD, color="green300"),
                padding=ft.padding.only(bottom=10)
            ),
            ft.Text("Adicionar Novo Item:", weight=ft.FontWeight.BOLD, size=16),
            self.txt_novo_item,
            self.txt_vida_nova_ferramenta,
            ft.Row([
                ft.ElevatedButton(
                    "➕ Máquina",
                    on_click=self.adicionar_maquina,
                    bgcolor="green800",
                    color="white",
                    expand=True
                ),
                ft.ElevatedButton(
                    "➕ Ferramenta",
                    on_click=self.adicionar_ferramenta,
                    bgcolor="green800",
                    color="white",
                    expand=True
                )
            ]),
            ft.Divider(height=20),
            ft.Text("Máquinas:", weight=ft.FontWeight.BOLD),
            self.lista_maquinas,
            ft.Text("Ferramentas:", weight=ft.FontWeight.BOLD),
            self.lista_ferramentas
        ], visible=False)
    
    def construir_interface(self):
        """Constrói a interface completa"""
        
        # Cabeçalho
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("ToolLife", size=32, weight=ft.FontWeight.BOLD, color="blue400"),
                    ft.Text("Pro", size=32, color="white")
                ], spacing=5),
                ft.Text("v13.0 - Controle de Ferramentas", 
                       size=12, color="grey")
            ], spacing=0),
            padding=15,
            border_radius=15,
            bgcolor="blue900"
        )
        
        # Campos de cabeçalho
        campos_cabecalho = ft.Column([
            ft.Row([self.txt_operador, self.txt_lote], spacing=10),
            ft.Row([self.sel_maq, self.sel_fer], spacing=10)
        ])
        
        # Botões de navegação
        nav_buttons = ft.Row([
            ft.ElevatedButton(
                "🧮 CALC",
                on_click=self.navegar,
                data="CALC",
                expand=True,
                height=45,
                bgcolor="blue700",
                color="white"
            ),
            ft.ElevatedButton(
                "🔧 TROCA",
                on_click=self.navegar,
                data="TROCA",
                expand=True,
                height=45,
                bgcolor="orange700",
                color="white"
            ),
            ft.ElevatedButton(
                "📜 HISTÓRICO",
                on_click=self.navegar,
                data="HISTORICO",
                expand=True,
                height=45,
                bgcolor="purple700",
                color="white"
            ),
            ft.ElevatedButton(
                "⚙️ CONFIG",
                on_click=self.navegar,
                data="CONFIG",
                expand=True,
                height=45,
                bgcolor="green700",
                color="white"
            )
        ], spacing=5)
        
        # Adicionar tudo à página
        self.page.add(
            header,
            ft.Divider(height=20),
            campos_cabecalho,
            ft.Divider(height=20),
            nav_buttons,
            ft.Divider(height=20),
            self.layout_calc,
            self.layout_troca,
            self.layout_historico,
            self.layout_config
        )
    
    def navegar(self, e):
        """Navega entre as abas"""
        self.layout_calc.visible = (e.control.data == "CALC")
        self.layout_troca.visible = (e.control.data == "TROCA")
        self.layout_historico.visible = (e.control.data == "HISTORICO")
        self.layout_config.visible = (e.control.data == "CONFIG")
        
        # Atualizar vida esperada ao abrir aba de troca
        if e.control.data == "TROCA":
            self.atualizar_vida_esperada()
        
        if e.control.data == "HISTORICO":
            self.atualizar_historico(None)
        
        self.page.update()
    
    def validar_campos_cabecalho(self):
        """Valida se os campos do cabeçalho estão preenchidos"""
        erros = []
        
        if not self.txt_operador.value or not self.txt_operador.value.strip():
            erros.append("Seu Nome")
        if not self.sel_maq.value:
            erros.append("Máquina")
        if not self.sel_fer.value:
            erros.append("Ferramenta")
        
        if erros:
            self.mostrar_alerta("Preencha os Campos", 
                               f"Faltou: {', '.join(erros)}")
            return False
        return True
    
    def calcular(self, e):
        """Calcula usando a operação selecionada"""
        try:
            num1 = float(self.in_num1.value or 0)
            num2 = float(self.in_num2.value or 0)
            operacao = self.sel_operacao.value
            
            resultado = 0
            operacao_texto = ""
            
            if "Somar" in operacao:
                resultado = num1 + num2
                operacao_texto = f"{num1} + {num2}"
            elif "Subtrair" in operacao:
                resultado = num1 - num2
                operacao_texto = f"{num1} - {num2}"
            elif "Multiplicar" in operacao:
                resultado = num1 * num2
                operacao_texto = f"{num1} × {num2}"
            elif "Dividir" in operacao:
                if num2 == 0:
                    self.mostrar_alerta("Erro", "Não pode dividir por zero!")
                    return
                resultado = num1 / num2
                operacao_texto = f"{num1} ÷ {num2}"
            
            # Atualizar display
            self.res_calc.content.controls[0].value = operacao_texto
            self.res_calc.content.controls[1].value = f"{resultado:.2f}"
            self.res_calc.bgcolor = "green900"
            self.page.update()
            
        except ValueError:
            self.mostrar_alerta("Erro", "Digite apenas números!")
    
    def limpar_calculadora(self, e):
        """Limpa os campos da calculadora"""
        self.in_num1.value = ""
        self.in_num2.value = ""
        self.sel_operacao.value = "➕ Somar (+)"
        self.res_calc.content.controls[0].value = "RESULTADO"
        self.res_calc.content.controls[1].value = "0"
        self.res_calc.bgcolor = "blue900"
        self.page.update()
    
    def atualizar_vida_esperada(self):
        """Atualiza a vida esperada quando a ferramenta é selecionada"""
        ferramenta = self.sel_fer.value
        if ferramenta and ferramenta in self.dados["vida_padrao"]:
            self.txt_vida_esperada.value = str(self.dados["vida_padrao"][ferramenta])
        else:
            self.txt_vida_esperada.value = "0"
        self.page.update()
    
    def gerar_relatorio(self, e):
        """Gera o relatório PDF"""
        
        # Atualizar vida esperada primeiro
        self.atualizar_vida_esperada()
        
        # Validar cabeçalho
        if not self.validar_campos_cabecalho():
            return
        
        # Validar campos específicos
        if not self.in_pecas_feitas.value:
            self.mostrar_alerta("Erro", "Preencha quantas peças você fez!")
            return
        
        try:
            pecas_feitas = int(self.in_pecas_feitas.value)
            vida_esperada = int(self.txt_vida_esperada.value or 0)
            
            if pecas_feitas < 0:
                self.mostrar_alerta("Erro", "O número de peças não pode ser negativo!")
                return
            
            # Calcular percentual de uso
            percentual = (pecas_feitas / vida_esperada * 100) if vida_esperada > 0 else 0
            
            # Atualizar display
            self.res_vida.visible = True
            self.res_vida.content.controls[1].value = f"{pecas_feitas:,} peças".replace(",", ".")
            
            status_texto = ""
            if percentual >= 100:
                status_texto = "✅ Vida útil completa"
                self.res_vida.bgcolor = "green900"
            elif percentual >= 80:
                status_texto = f"⚠️ {percentual:.0f}% da vida útil"
                self.res_vida.bgcolor = "orange900"
            else:
                status_texto = f"📊 {percentual:.0f}% da vida útil"
                self.res_vida.bgcolor = "blue900"
            
            self.res_vida.content.controls[2].value = status_texto
            self.page.update()
            
            # Gerar PDF
            agora = datetime.now()
            
            try:
                pdf = FPDF()
                pdf.add_page()
                
                # Cabeçalho do PDF
                pdf.set_font("Arial", 'B', 18)
                pdf.cell(0, 15, "TOOLLIFE PRO - RELATORIO DE TROCA", ln=True, align='C')
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Data: {agora.strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='C')
                pdf.ln(10)
                
                # Dados do relatório
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, "DADOS DA TROCA", ln=True)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(5)
                
                pdf.set_font("Arial", size=11)
                dados = [
                    ("Operador:", self.txt_operador.value),
                    ("Maquina:", self.sel_maq.value),
                    ("Ferramenta:", self.sel_fer.value),
                    ("Lote/OP:", self.txt_lote.value or "N/A"),
                    ("", ""),
                    ("Pecas Produzidas:", f"{pecas_feitas:,} pecas".replace(",", ".")),
                    ("Vida Esperada:", f"{vida_esperada:,} pecas".replace(",", ".")),
                    ("Percentual Utilizado:", f"{percentual:.1f}%"),
                    ("", ""),
                    ("Motivo da Troca:", self.motivo.value.replace("✅ ", "").replace("💥 ", "").replace("⚠️ ", "").replace("🔧 ", "").replace("🔄 ", "")),
                ]
                
                for label, valor in dados:
                    if label:
                        pdf.set_font("Arial", 'B', 11)
                        pdf.cell(70, 7, label, 0)
                        pdf.set_font("Arial", size=11)
                        pdf.cell(0, 7, str(valor), ln=True)
                    else:
                        pdf.ln(3)
                
                # Observações
                if self.txt_obs.value and self.txt_obs.value.strip():
                    pdf.ln(5)
                    pdf.set_font("Arial", 'B', 12)
                    pdf.cell(0, 8, "OBSERVACOES", ln=True)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(5)
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 6, self.txt_obs.value)
                
                # Rodapé
                pdf.ln(10)
                pdf.set_font("Arial", 'I', 9)
                pdf.cell(0, 5, "Relatorio gerado por ToolLife Pro v13.0", ln=True, align='C')
                
                # Salvar PDF
                nome_arquivo = f"Relatorio_Troca_{agora.strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf.output(nome_arquivo)
                
                # Salvar no histórico
                self.historico.insert(0, {
                    "data": agora.strftime('%d/%m/%Y %H:%M'),
                    "operador": self.txt_operador.value,
                    "maquina": self.sel_maq.value,
                    "ferramenta": self.sel_fer.value,
                    "lote": self.txt_lote.value or "N/A",
                    "pecas_feitas": pecas_feitas,
                    "vida_esperada": vida_esperada,
                    "percentual": round(percentual, 1),
                    "motivo": self.motivo.value,
                    "observacoes": self.txt_obs.value or ""
                })
                
                # Manter apenas os últimos 50 registros
                self.historico = self.historico[:50]
                self.salvar_historico()
                
                # Tentar abrir PDF
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(nome_arquivo)
                    elif os.name == 'posix':  # Linux/Mac
                        os.system(f'xdg-open "{nome_arquivo}" 2>/dev/null || open "{nome_arquivo}" 2>/dev/null &')
                except:
                    pass  # Ignora erro se não conseguir abrir
                
                self.status_pdf.value = f"✅ PDF criado: {nome_arquivo}"
                self.mostrar_alerta("Sucesso!", f"Relatório salvo como:\n{nome_arquivo}", "success")
                self.page.update()
                
            except Exception as ex:
                self.mostrar_alerta("Erro ao Criar PDF", f"Detalhes: {str(ex)}")
                print(f"Erro completo: {ex}")
            
        except ValueError:
            self.mostrar_alerta("Erro", "Digite apenas números no campo de peças!")
    
    def limpar_troca(self, e):
        """Limpa os campos de troca"""
        self.in_pecas_feitas.value = ""
        self.txt_obs.value = ""
        self.motivo.value = "✅ Completou a Vida Útil"
        self.res_vida.visible = False
        self.status_pdf.value = ""
        self.page.update()
    
    def atualizar_historico(self, e):
        """Atualiza a lista de histórico"""
        self.lista_historico.controls.clear()
        
        if not self.historico:
            self.lista_historico.controls.append(
                ft.Container(
                    content=ft.Text("Nenhuma troca registrada ainda.", 
                                   color="grey", italic=True),
                    padding=20
                )
            )
        else:
            for registro in self.historico:
                # Determinar cor baseada no percentual
                cor_card = "green900"
                if registro["percentual"] < 80:
                    cor_card = "blue900"
                elif registro["percentual"] < 100:
                    cor_card = "orange900"
                
                card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("🔧", size=20),
                            ft.Text(registro["ferramenta"], 
                                   weight=ft.FontWeight.BOLD, size=16),
                            ft.Text(f"({registro['percentual']}%)", 
                                   color="grey", size=14)
                        ]),
                        ft.Divider(height=10, color="white24"),
                        ft.Row([
                            ft.Column([
                                ft.Text(f"Máquina: {registro['maquina']}", size=12),
                                ft.Text(f"Operador: {registro['operador']}", size=12),
                                ft.Text(f"Data: {registro['data']}", size=12, color="grey"),
                            ], expand=True),
                            ft.Column([
                                ft.Text(f"Feitas: {registro['pecas_feitas']}", size=12),
                                ft.Text(f"Esperadas: {registro['vida_esperada']}", size=12),
                                ft.Text(f"{registro['motivo'][:20]}...", size=11, color="grey"),
                            ], expand=True)
                        ])
                    ]),
                    padding=15,
                    border_radius=10,
                    bgcolor=cor_card,
                    border=ft.border.all(1, "white24")
                )
                
                self.lista_historico.controls.append(card)
        
        self.page.update()
    
    def adicionar_maquina(self, e):
        """Adiciona uma nova máquina"""
        if not self.txt_novo_item.value or not self.txt_novo_item.value.strip():
            self.mostrar_alerta("Erro", "Digite o nome da máquina!")
            return
        
        nome = self.txt_novo_item.value.strip()
        
        if nome in self.dados["maquinas"]:
            self.mostrar_alerta("Erro", "Esta máquina já existe!")
            return
        
        self.dados["maquinas"].append(nome)
        self.dados["maquinas"].sort()
        self.salvar_dados()
        
        # Atualizar dropdown
        self.sel_maq.options = [ft.dropdown.Option(m) for m in self.dados["maquinas"]]
        
        # Atualizar lista
        self.atualizar_listas_config()
        
        self.txt_novo_item.value = ""
        self.page.update()
        
        self.mostrar_alerta("Pronto!", f"Máquina '{nome}' adicionada!", "success")
    
    def adicionar_ferramenta(self, e):
        """Adiciona uma nova ferramenta"""
        if not self.txt_novo_item.value or not self.txt_novo_item.value.strip():
            self.mostrar_alerta("Erro", "Digite o nome da ferramenta!")
            return
        
        if not self.txt_vida_nova_ferramenta.value:
            self.mostrar_alerta("Erro", "Digite a vida esperada!")
            return
        
        nome = self.txt_novo_item.value.strip()
        
        try:
            vida = int(self.txt_vida_nova_ferramenta.value)
            if vida <= 0:
                raise ValueError()
        except:
            self.mostrar_alerta("Erro", "Vida esperada deve ser um número positivo!")
            return
        
        if nome in self.dados["ferramentas"]:
            self.mostrar_alerta("Erro", "Esta ferramenta já existe!")
            return
        
        self.dados["ferramentas"].append(nome)
        self.dados["ferramentas"].sort()
        self.dados["vida_padrao"][nome] = vida
        self.salvar_dados()
        
        # Atualizar dropdown
        self.sel_fer.options = [ft.dropdown.Option(f) for f in self.dados["ferramentas"]]
        
        # Atualizar lista
        self.atualizar_listas_config()
        
        self.txt_novo_item.value = ""
        self.txt_vida_nova_ferramenta.value = ""
        self.page.update()
        
        self.mostrar_alerta("Pronto!", f"Ferramenta '{nome}' adicionada!", "success")
    
    def remover_maquina(self, nome, e):
        """Remove uma máquina"""
        self.dados["maquinas"].remove(nome)
        self.salvar_dados()
        self.sel_maq.options = [ft.dropdown.Option(m) for m in self.dados["maquinas"]]
        self.atualizar_listas_config()
        self.page.update()
    
    def remover_ferramenta(self, nome, e):
        """Remove uma ferramenta"""
        self.dados["ferramentas"].remove(nome)
        if nome in self.dados["vida_padrao"]:
            del self.dados["vida_padrao"][nome]
        self.salvar_dados()
        self.sel_fer.options = [ft.dropdown.Option(f) for f in self.dados["ferramentas"]]
        self.atualizar_listas_config()
        self.page.update()
    
    def atualizar_listas_config(self):
        """Atualiza as listas de máquinas e ferramentas na config"""
        self.lista_maquinas.controls.clear()
        for maq in self.dados["maquinas"]:
            self.lista_maquinas.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(maq, expand=True),
                        ft.TextButton(
                            "🗑️",
                            on_click=lambda e, m=maq: self.remover_maquina(m, e),
                            tooltip="Excluir"
                        )
                    ]),
                    padding=5,
                    border_radius=5,
                    bgcolor="grey900"
                )
            )
        
        self.lista_ferramentas.controls.clear()
        for fer in self.dados["ferramentas"]:
            vida = self.dados["vida_padrao"].get(fer, 0)
            self.lista_ferramentas.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(fer, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Vida: {vida} peças", 
                                   size=11, color="grey")
                        ], expand=True),
                        ft.TextButton(
                            "🗑️",
                            on_click=lambda e, f=fer: self.remover_ferramenta(f, e),
                            tooltip="Excluir"
                        )
                    ]),
                    padding=5,
                    border_radius=5,
                    bgcolor="grey900"
                )
            )
    
    def mostrar_alerta(self, titulo, mensagem, tipo="error"):
        """Mostra um alerta para o usuário"""
        emoji = "⚠️" if tipo == "error" else "✅"
        
        def fechar_dlg(e):
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text(f"{emoji} {titulo}"),
            content=ft.Text(mensagem),
            actions=[
                
                ft.TextButton("OK", on_click=fechar_dlg)
            ]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

def main(page: ft.Page):
    """Função principal"""
    ToolLifePro(page)

if __name__ == "__main__":
    ft.app(target=main)
