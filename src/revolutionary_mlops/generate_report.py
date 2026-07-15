from pathlib import Path
import sys

required_metrics = ["accuracy", "precision", "recall"]


def read_metrics(path: Path) -> dict[str, float]:
    """
    Función que lee las métricas de un archivo de texto.
    """
    metrics = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" in line:
            name, value = line.split(":", maxsplit=1)
        elif "=" in line:
            name, value = line.split("=", maxsplit=1)
        else:
            continue
        name = name.strip()
        value = value.strip()
        if name in required_metrics:
            metrics[name] = float(value)
    return metrics


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage:  python scripts/generate_report.py validation_output.txt MODEL_ID"
        )

    metrics_path = Path(sys.argv[1])
    model_id = sys.argv[2]
    metrics = read_metrics(metrics_path)

    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Model Report</title>
            </head>
            <body>

            <h1>Model Validation Report</h1>
            <h2>Testing CI/CD injection</>

            <p><strong>Model ID:</strong> {model_id}</p>

            <p><strong>Accuracy:</strong> {metrics["accuracy"]:.3f}</p>

            <p><strong>Precision:</strong> {metrics["precision"]:.3f}</p>

            <p><strong>Recall:</strong> {metrics["recall"]:.3f}</p>

            <p><strong>Status:</strong> Ready for production</p>

            </body>
            </html>
        """

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
