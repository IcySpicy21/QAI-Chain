from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.blockchain.block import Block
from core.blockchain.blockchain import Blockchain
from core.blockchain.miner import proof_of_work
from core.blockchain.transaction import Transaction
from crypto.pqc.keypair import PQCKeypair
from crypto.pqc.transaction_signer import sign_transaction
from scripts.benchmark_quick import run_benchmark


def _run_step(title: str, cmd: list[str], env: dict[str, str], cwd: Path | None = None) -> None:
    print(f"\n== {title} ==")
    print("$ " + " ".join(cmd))
    proc = subprocess.run(cmd, cwd=(cwd or ROOT), env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"Step failed: {title}")


def _run_blockchain_smoke() -> dict[str, str | int]:
    chain = Blockchain(difficulty=1)

    wallet = PQCKeypair()
    tx = Transaction(
        sender=wallet.get_public_key(),
        receiver="recruiter-demo-receiver",
        amount=1.0,
    )
    signed_tx = sign_transaction(tx, wallet.private_key)

    candidate = Block(
        index=len(chain.chain),
        transactions=[signed_tx],
        previous_hash=chain.last_block().hash,
    )
    mined = proof_of_work(candidate, chain.difficulty)
    chain.add_block(mined)

    return {
        "chain_height": len(chain.chain),
        "latest_hash": mined.hash,
        "tx_count": len(mined.transactions),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-command recruiter/interviewer showcase for QAI-Chain.",
    )
    parser.add_argument(
        "--with-paper",
        action="store_true",
        help="Also build paper/main.pdf as part of the showcase.",
    )
    args = parser.parse_args()

    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)

    print("QAI-Chain one-command showcase")
    print(f"Repository: {ROOT}")

    _run_step("Healthcheck", [sys.executable, "scripts/healthcheck.py"], env)
    _run_step("Tests", [sys.executable, "-m", "pytest", "-q"], env)

    print("\n== Quick Benchmark ==")
    benchmark = run_benchmark()
    for name, stats in benchmark.items():
        print(
            f"{name:16s} avg={stats['avg_ms']:8.3f} ms  "
            f"p50={stats['p50_ms']:8.3f} ms  p90={stats['p90_ms']:8.3f} ms"
        )

    print("\n== Blockchain Smoke Demo ==")
    smoke = _run_blockchain_smoke()
    print(f"Chain height: {smoke['chain_height']}")
    print(f"Latest block hash: {smoke['latest_hash']}")
    print(f"Transactions in latest block: {smoke['tx_count']}")

    if args.with_paper:
        _run_step(
            "Paper Build",
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            env,
            cwd=ROOT / "paper",
        )

    print("\nShowcase complete.")
    print("Suggested assets to show:")
    print("- paper/main.pdf")
    print("- docs/BENCHMARK_REPORT.md")
    print("- docs/RESEARCH_RESULTS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
