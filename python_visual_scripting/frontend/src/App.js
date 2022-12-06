import React, {useState} from "react";
import Diagram, { createSchema, useSchema } from 'beautiful-react-diagrams';
import axios from "axios";
import Modal from "react-modal";

function App() {
    const [blocks, setBlocks] = useState([]);
    const [diagramState, setDiagramState] = useState(new DiagramState());
    const [showModal, setShowModal] = useState(false);
    const [blockName, setBlockName] = useState("");
    const [blockFunc, setBlockFunc] = useState("");

    // Fetch the current blocks from the API
    const fetchBlocks = async () => {
        try {
            const response = await axios.get("/blocks");
            setBlocks(response.data);
        } catch (error) {
            console.error(error);
        }
    }

    // Add a new block to the diagram
    const addBlock = async (name, func) => {
        try {
            await axios.post("/add_block", {name, func});
            fetchBlocks();
        } catch (error) {
            console.error(error);
        }
    }

    // Remove an existing block from the diagram
    const removeBlock = async (block) => {
        try {
            await axios.delete("/remove_block", {block});
            fetchBlocks();
        } catch (error) {
            console.error(error);
        }
    }

    // Open the modal for adding a new block
    const openModal = () => {
        setShowModal(true);
    }

    // Close the modal for adding a new block
    const closeModal = () => {
        setShowModal(false);
    }

    // Handle changes to the block name input
    const handleBlockNameChange = (event) => {
        setBlockName(event.target.value);
    }

    // Handle changes to the block code input
    const handleBlockFuncChange = (event) => {
        setBlockFunc(event.target.value);
    }

    // Check out https://antonioru.github.io/beautiful-react-diagrams/#/Dynamic%20nodes
    // Render the diagram using the blocks fetched from the API
    return (
        <div>
            <div className="sidebar">
                <button onClick={openModal}>Add</button>
                <button onClick={() => removeBlock()}>Remove</button>
            </div>
            <Diagram diagramState={diagramState}>
                {blocks.map((block) => (
                    <Node
                        name={block.name}
                        func={block.func}
                        onDelete={() => removeBlock(block)}
                    />
                ))}
            </Diagram>
            <Modal
                isOpen={showModal}
                onRequestClose={closeModal}
            >
                <h2>Add Block</h2>
                <label>
                    Block Name:
                    <input
                        type="text"
                        value={blockName}
                        onChange={handleBlockNameChange}
                    />
                </label>
                <label>
                    Block Function:
                    <textarea
                        value={blockFunc}
                        onChange={handleBlockFuncChange}
                    />
                </label>
                <button onClick={() => addBlock(blockName, blockFunc)}>
                    Add Block
                </button>
                <button onClick={closeModal}>Cancel</button>
            </Modal>
        </div>
    );
}