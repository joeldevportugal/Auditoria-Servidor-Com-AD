import tkinter as tk
from tkinter import messagebox
import pyad.adquery
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def auditar_servidor():
    servidor = entry_servidor.get()
    pasta_auditoria = entry_pasta.get()

    if not servidor or not pasta_auditoria:
        messagebox.showerror("Erro", "Por favor, preencha o nome do servidor e o caminho da pasta de auditoria.")
        return

    if not os.path.exists(pasta_auditoria):
        messagebox.showerror("Erro", "O caminho da pasta de auditoria não é válido.")
        return

    adquery = pyad.adquery.ADQuery()
    adquery.execute_query(
        attributes=["uSNCreated", "uSNChanged", "whenCreated", "whenChanged", "description", "lastLogon", "lastLogoff", "userAccountControl", "objectSid", "sAMAccountName", "sn", "givenName", "distinguishedName", "memberOf"],
        where_clause="objectClass = 'user'",
        base_dn="DC=" + servidor + ",DC=com"
    )

    pdf_path = os.path.join(pasta_auditoria, "auditoria.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    for row in adquery.get_results():
        data = [
            ["Usuário:", row["sAMAccountName"]],
            ["Nome completo:", row["givenName"] + " " + row["sn"]],
            ["DN:", row["distinguishedName"]],
            ["Membro de:", row["memberOf"]],
        ]

        table = Table(data, colWidths=[100, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        elements.append(table)
        elements.append(Paragraph("\n", styles['Normal']))

    doc.build(elements)
    messagebox.showinfo("Concluído", f"Auditoria concluída com sucesso. Verifique o arquivo {pdf_path} na pasta especificada.")

# Interface
Janela = tk.Tk()
Janela.title("Auditoria de Servidor Active Directory")
Janela.geometry('400x100+100+100')
Janela.resizable(0,0)

frame = tk.Frame(Janela)
frame.pack(padx=10, pady=10)

label_servidor = tk.Label(frame, text="Servidor Active Directory:")
label_servidor.grid(row=0, column=0, sticky="e")

entry_servidor = tk.Entry(frame)
entry_servidor.grid(row=0, column=1)

label_pasta = tk.Label(frame, text="Caminho da Pasta de Auditoria:")
label_pasta.grid(row=1, column=0, sticky="e")

entry_pasta = tk.Entry(frame)
entry_pasta.grid(row=1, column=1)

button_auditar = tk.Button(frame, text="Auditar", command=auditar_servidor)
button_auditar.grid(row=2, columnspan=2, pady=10)

Janela.mainloop()
