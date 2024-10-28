from server import Server

app=Server()
app.host="127.0.0.1"
app.port=8080
app.template_dir="templates"
app.template_dic={
    "index":"index.html",
    "about":"about.html",
    "contact":"contact.html",
}
app.error_page="404.html"
app.static_dir="static"

app.startServer()