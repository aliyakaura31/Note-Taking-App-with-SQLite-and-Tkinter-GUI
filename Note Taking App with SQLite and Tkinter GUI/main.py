import tkinter as tk
import sqlite3

def createNote():
    title = titleEntry.get()
    content = contentText.get("1.0", "end-1c")
    tags = tagsEntry.get()

    cursor.execute("INSERT INTO notes (title, content, tags) VALUES (?, ?, ?)", (title, content, tags))
    conn.commit()
    clearEntries()
    readNotes()

def readNotes(event=None):
    noteList.delete(0, tk.END)

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    noteList.bind("<<ListboxSelect>>", displaySelectedNote)

    for note in notes:
        noteList.insert(tk.END, note[0])


def displaySelectedNote(event=None):
    selectedIndex = noteList.curselection()
    if selectedIndex:
        noteId = noteList.get(selectedIndex)
        cursor.execute("SELECT * FROM notes WHERE id=?", (noteId,))
        note = cursor.fetchone()

        if note is not None:
            titleEntry.delete(0, tk.END)
            titleEntry.insert(tk.END, note[1])

            contentText.delete("1.0", tk.END)
            contentText.insert(tk.END, note[2])

            tagsEntry.delete(0, tk.END)
            tagsEntry.insert(tk.END, note[3])
        else:
            clearEntries()

def updateNote():
    selectedIndex = noteList.curselection()
    if selectedIndex:
        noteId = noteList.get(selectedIndex)  # Retrieve the ID directly
        title = titleEntry.get()
        content = contentText.get("1.0", "end-1c")
        tags = tagsEntry.get()

        cursor.execute("UPDATE notes SET title=?, content=?, tags=? WHERE id=?", (title, content, tags, noteId))
        conn.commit()
        clearEntries()
        readNotes()

def deleteNote():
    selectedIndex = noteList.curselection()
    if selectedIndex:
        noteId = noteList.get(selectedIndex)
        cursor.execute("DELETE FROM notes WHERE id=?", (noteId,))
        conn.commit()
        clearEntries()
        readNotes()

def clearEntries():
    titleEntry.delete(0, tk.END)
    contentText.delete("1.0", tk.END)
    tagsEntry.delete(0, tk.END)

def clearNoteList():
    noteList.delete(0, tk.END)
    readNotes()

def searchNotes():
    clearNoteList()

    keyword = searchEntry.get()
    cursor.execute("SELECT * FROM notes WHERE id LIKE ? OR content LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%'))
    notes = cursor.fetchall()

    for note in notes:
        noteList.insert(tk.END, note[1])

root = tk.Tk()
root.title("Note Taking App")

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        tags TEXT
    )
""")
conn.commit()

titleLabel = tk.Label(root, text="Title:")
titleLabel.pack()

titleEntry = tk.Entry(root)
titleEntry.pack()

contentLabel = tk.Label(root, text="Content:")
contentLabel.pack()

contentText = tk.Text(root, height=10)
contentText.pack()

tagsLabel = tk.Label(root, text="Tags:")
tagsLabel.pack()

tagsEntry = tk.Entry(root)
tagsEntry.pack()

createButton = tk.Button(root, text="Create", command=createNote)
createButton.pack()

readButton = tk.Button(root, text="Read", command=readNotes)
readButton.pack()

updateButton = tk.Button(root, text="Update", command=updateNote)
updateButton.pack()

deleteButton = tk.Button(root, text="Delete", command=deleteNote)
deleteButton.pack()

searchLabel = tk.Label(root, text="Search:")
searchLabel.pack()

searchEntry = tk.Entry(root)
searchEntry.pack()

searchButton = tk.Button(root, text="Search", command=searchNotes)
searchButton.pack()

noteList = tk.Listbox(root, width=50)
noteList.pack()

# noteList.bind("<<ListboxSelect>>", displaySelectedNote)
# readNotes()

root.mainloop()
