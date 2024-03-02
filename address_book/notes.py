from collections import UserDict, defaultdict
from abc import ABC, abstractmethod

class Field(ABC):
    @abstractmethod
    def value_of(self):
        raise NotImplementedError

class Text(Field):
    def __init__(self, text: str) :
        self.text = text
    
    def value_of(self):
        return self.text
    

class Title(Field):
    def __init__(self, title: str) :
        self.title = title
    
    def value_of(self):
        return self.title
    

class Tag(Field):
    def __init__(self, name: str) :
        self.name = name
    
    def value_of(self):
        return self.name


class Item:
    def __init__(self, title: Title, text: Text, tag: Tag = []):
        self.title = title
        self.text = text
        self.tags = [tag] if tag else []

    def add_tag(self, name):
        new_tag = Tag(name)
        if new_tag in self.tags:
            return f'Tag with name {name} already exists!'
        
        self.tags.append(new_tag.value_of())
        return f'Tag with name {name} succesfully created!'
    
    def get_tags(self):
        return [tag for tag in self.tags]

    def __str__(self):
        return f"Note: {self.title} Text: {self.text} Tags: {', '.join(self.get_tags())}"


class Notes(UserDict):

    def add_note(self, title: Title, text: Text, tag: Tag = []):
        new_note = Item(title, text, tag)
        if new_note in self.data.values():
            return f"Note with title {title} already exists!"
        
        idx = len(self.data)+1 if len(self.data) > 0 else 1
        self.data[idx] = new_note
        return f"Note with title {title} was succesfully added!"
    
    def get_notes(self):
        notes = '|{:^30}|{:^50}|{:^30}|\n'.format("Title", "Text", "Tags")
        for value in self.data.values():
            tags = ", ".join(tag for tag in value.tags)
            notes += '|{:^30}|{:^50}|{:^30}|\n'.format(value.title, value.text, tags)
        return notes

    def find_notes(self, text_to_find):
        text_to_find = text_to_find.lower()
        notes_found = Notes()
        for note in self.data.values():
            if note.title.lower().find(text_to_find) != -1\
                or note.text.lower().find(text_to_find) != -1:
                notes_found.add_note(note.title, note.text)
        
        return notes_found
    
    def find_notes_by_tag(self, tag_name: Tag=None):
        result = []
        for value in self.data.values():
            if tag_name in value.tags:
                result.append(str(value))

        return "\n".join(note for note in result)

    def delete_note(self, title_text):
        for id, note in self.data.items():
            if title_text.lower().strip() in note.title.lower():
                del self.data[id]
                return "Removed note"
        return "No note with such title"
    
    def edit_note(self, title_text, new_text):
        for id, note in self.data.items():
            if title_text.lower().strip() in note.title.lower() or title_text.lower().strip() in note.title.lower():
                self.data[id] = Item(note.title, new_text)
                return self.get_notes()
        return "No note with such text"

    def get_note_id(self, note_title):
        note = Item(note_title, None)
        note_index = None
        for key, value in self.data.items():
            if value == note:
                note_index = key
                break
        
        return note_index
    
    def get_tags_by_note(self, notes, note_name):
        for note in notes:
            if note.title == note_name:
                return note.get_tags()
        return []

    def add_tag_for_note(self, tag_name, note_title):
        for value in self.data.values():
            if value.title == note_title:
                value.add_tag(tag_name)
            