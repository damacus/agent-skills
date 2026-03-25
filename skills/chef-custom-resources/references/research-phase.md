# Research Phase

Research the product's installation options, platform support, and limitations before writing any code.

## Steps

### 1. Identify the Product

Determine what software the cookbook manages. Check `metadata.rb` for the cookbook name and description.

### 2. Search Vendor Package Repositories

Use web search to find the vendor's official package repositories:

- **APT** (Debian/Ubuntu): Search for `<product> apt repository` or check the vendor's download page
- **DNF/YUM** (RHEL/Fedora/Amazon): Search for `<product> yum repository` or `<product> dnf repository`
- **Zypper** (SUSE): Search for `<product> zypper repository` or `<product> opensuse repository`

For each repository, note:

- Which distributions are supported (e.g. Ubuntu 20.04, 22.04, 24.04)
- Which architectures are available (amd64, arm64, etc.)
- Which product versions are available per distribution
- Repository URL pattern and GPG key location

### 3. Check Compiled/Source Installation

If the product can be built from source, note:

- Required build dependencies per platform family
- Platform-specific tooling (e.g. `build-essential`, `gcc`, `make`, `cmake`)
- Any platform-specific patches or configure flags
- Minimum supported versions of build tools

### 4. Note Limitations

Document any restrictions discovered:

- Architecture-only packages (e.g. "only amd64 packages available for version X")
- Platform gaps (e.g. "no official SUSE packages")
- Version constraints (e.g. "version 8.4 only available on Debian 13+")
- EOL versions that should not be supported

### 5. Cross-Reference with metadata.rb

Compare vendor support with the cookbook's `supports` declarations in `metadata.rb`. Flag:

- Platforms listed in `metadata.rb` but not supported by the vendor
- Platforms supported by the vendor but missing from `metadata.rb`
- Version ranges that need tightening

## LIMITATIONS.md Template

Write `LIMITATIONS.md` at the cookbook root using this format:

```markdown
# Limitations

## Package Availability

### APT (Debian/Ubuntu)

- Ubuntu 20.04: versions X.Y, X.Z (amd64 only)
- Ubuntu 22.04: versions X.Y, X.Z (amd64, arm64)
- Debian 12: versions X.Y (amd64 only)

### DNF/YUM (RHEL family)

- RHEL 8 / AlmaLinux 8: versions X.Y (amd64 only)
- RHEL 9 / AlmaLinux 9: versions X.Y, X.Z (amd64, arm64)
- Fedora: versions X.Z (amd64, arm64)

### Zypper (SUSE)

- openSUSE Leap 15: versions X.Y (amd64 only)

## Architecture Limitations

- Only amd64 packages are available for version X.Y
- arm64 packages available starting from version X.Z

## Source/Compiled Installation

### Build Dependencies

| Platform Family | Packages                         |
|-----------------|----------------------------------|
| Debian          | build-essential, libssl-dev, ... |
| RHEL            | gcc, make, openssl-devel, ...    |

## Known Issues

- Brief description of any known issues affecting cookbook behavior
```

The file should be factual, concise, and usable as instructions by both humans and AI agents.
