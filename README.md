# QuantumShield Finance
### Intelligent Financial Fraud Detection, Investigation & Quantum-Safe Security

> **Disclaimer**: QuantumShield Finance is an advanced research and hackathon prototype designed for algorithmic evaluation and post-quantum cryptographic security demonstrations. It operates exclusively on synthetic data and deterministic stress-test scenarios. It is not a certified production banking system and does not connect to live banking clearing rails or execute real monetary transfers.

---

## 1. Overview & Key Capabilities

QuantumShield Finance is an end-to-end financial crime prevention platform that bridges multi-signal intelligent fraud intelligence with standardized NIST Post-Quantum Cryptography (PQC):

1. **Multi-Signal Hybrid Fraud Detection**:
   - **Configurable Rules Engine**: Detects micro-authorization bursts (< $10), rapid transaction velocity, shared multi-account device sign-ons, and account takeover sequences.
   - **Isolation Forest ML Anomaly Detection**: Unsupervised scikit-learn anomaly scoring trained strictly on partitioned baseline distributions to prevent target leakage.
   - **NetworkX Graph Analytics**: Discovers multi-hop layering, circular money flows, rapid pass-through conduits (inflow followed by immediate >= 70% drainage), and dense mule clusters with Cytoscape.js visualization.
   - **Transparent Risk Fusion**: Calibrated 0–100 composite score with explicit reason codes (`CARD_TESTING_MICRO_BURST`, `GRAPH_RAPID_PASSTHROUGH_MULE`, `ACCOUNT_TAKEOVER_NEW_BENEFICIARY`).
2. **Investigation Workbench**:
   - Prioritized case queues ranked by risk severity, dollar exposure, corroborating evidence count, and network cluster importance.
   - Full case audit timeline, related entity graphs, analyst notes, and status lifecycle management (`OPEN`, `UNDER_REVIEW`, `CONFIRMED_FRAUD`, `RESOLVED`).
3. **Reproducible Five Stress-Test Scenarios**:
   - `NORMAL`: Routine transfers with false-positive control (e.g. legitimate high-value tuition transfer on a trusted device).
   - `CARD_TESTING`: High-frequency micro-authorizations trying multiple cards/recipients through an anonymous Tor session.
   - `MULE_NETWORK`: Layered dispersal across a multi-hop mule ring on a shared emulator.
   - `ACCOUNT_TAKEOVER`: Compromised customer credentials, unrecognized device login in foreign IP, rapid beneficiary addition, and high-value drain.
   - `MULTIPLE_EVENTS`: Compound concurrent attacks in a single window with alert correlation and deduplication.
4. **Empirical Baseline Benchmarking**:
   - Evaluated against a fixed $5,000 amount-threshold baseline on the exact same held-out test suite.
   - Full confusion matrix reporting (TP, FP, TN, FN), precision, recall, F1-score, and false-positive rate, with zero denominator safety.
   - Exportable as JSON and CSV.
5. **NIST Post-Quantum Cryptographic Security**:
   - **ML-KEM-768 (NIST FIPS 203)**: Key encapsulation for quantum-resistant shared secret agreement.
   - **ML-DSA-65 (NIST FIPS 204)**: Quantum-resistant digital signatures over canonical wire instructions (binding transaction ID, amount, currency, recipient, expiry, and nonce).
   - **AES-256-GCM + HKDF-SHA256**: Authenticated symmetric envelope encryption with 12-byte random nonces and AAD integrity verification.
   - **Tamper Testing Playground**: Demonstrates instantaneous AEAD rejection upon flipping any single byte in ciphertext or auth tag.
   - **Replay Attack Protection**: Cache-enforced nonce validation.

---

## 2. Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, Cytoscape.js, Framer Motion, Lucide React.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic migrations.
- **Intelligence**: pandas, NumPy, scikit-learn, NetworkX.
- **Security & PQC**: `mlkem` (NIST FIPS 203), `dilithium-py` (NIST FIPS 204 ML-DSA-65), `cryptography` (AES-256-GCM, HKDF-SHA256).
- **Persistence**: SQLite (local development zero-config fallback), PostgreSQL (production target).

---

## 3. Directory Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, startup seeder & CORS
│   │   ├── api/v1/              # Typed REST endpoints (dashboard, txs, graph, cases, security, model-lab)
│   │   ├── core/                # Configuration, logging with redaction, RBAC
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic validation schemas
│   │   ├── database/            # Database session & engine
│   │   └── services/            # Intelligence, PQC, graph, and policy services
│   ├── alembic/                 # Database migration scripts
│   └── tests/                   # Automated pytest suite (22 tests)
├── frontend/
│   ├── src/
│   │   ├── components/          # Header, Sidebar, common UI
│   │   ├── layouts/             # AppLayout
│   │   ├── pages/               # 8 mandatory dashboard pages
│   │   ├── services/            # Typed API client
│   │   └── types/               # TypeScript interfaces
├── data/
│   ├── manifests/               # Deterministic dataset manifest & seeds
│   └── raw/                     # Data stores
├── scripts/
│   ├── seed_data.py             # Deterministic synthetic data seeder
│   ├── start.ps1                # PowerShell single-command startup script
│   └── start.sh                 # Unix/Linux single-command startup script
├── docs/
│   ├── ARCHITECTURE.md          # Architecture and Mermaid diagrams
│   ├── SECURITY_THREAT_MODEL.md # STRIDE threat model & PQC analysis
│   ├── ALGORITHM_COMPLEXITY.md  # Theoretical complexity & measured latency
│   ├── DEMO_GUIDE.md            # Step-by-step five-scenario demo guide
│   └── BENCHMARK_REPORT.md      # Measured empirical benchmark report
├── requirements.txt             # Pinned Python dependencies
├── docker-compose.yml           # Container orchestration
└── .env.example                 # Environment configuration template
```

---

## 4. Single Local Startup Workflow

### Option A: Windows PowerShell
Run the startup script:
```powershell
.\scripts\start.ps1
```

### Option B: Linux / macOS
Run the shell script:
```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

### Option C: Manual Launch

1. **Activate Virtual Environment & Seed Database**:
   ```bash
   .\.venv\Scripts\python.exe scripts\seed_data.py
   ```
2. **Start Backend API** (Port 8000):
   ```bash
   .\.venv\Scripts\uvicorn.exe backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
3. **Start Frontend UI** (Port 5173):
   ```bash
   cd frontend
   npm run dev
   ```

Open your browser at **`http://localhost:5173`**.
Interactive OpenAPI documentation is available at **`http://127.0.0.1:8000/api/v1/docs`**.

---

## 5. Running Automated Tests

Run the full pytest suite:
```bash
.\.venv\Scripts\python.exe -m pytest backend/tests -v
```
All 22 test suites cover PQC roundtrips, tamper detection, ML-DSA signature verification, replay protection, rules engine, Isolation Forest scoring, NetworkX graph cycles, risk fusion boundaries, case prioritization, and FastAPI contracts.

---

## 6. Mandatory Frontend Pages

1. **Command Center**: Layout matching financial AML command center visual reference with KPI cards, risk band donut charts, hourly telemetry, recent risk alerts, and AI risk intelligence.
2. **Transaction Monitor**: Real-time streaming table, search and scenario filters, explainable component breakdowns, and live synthetic event replay injection.
3. **Fraud Network Explorer**: Cytoscape.js directed money movement topology, shared emulator nodes, cluster ring highlighting (`RING_01`), topological inspector, and table fallback.
4. **Investigation Workbench**: Prioritized case queues, timeline events, evidence summaries, correlated accounts, analyst notes appending, and lifecycle status transitions.
5. **Quantum-Safe Security Center**: NIST FIPS 203 ML-KEM-768 and FIPS 204 ML-DSA-65 status, interactive hybrid encryption playground, 1-click tamper integrity testing, digital wire instruction signing, and replay defense validation.
6. **Model Lab & Stress Tests**: Independent execution of all 5 scenarios, head-to-head comparison against fixed amount threshold baseline, confusion matrices, latency percentiles, and instant JSON/CSV export.
7. **Audit Logs**: Immutable regulatory trace of administrative decisions and case status updates.
8. **Settings**: Configurable baseline thresholds, prevention policy cutoffs, and cryptographic parameters.
