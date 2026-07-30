import Button from "./Button.jsx";
import Modal from "./Modal.jsx";

const ConfirmDialog = ({
    open,
    title,
    description,
    confirmLabel = "Confirm",
    cancelLabel = "Cancel",
    tone = "primary",
    onConfirm,
    onCancel,
    loading = false,
}) => (
    <Modal
        open={open}
        title={title}
        description={description}
        onClose={onCancel}
        size="sm"
        footer={
            <>
                <Button variant="ghost" onClick={onCancel} disabled={loading}>
                    {cancelLabel}
                </Button>
                <Button variant={tone} onClick={onConfirm} loading={loading}>
                    {confirmLabel}
                </Button>
            </>
        }
    >
        {" "}
    </Modal>
);

export default ConfirmDialog;
