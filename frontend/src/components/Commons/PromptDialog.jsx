import {
    Button as MuiButton,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    TextField
} from "@mui/material";
import { useState } from "react";

function PromptDialog({
    open,
    title,
    label = "Optional prompt",
    confirmText = "Continue",
    onClose,
    onConfirm
}) {
    const [prompt, setPrompt] = useState("");

    const handleClose = () => {
        console.log("[PromptDialog] Closed:", title);
        setPrompt("");
        onClose();
    };

    const handleConfirm = () => {
        console.log("[PromptDialog] Confirmed:", title, "prompt:", prompt);
        onConfirm(prompt);
        setPrompt("");
    };

    return (
        <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    label={label}
                    fullWidth
                    multiline
                    minRows={3}
                    value={prompt}
                    onChange={(event) => setPrompt(event.target.value)}
                />
            </DialogContent>
            <DialogActions>
                <MuiButton onClick={handleClose}>
                    Cancel
                </MuiButton>
                <MuiButton variant="contained" onClick={handleConfirm}>
                    {confirmText}
                </MuiButton>
            </DialogActions>
        </Dialog>
    );
}

export default PromptDialog;
