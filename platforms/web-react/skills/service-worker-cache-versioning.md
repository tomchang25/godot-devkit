# Service Worker Cache Versioning

Platform: Web React.

A service worker creates a second runtime owner between an old page and a new deployment. Without explicit version and activation policy, navigation documents, application chunks, content, and persistence code may come from incompatible versions.

## Hazard

- Development registers a worker and caches hot-reload or local chunks as stale responses.
- Navigation uses cache-first HTML while referenced chunks belong to another deployment.
- Activation deletes every origin cache, including unrelated applications or tooling.
- A new worker forcefully takes over an old page midway through a gameplay or persistence transaction.

## Safe Shape

1. Register only in the intended production environment and provide an application-scoped development recovery path.
2. Cache names include an application prefix and deployment or schema version; activation deletes expired caches with that prefix only.
3. Navigation, content-addressed static assets, mutable runtime data, and APIs use explicit separate strategies.
4. Update UI asks for a safe reload instead of silently replacing the active runtime contract.
5. Sequential save migration remains available across supported deployments; do not depend on mixing old code with new content.
6. Tests or build smoke cover first install, waiting update, activation, offline navigation where supported, and old-cache cleanup.

## Review Prompts

- Does each request class use a cache strategy that matches its versioning model?
- Does activation clean only this application namespace?
- Can an old page and new worker mix incompatible contracts inside one transaction?
