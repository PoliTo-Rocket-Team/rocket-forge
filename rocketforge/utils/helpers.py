from customtkinter import CTkEntry, CTkTextbox


def updateentry(entry: CTkEntry, value: any, disabled: bool=False) -> None:
    '''
    This function is used to update CTkEntry contents
    '''
    entry.configure(state="normal")
    entry.delete("0", "200")
    if type(value) == str:
        entry.insert("0", value)
    else:
        entry.insert("0", f"{value:.4f}")
    if disabled:
        entry.configure(state="disabled")


def updatetextbox(textbox: CTkTextbox, value: any, disabled: bool=False) -> None:
    '''
    This function is used to update CTkTextbox contents
    '''
    textbox.configure(state="normal")
    textbox.delete("0.0", "200.0")
    textbox.insert("0.0", value)
    if disabled:
        textbox.configure(state="disabled")