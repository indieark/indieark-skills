# Provider Adapter Contract

Load when adding a concrete image model/provider.

## Required Adapter Shape

Each provider should define:

- `provider_id`
- supported input modes
- required credential sources
- request builder
- local validation
- submission hook placeholder
- result parser
- artifact writer
- error mapping

## Core Boundary

Core may own:

- config loading
- run directories
- neutral request schema
- redaction helpers
- common CLI shape
- generic validation framework

Provider adapter owns:

- provider connection details
- credential mapping
- model identifiers
- request/response mapping
- provider-specific limits
- result semantics

No concrete values belong in this placeholder scaffold.

Do not put provider API specifics in core files.
