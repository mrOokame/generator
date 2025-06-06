class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""

        result = ""
        for k, v in self.props.items():
            result += f" {k}=\"{v}\""

        return result
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"  

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("All children must be instances of HTMLNode")
            
            if isinstance(child, LeafNode) and child.value is None:
                raise ValueError("All children of parent nodes must have a value")
            

        html = f"<{self.tag}{self.props_to_html()}>"  

        for children in self.children:
            html += children.to_html()

        return f"{html}</{self.tag}>"

