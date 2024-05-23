class HTMLNode:

    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __repr__(self) -> str:
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"


class LeafNode(HTMLNode):

    def __init__(
            self, tag: str = None, value: str = None, props: dict = None
    ) -> None:

        if value is None:
            raise ValueError("Value parameter cannot be None")

        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.tag is None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):

    def __init__(
        self, tag: str = None, children: list = None, props: dict = None
    ) -> None:

        if tag is None:
            raise ValueError("Tag cannot be None")

        if children is None or len(children) == 0:
            raise ValueError("Children cannot be None")

        super().__init__(tag, None, children, props)

    def to_html(self):

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
