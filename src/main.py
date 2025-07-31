from core.database import DataManager
from core.conn import ConnectionServer
from core.selectors import SelectorsManager
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, TabbedContent, TabPane, Button, Tree, Input
from textual.containers import Container
from pathlib import Path

sl = SelectorsManager()
cn = ConnectionServer()
db = DataManager()

class FeedsTree(Tree):

    def __init__(self, label, data, **kwargs):
        super().__init__(label, **kwargs)
        self.data = data

    def on_mount(self) -> None:
        if isinstance(self.data, list):
            for feed in self.data:
                self.root.add_leaf(feed["nome"])
        elif isinstance(self.data, dict):
            self.root.add_leaf(self.data["nome"])
        self.root.expand()

    @on(Tree.NodeHighlighted)
    def on_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        if event.node.label != "feeds":
            self.log(f"******feed******: {event.node.label}")

class MyApp(App):
    TITLE = "Veritas Scrapping"
    CSS_PATH = Path(__file__).parent / "ui" / "principal.css"
    BINDINGS = [
        ("s", "sair()", "Sair Do Aplicativo.")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

        with TabbedContent():
            with TabPane("Main", id="principal"):
                yield Container(
                    Label("Painel Veritas Scrapping", id="label_main"),
                    Button("Acessar Painel", id="btn_access"),
                    id="centred"
                )
                yield Container(
                    Label("Carregando...", id="loading_label"),
                    id="loading_screen", classes="hidden"
                )
                yield Container(id="feed_panel", classes="hidden")
            
            with TabPane("Logs", id="logs"):
                yield Label("Em breve.", id="label_breve")
    
    def action_sair(self):
        self.exit()

    @on(Button.Pressed, "#btn_access")
    def acessar_painel(self):
        self.query_one("#centred").add_class("hidden")
        self.query_one("#loading_screen").remove_class("hidden")
        
        feeds = db.get_feeds()

        self.query_one("#loading_screen").add_class("hidden")
        
        if feeds is not None:
            self.query_one("#feed_panel").remove_class("hidden")
            
            fp = self.query_one("#feed_panel")
            fp.mount(
                Label("[green]Database Conectada:[/] [yellow] [/]", id="connected_label"),
                FeedsTree("feeds", feeds)
            )
        else:
            cc = self.query_one("#centred")
            cc.remove_class("hidden")
            label = self.query_one("#label_main")
            label.update("[red]Nenhum Feed Cadastrado.[/]")
            cc.mount(
                self.query_one("#btn_access")
            )

MyApp().run()