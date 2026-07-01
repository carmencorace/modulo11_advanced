from pathlib import Path
import sys

min_score = 0.80
required_metrics = ["accuracy", "precision", "recall"]


def read_metrics(path: Path) -> dict[str, float]:
    """
    Función que lee las métricas de un archivo de texto. 
    """
    metrics = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        name, value = line.split("=", maxsplit=1)
        if name in required_metrics:
            metrics[name] = float(value)
    return metrics


def main() -> None:
    """
    Función principal que ejecuta la validación de las métricas. 
    """
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/check_metrics.py validation_output.txt")


    metrics_path = Path(sys.argv[1])
    metrics = read_metrics(metrics_path)


    missing_metrics = []
    for name in required_metrics: 
        if name not in metrics: 
            missing_metrics.append(name)   
    if missing_metrics:
        raise SystemExit(f"Missing metrics: {', '.join(missing_metrics)}")


    failed_metrics = {}
    for name, value in metrics.items():
        if value < min_score:
            failed_metrics[name] = value
    if failed_metrics: 
        for name, value in failed_metrics.items():
            print(f"{name}={value:.3f} is below {min_score:.2f}")
        raise SystemExit(1) 

   
    print("All validation metrics passed:")
    for name in required_metrics:
        print(f"{name}={metrics[name]:.3f}")


if __name__ == "__main__":
    main()