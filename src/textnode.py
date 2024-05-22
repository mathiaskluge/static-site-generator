class TextNode:

    def __init__(self, text: str, text_type: str, url: str) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self) -> bool:
        return self.text == self.text_type == self.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"