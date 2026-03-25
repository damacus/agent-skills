# Async, Client Reuse & Authentication

## Client Lifecycle Pattern (Rust/Reqwest)

Don't recreate the HTTP client on every request. Share it to reuse connection pools.

### Singleton / Dedicated Client Struct
```rust
pub struct Client {
    http: reqwest::Client,
    base_url: String,
    token: String,
}

impl Client {
    pub fn new(host: String, token: String) -> Result<Self> {
        let mut headers = HeaderMap::new();
        // Set shared auth headers once
        headers.insert("PRIVATE-TOKEN", HeaderValue::from_str(&token)?);
        
        let http = reqwest::Client::builder()
            .default_headers(headers)
            .build()?;
            
        Ok(Self { http, base_url: host, token })
    }
}
```

## The "Conductor" Pattern

The Conductor is the bridge between the raw Client and the high-level App state.

### Role of the Conductor:
1. **Orchestration:** High-level methods like `fetch_health_check()` or `rotate_runners()`.
2. **Parallelisation:** Use `futures::future::join_all` to fetch detail for multiple items in parallel.
3. **Caching:** Maintain the raw model data so the App can re-filter/re-sort without re-fetching.
4. **Resiliency:** Handles retry logic and error mapping (converting API errors to UI-friendly messages).

### Parallel Fetch Pattern
```rust
let tasks: Vec<_> = runners.iter().map(|r| self.fetch_detail(r.id)).collect();
let results = futures::future::join_all(tasks).await;
```

## Authentication Management
- Use `rpassword` for secure CLI token prompts.
- Persist settings in TOML via `dirs` and `toml` crate.
- Redact tokens in `Debug` implementations by hand-coding `fmt::Debug` for Config structs.
