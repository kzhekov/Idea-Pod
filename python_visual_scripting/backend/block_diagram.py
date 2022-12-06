from typing import Callable


class Block:
    # Initialize a block with the given function
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
        self.input = None
        self.output = None

    # Set the input for this block
    def set_input(self, block_input):
        self.input = block_input

    # Execute the function with the given input and set the output
    def execute(self):
        self.output = self.func(self.input)


class Link:
    # Initialize a link between the given source and destination blocks
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    # Set the input of the destination block to the output of the source block
    def execute(self):
        self.dest.set_input(self.src.output)


class BlockDiagram:
    # Initialize the diagram with the given list of blocks and links
    def __init__(self, blocks: tuple = (), links: tuple = ()):
        self.blocks = [*blocks]
        self.links = [*links]
        self.selected_block = None

    # Execute the diagram by executing each link in sequence
    def execute(self):
        for link in self.links:
            link.execute()

        # Execute each block after all the links have been executed
        for block in self.blocks:
            block.execute()

    def add_block(self, name: str, function: Callable):
        # Create a new block with a default function
        block = Block(name, function)

        # Add the block to the diagram
        self.blocks.append(block)

        # Select the new block
        self.select_block(block)

    # Remove the selected block from the diagram
    def remove_block(self, block_to_remove: Block):
        if block_to_remove in self.blocks:
            # Remove the block from the diagram
            self.blocks.remove(block_to_remove)

            # Clear the selection
            self.select_block(None)

    # Select the given block
    def select_block(self, block_to_select: Block | None):
        self.selected_block = block_to_select
