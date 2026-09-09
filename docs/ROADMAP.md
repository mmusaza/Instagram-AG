# Roadmap

## Phase 1 — Foundation

- [x] Repository initialized
- [x] Provider abstraction
- [x] Agent orchestration
- [x] AI client abstraction
- [x] Comment analysis foundation
- [x] Initial SQLite persistence layer
- [x] Project documentation

## Phase 2 — Instagram provider

- [ ] Implement browser provider behind `InstagramProvider`
- [ ] Post discovery and pagination
- [ ] Robust comment loading
- [ ] Reliable page-reply detection
- [ ] Dry-run mode
- [ ] Reply executor with explicit safety gate

## Phase 3 — Reliability

- [ ] Idempotent processing using comment IDs
- [ ] Retry/backoff
- [ ] Structured logs
- [ ] Agent run history
- [ ] Error classification
- [ ] Tests with mocked provider

## Phase 4 — Product intelligence

- [ ] Brand profile/configuration
- [ ] Conversation memory
- [ ] Intent taxonomy expansion
- [ ] Spam/moderation rules
- [ ] Confidence thresholds
- [ ] Human approval mode

## Phase 5 — Dashboard and cloud

- [ ] Web dashboard
- [ ] Worker/queue model
- [ ] PostgreSQL production database
- [ ] Authentication and account management
- [ ] Multi-account support
- [ ] Monitoring and health checks

## Phase 6 — Production integrations

- [ ] Evaluate and implement supported Instagram/Meta API integration where appropriate
- [ ] Provider capability detection
- [ ] Migration tooling from browser-provider state
