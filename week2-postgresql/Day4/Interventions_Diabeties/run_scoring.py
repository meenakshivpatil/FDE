"""Phase 2: calculate risk_score and risk_level for every encounter. Safe to re-run."""
import service

if __name__ == "__main__":
    result = service.score_all_encounters()
    print("Scoring complete:")
    for key, value in result.items():
        print(f"  {key}: {value}")
