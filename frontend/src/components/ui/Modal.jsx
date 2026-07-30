import { useEffect } from "react";
import { createPortal } from "react-dom";

import "./Modal.css";

const Modal = ({ open, title, description, onClose, size = "md", children, footer }) => {
    useEffect(() => {
        if (!open) return undefined;
        const original = document.body.style.overflow;
        document.body.style.overflow = "hidden";
        const escape = (event) => event.key === "Escape" && onClose?.();
        document.addEventListener("keydown", escape);
        return () => {
            document.body.style.overflow = original;
            document.removeEventListener("keydown", escape);
        };
    }, [open, onClose]);

    if (!open) return null;

    return createPortal(
        <div className="modal-overlay" onClick={onClose}>
            <div
                className={`modal modal--${size}`}
                role="dialog"
                aria-modal="true"
                onClick={(event) => event.stopPropagation()}
            >
                <header className="modal__header">
                    <div>
                        <h2 className="modal__title">{title}</h2>
                        {description && <p className="modal__description">{description}</p>}
                    </div>
                    <button className="modal__close" onClick={onClose} aria-label="Close">
                        ×
                    </button>
                </header>
                <div className="modal__body">{children}</div>
                {footer && <footer className="modal__footer">{footer}</footer>}
            </div>
        </div>,
        document.body,
    );
};

export default Modal;
