# Family Record: evidence-backed educational record

Institutions issue credentials by authority. METHEAN issues them by
evidence. The Family Record is the data layer that proves it: a
cumulative, per-child record where every mastery claim carries its
evidence chain, sealed into an export whose manifest ties to the
household's tamper-evident governance chain (migration 052).

## Data flow

```
                       (read-only lens; writes nothing to learner state)

  annual_curricula ----+
  compliance hours ----+--> assemble_transcript_data()   [document_generator]
                       |        |                shared by PDF transcript
                       |        v                and the JSON record
  child_node_states    |   FamilyRecord (Pydantic)
   (proficient+) ------+--> mastery_evidence[]
  attempts+activities -+        each node: attempts, assessments,
  assessments ---------+        governance events w/ event_hash
  fsrs_cards ----------+
  state_events --------+--> achieved_at per node
  reading_log ---------+--> reading_log[]
  governance_events ---+--> integrity {head_hash, verified, count}
                                |
                                v
                     build_record_bundle()
            record.json + transcript.pdf + attendance.pdf
            + compliance PDFs (when inputs exist) + VERIFICATION.md
                                |
                                v
                     manifest.json {file sha256s, content_hash,
                       chain_head_hash, bundle_hash}
                                |
                                v
                  ZIP -> S3 (artifact row) -> presigned URL
                                |
                                v
            governance event family_record_exported (bundle_hash)
            the export itself becomes part of the immutable chain
```

## Integrity model

Three nested guarantees, weakest to strongest:

1. File integrity: manifest.json holds the SHA-256 of every file in
   the bundle. Any post-export edit to any file is detectable by
   recomputing one hash.
2. Bundle integrity: `bundle_hash = sha256(sorted "name:hash" lines +
   chain_head_hash)`. The bundle hash commits to the exact file set
   AND the household's chain head at export time, so files cannot be
   added, removed, or swapped between bundles without detection.
3. Chain anchoring: the chain head is the latest link of the
   household's append-only governance hash chain (migration 052:
   UPDATE and DELETE raise at the database level, each event's hash
   commits to the full history before it). The export action itself
   is logged into that chain carrying the bundle_hash, so METHEAN
   retains a tamper-evident receipt of every bundle ever issued, and
   the next export's head necessarily differs.

`content_hash` versus file hash of record.json: record.json embeds
`record_generated_at`, which varies per export. `content_hash` is the
SHA-256 of the canonical record with that one generation-metadata
field removed, so two exports with no intervening events carry the
same content_hash even though their file hashes differ. The manifest
carries both, distinguishing "the record's content" from "this
particular generation of it".

## What the bundle proves, and what it does not

Proves:
- The bundle's files are exactly what METHEAN exported (hashes).
- Every mastery claim traces to logged attempts, assessments, and
  parent governance decisions, each tied into a hash chain that the
  database refuses to rewrite.
- The export event exists in the family's immutable record.

Does not prove:
- Real-world identity of the student. The record says "this account's
  evidence", not "this human". Registrars verify identity the same
  way they would for any submitted document.
- Anything about events after export: the bundle is a sealed snapshot.
- Independent existence of the chain: verification against METHEAN's
  live chain requires querying the household's account (see roadmap).

## Privacy posture

The export leaves the household, so the record carries birth year
only, never the full date of birth. The existing PDF documents keep
their current behavior inside the product; the JSON record is the
export-grade surface.

## Performance

Assembly is bounded-query by construction: one query per collection
(node states, nodes+subjects, attempts+activities, assessments, FSRS
cards, state events, referenced governance events, full chain,
reading log) using batched IN lists keyed by the child's
evidence-bearing nodes. Query count is constant regardless of node or
attempt count.

## Deferred roadmap (explicitly out of scope here)

- External chain anchoring: periodically anchoring the household
  chain head into an external timestamping service so chain integrity
  is verifiable without trusting METHEAN's database.
- Third-party verifier endpoint: a public, rate-limited endpoint where
  a registrar can paste a bundle_hash and receive a yes/no plus the
  export's governance receipt.
- ESA-formatted variants: jurisdiction-specific bundle layouts for
  education savings account and umbrella-school submissions.
