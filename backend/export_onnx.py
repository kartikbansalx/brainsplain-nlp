"""Export and verify Brainsplain's Sentence Transformers model as ONNX.

Run this once during the deployment build (or manually before local testing).
The saved directory is then loaded by rag.py without exporting at app startup.
"""
import os
from pathlib import Path

import onnxruntime as ort
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = Path(
    os.environ.get(
        "EMBEDDING_MODEL_PATH",
        str(BASE_DIR / "models" / "all-MiniLM-L6-v2-onnx"),
    )
).resolve()


def main():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    print(f"Exporting {MODEL_NAME} to ONNX...")
    print("Available ONNX providers:", ort.get_available_providers())

    # If the model is already present, this loads it instead of exporting again.
    model = SentenceTransformer(
        MODEL_NAME,
        backend="onnx",
        model_kwargs={"provider": "CPUExecutionProvider"},
    )

    model.save_pretrained(str(OUTPUT_PATH))
    print(f"Saved ONNX Sentence Transformers model to: {OUTPUT_PATH}")

    # Reload from the saved path with export=False to verify the deployment path.
    verified_model = SentenceTransformer(
        str(OUTPUT_PATH),
        backend="onnx",
        model_kwargs={
            "provider": "CPUExecutionProvider",
            "export": False,
        },
    )

    embeddings = verified_model.encode(
        ["Testing Brainsplain ONNX embeddings."],
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    print("Verification successful.")
    print("Embedding shape:", embeddings.shape)
    print("Embedding dimension:", embeddings.shape[-1])


if __name__ == "__main__":
    main()
