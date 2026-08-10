---
applyTo: "backend/**"
---
- Storage access goes through app/storage.py only; endpoints never touch the
  file system directly.
- Raise HTTPException with correct status codes: 404 unknown resource,
  422 invalid input.
- Every new endpoint ships in the same PR as its pytest coverage.
