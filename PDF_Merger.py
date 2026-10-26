
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

# Colors
BG = "#F3F5FA"
NAVY = "#172554"
PURPLE = "#635BDB"
WHITE = "#FFFFFF"
TEXT = "#202943"
MUTED = "#64748B"

root = tk.Tk()
root.title("PDF Merge Studio")
root.geometry("700x540")
root.minsize(620, 480)
root.configure(bg=BG)

selected_files = []

# Header
header = tk.Frame(root, bg=NAVY, height=105)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header, text="PDF MERGE STUDIO",
    font=("Segoe UI", 21, "bold"),
    bg=NAVY, fg=WHITE
).pack(anchor="w", padx=30, pady=(20, 2))

tk.Label(
    header, text="A simple, secure way to combine PDF files",
    font=("Segoe UI", 10),
    bg=NAVY, fg="#CBD5E1"
).pack(anchor="w", padx=32)

# Main workspace
main = tk.Frame(root, bg=BG, padx=28, pady=22)
main.pack(fill="both", expand=True)

tk.Label(
    main, text="Merge your documents",
    font=("Segoe UI", 17, "bold"),
    bg=BG, fg=TEXT
).pack(anchor="w")

tk.Label(
    main, text="Select multiple PDF files and combine them into one document.",
    font=("Segoe UI", 10),
    bg=BG, fg=MUTED
).pack(anchor="w", pady=(5, 15))

# File card
card = tk.Frame(
    main, bg=WHITE,
    highlightbackground="#DCE2EE",
    highlightthickness=1
)
card.pack(fill="both", expand=True)

top_row = tk.Frame(card, bg=WHITE)
top_row.pack(fill="x", padx=18, pady=14)

file_count = tk.Label(
    top_row, text="Selected files (0)",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE, fg=TEXT
)
file_count.pack(side="left")

file_list = tk.Listbox(
    card,
    font=("Segoe UI", 10),
    bg=WHITE, fg=TEXT,
    selectbackground="#E0E7FF",
    selectforeground=NAVY,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    height=7,
    activestyle="none"
)
file_list.pack(fill="both", expand=True, padx=18, pady=(0, 12))

status = tk.Label(
    main, text="Ready to merge your PDFs",
    font=("Segoe UI", 9),
    bg=BG, fg=MUTED
)
status.pack(anchor="w", pady=(10, 8))


def update_list():
    file_list.delete(0, tk.END)

    for path in selected_files:
        file_list.insert(tk.END, "  📄  " + os.path.basename(path))

    file_count.config(
        text=f"Selected files ({len(selected_files)})"
    )


def add_files():
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF files", "*.pdf")]
    )

    for path in files:
        if path not in selected_files:
            selected_files.append(path)

    update_list()

    if selected_files:
        status.config(text="Files ready to merge", fg=PURPLE)


def clear_files():
    selected_files.clear()
    update_list()
    status.config(text="Selection cleared", fg=MUTED)


def merge_pdfs():
    if len(selected_files) < 2:
        messagebox.showwarning(
            "Select PDFs",
            "Please select at least two PDF files."
        )
        return

    output = filedialog.asksaveasfilename(
        title="Save merged PDF",
        defaultextension=".pdf",
        initialfile="merged.pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not output:
        return

    if os.path.abspath(output) in [
        os.path.abspath(path) for path in selected_files
    ]:
        messagebox.showerror(
            "Invalid destination",
            "Choose a new output file, not one of the source PDFs."
        )
        return

    merger = PdfMerger()

    try:
        for path in selected_files:
            merger.append(path)

        merger.write(output)

        status.config(text="PDFs merged successfully!", fg="#15803D")
        messagebox.showinfo(
            "Success",
            f"Your merged PDF was saved to:\n{output}"
        )

    except Exception as error:
        status.config(text="Unable to merge the PDFs", fg="#DC2626")
        messagebox.showerror("Merge failed", str(error))

    finally:
        merger.close()


# Action buttons
buttons = tk.Frame(main, bg=BG)
buttons.pack(fill="x", pady=(2, 0))

tk.Button(
    buttons, text="+  Add PDF Files",
    command=add_files,
    font=("Segoe UI", 10, "bold"),
    bg=WHITE, fg=PURPLE,
    activebackground="#EDEBFF",
    relief="flat", cursor="hand2",
    padx=14, pady=11
).pack(side="left")

tk.Button(
    buttons, text="Clear",
    command=clear_files,
    font=("Segoe UI", 10),
    bg=BG, fg=MUTED,
    activebackground="#E2E8F0",
    relief="flat", cursor="hand2",
    padx=14, pady=11
).pack(side="left", padx=6)

tk.Button(
    buttons, text="Merge PDFs  →",
    command=merge_pdfs,
    font=("Segoe UI", 10, "bold"),
    bg=PURPLE, fg=WHITE,
    activebackground="#4F46B5",
    activeforeground=WHITE,
    relief="flat", cursor="hand2",
    padx=20, pady=11
).pack(side="right")

root.mainloop()
